import base64
import json
import zlib
import bpy
import mathutils
import math

from collections import defaultdict
from bpy_extras.io_utils import axis_conversion
from mathutils import Matrix

def translate_hash(the_hasherrrr: str) -> tuple[int | None, dict]:
    """
    Decodes and decompresses a C+ string, returning the version and data dict.
    """
    try:
        decoded = base64.b64decode(the_hasherrrr)
        inflated = zlib.decompress(decoded, zlib.MAX_WBITS | 16)
        version = inflated[0]
        json_str = inflated.decode('utf-8')
        data = json.loads(json_str[1:])
        return version, data
    except Exception as e:
        print("[AetherBlend] Failed to parse C+ string:", e)
        return None, {}

def get_bone_values(cplus_dict: dict, value_key: str) -> dict:
    """
    Extracts bone values for a given key from the C+ data dict.
    """
    bones = cplus_dict.get('Bones', {})
    new_bones = defaultdict(dict)
    for key in bones.keys():
        values = bones[key][value_key]
        if value_key in ['Translation', 'Rotation']:
            if values['X'] == values['Y'] == values['Z'] == 0.0:
                continue
        new_bones[key] = values
    return new_bones

def apply_transforms(
    armature: bpy.types.Object, 
    scale_dict: dict, 
    rot_dict: dict, 
    pos_dict: dict, 
    bones: dict[str, bpy.types.PoseBone] = None,
    primary_axis: str = 'Y',
    secondary_axis: str = 'X',
) -> None:
    """
    Applies C+ transforms after reverting bone orientation to Y/X.
    Note: Bones remain in Y/X orientation after this function.
    Call reapply_bone_orientation() after rest pose is applied.
    """
    original_mode = armature.mode
    
    if bones is None:
        bones = armature.pose.bones
    
    if (primary_axis, secondary_axis) != ('Y', 'X'):
        # Create the correction matrix used during import
        bone_correction_matrix = axis_conversion(
            from_up='Y',
            from_forward='X',
            to_up=primary_axis,
            to_forward=secondary_axis,
        ).to_4x4()
        
        # Step 1: Revert bones back to Y/X (undo import correction)
        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='EDIT')
        
        edit_bones = armature.data.edit_bones
        for bone in edit_bones:
            bone_matrix = bone.matrix.copy()
            reverted_matrix = bone_matrix @ bone_correction_matrix.inverted()
            bone.matrix = reverted_matrix
    
    # Step 2: Apply C+ transforms (bones are now in Y/X orientation)
    bpy.ops.object.mode_set(mode='POSE')
    bpy.context.view_layer.objects.active = armature
    
    for posebone in bones.values():
        scale_vector = scale_dict.get(posebone.name)
        if scale_vector:
            posebone.scale = mathutils.Vector((scale_vector['X'], scale_vector['Y'], scale_vector['Z']))

        rotation = rot_dict.get(posebone.name)
        if rotation:
            rot_radians = mathutils.Vector((
                math.radians(rotation['X']),
                math.radians(rotation['Y']),
                math.radians(rotation['Z'])
            ))
            euler_rot = mathutils.Euler(rot_radians, 'XYZ')
            posebone.rotation_quaternion.rotate(euler_rot)

        translation = pos_dict.get(posebone.name)
        if translation:
            posebone.location += mathutils.Vector((translation['X'], translation['Y'], translation['Z']))
    
    bpy.ops.object.mode_set(mode=original_mode)

def reapply_bone_orientation(
    armature: bpy.types.Object,
    primary_axis: str = 'Y',
    secondary_axis: str = 'X',
) -> None:
    """Reapplies bone orientation correction after rest pose has been applied."""
    
    previous_mode = armature.mode if hasattr(armature, 'mode') else 'OBJECT'
    
    # Create the correction matrix used during import
    bone_correction_matrix = axis_conversion(
        from_up='Y',
        from_forward='X',
        to_up=primary_axis,
        to_forward=secondary_axis,
    ).to_4x4()
    
    # Reapply correction (convert back to primary_axis/secondary_axis)
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='EDIT')
    
    edit_bones = armature.data.edit_bones
    for bone in edit_bones:
        bone_matrix = bone.matrix.copy()
        corrected_matrix = bone_matrix @ bone_correction_matrix
        bone.matrix = corrected_matrix
    
    bpy.ops.object.mode_set(mode=previous_mode)