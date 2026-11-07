"""Decode Customize+ data and apply its model-space transforms to Blender bones."""

import base64
import json
import math
import warnings
import zlib
from collections.abc import Mapping
from dataclasses import dataclass
from io import BytesIO
from typing import Any, BinaryIO

import bpy
import lz4.block
import mathutils

from ...utils.axis_conversion import DEFAULT_PRIMARY_BONE_AXIS, DEFAULT_SECONDARY_BONE_AXIS, get_import_correction_matrix

# Read the thresholds as float32, matching Customize+'s C# float comparisons.
_VECTOR_EDIT_EPSILON = mathutils.Vector((0.00001, 0.0, 0.0)).x
_ROTATION_EDIT_EPSILON = mathutils.Vector((0.1, 0.0, 0.0)).x
_MATRIX_ERROR_TOLERANCE = 2e-5


########
# C+ String Decoding
########


def _get_bones(cplus_data: Mapping[str, Any]) -> dict[str, Any]:
    bones = cplus_data.get("Bones")
    if not isinstance(bones, dict):
        raise ValueError("The C+ data does not contain a Bones object")
    return bones


def translate_hash(compressed: bytes) -> tuple[int, dict[str, Any]]:
    """Decompress a Customize+ string and return its version and data."""
    inflated = zlib.decompress(compressed, zlib.MAX_WBITS | 16)
    if len(inflated) < 2:
        raise ValueError("C+ gzip data is missing its version or JSON payload")
    return inflated[0], json.loads(inflated[1:].decode("utf-8"))


def decode_cplus_string(code: str) -> dict[str, Any]:
    """Decode gzip or legacy JSON templates without gating on version metadata."""
    decoded = base64.b64decode(code.strip(), validate=True)
    if decoded.startswith(b"\x1f\x8b"):
        _, data = translate_hash(decoded)
    else:
        data = json.loads(decoded)
    if not isinstance(data, dict):
        raise ValueError("The C+ data does not contain a Bones object")
    _get_bones(data)
    return data


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


########
# C+ Bone Data
########


def _transform_vector(data: Mapping[str, Any], key: str) -> mathutils.Vector:
    values = data.get(key, {})
    if not isinstance(values, dict):
        raise ValueError(f"{key} must be an XYZ object")
    default = 1.0 if key in {"Scaling", "ChildScaling"} else 0.0
    result = []
    for axis in ("X", "Y", "Z"):
        value = values.get(axis, default)
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError(f"{key}.{axis} must be a finite number")
        if key == "Rotation":
            # C+ wraps angles both in the property setter and after deserialization.
            for _ in range(2):
                if value > 180:
                    value -= 360
                elif value < -180:
                    value += 360
        elif value < -512 or value > 512:
            warnings.warn(f"{key}.{axis} clamped to Customize+'s [-512, 512] limits", RuntimeWarning, stacklevel=2)
            value = max(-512, min(512, value))
        result.append(float(value))
    return mathutils.Vector(result)


@dataclass
class _BoneTransform:
    """C+ transform values and propagation settings for one bone."""

    translation: mathutils.Vector
    rotation: mathutils.Vector
    scale: mathutils.Vector
    child_scale: mathutils.Vector
    propagate_translation: bool
    propagate_rotation: bool
    propagate_scale: bool
    child_scaling_independent: bool

    @classmethod
    def from_data(cls, name: str, data: Any) -> "_BoneTransform":
        """Read and validate a bone's values before modifying the armature."""
        if not isinstance(data, dict):
            raise ValueError(f"Bone '{name}' must contain a transform object")

        translation = _transform_vector(data, "Translation")
        rotation = _transform_vector(data, "Rotation")
        scale = _transform_vector(data, "Scaling")
        child_scale = _transform_vector(data, "ChildScaling")
        flags = {}
        for key in ("PropagateTranslation", "PropagateRotation", "PropagateScale", "ChildScalingIndependent"):
            value = data.get(key, False)
            if not isinstance(value, bool):
                raise ValueError(f"{name}.{key} must be a boolean")
            flags[key] = value

        return cls(
            translation=translation,
            rotation=rotation,
            scale=scale,
            child_scale=child_scale,
            propagate_translation=flags["PropagateTranslation"],
            propagate_rotation=flags["PropagateRotation"],
            propagate_scale=flags["PropagateScale"],
            child_scaling_independent=flags["ChildScalingIndependent"],
        )

    def is_edited(self) -> bool:
        """Match the thresholds C+ uses to skip unchanged bones."""
        translation_edited = any(abs(value) >= _VECTOR_EDIT_EPSILON for value in self.translation)
        rotation_edited = any(abs(value) >= _ROTATION_EDIT_EPSILON for value in self.rotation)
        scale_edited = any(abs(value - 1.0) >= _VECTOR_EDIT_EPSILON for value in self.scale)
        child_scale_edited = self.child_scaling_independent and any(abs(value - 1.0) >= _VECTOR_EDIT_EPSILON for value in self.child_scale)
        return translation_edited or rotation_edited or scale_edited or child_scale_edited


########
# Model-Space Transform Math
########

