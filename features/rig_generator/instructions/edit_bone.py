"""Edit-mode instructions: create and parent bones."""

import math
import re
from collections.abc import Sequence
from typing import Literal

import bpy
import mathutils

Point = Literal["head", "tail"]
Axis = Literal["X", "Y", "Z", "-X", "-Y", "-Z"]
AxisSpace = Literal["local", "armature", "global"]
BoneNames = str | Sequence[str]

_AXIS_INDEX = {"X": 0, "Y": 1, "Z": 2, "-X": 0, "-Y": 1, "-Z": 2}
_AXIS_SIGN = {"X": 1.0, "Y": 1.0, "Z": 1.0, "-X": -1.0, "-Y": -1.0, "-Z": -1.0}
_MINIMUM_AXIS_COMPONENT = 0.0001

# Parents whose preferred bone does not exist yet; resolved once every module has run.
_pending_parents: list[tuple[str, list[str], bool]] = []


def _as_list(names: BoneNames) -> list[str]:
    return [names] if isinstance(names, str) else list(names)


def _point(edit_bone: bpy.types.EditBone, point: Point) -> mathutils.Vector:
    return edit_bone.tail.copy() if point == "tail" else edit_bone.head.copy()


def _axis_direction(
    rig: bpy.types.Object, reference: bpy.types.EditBone, axis: Axis, axis_space: AxisSpace
) -> mathutils.Vector:
    index = _AXIS_INDEX[axis]
    sign = _AXIS_SIGN[axis]
    if axis_space == "local":
        return mathutils.Vector(reference.matrix.to_3x3().inverted()[index]) * sign

    unit_vector = mathutils.Vector((0.0, 0.0, 0.0))
    unit_vector[index] = sign
    if axis_space == "armature":
        return unit_vector
    return rig.matrix_world.to_3x3().inverted() @ unit_vector


def _assign_parent(
    rig: bpy.types.Object, bone_name: str, candidates: Sequence[str], connected: bool, *, report_failure: bool = True
) -> bool:
    edit_bones = rig.data.edit_bones
    edit_bone = edit_bones.get(bone_name)
    if not edit_bone:
        if report_failure:
            print(f"[AetherBlend] Cannot parent '{bone_name}': bone not found.")
        return False

    for candidate in candidates:
        parent_bone = edit_bones.get(candidate)
        if parent_bone:
            edit_bone.use_connect = connected
            edit_bone.parent = parent_bone
            return True

    if report_failure:
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


def copy(
    rig: bpy.types.Object,
    name: str,
    source_bone: str,
    *,
    parent: BoneNames | None = None,
    connected: bool = False,
    roll: float | None = None,
) -> None:
    """Create a bone at the position of a source bone; the roll of the source is kept unless one is given."""
    edit_source = rig.data.edit_bones.get(source_bone)
    if not edit_source:
        print(f"[AetherBlend] Cannot copy '{name}': '{source_bone}' not found.")
        return

    roll_degrees = math.degrees(edit_source.roll) if roll is None else roll
    _create_bone(rig, name, edit_source.head.copy(), edit_source.tail.copy(), parent, connected, roll_degrees)


def center(
    rig: bpy.types.Object,
    name: str,
    reference_bones: Sequence[str],
    *,
    size_factor: float = 1.0,
    axis: Axis = "Z",
    inverted: bool = False,
    parent: BoneNames | None = None,
    connected: bool = False,
) -> None:
    """Create a bone at the average head of the reference bones, pointing along an armature axis."""
    edit_bones = rig.data.edit_bones
    references = [edit_bones[reference] for reference in reference_bones if reference in edit_bones]
    if not references:
        print(f"[AetherBlend] Cannot create '{name}': none of {list(reference_bones)} found.")
        return

    center_position = sum((reference.head for reference in references), mathutils.Vector((0.0, 0.0, 0.0))) / len(
        references
    )
    average_length = sum(reference.length for reference in references) / len(references)
    length = (average_length if average_length > 0 else 0.3) * size_factor

    direction = mathutils.Vector((0.0, 0.0, 0.0))
    direction[_AXIS_INDEX[axis]] = length * _AXIS_SIGN[axis]
    if inverted:
        head, tail = center_position + direction, center_position
    else:
        head, tail = center_position, center_position + direction
    _create_bone(rig, name, head, tail, parent, connected, 0.0)


def offset(
    rig: bpy.types.Object,
    name: str,
    source_bone: str,
    local_offset: Sequence[float],
    *,
    size_factor: float = 1.0,
    parent: BoneNames | None = None,
    connected: bool = False,
    roll: float = 0.0,
) -> None:
    """Create a bone shifted from a source bone by a vector in the source bone's own axes."""
    edit_source = rig.data.edit_bones.get(source_bone)
    if not edit_source:
        print(f"[AetherBlend] Cannot offset '{name}': '{source_bone}' not found.")
        return

    head = edit_source.head + edit_source.matrix.to_3x3() @ mathutils.Vector(local_offset)
    tail = head + (edit_source.tail - edit_source.head) * size_factor
    _create_bone(rig, name, head, tail, parent, connected, roll)


