"""Rigify type instructions: give a bone a rigify type and its parameters."""

from collections.abc import Sequence

import bpy

from .... import utils


def _activate(rig: bpy.types.Object, pose_bone: bpy.types.PoseBone, rigify_type: str) -> None:
    rig.data.bones.active = pose_bone.bone
    pose_bone.rigify_type = rigify_type


def _set_collection_reference(rigify_parameters: bpy.types.PropertyGroup, reference_property: str, collection_name: str) -> None:
    """Replace a rigify collection reference list with a single reference to the named collection."""
    references = getattr(rigify_parameters, reference_property)
    references.clear()
    bpy.ops.pose.rigify_collection_ref_add(prop_name=reference_property)
    if len(references) > 0:
        references[-1].name = collection_name


def _set_control_collection(rigify_parameters: bpy.types.PropertyGroup, control: str, collection_name: str | None) -> None:
    """Disable collection overrides when controls should keep their inherited collections."""
    setattr(rigify_parameters, f"{control}_layers_extra", collection_name is not None)
    if collection_name is None:
        getattr(rigify_parameters, f"{control}_coll_refs").clear()
    else:
        _set_collection_reference(rigify_parameters, f"{control}_coll_refs", collection_name)


def limbs_leg(
    rig: bpy.types.Object,
    bone: str,
    *,
    fk_collection: str | None = None,
    tweak_collection: str | None = None,
) -> None:
    """Rigify type limbs.leg."""
    pose_bone = utils.armature.get_pose_bone(rig, bone)
    if not pose_bone:
        return

    _activate(rig, pose_bone, "limbs.leg")
    _set_control_collection(pose_bone.rigify_parameters, "fk", fk_collection)
    _set_control_collection(pose_bone.rigify_parameters, "tweak", tweak_collection)


def basic_super_copy(rig: bpy.types.Object, bone: str, *, widget_type: str | None = None) -> None:
    """Rigify type basic.super_copy: a simple control bone."""
    pose_bone = utils.armature.get_pose_bone(rig, bone)
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
    pose_bone = utils.armature.get_pose_bone(rig, bone)
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


def limbs_spline_tentacle(
    rig: bpy.types.Object,
    bone: str,
    *,
    fk_collection: str | None = None,
    tweak_collection: str | None = None,
    sik_stretch_control: str | None = None,
) -> None:
    """Rigify type limbs.spline_tentacle."""
    pose_bone = utils.armature.get_pose_bone(rig, bone)
    if not pose_bone:
        return

    _activate(rig, pose_bone, "limbs.spline_tentacle")
    if sik_stretch_control:
        pose_bone.rigify_parameters.sik_stretch_control = sik_stretch_control
    _set_control_collection(pose_bone.rigify_parameters, "fk", fk_collection)
    _set_control_collection(pose_bone.rigify_parameters, "tweak", tweak_collection)


def basic_copy_chain(
    rig: bpy.types.Object,
    bone: str,
    *,
    make_deforms: bool | None = None,
    make_controls: bool | None = None,
) -> None:
    """Rigify type basic.copy_chain."""
    pose_bone = utils.armature.get_pose_bone(rig, bone)
    if not pose_bone:
        return

    _activate(rig, pose_bone, "basic.copy_chain")
    if make_deforms is not None:
        pose_bone.rigify_parameters.make_deforms = make_deforms
    if make_controls is not None:
        pose_bone.rigify_parameters.make_controls = make_controls


def limbs_arm(
    rig: bpy.types.Object,
    bone: str,
    *,
    fk_collection: str | None = None,
    tweak_collection: str | None = None,
    rotation_axis: str | None = None,
    auto_align_extremity: bool = False,
) -> None:
    """Rigify type limbs.arm."""
    pose_bone = utils.armature.get_pose_bone(rig, bone)
    if not pose_bone:
        return

    _activate(rig, pose_bone, "limbs.arm")
    if rotation_axis:
        pose_bone.rigify_parameters.rotation_axis = rotation_axis
        pose_bone.rigify_parameters.auto_align_extremity = auto_align_extremity
    _set_control_collection(pose_bone.rigify_parameters, "fk", fk_collection)
    _set_control_collection(pose_bone.rigify_parameters, "tweak", tweak_collection)


