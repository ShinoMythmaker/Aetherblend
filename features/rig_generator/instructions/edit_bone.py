"""Edit-mode instructions: create and parent bones."""
import math
from collections.abc import Sequence
from typing import Literal

import bpy
import mathutils

Point = Literal["head", "tail"]
Axis = Literal["X", "Y", "Z"]
AxisSpace = Literal["local", "armature", "global"]
BoneNames = str | Sequence[str]

_AXIS_INDEX = {"X": 0, "Y": 1, "Z": 2}
_MINIMUM_AXIS_COMPONENT = 0.0001

# Parents whose preferred bone does not exist yet; resolved once every module has run.
_pending_parents: list[tuple[str, list[str], bool]] = []


def _as_list(names: BoneNames) -> list[str]:
    return [names] if isinstance(names, str) else list(names)


def _point(edit_bone: bpy.types.EditBone, point: Point) -> mathutils.Vector:
    return edit_bone.tail.copy() if point == "tail" else edit_bone.head.copy()


def _axis_direction(rig: bpy.types.Object, reference: bpy.types.EditBone, axis: Axis, axis_space: AxisSpace) -> mathutils.Vector:
    index = _AXIS_INDEX[axis]
    if axis_space == "local":
        return mathutils.Vector(reference.matrix.to_3x3().inverted()[index])

    unit_vector = mathutils.Vector((0.0, 0.0, 0.0))
    unit_vector[index] = 1.0
    if axis_space == "armature":
        return unit_vector
    return rig.matrix_world.to_3x3().inverted() @ unit_vector


def _assign_parent(rig: bpy.types.Object, bone_name: str, candidates: Sequence[str], connected: bool) -> bool:
    edit_bones = rig.data.edit_bones
    edit_bone = edit_bones.get(bone_name)
    if not edit_bone:
        print(f"[AetherBlend] Cannot parent '{bone_name}': bone not found.")
        return False

    for candidate in candidates:
        parent_bone = edit_bones.get(candidate)
        if parent_bone:
            edit_bone.use_connect = connected
            edit_bone.parent = parent_bone
            return True

    print(f"[AetherBlend] Cannot parent '{bone_name}': none of {list(candidates)} exist.")
    return False


def _create_bone(
    rig: bpy.types.Object,
    name: str,
    head: mathutils.Vector,
    tail: mathutils.Vector,
    parent_bone: BoneNames | None,
    connected: bool,
    roll: float,
) -> None:
    edit_bones = rig.data.edit_bones
    existing_bone = edit_bones.get(name)
    if existing_bone:
        edit_bones.remove(existing_bone)

    new_bone = edit_bones.new(name)
    new_bone.head = head
    new_bone.tail = tail
    new_bone.roll = math.radians(roll)

    if not parent_bone:
        return

    candidates = _as_list(parent_bone)
    if edit_bones.get(candidates[0]):
        _assign_parent(rig, name, candidates, connected)
    else:
        _pending_parents.append((name, candidates, connected))


def connect(
    rig: bpy.types.Object,
    name: str,
    start_bone: str,
    end_bone: str,
    *,
    start_point: Point = "head",
    end_point: Point = "head",
    parent: BoneNames | None = None,
    connected: bool = False,
    roll: float = 0.0,
) -> None:
    """Create a bone running from a point of one bone to a point of another."""
    edit_bones = rig.data.edit_bones
    first_bone = edit_bones.get(start_bone)
    second_bone = edit_bones.get(end_bone)
    if not first_bone or not second_bone:
        print(f"[AetherBlend] Cannot connect '{name}': '{start_bone}' or '{end_bone}' not found.")
        return

    _create_bone(rig, name, _point(first_bone, start_point), _point(second_bone, end_point), parent, connected, roll)


def extend(
    rig: bpy.types.Object,
    name: str,
    source_bone: str,
    *,
    size_factor: float = 1.0,
    axis: Axis = "Y",
    axis_space: AxisSpace = "local",
    start_point: Point = "tail",
    parent: BoneNames | None = None,
    connected: bool = False,
    roll: float = 0.0,
) -> None:
    """Create a bone that continues from a source bone along an axis."""
    edit_source = rig.data.edit_bones.get(source_bone)
    if not edit_source:
        print(f"[AetherBlend] Cannot extend '{name}': '{source_bone}' not found.")
        return

    head = _point(edit_source, start_point)
    direction = _axis_direction(rig, edit_source, axis, axis_space).normalized()
    source_length = edit_source.length if edit_source.length > 0 else 1.0
    tail = head + direction * source_length * size_factor
    _create_bone(rig, name, head, tail, parent, connected, roll)


def parallel(
    rig: bpy.types.Object,
    name: str,
    start_bone: str,
    target_bone: str,
    *,
    coordinate: Axis = "Y",
    axis: Axis = "Y",
    axis_space: AxisSpace = "local",
    start_point: Point = "tail",
    end_point: Point = "head",
    parent: BoneNames | None = None,
    connected: bool = False,
    roll: float = 0.0,
) -> None:
    """Create a bone along an axis from the start bone until it reaches the target point's coordinate."""
    edit_bones = rig.data.edit_bones
    edit_start = edit_bones.get(start_bone)
    edit_target = edit_bones.get(target_bone)
    if not edit_start or not edit_target:
        print(f"[AetherBlend] Cannot create '{name}': '{start_bone}' or '{target_bone}' not found.")
        return

    head = _point(edit_start, start_point)
    target_point = _point(edit_target, end_point)
    direction = _axis_direction(rig, edit_start, axis, axis_space).normalized()

    coordinate_index = _AXIS_INDEX[coordinate]
    if abs(direction[coordinate_index]) < _MINIMUM_AXIS_COMPONENT:
        print(f"[AetherBlend] Cannot create '{name}': axis never reaches coordinate {coordinate}.")
        return

    distance = (target_point[coordinate_index] - head[coordinate_index]) / direction[coordinate_index]
    _create_bone(rig, name, head, head + direction * distance, parent, connected, roll)


def parent(rig: bpy.types.Object, bone: str, new_parent: BoneNames, *, connected: bool = False) -> None:
    """Parent a bone to the first existing bone of new_parent."""
    _assign_parent(rig, bone, _as_list(new_parent), connected)


def resolve_pending_parents(rig: bpy.types.Object) -> None:
    """Parent bones whose preferred parent did not exist when they were created."""
    for bone_name, candidates, connected in _pending_parents:
        _assign_parent(rig, bone_name, candidates, connected)
    _pending_parents.clear()
