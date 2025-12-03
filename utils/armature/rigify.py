import bpy
from ...data import *

def _select_pose_bone(pose_bone: bpy.types.PoseBone, state: bool = True) -> None:
    """Helper function to select a pose bone in a version-compatible way.
    
    Blender 5.0+ uses pose_bone.select, while 4.x uses pose_bone.bone.select.
    """
    try:
        pose_bone.select = state
    except AttributeError:
        pose_bone.bone.select = state

def rigify_set_tweak_collection(armature: bpy.types.Armature, bone_name: str, collection_name: str) -> None:
    """Sets the rigify tweak collection for a given bone."""
    
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='POSE')
    
    pose_bone = armature.pose.bones.get(bone_name)
    _select_pose_bone(pose_bone)
    bpy.ops.pose.select_all(action='DESELECT')
    
    armature.data.bones.active = pose_bone.bone
    
    try:
        rigify_params = pose_bone.rigify_parameters
        
        rigify_params.tweak_coll_refs.clear()
        
        if collection_name in armature.data.collections:
            bpy.ops.pose.rigify_collection_ref_add(prop_name="tweak_coll_refs")
            
            if len(rigify_params.tweak_coll_refs) > 0:
                tweak_ref = rigify_params.tweak_coll_refs[-1]
                tweak_ref.name = collection_name
        else:
            print(f"[AetherBlend] Collection '{collection_name}' not found in armature '{armature.name}'")
            
    except Exception as e:
        print(f"[AetherBlend] Error setting rigify tweak collection: {e}")
    
    bpy.ops.object.mode_set(mode='OBJECT')

def rigify_set_fk_collection(armature: bpy.types.Armature, bone_name: str, collection_name: str) -> None:
    """Sets the rigify FK collection for a given bone."""
    
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='POSE')
    
    pose_bone = armature.pose.bones.get(bone_name)
    
    bpy.ops.pose.select_all(action='DESELECT')
    _select_pose_bone(pose_bone)
    armature.data.bones.active = pose_bone.bone
    
    try:
        rigify_params = pose_bone.rigify_parameters
        
        rigify_params.tweak_coll_refs.clear()
        
        if collection_name in armature.data.collections:
            bpy.ops.pose.rigify_collection_ref_add(prop_name="fk_coll_refs")

            if len(rigify_params.fk_coll_refs) > 0:
                fk_ref = rigify_params.fk_coll_refs[-1]
                fk_ref.name = collection_name
        else:
            print(f"[AetherBlend] Collection '{collection_name}' not found in armature '{armature.name}'")
            
    except Exception as e:
        print(f"[AetherBlend] Error setting rigify FK collection: {e}")
    
    bpy.ops.object.mode_set(mode='OBJECT')

def rigify_set_copy_rotation_axes(armature: bpy.types.Armature, bone_name: str, use_x: bool, use_y: bool, use_z: bool) -> None:
    """sets rigify copy rotation axes parameter for a given bone."""

    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='POSE')
    
    pose_bone = armature.pose.bones.get(bone_name)
    
    bpy.ops.pose.select_all(action='DESELECT')
    _select_pose_bone(pose_bone)
    armature.data.bones.active = pose_bone.bone
    
    try:
        rigify_params = pose_bone.rigify_parameters
        
        rigify_params.copy_rotation_axes[0] = use_x
        rigify_params.copy_rotation_axes[1] = use_y
        rigify_params.copy_rotation_axes[2] = use_z
    except Exception as e:
        print(f"[AetherBlend] Error setting rigify copy rotation axes: {e}")
    
    bpy.ops.object.mode_set(mode='OBJECT')

def rigify_make_extra_ik_control(armature: bpy.types.Armature, bone_name: str, make_extra_ik_control: bool) -> None:
    """sets rigify make_extra_ik_control parameter for a given bone."""

    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='POSE')
    
    pose_bone = armature.pose.bones.get(bone_name)

    bpy.ops.pose.select_all(action='DESELECT')
    _select_pose_bone(pose_bone)
    armature.data.bones.active = pose_bone.bone

    try:
        rigify_params = pose_bone.rigify_parameters

        rigify_params.make_extra_ik_control = make_extra_ik_control
    except Exception as e:
        print(f"[AetherBlend] Error setting rigify make_extra_ik_control: {e}")

    bpy.ops.object.mode_set(mode='OBJECT')

def rigify_set_super_copy_widget_type(armature: bpy.types.Armature, bone_name: str, super_copy_widget_type: str) -> None:
    """sets rigify super_copy_widget_type parameter for a given bone."""

    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='POSE')
    
    pose_bone = armature.pose.bones.get(bone_name)

    bpy.ops.pose.select_all(action='DESELECT')
    _select_pose_bone(pose_bone)
    armature.data.bones.active = pose_bone.bone

    try:
        rigify_params = pose_bone.rigify_parameters

        rigify_params.super_copy_widget_type = super_copy_widget_type
    except Exception as e:
        print(f"[AetherBlend] Error setting rigify super_copy_widget_type: {e}")

    bpy.ops.object.mode_set(mode='OBJECT')

