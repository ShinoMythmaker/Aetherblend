import bpy
from ... import utils
from ...data import constants
## This code is highly experiemental and subject to change as we refine the meta rig generation process ##

def cleanup_linked_rigify_bones(ffxiv_armature: bpy.types.Armature, rigify_rig: bpy.types.Armature) -> None:
    """Remove old control rig bones and data from FFXIV armature before linking new ones."""
    original_mode = bpy.context.object.mode
    bpy.ops.object.mode_set(mode='POSE')

    for rigify_coll in rigify_rig.data.collections:
        bpy.ops.object.mode_set(mode='POSE')
        if ffxiv_armature.data.collections.get(rigify_coll.name):
            utils.armature.b_collection.delete_with_bones(ffxiv_armature, collection_name=rigify_coll.name)

    bpy.ops.object.mode_set(mode='POSE')
    pose_bones = ffxiv_armature.pose.bones

    for bone in pose_bones:
        utils.armature.bone.remove_constraint_by_name_contains(armature=ffxiv_armature, bone_name=bone.name, substring='AetherBlend')
    
    bpy.ops.object.mode_set(mode=original_mode)

class AETHER_OT_Generate_Meta_Rig(bpy.types.Operator):
    bl_idname = "aether.generate_meta_rig"
    bl_label = "Generate Meta Rig"
    bl_description = ("Generate a meta rig based on available bones")
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "Select an armature object")
            return {'CANCELLED'}

        armature.hide_set(False)

        existing_meta_rig = armature.aether_rig.meta_rig
        
        if existing_meta_rig:
            existing_meta_rig.hide_set(False)
            bpy.data.objects.remove(existing_meta_rig, do_unlink=True)


        meta_rig = utils.armature.create(location=armature.location, armature_name=f"META_{armature.name}")

        bpy.context.view_layer.objects.active = meta_rig

        meta_rig.show_in_front = True 

        bpy.ops.armature.rigify_use_standard_colors()

        bpy.ops.armature.rigify_add_color_sets()

        for collection in constants.META_RIG_COLLECTIONS_INFO:
            coll = meta_rig.data.collections.new(collection.name)
            if coll:
                coll.rigify_color_set_name = collection.color_type
                coll.rigify_ui_row = collection.row_index
                coll.rigify_ui_title = collection.title

        self.generate_torso(source_armature=armature, meta_rig=meta_rig)
        self.generate_arms(source_armature=armature, meta_rig=meta_rig)
        self.generate_tail(source_armature=armature, meta_rig=meta_rig)
        self.generate_legs(source_armature=armature, meta_rig=meta_rig)
        self.generate_fingers(source_armature=armature, meta_rig=meta_rig)
        self.generate_eyes(source_armature=armature, meta_rig=meta_rig)

                
        armature.aether_rig.meta_rig = meta_rig
        
        bpy.ops.object.mode_set(mode='OBJECT')
        meta_rig.parent = armature
        meta_rig.hide_set(True)

        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = armature
        armature.select_set(True)
        
        return {'FINISHED'}

    
    def generate_eyes(self, source_armature: bpy.types.Armature, meta_rig: bpy.types.Armature) -> list[str]:
        """Generate the individual eye bones"""

        original_mode = bpy.context.object.mode
        bpy.ops.object.mode_set(mode='POSE')
        all_created_bones = []
        for (collection_name, segment_name), gen_info in constants.EYES_GEN_INFO.items():
            created_bones = []
            for skin_bone in gen_info.outer_bones:
                bones = utils.armature.generate.skin_bone(
                    src=source_armature,
                    target=meta_rig,
                    skin_bone_info=skin_bone
                )
                created_bones.extend(bones)

            eye_bone = utils.armature.generate.eye_bone(
                armature=meta_rig,
                outer_bones=created_bones,
                name=gen_info.eye_name,
                length=float(0.010)
            )
            if eye_bone and meta_rig.data.collections.get(gen_info.eye_collection):
                utils.armature.b_collection.assign_bones(meta_rig, eye_bone, gen_info.eye_collection)
                if eye_bone and gen_info.parent_bone: 
                    utils.armature.bone.set_parent(
                        armature=meta_rig,
                        bone_name=gen_info.eye_name,
                        parent_bone_name=gen_info.parent_bone
                    )

            for bone in created_bones:
                utils.armature.bone.set_parent(
                    armature=meta_rig,
                    bone_name=bone,
                    parent_bone_name=gen_info.eye_name
                )

            for bridge in gen_info.bridges:
                bones = utils.armature.generate.bridge_bones(
                    armature=meta_rig,
                    bridge_info=bridge
                )
                created_bones.extend(bones)

            if created_bones and meta_rig.data.collections.get(collection_name):
                utils.armature.b_collection.assign_bones(meta_rig, created_bones, collection_name)
                for bone_name, rigify_settings in gen_info.bone_settings.items():
                    self.set_rigify_properties(armature=meta_rig, bone_name=bone_name, settings=rigify_settings)
                created_bones.extend(bones)

            all_created_bones.extend(created_bones)

        bpy.ops.object.mode_set(mode=original_mode)

        return all_created_bones

    def generate_torso(self, source_armature: bpy.types.Armature, meta_rig: bpy.types.Armature) -> list[str]:
        """Generate the individual torso bones"""

        original_mode = bpy.context.object.mode
        bpy.ops.object.mode_set(mode='POSE')
        created_limbs = []
        for (torso_coll, chain_name), chain_info in constants.SPINE_INFO.items():
            bones = utils.armature.generate.bone_chain(
                src=source_armature,
                target=meta_rig,
                chain_info=chain_info
            )
            extension_bones = utils.armature.generate.bone_extensions(
                target=meta_rig,
                extension_info=chain_info.bone_extensions
            )
            if extension_bones:
                bones.extend(extension_bones)
            
            if bones and meta_rig.data.collections.get(torso_coll):
                utils.armature.b_collection.assign_bones(meta_rig, bones, torso_coll)
                for bone_name, rigify_settings in chain_info.gen_bones.items():
                    self.set_rigify_properties(armature=meta_rig, bone_name=bone_name, settings=rigify_settings)
                created_limbs.extend(bones)

        bpy.ops.object.mode_set(mode=original_mode)

        return created_limbs

    def generate_arms(self, source_armature: bpy.types.Armature, meta_rig: bpy.types.Armature) -> list[str]:
        """Generate the individual limbs"""

        original_mode = bpy.context.object.mode
        bpy.ops.object.mode_set(mode='POSE')
        created_limbs = []
        for limb_coll, chain_info in constants.ARMS_INFO.items():
            bones = utils.armature.generate.bone_chain(
                src=source_armature,
                target=meta_rig,
                chain_info=chain_info
            )
            if bones and meta_rig.data.collections.get(limb_coll):
                utils.armature.b_collection.assign_bones(meta_rig, bones, limb_coll)
                for bone_name, rigify_settings in chain_info.gen_bones.items():
                    self.set_rigify_properties(armature=meta_rig, bone_name=bone_name, settings=rigify_settings)
                created_limbs.extend(bones)

        bpy.ops.object.mode_set(mode=original_mode)

        return created_limbs
    
    def generate_tail(self, source_armature: bpy.types.Armature, meta_rig: bpy.types.Armature) -> list[str]:
        """Generate the individual tail bones"""

        original_mode = bpy.context.object.mode
        bpy.ops.object.mode_set(mode='POSE')
        created_limbs = []
        for tail_coll, chain_info in constants.TAILS_INFO.items():
            bones = utils.armature.generate.bone_chain(
                src=source_armature,
                target=meta_rig,
                chain_info=chain_info
            )
            if bones and meta_rig.data.collections.get(tail_coll):
                utils.armature.b_collection.assign_bones(meta_rig, bones, tail_coll)
                for bone_name, rigify_settings in chain_info.gen_bones.items():
                    self.set_rigify_properties(armature=meta_rig, bone_name=bone_name, settings=rigify_settings)
                created_limbs.extend(bones)

        bpy.ops.object.mode_set(mode=original_mode)

        return created_limbs
    
    def generate_legs(self, source_armature: bpy.types.Armature, meta_rig: bpy.types.Armature) -> list[str]:
        """Generate the individual leg bones"""

        original_mode = bpy.context.object.mode
        bpy.ops.object.mode_set(mode='POSE')
        created_limbs = []
        for leg_coll, chain_info in constants.LEGS_INFO.items():
            bones = utils.armature.generate.bone_chain(
                src=source_armature,
                target=meta_rig,
                chain_info=chain_info
            )
            extension_bones = utils.armature.generate.bone_extensions(
                target=meta_rig,
                extension_info=chain_info.bone_extensions
            )
            if extension_bones:
                bones.extend(extension_bones)
            
            if bones and meta_rig.data.collections.get(leg_coll):
                utils.armature.b_collection.assign_bones(meta_rig, bones, leg_coll)
                for bone_name, rigify_settings in chain_info.gen_bones.items():
                    self.set_rigify_properties(armature=meta_rig, bone_name=bone_name, settings=rigify_settings)
                created_limbs.extend(bones)

        bpy.ops.object.mode_set(mode=original_mode)

        return created_limbs

    def generate_fingers(self, source_armature: bpy.types.Armature, meta_rig: bpy.types.Armature) -> list[str]:
        """Generate the individual limbs"""

        original_mode = bpy.context.object.mode
        bpy.ops.object.mode_set(mode='POSE')
        created_limbs = []
        for (fingers_coll, finger_name), chain_info in constants.FINGERS_INFO.items():
            bones = utils.armature.generate.bone_chain(
                src=source_armature,
                target=meta_rig,
                chain_info=chain_info
            )
            if bones and meta_rig.data.collections.get(fingers_coll):
                utils.armature.b_collection.assign_bones(meta_rig, bones, fingers_coll)
                for bone_name, rigify_settings in chain_info.gen_bones.items():
                    self.set_rigify_properties(armature=meta_rig, bone_name=bone_name, settings=rigify_settings)
                created_limbs.extend(bones)

        bpy.ops.object.mode_set(mode=original_mode)

        return created_limbs

    def rigify_set_tweak_collection(self, armature: bpy.types.Armature, bone_name: str, collection_name: str) -> None:
        """Sets the rigify tweak collection for a given bone."""
        
        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='POSE')
        
        pose_bone = armature.pose.bones.get(bone_name)
        
        bpy.ops.pose.select_all(action='DESELECT')
        pose_bone.bone.select = True
        armature.data.bones.active = pose_bone.bone
        
        try:
            rigify_params = pose_bone.rigify_parameters
            
            rigify_params.tweak_coll_refs.clear()
            
            if collection_name in armature.data.collections:
                bpy.ops.pose.rigify_collection_ref_add(prop_name="tweak_coll_refs")
                
                if len(rigify_params.tweak_coll_refs) > 0:
                    tweak_ref = rigify_params.tweak_coll_refs[-1]
                    tweak_ref.name = collection_name
                    print(f"[AetherBlend] Set tweak collection reference to '{collection_name}' for bone '{bone_name}'")
            else:
                print(f"[AetherBlend] Collection '{collection_name}' not found in armature '{armature.name}'")
                
        except Exception as e:
            print(f"[AetherBlend] Error setting rigify tweak collection: {e}")
        
        bpy.ops.object.mode_set(mode='OBJECT')

    def rigify_set_fk_collection(self, armature: bpy.types.Armature, bone_name: str, collection_name: str) -> None:
        """Sets the rigify FK collection for a given bone."""
        
        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='POSE')
        
        pose_bone = armature.pose.bones.get(bone_name)
        
        bpy.ops.pose.select_all(action='DESELECT')
        pose_bone.bone.select = True
        armature.data.bones.active = pose_bone.bone
        
        try:
            rigify_params = pose_bone.rigify_parameters
            
            rigify_params.tweak_coll_refs.clear()
            
            if collection_name in armature.data.collections:
                bpy.ops.pose.rigify_collection_ref_add(prop_name="fk_coll_refs")

                if len(rigify_params.fk_coll_refs) > 0:
                    fk_ref = rigify_params.fk_coll_refs[-1]
                    fk_ref.name = collection_name
                    print(f"[AetherBlend] Set FK collection reference to '{collection_name}' for bone '{bone_name}'")
            else:
                print(f"[AetherBlend] Collection '{collection_name}' not found in armature '{armature.name}'")
                
        except Exception as e:
            print(f"[AetherBlend] Error setting rigify FK collection: {e}")
        
        bpy.ops.object.mode_set(mode='OBJECT')

    def rigify_set_copy_rotation_axes(self, armature: bpy.types.Armature, bone_name: str, use_x: bool, use_y: bool, use_z: bool) -> None:
        """sets rigify copy rotation axes parameter for a given bone."""

        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='POSE')
        
        pose_bone = armature.pose.bones.get(bone_name)
        
        bpy.ops.pose.select_all(action='DESELECT')
        pose_bone.bone.select = True
        armature.data.bones.active = pose_bone.bone
        
        try:
            rigify_params = pose_bone.rigify_parameters
            
            rigify_params.copy_rotation_axes[0] = use_x
            rigify_params.copy_rotation_axes[1] = use_y
            rigify_params.copy_rotation_axes[2] = use_z
        except Exception as e:
            print(f"[AetherBlend] Error setting rigify copy rotation axes: {e}")
        
        bpy.ops.object.mode_set(mode='OBJECT')

    def rigify_make_extra_ik_control(self, armature: bpy.types.Armature, bone_name: str, make_extra_ik_control: bool) -> None:
        """sets rigify make_extra_ik_control parameter for a given bone."""

        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='POSE')
        
        pose_bone = armature.pose.bones.get(bone_name)

        bpy.ops.pose.select_all(action='DESELECT')
        pose_bone.bone.select = True
        armature.data.bones.active = pose_bone.bone

        try:
            rigify_params = pose_bone.rigify_parameters

            rigify_params.make_extra_ik_control = make_extra_ik_control
        except Exception as e:
            print(f"[AetherBlend] Error setting rigify make_extra_ik_control: {e}")

        bpy.ops.object.mode_set(mode='OBJECT')

    def rigify_set_super_copy_widget_type(self, armature: bpy.types.Armature, bone_name: str, super_copy_widget_type: str) -> None:
        """sets rigify super_copy_widget_type parameter for a given bone."""

        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='POSE')
        
        pose_bone = armature.pose.bones.get(bone_name)

        bpy.ops.pose.select_all(action='DESELECT')
        pose_bone.bone.select = True
        armature.data.bones.active = pose_bone.bone

        try:
            rigify_params = pose_bone.rigify_parameters

            rigify_params.super_copy_widget_type = super_copy_widget_type
        except Exception as e:
            print(f"[AetherBlend] Error setting rigify super_copy_widget_type: {e}")

        bpy.ops.object.mode_set(mode='OBJECT')

    def rigify_set_pivot_pos(self, armature: bpy.types.Armature, bone_name: str, pivot_pos: int) -> None:
        """sets rigify pivot_pos parameter for a given bone."""

        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='POSE')
        
        pose_bone = armature.pose.bones.get(bone_name)

        bpy.ops.pose.select_all(action='DESELECT')
        pose_bone.bone.select = True
        armature.data.bones.active = pose_bone.bone

        try:
            rigify_params = pose_bone.rigify_parameters

            rigify_params.pivot_pos = pivot_pos
        except Exception as e:
            print(f"[AetherBlend] Error setting rigify pivot_pos: {e}")

        bpy.ops.object.mode_set(mode='OBJECT')

    def rigify_set_skin_stretchy_chain_properties(self, armature: bpy.types.Armature, bone_name: str, settings: constants.RigifySettings) -> None:
        """Sets up rigify skin stretchy chain properties for a pose bone"""

        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='POSE')

        pose_bone = armature.pose.bones.get(bone_name)

        bpy.ops.pose.select_all(action='DESELECT')
        pose_bone.bone.select = True
        armature.data.bones.active = pose_bone.bone

        try:
            rigify_params = pose_bone.rigify_parameters


            if settings.skin_chain_pivot_pos is not None:
                rigify_params.skin_chain_pivot_pos = settings.skin_chain_pivot_pos
            if settings.skin_control_orientation_bone is not None:
                rigify_params.skin_control_orientation_bone = settings.skin_control_orientation_bone
            if settings.skin_chain_falloff_spherical is not None:
                rigify_params.skin_chain_falloff_spherical = settings.skin_chain_falloff_spherical

            if settings.secondary_layer_extra is not None:
                rigify_params.skin_secondary_layers_extra = True
                rigify_params.skin_secondary_coll_refs.clear()
                if settings.secondary_layer_extra in armature.data.collections:
                    bpy.ops.pose.rigify_collection_ref_add(prop_name="skin_secondary_coll_refs")

                    if len(rigify_params.skin_secondary_coll_refs) > 0:
                        skin_ref = rigify_params.skin_secondary_coll_refs[-1]
                        skin_ref.name = settings.secondary_layer_extra
                        print(f"[AetherBlend] Set Skin Secondary collection reference to '{settings.secondary_layer_extra}' for bone '{bone_name}'")
                    else:
                        print(f"[AetherBlend] Collection '{settings.secondary_layer_extra}' not found in armature '{armature.name}'")

        except Exception as e:
            print(f"[AetherBlend] Error setting rigify skin stretchy chain properties: {e}")

        bpy.ops.object.mode_set(mode='OBJECT')

    def set_rigify_properties(self, armature: bpy.types.Armature, bone_name: str, settings: constants.RigifySettings) -> None:
        """Sets up rigify properties for a pose bone"""
        original_mode = armature.mode
        pose_bone = armature.pose.bones.get(bone_name)

        if settings is None:
            return
        
        if settings.rigify_type:
            pose_bone.rigify_type = settings.rigify_type

        if settings.fk_coll:
            self.rigify_set_fk_collection(armature, pose_bone.name, settings.fk_coll)

        if settings.tweak_coll:
            self.rigify_set_tweak_collection(armature, pose_bone.name, settings.tweak_coll)

        if settings.copy_rot_axes:
            self.rigify_set_copy_rotation_axes(
                armature,
                pose_bone.name,
                use_x=settings.copy_rot_axes.get('use_x'),
                use_y=settings.copy_rot_axes.get('use_y'),
                use_z=settings.copy_rot_axes.get('use_z')
            )

        if settings.make_extra_ik_control:
            self.rigify_make_extra_ik_control(
                armature,
                pose_bone.name,
                make_extra_ik_control=settings.make_extra_ik_control
            )

        if settings.super_copy_widget_type:
            self.rigify_set_super_copy_widget_type(
                armature,
                pose_bone.name,
                super_copy_widget_type=settings.super_copy_widget_type
            )

        if settings.pivot_pos:
            self.rigify_set_pivot_pos(
                armature,
                pose_bone.name,
                pivot_pos=settings.pivot_pos
            )

        if settings.rigify_type == "skin.stretchy_chain":
            self.rigify_set_skin_stretchy_chain_properties(
                armature,
                pose_bone.name,
                settings=settings
            )

        bpy.ops.object.mode_set(mode=original_mode)

