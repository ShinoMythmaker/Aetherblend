"""Pose-mode instructions: bone collections, custom properties and links."""

from collections.abc import Sequence

import bpy

from .... import utils
from . import constraints, rigify

LINKED_PROPERTY = "ab_linked"


def collection(rig: bpy.types.Object, bones: Sequence[str], collection_name: str) -> None:
    """Assign bones to a bone collection."""
    utils.armature.b_collection.assign_bones(rig, list(bones), collection_name)


def prop(rig: bpy.types.Object, bone: str, property_name: str, value: float | int | str) -> None:
    """Set a custom property on a bone."""
    pose_bone = utils.armature.get_pose_bone(rig, bone)
    if pose_bone:
        pose_bone[property_name] = value


def restrict(
    rig: bpy.types.Object,
    bone: str,
    *,
    hide_select: bool | None = None,
    lock_location: bool | tuple[bool, bool, bool] | None = None,
    lock_rotation: bool | tuple[bool, bool, bool] | None = None,
    lock_scale: bool | tuple[bool, bool, bool] | None = None,
    inherit_rotation: bool | None = None,
    inherit_scale: str | None = None,
) -> None:
    """Lock transform channels, make a bone unselectable or change what it inherits."""
    pose_bone = utils.armature.get_pose_bone(rig, bone)
    if not pose_bone:
        return

    def axes(value: bool | tuple[bool, bool, bool]) -> tuple[bool, bool, bool]:
        return (value, value, value) if isinstance(value, bool) else value

    if hide_select is not None:
        pose_bone.bone.hide_select = hide_select
    if lock_location is not None:
        pose_bone.lock_location = axes(lock_location)
    if lock_rotation is not None:
        pose_bone.lock_rotation = axes(lock_rotation)
    if lock_scale is not None:
        pose_bone.lock_scale = axes(lock_scale)
    if inherit_rotation is not None:
        pose_bone.bone.use_inherit_rotation = inherit_rotation
    if inherit_scale is not None:
        pose_bone.bone.inherit_scale = inherit_scale


def pose(rig: bpy.types.Object, bone: str, *, scale: tuple[float, float, float]) -> None:
    """Set the pose scale of a bone."""
    pose_bone = utils.armature.get_pose_bone(rig, bone)
    if pose_bone:
        pose_bone.scale = scale


def link(rig: bpy.types.Object, source_bone: str, target: str, *, location_only: bool = False) -> None:
    """Make an original bone follow the generated bone `target` through its LINK copy."""
    link_bone = f"LINK-{source_bone}"
    link_pose_bone = utils.armature.get_pose_bone(rig, link_bone)
    if not utils.armature.get_pose_bone(rig, source_bone) or not link_pose_bone:
        return

    if location_only:
        constraints.copy_location(rig, source_bone, link_bone, name=f"AB-LINK@{link_bone}")
    else:
        constraints.copy_transforms(rig, source_bone, link_bone, name=f"AB-LINK@{link_bone}", remove_target_shear=True)
    rigify.basic_raw_copy(rig, link_bone, relink_constraints=True, parent=target)
    link_pose_bone[LINKED_PROPERTY] = True


def armature_prop(
    rig: bpy.types.Object,
    property_name: str,
    value: float,
    *,
    minimum: float | None = None,
    maximum: float | None = None,
) -> None:
    """Define a float property on the armature data, set its value and make it available to drivers and the UI."""
    options = {}
    if minimum is not None:
        options["min"] = minimum
    if maximum is not None:
        options["max"] = maximum

    setattr(type(rig.data), property_name, bpy.props.FloatProperty(**options))
    setattr(rig.data, property_name, value)
