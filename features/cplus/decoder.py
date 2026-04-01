import base64
import json
import zlib
import bpy
import mathutils
import math
import lz4.block

from collections import defaultdict
from bpy_extras.io_utils import axis_conversion
from mathutils import Matrix
from io import BufferedIOBase, BytesIO

def translate_hash(the_hasherrrr: bytes) -> tuple[int, dict]:
    """
    Decompresses a C+ string, returning the version and data dict.
    """
    inflated = zlib.decompress(the_hasherrrr, zlib.MAX_WBITS | 16)
    version = inflated[0]
    json_str = inflated.decode('utf-8')
    data = json.loads(json_str[1:])
    return version, data

def get_bone_values(cplus_dict: dict, value_key: str) -> dict:
    """
    Extracts bone values for a given key from the C+ data dict.
    """
    bones = cplus_dict.get('Bones', {})
    new_bones = defaultdict(dict)
    for key in bones.keys():
        if value_key not in bones[key]:
            continue

        values = bones[key][value_key]
        if value_key in ['Translation', 'Rotation']:
            if 'X' not in values:
                values['X'] = 0.0
            
            if 'Y' not in values:
                values['Y'] = 0.0

            if 'Z' not in values:
                values['Z'] = 0.0

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

def read_size(reader: BufferedIOBase, size: int) -> int | None:
    """
    Reads the specified size of bytes, and returns the value as an integer.
    Returns None if no more data can be read.
    """
    byte = reader.read(size)

    if not byte:
        return None

    return int.from_bytes(byte, byteorder='little')

def read_byte(reader: BufferedIOBase) -> int | None:
    """
    Reads a byte and returns the value as an integer.
    Returns None if no more data can be read.
    """
    return read_size(reader, 1)

def read_int(reader: BufferedIOBase) -> int | None:
    """
    Reads an integer and returns the value.
    Returns None if no more data can be read.
    """
    return read_size(reader, 4)

def read_leb128(reader: BufferedIOBase) -> int:
    """
    Reads an LEB128 compressed number and returns the value as an integer.
    """
    result = 0
    shift = 0

    while True:
        byte = read_byte(reader)

        if byte is None:
            break

        result |= (byte & 0x7F) << shift
        shift += 7

        if (byte & 0x80) == 0:
            break

    return result

def get_chunk(file: BufferedIOBase) -> bytes | None:
    """
    Reads and processes a chunk, starting from where the file reader position is currently.
    Returns None if no more data can be read.
    """
    magic = read_byte(file)

    if magic is None:
        return None

    uncompressed_size = read_leb128(file)

    # Uncompressed
    if magic == 2:
        return file.read(uncompressed_size)
    # Compressed
    elif magic == 3:
        chunk_size = read_leb128(file)
        chunk_data = file.read(chunk_size)
        return lz4.block.decompress(chunk_data, uncompressed_size=uncompressed_size)
    # Unknown
    else:
        raise Exception(f'Unknown Chunk Magic Value: {magic}')

def get_mcdf_cplus(path: str) -> str | None:
    """
    Reads an MCDF file to retrieve it's C+ string.
    Returns None if there was an error while reading the file.
    """
    try:
        data = bytearray()

        with open(path, 'rb') as file:
            while True:
                chunk = get_chunk(file)

                if chunk is None:
                    break

                data.extend(chunk)

        data_reader = BytesIO(data)
        signature = data_reader.read(4).decode('utf-8')

        if signature != 'MCDF':
            raise Exception(f'"MCDF" expected at the start of the file, got "{signature}" instead.')

        version = read_byte(data_reader)

        if version != 1:
            raise Exception(f'Version {version} is unsupported.')

        mcdf_json_size = read_int(data_reader)
        mcdf_json = json.loads(data_reader.read(mcdf_json_size).decode('utf-8'))
        return mcdf_json['CustomizePlusData']
    except Exception as e:
        print("[AetherBlend] Failed to parse C+ string from MCDF file:", e)
        return None