# Mirrors BoneTransform and ModelBone in Customize+
# Incase anyone is curious here are the main references to the relevant C+ source files:
# https://github.com/Aether-Tools/CustomizePlus/blob/44d25415b961e0bbba759d1508b6d06acef88d90/CustomizePlus/Core/Data/BoneTransform.cs
# https://github.com/Aether-Tools/CustomizePlus/blob/44d25415b961e0bbba759d1508b6d06acef88d90/CustomizePlus/Armatures/Data/ModelBone.cs


def _rotation_offset(rotation: mathutils.Vector) -> mathutils.Quaternion:
    # Customize+ passes X, Y, Z to .NET's yaw(Y), pitch(X), roll(Z).
    yaw = mathutils.Quaternion((0.0, 1.0, 0.0), math.radians(rotation.x))
    pitch = mathutils.Quaternion((1.0, 0.0, 0.0), math.radians(rotation.y))
    roll = mathutils.Quaternion((0.0, 0.0, 1.0), math.radians(rotation.z))
    return yaw @ pitch @ roll


def _model_trs(matrix: mathutils.Matrix, name: str) -> mathutils.Matrix:
    position, rotation, scale = matrix.decompose()
    result = mathutils.Matrix.LocRotScale(position, rotation, scale)
    basis_error = max(abs(matrix[row][col] - result[row][col]) for row in range(3) for col in range(3))
    if basis_error > _MATRIX_ERROR_TOLERANCE:
        warnings.warn(
            f"Bone '{name}' requires shear extraction: Blender TRS is used; native Havok parity is unverified",
            RuntimeWarning,
            stacklevel=2,
        )
    return result


def _propagate_to_descendants(
    bone_name: str,
    model_matrices: dict[str, mathutils.Matrix],
    parents: Mapping[str, str | None],
    original_position: mathutils.Vector,
    rotation_delta: mathutils.Quaternion,
    child_scale: mathutils.Vector,
    propagate_rotation: bool,
    propagate_scale: bool,
) -> None:
    """Update descendant model matrices using Customize+'s post-edit pivot."""
    source_position = model_matrices[bone_name].translation
    translation_delta = source_position - original_position
    scale_matrix = mathutils.Matrix.Diagonal((*child_scale, 1.0))
    rotation_matrix = rotation_delta.to_matrix().to_4x4()

    for child_name, child_matrix in model_matrices.items():
        ancestor = parents.get(child_name)
        while ancestor is not None and ancestor != bone_name:
            ancestor = parents.get(ancestor)
        if ancestor != bone_name:
            continue

        offset_from_source = child_matrix.translation - source_position
        if propagate_scale:
            child_matrix = scale_matrix @ child_matrix
            offset_from_source = scale_matrix.to_3x3() @ offset_from_source
        if propagate_rotation:
            child_matrix = rotation_matrix @ child_matrix
            offset_from_source = rotation_delta @ offset_from_source

        # Upstream adds translation_delta even if PropagateTranslation is false.
        child_matrix.translation = translation_delta + source_position + offset_from_source
        model_matrices[child_name] = _model_trs(child_matrix, child_name)


def calculate_model_transforms(
    matrices: Mapping[str, mathutils.Matrix],
    parents: Mapping[str, str | None],
    cplus_data: Mapping[str, Any],
    translation_factor: float = 1.0,
) -> dict[str, mathutils.Matrix]:
    """Evaluate C+ edits in game model space, independently of Blender parenting."""
    ########
    # Read Bone Edits
    ########
    bone_data = _get_bones(cplus_data)
    if not math.isfinite(translation_factor) or translation_factor <= 0:
        raise ValueError("Translation unit factor must be positive and finite")
    edits = {name: _BoneTransform.from_data(name, data) for name, data in bone_data.items()}

    ########
    # Transform Bones and Propagate Changes
    ########
    model_matrices = {name: matrix.copy() for name, matrix in matrices.items()}
    root_edit = None
    for bone_name in model_matrices:
        if bone_name not in edits:
            continue
        edit = edits[bone_name]
        if bone_name == "n_root" and parents.get(bone_name) is None:
            root_edit = edit
            continue
        if not edit.is_edited():
            continue

        translation_offset = edit.translation * translation_factor
        rotation_offset = _rotation_offset(edit.rotation)
        scale_multiplier = edit.scale
        original_position, original_rotation, original_scale = model_matrices[bone_name].decompose()

        rotation = original_rotation @ rotation_offset
        scale = mathutils.Vector(original * multiplier for original, multiplier in zip(original_scale, scale_multiplier))
        position = original_position + rotation @ translation_offset
        model_matrices[bone_name] = mathutils.Matrix.LocRotScale(position, rotation, scale)

        if not (edit.propagate_translation or edit.propagate_rotation or edit.propagate_scale):
            continue

        child_scale = edit.child_scale if edit.child_scaling_independent else scale_multiplier
        identity_scale = mathutils.Vector((1.0, 1.0, 1.0))
        propagate_scale = edit.propagate_scale and (
            scale_multiplier != identity_scale or (edit.child_scaling_independent and child_scale != identity_scale)
        )
        propagate_rotation = edit.propagate_rotation and edit.rotation.length_squared != 0
        _propagate_to_descendants(
            bone_name,
            model_matrices,
            parents,
            original_position,
            rotation @ original_rotation.inverted(),
            child_scale,
            propagate_rotation,
            propagate_scale,
        )

    ########
    # Apply Root Transform to the Whole Actor
    ########
    if root_edit is not None:
        root_scale = root_edit.scale
        root_matrix = mathutils.Matrix.Identity(4)
        if any(value != 0.0 and value != 1.0 for value in root_scale):
            root_matrix = mathutils.Matrix.Diagonal((*root_scale, 1.0))
        if any(abs(value) >= _VECTOR_EDIT_EPSILON for value in root_edit.translation):
            root_matrix.translation = root_edit.translation * translation_factor
        model_matrices = {name: _model_trs(root_matrix @ matrix, name) for name, matrix in model_matrices.items()}
    return model_matrices