def rigify_set_pivot_pos(armature: bpy.types.Armature, bone_name: str, pivot_pos: int) -> None:
    """sets rigify pivot_pos parameter for a given bone."""

    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='POSE')
    
    pose_bone = armature.pose.bones.get(bone_name)

    bpy.ops.pose.select_all(action='DESELECT')
    _select_pose_bone(pose_bone)
    armature.data.bones.active = pose_bone.bone

    try:
        rigify_params = pose_bone.rigify_parameters

        rigify_params.pivot_pos = pivot_pos
    except Exception as e:
        print(f"[AetherBlend] Error setting rigify pivot_pos: {e}")

    bpy.ops.object.mode_set(mode='OBJECT')

def rigify_set_skin_anchor_properties(armature: bpy.types.Armature, bone_name: str, settings: RigifySettings) -> None:
    """Sets up rigify skin anchor properties for a pose bone"""

    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='POSE')

    pose_bone = armature.pose.bones.get(bone_name)

    bpy.ops.pose.select_all(action='DESELECT')
    _select_pose_bone(pose_bone)
    armature.data.bones.active = pose_bone.bone

    try:
        rigify_params = pose_bone.rigify_parameters

        if settings.pivot_master_widget_type is not None:
            rigify_params.pivot_master_widget_type = settings.pivot_master_widget_type

    except Exception as e:
        print(f"[AetherBlend] Error setting rigify skin anchor properties: {e}")

    bpy.ops.object.mode_set(mode='OBJECT')

def rigify_set_jaw_master_properties(armature: bpy.types.Armature, bone_name: str, settings: RigifySettings) -> None:
    """Sets up rigify jaw master properties for a pose bone"""

    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='POSE')

    pose_bone = armature.pose.bones.get(bone_name)

    bpy.ops.pose.select_all(action='DESELECT')
    _select_pose_bone(pose_bone)
    armature.data.bones.active = pose_bone.bone

    try:
        rigify_params = pose_bone.rigify_parameters

        if settings.jaw_mouth_influence is not None:
            rigify_params.jaw_mouth_influence = settings.jaw_mouth_influence

    except Exception as e:
        print(f"[AetherBlend] Error setting rigify jaw master properties: {e}")

    bpy.ops.object.mode_set(mode='OBJECT')

def rigify_set_skin_basic_chain_properties(armature: bpy.types.Armature, bone_name: str, settings: RigifySettings) -> None:
    """Sets up rigify skin basic chain properties for a pose bone"""

    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='POSE')

    pose_bone = armature.pose.bones.get(bone_name)

    bpy.ops.pose.select_all(action='DESELECT')
    _select_pose_bone(pose_bone)
    armature.data.bones.active = pose_bone.bone

    try:
        rigify_params = pose_bone.rigify_parameters

        if settings.skin_chain_priority is not None:
            rigify_params.skin_chain_priority = settings.skin_chain_priority

    except Exception as e:
        print(f"[AetherBlend] Error setting rigify skin basic chain properties: {e}")

    bpy.ops.object.mode_set(mode='OBJECT')

def rigify_set_skin_glue_properties(armature: bpy.types.Armature, bone_name: str, settings: RigifySettings) -> None:
    """Sets up the rigify skin glue properties for a pose bone"""

    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='POSE')

    pose_bone = armature.pose.bones.get(bone_name)

    bpy.ops.pose.select_all(action='DESELECT')
    _select_pose_bone(pose_bone)
    armature.data.bones.active = pose_bone.bone

    try:
        rigify_params = pose_bone.rigify_parameters

        if settings.relink_constraints is not None:
            rigify_params.relink_constraints = settings.relink_constraints
        if settings.skin_glue_use_tail is not None:
            rigify_params.skin_glue_use_tail = settings.skin_glue_use_tail
        if settings.skin_glue_tail_reparent is not None:
            rigify_params.skin_glue_tail_reparent = settings.skin_glue_tail_reparent
        if settings.skin_glue_add_constraint is not None:
            rigify_params.skin_glue_add_constraint = settings.skin_glue_add_constraint
        if settings.skin_glue_add_constraint_influence is not None:
            rigify_params.skin_glue_add_constraint_influence = settings.skin_glue_add_constraint_influence

    except Exception as e:
        print(f"[AetherBlend] Error settings rigify skin glue properties: {e}")

    bpy.ops.object.mode_set(mode='OBJECT')



