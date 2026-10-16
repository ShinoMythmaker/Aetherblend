"""Rigify type instructions: give a bone a rigify type and its parameters."""
import bpy

from ._bones import get_pose_bone


def _activate(rig: bpy.types.Object, pose_bone: bpy.types.PoseBone, rigify_type: str) -> None:
    rig.data.bones.active = pose_bone.bone
    pose_bone.rigify_type = rigify_type


def _set_collection_reference(rigify_parameters, reference_property: str, collection_name: str) -> None:
    """Replace a rigify collection reference list with a single reference to the named collection."""
    references = getattr(rigify_parameters, reference_property)
    references.clear()
    bpy.ops.pose.rigify_collection_ref_add(prop_name=reference_property)
    if len(references) > 0:
        references[-1].name = collection_name


def limbs_leg(
    rig: bpy.types.Object,
    bone: str,
    *,
    fk_collection: str | None = None,
    tweak_collection: str | None = None,
) -> None:
    """Rigify type limbs.leg."""
    pose_bone = get_pose_bone(rig, bone)
    if not pose_bone:
        return

    _activate(rig, pose_bone, "limbs.leg")
    if fk_collection:
        _set_collection_reference(pose_bone.rigify_parameters, "fk_coll_refs", fk_collection)
    if tweak_collection:
        _set_collection_reference(pose_bone.rigify_parameters, "tweak_coll_refs", tweak_collection)


def basic_super_copy(rig: bpy.types.Object, bone: str, *, widget_type: str | None = None) -> None:
    """Rigify type basic.super_copy: a simple control bone."""
    pose_bone = get_pose_bone(rig, bone)
    if not pose_bone:
        return

    _activate(rig, pose_bone, "basic.super_copy")
    if widget_type:
        pose_bone.rigify_parameters.super_copy_widget_type = widget_type


def basic_raw_copy(
    rig: bpy.types.Object,
    bone: str,
    *,
    relink_constraints: bool = False,
    parent: str | None = None,
    widget_type: str | None = None,
) -> None:
    """Rigify type basic.raw_copy: copies the bone as is; `parent` only applies together with relink_constraints."""
    pose_bone = get_pose_bone(rig, bone)
    if not pose_bone:
        return

    _activate(rig, pose_bone, "basic.raw_copy")
    rigify_parameters = pose_bone.rigify_parameters
    if relink_constraints:
        rigify_parameters.relink_constraints = True
        if parent:
            rigify_parameters.parent_bone = parent
    if widget_type:
        rigify_parameters.raw_copy_widget_type = widget_type
