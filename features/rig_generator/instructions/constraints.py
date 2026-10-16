"""Constraint instructions: add a constraint to a bone of the rig."""
import bpy

from ._bones import get_pose_bone


def copy_transforms(
    rig: bpy.types.Object,
    bone: str,
    target: str,
    *,
    name: str = "AetherBlend_CopyTransform",
    remove_target_shear: bool = False,
    mix_mode: str = "REPLACE",
    target_space: str = "WORLD",
    owner_space: str = "WORLD",
    head_tail: float = 0.0,
    influence: float = 1.0,
) -> None:
    """Make a bone copy the transforms of the target bone."""
    pose_bone = get_pose_bone(rig, bone)
    if not pose_bone:
        return

    constraint = pose_bone.constraints.new(type="COPY_TRANSFORMS")
    constraint.name = name
    constraint.target = rig
    constraint.subtarget = target
    constraint.head_tail = head_tail
    constraint.remove_target_shear = remove_target_shear
    constraint.mix_mode = mix_mode
    constraint.target_space = target_space
    constraint.owner_space = owner_space
    constraint.influence = influence


def damped_track(
    rig: bpy.types.Object,
    bone: str,
    target: str,
    *,
    name: str = "AetherBlend_DampedTrack",
    track_axis: str = "TRACK_Y",
    head_tail: float = 0.0,
    influence: float = 1.0,
) -> None:
    """Make a bone point at the target bone."""
    pose_bone = get_pose_bone(rig, bone)
    if not pose_bone:
        return

    constraint = pose_bone.constraints.new(type="DAMPED_TRACK")
    constraint.name = name
    constraint.target = rig
    constraint.subtarget = target
    constraint.track_axis = track_axis
    constraint.head_tail = head_tail
    constraint.influence = influence


def limit_location(
    rig: bpy.types.Object,
    bone: str,
    *,
    name: str = "AetherBlend_LimitLocation",
    minimum: tuple[float | None, float | None, float | None] = (None, None, None),
    maximum: tuple[float | None, float | None, float | None] = (None, None, None),
    use_transform_limit: bool = False,
    owner_space: str = "LOCAL",
) -> None:
    """Limit the location of a bone per axis; None leaves that side of the axis free."""
    pose_bone = get_pose_bone(rig, bone)
    if not pose_bone:
        return

    constraint = pose_bone.constraints.new(type="LIMIT_LOCATION")
    constraint.name = name
    constraint.use_transform_limit = use_transform_limit
    constraint.owner_space = owner_space
    for index, axis in enumerate("xyz"):
        if minimum[index] is not None:
            setattr(constraint, f"use_min_{axis}", True)
            setattr(constraint, f"min_{axis}", minimum[index])
        if maximum[index] is not None:
            setattr(constraint, f"use_max_{axis}", True)
            setattr(constraint, f"max_{axis}", maximum[index])


def copy_location(
    rig: bpy.types.Object,
    bone: str,
    target: str,
    *,
    name: str = "AetherBlend_CopyLocation",
    target_space: str = "WORLD",
    owner_space: str = "WORLD",
    head_tail: float = 0.0,
    influence: float = 1.0,
) -> None:
    """Make a bone copy the location of the target bone."""
    pose_bone = get_pose_bone(rig, bone)
    if not pose_bone:
        return

    constraint = pose_bone.constraints.new(type="COPY_LOCATION")
    constraint.name = name
    constraint.target = rig
    constraint.subtarget = target
    constraint.head_tail = head_tail
    constraint.target_space = target_space
    constraint.owner_space = owner_space
    constraint.influence = influence