########
# Apply Transforms to Blender
########


def apply_transforms(
    armature: bpy.types.Object,
    cplus_data: Mapping[str, Any],
    bones: Mapping[str, bpy.types.PoseBone] | None = None,
    primary_axis: str = DEFAULT_PRIMARY_BONE_AXIS,
    secondary_axis: str = DEFAULT_SECONDARY_BONE_AXIS,
    gltf_model_space: bool = True,
    translation_factor: float | None = None,
) -> dict[str, str]:
    """Set model-space C+ poses without unparenting or editing rest orientations."""
    if armature.type != "ARMATURE" or armature.mode == "EDIT":
        raise ValueError("C+ transforms require an armature in Object or Pose mode")
    if translation_factor is None:
        translation_factor = 1.0 / bpy.context.scene.unit_settings.scale_length
    target_bones = dict(bones) if bones is not None else {bone.name: bone for bone in armature.pose.bones}
    ordered_bones = sorted(armature.pose.bones, key=lambda bone: len(bone.parent_recursive))

    ########
    # Convert Blender Bones to Game Coordinates
    ########
    bone_axis_correction = get_import_correction_matrix(primary_axis, secondary_axis)
    inverse_bone_axis_correction = bone_axis_correction.inverted()
    game_to_blender = mathutils.Matrix.Rotation(math.pi / 2, 4, "X") if gltf_model_space else mathutils.Matrix.Identity(4)
    blender_to_game = game_to_blender.inverted()
    # Convert model coordinates on the left, and bone-local axes on the right.
    game_matrices = {bone.name: blender_to_game @ bone.matrix @ inverse_bone_axis_correction for bone in ordered_bones}
    parents = {bone.name: bone.parent.name if bone.parent else None for bone in ordered_bones}

    # Excluded control bones do not receive named C+ edits, but still follow
    # explicitly propagated transforms so hierarchy evaluation stays coherent.
    filtered_data = dict(cplus_data)
    bone_data = _get_bones(cplus_data)
    filtered_data["Bones"] = {name: data for name, data in bone_data.items() if name in target_bones}
    game_targets = calculate_model_transforms(game_matrices, parents, filtered_data, translation_factor)
    blender_targets = {name: game_to_blender @ matrix @ bone_axis_correction for name, matrix in game_targets.items()}

    ########
    # Solve and Apply Blender Pose
    ########
    original_inheritance = {bone.name: bone.bone.inherit_scale for bone in ordered_bones}
    original_pose_basis = {bone.name: bone.matrix_basis.copy() for bone in ordered_bones}
    pose_applied = False
    try:
        for bone in ordered_bones:
            bone.bone.inherit_scale = "NONE"

        for bone in ordered_bones:
            target_matrix = blender_targets[bone.name]
            if bone.parent:
                bone.matrix_basis = bone.bone.convert_local_to_pose(
                    target_matrix,
                    bone.bone.matrix_local,
                    parent_matrix=blender_targets[bone.parent.name],
                    parent_matrix_local=bone.parent.bone.matrix_local,
                    invert=True,
                )
            else:
                bone.matrix_basis = bone.bone.convert_local_to_pose(target_matrix, bone.bone.matrix_local, invert=True)

        bpy.context.view_layer.update()
        for bone in ordered_bones:
            target_matrix = blender_targets[bone.name]
            evaluated_matrix = bone.matrix
            basis_error = max(abs(evaluated_matrix[row][col] - target_matrix[row][col]) for row in range(3) for col in range(3))
            position_error = max(abs(evaluated_matrix[row][3] - target_matrix[row][3]) for row in range(3))
            matrix_error = max(basis_error, position_error / translation_factor)
            if matrix_error > _MATRIX_ERROR_TOLERANCE:
                raise ValueError(f"Blender cannot represent the C+ model transform for '{bone.name}' (matrix error {matrix_error:.6g})")
        pose_applied = True
    finally:
        if not pose_applied:
            for bone in ordered_bones:
                bone.bone.inherit_scale = original_inheritance[bone.name]
                bone.matrix_basis = original_pose_basis[bone.name]
            bpy.context.view_layer.update()
    return original_inheritance


########
# MCDF File Reading
########


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