def spines_basic_spine(
    rig: bpy.types.Object,
    bone: str,
    *,
    fk_collection: str | None = None,
    tweak_collection: str | None = None,
    pivot_position: int | None = None,
) -> None:
    """Rigify type spines.basic_spine."""
    pose_bone = utils.armature.get_pose_bone(rig, bone)
    if not pose_bone:
        return

    _activate(rig, pose_bone, "spines.basic_spine")
    _set_control_collection(pose_bone.rigify_parameters, "fk", fk_collection)
    _set_control_collection(pose_bone.rigify_parameters, "tweak", tweak_collection)
    if pivot_position is not None:
        pose_bone.rigify_parameters.pivot_pos = pivot_position


def spines_super_head(rig: bpy.types.Object, bone: str, *, tweak_collection: str | None = None) -> None:
    """Rigify type spines.super_head."""
    pose_bone = utils.armature.get_pose_bone(rig, bone)
    if not pose_bone:
        return

    _activate(rig, pose_bone, "spines.super_head")
    _set_control_collection(pose_bone.rigify_parameters, "tweak", tweak_collection)


def limbs_super_finger(
    rig: bpy.types.Object,
    bone: str,
    *,
    primary_rotation_axis: str | None = None,
    tweak_collection: str | None = None,
    extra_ik_control: bool = False,
    extra_ik_collection: str | None = None,
) -> None:
    """Rigify type limbs.super_finger: fingers and toes; the extra IK collection is only referenced if it exists."""
    pose_bone = utils.armature.get_pose_bone(rig, bone)
    if not pose_bone:
        return

    _activate(rig, pose_bone, "limbs.super_finger")
    rigify_parameters = pose_bone.rigify_parameters
    if primary_rotation_axis:
        rigify_parameters.primary_rotation_axis = primary_rotation_axis
    _set_control_collection(rigify_parameters, "tweak", tweak_collection)
    _set_control_collection(
        rigify_parameters,
        "extra_ik",
        extra_ik_collection if extra_ik_collection and extra_ik_collection in rig.data.collections else None,
    )
    if extra_ik_control:
        rigify_parameters.make_extra_ik_control = True


def limbs_super_palm(rig: bpy.types.Object, bone: str, *, palm_both_sides: bool = False) -> None:
    """Rigify type limbs.super_palm: a palm control shared by the neighbouring fingers."""
    pose_bone = utils.armature.get_pose_bone(rig, bone)
    if not pose_bone:
        return

    _activate(rig, pose_bone, "limbs.super_palm")
    if palm_both_sides:
        pose_bone.rigify_parameters.palm_both_sides = True


def _extra_layer(
    rig: bpy.types.Object,
    rigify_parameters: bpy.types.PropertyGroup,
    layers_flag: str,
    reference_property: str,
    collection_name: str,
) -> None:
    """Show a skin chain's controls in an extra bone collection, if that collection exists."""
    setattr(rigify_parameters, layers_flag, True)
    getattr(rigify_parameters, reference_property).clear()
    if collection_name in rig.data.collections:
        _set_collection_reference(rigify_parameters, reference_property, collection_name)


def _skin_chain_parameters(
    rig: bpy.types.Object,
    rigify_parameters: bpy.types.PropertyGroup,
    *,
    chain_priority: int | None,
    control_orientation_bone: str | None,
    use_scale: Sequence[bool] | None,
) -> None:
    if chain_priority is not None:
        rigify_parameters.skin_chain_priority = chain_priority
    if control_orientation_bone:
        rigify_parameters.skin_control_orientation_bone = control_orientation_bone
    if use_scale is not None:
        rigify_parameters.skin_chain_use_scale = list(use_scale)


def face_skin_eye(rig: bpy.types.Object, bone: str) -> None:
    """Rigify type face.skin_eye."""
    pose_bone = utils.armature.get_pose_bone(rig, bone)
    if pose_bone:
        _activate(rig, pose_bone, "face.skin_eye")