def bridge(
    rig: bpy.types.Object,
    name: str,
    start_bone: str,
    end_bone: str,
    *,
    offset: Sequence[float] = (0.0, 0.0, 0.0),
    start_parent: BoneNames | None = None,
    connect_end: bool = True,
) -> None:
    """Split the way from start_bone to end_bone with a bone at the midpoint shifted by an offset.

    The start bone is shortened to end at the new bone, which continues to the head of the end bone.
    With connect_end the end bone is attached to the new bone. start_parent re-parents the start bone.
    """
    edit_bones = rig.data.edit_bones
    edit_start = edit_bones.get(start_bone)
    edit_end = edit_bones.get(end_bone)
    if not edit_start or not edit_end:
        print(f"[AetherBlend] Cannot bridge '{name}': '{start_bone}' or '{end_bone}' not found.")
        return

    end_position = edit_end.head.copy()
    bridge_head = (edit_start.head + end_position) / 2.0 + mathutils.Vector(offset)

    existing_bone = edit_bones.get(name)
    if existing_bone:
        edit_bones.remove(existing_bone)

    new_bone = edit_bones.new(name)
    new_bone.head = bridge_head
    new_bone.tail = end_position
    edit_start.tail = bridge_head
    new_bone.parent = edit_start
    new_bone.use_connect = True

    if start_parent:
        parent(rig, start_bone, start_parent)
    if connect_end:
        edit_end.parent = new_bone
        edit_end.use_connect = True


def _heaviest_vertex_position(
    source_rig: bpy.types.Object, mesh: bpy.types.Object, bone: str
) -> mathutils.Vector | None:
    vertex_group = mesh.vertex_groups.get(bone)
    deformed_by_rig = any(modifier.type == "ARMATURE" and modifier.object == source_rig for modifier in mesh.modifiers)
    if not vertex_group or not deformed_by_rig:
        return None

    evaluated_mesh_object = mesh.evaluated_get(bpy.context.evaluated_depsgraph_get())
    evaluated_mesh = evaluated_mesh_object.to_mesh()
    try:
        original_vertices = mesh.data.vertices
        if len(evaluated_mesh.vertices) != len(original_vertices):
            return None

        best_weight = 0.0
        best_position = None
        for index, vertex in enumerate(original_vertices):
            for assignment in vertex.groups:
                if assignment.group == vertex_group.index and assignment.weight > best_weight:
                    best_weight = assignment.weight
                    best_position = mesh.matrix_world @ evaluated_mesh.vertices[index].co
        return best_position
    finally:
        evaluated_mesh_object.to_mesh_clear()


def heaviest_vertex(
    rig: bpy.types.Object,
    name: str,
    bone: str,
    mesh: bpy.types.Object,
    *,
    source_rig: bpy.types.Object,
    size_factor: float = 1.0,
    parent: BoneNames | None = None,
) -> None:
    """Create an upright bone at the vertex of the mesh that the bone's vertex group weights the most.

    source_rig is the armature that deforms the mesh; the new bone is as long as the bone times size_factor.
    """
    edit_reference = rig.data.edit_bones.get(bone)
    if not edit_reference:
        print(f"[AetherBlend] Cannot place '{name}': '{bone}' not found.")
        return

    world_position = _heaviest_vertex_position(source_rig, mesh, bone)
    if world_position is None:
        print(f"[AetherBlend] Cannot place '{name}': no weighted vertices for '{bone}' on '{mesh.name}'.")
        return

    length = (edit_reference.length if edit_reference.length > 0 else 0.3) * size_factor
    head = rig.matrix_world.inverted() @ world_position
    _create_bone(rig, name, head, head + mathutils.Vector((0.0, 0.0, length)), parent, False, 0.0)


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
    """Parent a bone, retrying unresolved requests at the end of the edit phase."""
    candidates = _as_list(new_parent)
    _pending_parents[:] = [request for request in _pending_parents if request[0] != bone]
    if not _assign_parent(rig, bone, candidates, connected, report_failure=False):
        _pending_parents.append((bone, candidates, connected))


def resolve_pending_parents(rig: bpy.types.Object) -> None:
    """Make the final parenting attempts for this edit phase and report unresolved requests."""
    for bone_name, candidates, connected in _pending_parents:
        _assign_parent(rig, bone_name, candidates, connected)
    _pending_parents.clear()


def find_chains(rig: bpy.types.Object, pattern: str) -> list[list[str]]:
    """Group the bones whose name matches the regular expression into parent-child chains."""
    edit_bones = rig.data.edit_bones
    matching_names = [bone.name for bone in edit_bones if re.match(pattern, bone.name)]

    chains: list[list[str]] = []
    for name in matching_names:
        parent_bone = edit_bones[name].parent
        if parent_bone and re.match(pattern, parent_bone.name):
            continue
        chain = [name]
        current = edit_bones[name]
        while True:
            matching_children = [child for child in current.children if re.match(pattern, child.name)]
            if not matching_children:
                break
            current = matching_children[0]
            chain.append(current.name)
        chains.append(chain)
    return chains


def has_bone(rig: bpy.types.Object, bone: str) -> bool:
    """Whether the bone exists in the rig while it is in edit mode."""
    return bone in rig.data.edit_bones


def require_bones(rig: bpy.types.Object, bones: Sequence[str], module_name: str) -> bool:
    """Let a module check its own source bones and report why it cannot build."""
    missing = [bone for bone in bones if not has_bone(rig, bone)]
    if missing:
        print(f"[AetherBlend] Skipping module '{module_name}': missing bones {missing}")
    return not missing