class AETHER_OT_Generate_Rigify_Rig(bpy.types.Operator):
    bl_idname = "aether.generate_rigify_rig"
    bl_label = "Generate Rigify Rig"
    bl_description = ("Generate the rigify control rig from the meta rig")
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "Select an armature object")
            return {'CANCELLED'}

        if not armature.aether_rig.meta_rig:
            self.report({'ERROR'}, "No meta rig found. Generate a meta rig first.")
            return {'CANCELLED'}

        meta_rig = armature.aether_rig.meta_rig
        meta_rig.hide_set(False)
        bpy.context.view_layer.objects.active = meta_rig
        bpy.ops.object.select_all(action='DESELECT')
        meta_rig.select_set(True)
    

        bpy.ops.object.mode_set(mode='POSE')

        result = bpy.ops.pose.rigify_generate()
        
        if result == {'FINISHED'}:
            rigify_rig = getattr(meta_rig.data, 'rigify_target_rig', None)
            
            if rigify_rig:
                armature.aether_rig.rigify_rig = rigify_rig
                rigify_rig.parent = armature

                bpy.ops.object.select_all(action='DESELECT')
                rigify_rig.hide_set(True)

                bpy.context.view_layer.objects.active = armature
                armature.select_set(True)
                
                meta_rig.hide_set(True)
                return {'FINISHED'}
            else:
                meta_rig.hide_set(True)
                self.report({'ERROR'}, "Failed to get reference to generated Rigify Rig")
                return {'CANCELLED'}
        else:
            meta_rig.hide_set(True)
            self.report({'ERROR'}, "Rigify generation failed")
            return {'CANCELLED'}
            
