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