def face_skin_jaw(rig: bpy.types.Object, bone: str, *, jaw_mouth_influence: float | None = None) -> None:
    """Rigify type face.skin_jaw."""
    pose_bone = utils.armature.get_pose_bone(rig, bone)
    if not pose_bone:
        return

    _activate(rig, pose_bone, "face.skin_jaw")
    if jaw_mouth_influence is not None:
        pose_bone.rigify_parameters.jaw_mouth_influence = jaw_mouth_influence


def skin_basic_chain(
    rig: bpy.types.Object,
    bone: str,
    *,
    chain_priority: int | None = None,
    control_orientation_bone: str | None = None,
    use_scale: Sequence[bool] | None = None,
) -> None:
    """Rigify type skin.basic_chain."""
    pose_bone = utils.armature.get_pose_bone(rig, bone)
    if not pose_bone:
        return

    _activate(rig, pose_bone, "skin.basic_chain")
    _skin_chain_parameters(
        rig,
        pose_bone.rigify_parameters,
        chain_priority=chain_priority,
        control_orientation_bone=control_orientation_bone,
        use_scale=use_scale,
    )


def skin_stretchy_chain(
    rig: bpy.types.Object,
    bone: str,
    *,
    pivot_position: int | None = None,
    falloff: Sequence[float] | None = None,
    falloff_length: bool | None = None,
    falloff_spherical: Sequence[bool] | None = None,
    chain_priority: int | None = None,
    control_orientation_bone: str | None = None,
    use_scale: Sequence[bool] | None = None,
    primary_collection: str | None = None,
    secondary_collection: str | None = None,
) -> None:
    """Rigify type skin.stretchy_chain."""
    pose_bone = utils.armature.get_pose_bone(rig, bone)
    if not pose_bone:
        return

    _activate(rig, pose_bone, "skin.stretchy_chain")
    parameters = pose_bone.rigify_parameters
    _skin_chain_parameters(
        rig,
        parameters,
        chain_priority=chain_priority,
        control_orientation_bone=control_orientation_bone,
        use_scale=use_scale,
    )
    if pivot_position is not None:
        parameters.skin_chain_pivot_pos = pivot_position
    if falloff is not None:
        parameters.skin_chain_falloff = list(falloff)
    if falloff_length is not None:
        parameters.skin_chain_falloff_length = falloff_length
    if falloff_spherical is not None:
        parameters.skin_chain_falloff_spherical = list(falloff_spherical)
    if primary_collection:
        _extra_layer(rig, parameters, "skin_primary_layers_extra", "skin_primary_coll_refs", primary_collection)
    if secondary_collection:
        _extra_layer(rig, parameters, "skin_secondary_layers_extra", "skin_secondary_coll_refs", secondary_collection)


def skin_glue(
    rig: bpy.types.Object,
    bone: str,
    *,
    relink_constraints: bool = False,
    use_tail: bool = False,
    reparent_tail: bool = False,
    add_constraint: str | None = None,
    add_constraint_influence: float | None = None,
) -> None:
    """Rigify type skin.glue."""
    pose_bone = utils.armature.get_pose_bone(rig, bone)
    if not pose_bone:
        return

    _activate(rig, pose_bone, "skin.glue")
    parameters = pose_bone.rigify_parameters
    if relink_constraints:
        parameters.relink_constraints = True
    if use_tail:
        parameters.skin_glue_use_tail = True
    if reparent_tail:
        parameters.skin_glue_tail_reparent = True
    if add_constraint:
        parameters.skin_glue_add_constraint = add_constraint
    if add_constraint_influence is not None:
        parameters.skin_glue_add_constraint_influence = add_constraint_influence


def skin_anchor(
    rig: bpy.types.Object,
    bone: str,
    *,
    pivot_master_widget_type: str | None = None,
    hide: bool | None = None,
) -> None:
    """Rigify type skin.anchor."""
    pose_bone = utils.armature.get_pose_bone(rig, bone)
    if not pose_bone:
        return

    _activate(rig, pose_bone, "skin.anchor")
    if pivot_master_widget_type:
        pose_bone.rigify_parameters.pivot_master_widget_type = pivot_master_widget_type
    if hide is not None:
        pose_bone.rigify_parameters.skin_anchor_hide = hide