class AETHER_OT_Link_Rigify_Rig(bpy.types.Operator):
    bl_idname = "aether.link_rigify_rig"
    bl_label = "Link Rigify Rig"
    bl_description = ("Link the Rigify Rig to the FFXIV Rig by merging control bones and setting up constraints")
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "Select an armature object")
            return {'CANCELLED'}

        if not armature.aether_rig.rigify_rig:
            self.report({'ERROR'}, "No Rigify Rig found. Generate a Rigify Rig first.")
            return {'CANCELLED'}

        rigify_rig = armature.aether_rig.rigify_rig
        rigify_rig.hide_set(False)

        if armature.aether_rig.rigify_linked:
            cleanup_linked_rigify_bones(armature, rigify_rig)

        self.merge_control_rig_bones(armature, rigify_rig)

        armature.aether_rig.rigify_linked = True

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        rigify_rig.hide_set(True)
        bpy.context.view_layer.objects.active = armature

        bpy.ops.object.mode_set(mode='POSE')
        ffxiv_collection = armature.data.collections.get("FFXIV")
        ffxiv_ref_collection = armature.data.collections.get("FFXIV-REF")

        if ffxiv_collection:
            ffxiv_collection.is_visible = False

        if ffxiv_ref_collection:
            ffxiv_ref_collection.is_visible = False

        armature.select_set(True)

        return {'FINISHED'}
            
    def merge_control_rig_bones(self, ffxiv_armature: bpy.types.Armature, rigify_rig: bpy.types.Armature) -> bool:
        """Duplicate the control rig and merge it with the FFXIV armature."""
        original_mode = bpy.context.object.mode
        bpy.ops.object.mode_set(mode='OBJECT')

        bpy.ops.object.select_all(action='DESELECT')
        rigify_rig.select_set(True)
        bpy.context.view_layer.objects.active = rigify_rig
        bpy.ops.object.duplicate()
        
        dupplicated_rigify_rig = bpy.context.active_object
        dupplicated_rigify_rig.name = f"{rigify_rig.name}_temp_duplicate"
        
        bpy.ops.object.select_all(action='DESELECT')
        ffxiv_armature.select_set(True)
        dupplicated_rigify_rig.select_set(True)
        bpy.context.view_layer.objects.active = ffxiv_armature 
        
        bpy.ops.object.join()

        bpy.ops.object.mode_set(mode='EDIT')
        self.set_org_bone_parents(bpy.context.active_object)
        
        bpy.ops.object.mode_set(mode='OBJECT')
        
        self.copy_rigify_properties(ffxiv_armature, rigify_rig)


        constraints_track_to_after = utils.armature.bone.add_constraint_track_to_after_original(ffxiv_armature, constants.CONSTRAINTS_TRACK_TO_AFTER_ORIGINAL)
        constraints_copy_rot = utils.armature.bone.add_constraint_copy_rotation(ffxiv_armature, constants.CONSTRAINTS_COPY_ROT, overwrite=False)
        constraints_copy_loc = utils.armature.bone.add_constraint_copy_location(ffxiv_armature, constants.CONSTRAINTS_COPY_LOC, overwrite=False)
        constraints_child_of = utils.armature.bone.add_constraint_child_of(ffxiv_armature, constants.CONSTRAINTS_CHILD_OF, overwrite=False)

        bpy.ops.object.mode_set(mode=original_mode)
        return True
    
    def set_org_bone_parents(self, armature: bpy.types.Armature) -> bool:
        original_mode = bpy.context.object.mode
        bpy.ops.object.mode_set(mode='EDIT')

        edit_bones = armature.data.edit_bones
        for edit_bone in edit_bones:
            if edit_bone.name.startswith("ORG-"):
                ref_bone_name = edit_bone.name[4:]
                ref_bone = edit_bones.get(ref_bone_name)
                if ref_bone and ref_bone.collections.get("FFXIV"):
                    edit_bone.parent = ref_bone
                    edit_bone.use_connect = False

        bpy.ops.object.mode_set(mode=original_mode)
        return True

    def copy_rigify_properties(self, ffxiv_armature: bpy.types.Armature, rigify_rig: bpy.types.Armature) -> bool:
        """Copy essential rigify properties like rig_id that are needed for the UI."""

        if "rig_id" in rigify_rig.data:
            ffxiv_armature.data["rig_id"] = rigify_rig.data["rig_id"]
        
        rigify_properties = ["rigify_colors", "rigify_selection_colors"]
        for prop_name in rigify_properties:
            if prop_name in rigify_rig.data:
                ffxiv_armature.data[prop_name] = rigify_rig.data[prop_name]
                print(f"[AetherBlend] Copied rigify property from armature data: {prop_name}")
        
        return True

