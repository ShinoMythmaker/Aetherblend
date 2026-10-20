"""Decoding helpers for Customize+ strings and MCDF files."""

import json
import math
import zlib
from io import BytesIO
from typing import Any, BinaryIO

import bpy
import lz4.block
import mathutils


def translate_hash(compressed: bytes) -> tuple[int, dict[str, Any]]:
    """Decompress a Customize+ string and return its version and data."""
    inflated = zlib.decompress(compressed, zlib.MAX_WBITS | 16)
    return inflated[0], json.loads(inflated[1:].decode("utf-8"))


def get_bone_values(cplus_dict: dict[str, Any], value_key: str) -> dict[str, dict[str, float]]:
    """Extract complete XYZ transform values for one transform type."""
    result: dict[str, dict[str, float]] = {}
    for bone_name, bone_data in cplus_dict.get("Bones", {}).items():
        values = bone_data.get(value_key)
        if not values:
            continue

        default = 1.0 if value_key == "Scaling" else 0.0
        coordinates = {axis: float(values.get(axis, default)) for axis in ("X", "Y", "Z")}
        if value_key in {"Translation", "Rotation"} and not any(coordinates.values()):
            continue
        result[bone_name] = coordinates
    return result


def apply_transforms(
    armature: bpy.types.Object,
    scale_dict: dict[str, dict[str, float]],
    rot_dict: dict[str, dict[str, float]],
    pos_dict: dict[str, dict[str, float]],
    bones: dict[str, bpy.types.PoseBone] | None = None,
) -> None:
    """Apply Customize+ scale, rotation, and translation to the specified bones."""
    original_mode = armature.mode
    bpy.context.view_layer.objects.active = armature
    if original_mode != "POSE":
        bpy.ops.object.mode_set(mode="POSE")

    try:
        target_bones = bones if bones is not None else armature.pose.bones
        for pose_bone in target_bones.values():
            scale = scale_dict.get(pose_bone.name)
            if scale:
                pose_bone.scale = mathutils.Vector((scale["X"], scale["Y"], scale["Z"]))

            rotation = rot_dict.get(pose_bone.name)
            if rotation:
                euler = mathutils.Euler(
                    tuple(math.radians(rotation[axis]) for axis in ("X", "Y", "Z")),
                    "XYZ",
                )
                pose_bone.rotation_quaternion.rotate(euler)

            translation = pos_dict.get(pose_bone.name)
            if translation:
                pose_bone.location += mathutils.Vector((translation["X"], translation["Y"], translation["Z"]))
    finally:
        if original_mode != "POSE":
            bpy.ops.object.mode_set(mode=original_mode)


def read_size(reader: BinaryIO, size: int) -> int | None:
    """Read a little-endian integer of the requested byte size."""
    data = reader.read(size)
    return int.from_bytes(data, byteorder="little") if data else None


def read_byte(reader: BinaryIO) -> int | None:
    """Read one byte as an integer, or return None at end of input."""
    return read_size(reader, 1)


def read_int(reader: BinaryIO) -> int | None:
    """Read a four-byte integer, or return None at end of input."""
    return read_size(reader, 4)


def read_leb128(reader: BinaryIO) -> int:
    """Read an unsigned LEB128 integer."""
    result = 0
    shift = 0
    while True:
        byte = read_byte(reader)
        if byte is None:
            raise ValueError("Unexpected end of file while reading LEB128 value")
        result |= (byte & 0x7F) << shift
        if byte & 0x80 == 0:
            return result
        shift += 7
        if shift > 63:
            raise ValueError("LEB128 value is too large")


def get_chunk(reader: BinaryIO) -> bytes | None:
    """Read and decompress one MCDF chunk."""
    magic = read_byte(reader)
    if magic is None:
        return None

    uncompressed_size = read_leb128(reader)
    if magic == 2:
        chunk = reader.read(uncompressed_size)
        if len(chunk) != uncompressed_size:
            raise ValueError("MCDF chunk ended before its declared size")
        return chunk
    if magic == 3:
        chunk_size = read_leb128(reader)
        chunk_data = reader.read(chunk_size)
        if len(chunk_data) != chunk_size:
            raise ValueError("Compressed MCDF chunk ended before its declared size")
        return lz4.block.decompress(chunk_data, uncompressed_size=uncompressed_size)
    raise ValueError(f"Unknown MCDF chunk magic value: {magic}")


def get_mcdf_cplus(path: str) -> str | None:
    """Extract the Customize+ string from an MCDF file."""
    try:
        contents = bytearray()
        with open(path, "rb") as source:
            while (chunk := get_chunk(source)) is not None:
                contents.extend(chunk)

        with BytesIO(contents) as reader:
            if reader.read(4) != b"MCDF":
                raise ValueError("MCDF signature is missing")
            version = read_byte(reader)
            if version != 1:
                raise ValueError(f"Unsupported MCDF version: {version}")
            json_size = read_int(reader)
            if json_size is None:
                raise ValueError("MCDF JSON size is missing")
            json_data = reader.read(json_size)
            if len(json_data) != json_size:
                raise ValueError("MCDF JSON ended before its declared size")
            data = json.loads(json_data.decode("utf-8"))
            return data.get("CustomizePlusData")
    except (
        OSError,
        ValueError,
        KeyError,
        AttributeError,
        TypeError,
        json.JSONDecodeError,
        zlib.error,
        lz4.block.LZ4BlockError,
    ) as exc:
        print(f"[AetherBlend] Failed to parse C+ string from MCDF file: {exc}")
        return None
