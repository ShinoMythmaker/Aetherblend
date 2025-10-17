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

        self.generate_limbs(source_armature=armature, meta_rig=meta_rig)
                
        armature.aether_rig.meta_rig = meta_rig
        
        bpy.ops.object.mode_set(mode='OBJECT')
        meta_rig.parent = armature
        meta_rig.hide_set(True)

        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = armature
        armature.select_set(True)
        
        return {'FINISHED'}

    def generate_limbs(self, source_armature: bpy.types.Armature, meta_rig: bpy.types.Armature) -> list[str]:
        """Generate the individual limbs"""

        original_mode = bpy.context.object.mode
        bpy.ops.object.mode_set(mode='POSE')
        created_limbs = []
        for limb_coll, limb_info in constants.LIMBS_INFO.items():
            bones = utils.armature.generate.bone_chain(
                src=source_armature,
                target=meta_rig,
                chain_info=limb_info
            )
            if bones and meta_rig.data.collections.get(limb_coll):
                utils.armature.b_collection.assign_bones(meta_rig, bones, limb_coll)
                for bone_name, rigify_settings in limb_info.gen_bones.items():
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
        
        self.copy_rigify_properties(ffxiv_armature, rigify_rig)
        
        constraints = utils.armature.bone.add_constraint_copy_rotation(ffxiv_armature, constants.CONSTRAINT_BONE_MAP, overwrite=True)
        for con in constraints:
            con.name = f"AetherBlend_CopyRot_{con.name}"

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