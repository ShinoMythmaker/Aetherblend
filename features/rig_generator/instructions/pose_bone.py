"""Pose-mode instructions: bone collections, custom properties and links."""
from collections.abc import Sequence

import bpy

from .... import utils
from . import constraints, rigify
from ._bones import get_pose_bone

LINKED_PROPERTY = "ab_linked"


def collection(rig: bpy.types.Object, bones: Sequence[str], collection_name: str) -> None:
    """Assign bones to a bone collection."""
    utils.armature.b_collection.assign_bones(rig, list(bones), collection_name)


def prop(rig: bpy.types.Object, bone: str, property_name: str, value: float | int | str) -> None:
    """Set a custom property on a bone."""
    pose_bone = get_pose_bone(rig, bone)
    if pose_bone:
        pose_bone[property_name] = value


def link(rig: bpy.types.Object, source_bone: str, target: str) -> None:
    """Make an original bone follow the generated bone `target` through its LINK copy."""
    link_bone = f"LINK-{source_bone}"
    link_pose_bone = get_pose_bone(rig, link_bone)
    if not get_pose_bone(rig, source_bone) or not link_pose_bone:
        return

    constraints.copy_transforms(rig, source_bone, link_bone, name=f"AB-LINK@{link_bone}", remove_target_shear=True)
    rigify.basic_raw_copy(rig, link_bone, relink_constraints=True, parent=target)
    link_pose_bone[LINKED_PROPERTY] = True
