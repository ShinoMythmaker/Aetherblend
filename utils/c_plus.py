""" Provides utility functions for decoding and processing C+ strings. """

import base64
import json
import zlib
import bpy
import mathutils
import math

from collections import defaultdict

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



#i want to implement an opotion to also give a collection name to only apply to bones in that collection
def apply_transforms(armature: bpy.types.Object, scale_dict: dict, rot_dict: dict, pos_dict: dict, bones: dict[str, bpy.types.PoseBone] = None) -> None:
    """
    Applies C+ scale, rotation, and translation transforms to the pose bones of the given armature.
    """
    original_mode = armature.mode
    bpy.ops.object.mode_set(mode='POSE')
    
    if bones is None:
        bones = armature.pose.bones

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