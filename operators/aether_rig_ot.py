import bpy
from .. import utils
from ..data import *
from ..data.bone_mappings.humanoid import EYES_GEN_INFO
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


class GenerativeMetaBoneGroup():
    src_armature: bpy.types.Armature
    target_armature: bpy.types.Armature
    generative_bones: list[GenerativeBone]

    def __init__(self, src_armature: bpy.types.Armature, target_armature: bpy.types.Armature, generative_bones: list[GenerativeBone]):
        self.src_armature = src_armature
        self.target_armature = target_armature
        self.generative_bones = generative_bones

    def check(self) -> bool:
        """Check if all required bones exist in the source armature."""
        future_bones = []
        for gen_bone in self.generative_bones:
            armature_to_check = self.src_armature if gen_bone.ref == "src" else self.target_armature
            future_bones.append(gen_bone.data.name)
            if gen_bone.req_bones:
                for req_bone in gen_bone.req_bones:
                    if req_bone not in future_bones:
                        if req_bone not in armature_to_check.data.bones:
                            if gen_bone.is_optional:
                                print(f"[AetherBlend] Optional bone '{req_bone}' not found in armature '{armature_to_check.name}', Skipping this bone.")
                                future_bones.remove(gen_bone.data.name)
                                continue
                            print(f"[AetherBlend] Required bone '{req_bone}' not found in armature '{armature_to_check.name}', Skipping MetaBoneGroup generation.")
                            return False
                        
        return True
    
    def generateBones(self) -> list[str]:
        """Generate the bones in the target armature based on the generative bones list."""
        generated_bones = []
        for gen_bone in self.generative_bones:
            ref = self.target_armature if gen_bone.ref == "tgt" else self.src_armature
            tgt = self.target_armature
            new_bone = gen_bone.generate(ref, tgt)
            if new_bone:
                generated_bones.append(new_bone)

        return generated_bones

    def setRigifySettings(self) -> None:
        """Set rigify settings for the generated bones in the target armature."""
        for gen_bone in self.generative_bones:
            if gen_bone.settings:
                utils.armature.rigify.set_rigify_properties(
                    armature=self.target_armature,
                    settings=gen_bone.settings
                )

    def execute(self) -> list[str]:
        """Execute the full generation process for this bone group."""
        verified = self.check()
        if not verified:
            return []
        
        generated_bones = self.generateBones()
        self.setRigifySettings()
        return generated_bones

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

        for collection in META_RIG_COLLECTIONS_INFO:
            coll = meta_rig.data.collections.new(collection.name)
            if coll:
                coll.rigify_color_set_name = collection.color_type
                coll.rigify_ui_row = collection.row_index
                coll.rigify_ui_title = collection.title

        for bone_group in HUMAN:
            gen_group = GenerativeMetaBoneGroup(src_armature=armature, target_armature=meta_rig, generative_bones=bone_group)
            bones = gen_group.execute()
            print(bones)

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
        for (collection_name, segment_name), gen_info in EYES_GEN_INFO.items():
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
                    utils.armature.rigify.set_rigify_properties(armature=meta_rig, bone_name=bone_name, settings=rigify_settings)
                created_bones.extend(bones)

            all_created_bones.extend(created_bones)

        bpy.ops.object.mode_set(mode=original_mode)

        return all_created_bones

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


        constraints_track_to_after = utils.armature.bone.add_constraint_track_to_after_original(ffxiv_armature, CONSTRAINTS_TRACK_TO_AFTER_ORIGINAL)
        constraints_copy_rot = utils.armature.bone.add_constraint_copy_rotation(ffxiv_armature, CONSTRAINTS_COPY_ROT, overwrite=False)
        constraints_copy_loc = utils.armature.bone.add_constraint_copy_location(ffxiv_armature, CONSTRAINTS_COPY_LOC, overwrite=False)
        constraints_child_of = utils.armature.bone.add_constraint_child_of(ffxiv_armature, CONSTRAINTS_CHILD_OF, overwrite=False)

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