class AETHER_OT_Unlink_Rigify_Rig(bpy.types.Operator):
    bl_idname = "aether.unlink_rigify_rig"
    bl_label = "Unlink Rigify Rig"
    bl_description = ("Unlink the Rigify Rig from the FFXIV Rig by removing control bones and constraints")
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "Select an armature object")
            return {'CANCELLED'}
        
        rigify_rig = armature.aether_rig.rigify_rig
        if rigify_rig:
            rigify_rig.hide_set(False)
            cleanup_linked_rigify_bones(armature, rigify_rig)
            armature.aether_rig.rigify_linked = False
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "No Rigify Rig found to unlink.")
            return {'CANCELLED'}
    
def register():
    bpy.utils.register_class(AETHER_OT_Generate_Meta_Rig)
    bpy.utils.register_class(AETHER_OT_Generate_Rigify_Rig)
    bpy.utils.register_class(AETHER_OT_Link_Rigify_Rig)
    bpy.utils.register_class(AETHER_OT_Unlink_Rigify_Rig)

def unregister():
    bpy.utils.unregister_class(AETHER_OT_Generate_Meta_Rig)
    bpy.utils.unregister_class(AETHER_OT_Generate_Rigify_Rig)
    bpy.utils.unregister_class(AETHER_OT_Link_Rigify_Rig)
    bpy.utils.unregister_class(AETHER_OT_Unlink_Rigify_Rig)