def rigify_set_skin_stretchy_chain_properties(armature: bpy.types.Armature, bone_name: str, settings: RigifySettings) -> None:
    """Sets up rigify skin stretchy chain properties for a pose bone"""

    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='POSE')

    pose_bone = armature.pose.bones.get(bone_name)

    bpy.ops.pose.select_all(action='DESELECT')
    _select_pose_bone(pose_bone)
    armature.data.bones.active = pose_bone.bone

    try:
        rigify_params = pose_bone.rigify_parameters


        if settings.skin_chain_pivot_pos is not None:
            rigify_params.skin_chain_pivot_pos = settings.skin_chain_pivot_pos
        if settings.skin_control_orientation_bone is not None:
            rigify_params.skin_control_orientation_bone = settings.skin_control_orientation_bone
        if settings.skin_chain_falloff is not None:
            rigify_params.skin_chain_falloff = settings.skin_chain_falloff
        if settings.skin_chain_falloff_length is not None:
            rigify_params.skin_chain_falloff_length = settings.skin_chain_falloff_length
        if settings.skin_chain_falloff_spherical is not None:
            rigify_params.skin_chain_falloff_spherical = settings.skin_chain_falloff_spherical
        if settings.skin_chain_priority is not None:
            rigify_params.skin_chain_priority = settings.skin_chain_priority

        if settings.primary_layer_extra is not None:
            rigify_params.skin_primary_layers_extra = True
            rigify_params.skin_primary_coll_refs.clear()
            if settings.primary_layer_extra in armature.data.collections:
                bpy.ops.pose.rigify_collection_ref_add(prop_name="skin_primary_coll_refs")

                if len(rigify_params.skin_primary_coll_refs) > 0:
                    skin_ref = rigify_params.skin_primary_coll_refs[-1]
                    skin_ref.name = settings.primary_layer_extra
                else:
                    print(f"[AetherBlend] Collection '{settings.primary_layer_extra}' not found in armature '{armature.name}'")

        if settings.secondary_layer_extra is not None:
            rigify_params.skin_secondary_layers_extra = True
            rigify_params.skin_secondary_coll_refs.clear()
            if settings.secondary_layer_extra in armature.data.collections:
                bpy.ops.pose.rigify_collection_ref_add(prop_name="skin_secondary_coll_refs")

                if len(rigify_params.skin_secondary_coll_refs) > 0:
                    skin_ref = rigify_params.skin_secondary_coll_refs[-1]
                    skin_ref.name = settings.secondary_layer_extra
                else:
                    print(f"[AetherBlend] Collection '{settings.secondary_layer_extra}' not found in armature '{armature.name}'")

    except Exception as e:
        print(f"[AetherBlend] Error setting rigify skin stretchy chain properties: {e}")

    bpy.ops.object.mode_set(mode='OBJECT')
    
def set_rigify_properties(armature: bpy.types.Armature,settings: RigifySettings, bone_name: str = None) -> None:
    """Sets up rigify properties for a pose bone"""
    original_mode = armature.mode
    bpy.ops.object.mode_set(mode='POSE')
    if bone_name is None:
        if settings.bone_name is not None:
            bone_name = settings.bone_name
        
    pose_bone = armature.pose.bones.get(bone_name)

    if settings is None or pose_bone is None:
        return
    
    if settings.rigify_type:
        pose_bone.rigify_type = settings.rigify_type

    if settings.fk_coll:
        rigify_set_fk_collection(armature, pose_bone.name, settings.fk_coll)

    if settings.tweak_coll:
        rigify_set_tweak_collection(armature, pose_bone.name, settings.tweak_coll)

    if settings.copy_rot_axes:
        rigify_set_copy_rotation_axes(
            armature,
            pose_bone.name,
            use_x=settings.copy_rot_axes.get('use_x'),
            use_y=settings.copy_rot_axes.get('use_y'),
            use_z=settings.copy_rot_axes.get('use_z')
        )

    if settings.make_extra_ik_control:
        rigify_make_extra_ik_control(
            armature,
            pose_bone.name,
            make_extra_ik_control=settings.make_extra_ik_control
        )

    if settings.super_copy_widget_type:
        rigify_set_super_copy_widget_type(
            armature,
            pose_bone.name,
            super_copy_widget_type=settings.super_copy_widget_type
        )

    if settings.pivot_pos:
        rigify_set_pivot_pos(
            armature,
            pose_bone.name,
            pivot_pos=settings.pivot_pos
        )

    if settings.rigify_type == "skin.stretchy_chain":
        rigify_set_skin_stretchy_chain_properties(
            armature,
            pose_bone.name,
            settings=settings
        )

    if settings.rigify_type == "skin.basic_chain":
        rigify_set_skin_basic_chain_properties(
            armature,
            pose_bone.name,
            settings=settings
        )

    if settings.rigify_type == "skin.glue":
        rigify_set_skin_glue_properties(
            armature,
            pose_bone.name,
            settings=settings
        )
    
    if settings.rigify_type == "face.skin_jaw":
        rigify_set_jaw_master_properties(
            armature,
            pose_bone.name,
            settings=settings
        )

    if settings.rigify_type == "skin.anchor":
        rigify_set_skin_anchor_properties(
            armature,
            pose_bone.name,
            settings=settings
        )


    bpy.ops.object.mode_set(mode=original_mode)