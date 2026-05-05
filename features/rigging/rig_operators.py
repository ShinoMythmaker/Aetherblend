import bpy
import time

from ... import utils
from . import template_manager
from ...preferences import get_preferences
from ...properties.tab_prop import set_active_tab

class _ArmatureSelectionHelpers:
    def _resolve_source_armature(self, armature: bpy.types.Object | None) -> bpy.types.Object | None:
        if not armature or armature.type != 'ARMATURE':
            return armature

        parent = armature.parent
        if not parent or parent.type != 'ARMATURE':
            return armature

        parent_rig = getattr(parent, 'aether_rig', None)
        if not parent_rig:
            return armature

        if getattr(parent_rig, 'meta_rig', None) != armature:
            return armature

        utils.object.set_visibility(parent, visible=True)
        utils.object.select_only(parent)
        return parent

    def _get_active_armature(self, context) -> bpy.types.Object | None:
        armature = self._resolve_source_armature(context.active_object)
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "Select an armature object")
            return None

        return armature

class AETHER_OT_Generate_Full_Rig(_ArmatureSelectionHelpers, bpy.types.Operator):
    bl_idname = "aether.generate_full_rig"
    bl_label = "Generate Full Rig"
    bl_description = ("Generate meta rig, rigify rig, and link them in one operation")
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        time_start = time.time()
        bpy.context.window.cursor_set('WAIT')

        try:
            armature = self._get_active_armature(context)
            if not armature:
                return {'CANCELLED'}

            rig_generator = template_manager.get_rig_generator(armature.aether_rig)
            if not rig_generator:
                self.report({'ERROR'}, "No rig template/modules configured for this armature")
                return {'CANCELLED'}

            state = rig_generator.generate_meta_rig(
                armature,
                cleanup_existing=lambda: bpy.ops.aether.clean_up_rig(),
            )
            if not state:
                self.report({'ERROR'}, "Meta rig generation failed")
                return {'CANCELLED'}

            if not rig_generator.generate_rigify_rig(state):
                self.report({'ERROR'}, "Rigify generation failed")
                return {'CANCELLED'}
            
            if get_preferences().auto_navigate_tabs == 'ON':
                set_active_tab(context, 'RIG_LAYERS')
            
            utils.object.select_only(armature)
            bpy.ops.object.mode_set(mode='POSE')

            print(f"[AetherBlend] Full rig generation: {time.time() - time_start:.3f}s")
            return {'FINISHED'}
        finally:
            bpy.context.window.cursor_set('DEFAULT')

class AETHER_OT_Generate_Meta_Rig(_ArmatureSelectionHelpers, bpy.types.Operator):
    bl_idname = "aether.generate_meta_rig"
    bl_label = "Generate Meta Rig"
    bl_description = "Generate only the meta rig without running Rigify"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        time_start = time.time()
        bpy.context.window.cursor_set('WAIT')

        try:
            armature = self._get_active_armature(context)
            if not armature:
                return {'CANCELLED'}

            rig_generator = template_manager.get_rig_generator(armature.aether_rig)
            if not rig_generator:
                self.report({'ERROR'}, "No rig template/modules configured for this armature")
                return {'CANCELLED'}

            state = rig_generator.generate_meta_rig(
                armature,
                cleanup_existing=lambda: bpy.ops.aether.clean_up_rig(),
            )
            if not state:
                self.report({'ERROR'}, "Meta rig generation failed")
                return {'CANCELLED'}

            rig_generator.reveal_meta_rig(state)

            print(f"[AetherBlend] Meta rig generation: {time.time() - time_start:.3f}s")
            return {'FINISHED'}
        finally:
            bpy.context.window.cursor_set('DEFAULT')
    
class AETHER_OT_Clean_Up_Rig(bpy.types.Operator):
    bl_idname = "aether.clean_up_rig"
    bl_label = "Remove Rigify Rig"
    bl_description = ("Removes Rigify Control bones while preserving FFXIV animation Data")
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        time_start = time.time()
        bpy.context.window.cursor_set('WAIT') 

        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            return {'CANCELLED'}
        
        rig_collections = armature.data.collections
        if not rig_collections.get("FFXIV"):
            return {'FINISHED'} # If it doesnt have a FFXIV collection, we can assume its already clean and just exit

        ## Delete Meta Rig and Scripts
        existing_meta_rig = armature.aether_rig.meta_rig
        
        if existing_meta_rig:
            if hasattr(existing_meta_rig.data, 'rigify_rig_ui') and existing_meta_rig.data.rigify_rig_ui:
                script = existing_meta_rig.data.rigify_rig_ui
                if script and script.name in bpy.data.texts:
                    bpy.data.texts.remove(script)
            bpy.data.objects.remove(existing_meta_rig, do_unlink=True)
        
        ## Cleanup Rigify ID
        if "rig_id" in armature.data:
            del armature.data["rig_id"]

        ## Delete Drivers 
        try:
            for fc in armature.data.animation_data.drivers:
                armature.data.driver_remove(fc.data_path, fc.array_index)
        except:
            pass
        
        # Cleanup Bones
        bpy.ops.object.mode_set(mode='EDIT')
        edit_bones = armature.data.edit_bones
        for bone in edit_bones:
            delete = True
            for coll in bone.collections:
                if coll.name == "FFXIV":
                    delete = False
                else:
                    coll.unassign(bone)
            if delete:
                edit_bones.remove(bone)

        try:
            bpy.ops.armature.collection_remove_unused()
        except RuntimeError:
            pass

        armature.aether_rig.rigified = False

        for coll in armature.data.collections:
            if coll.name == "FFXIV":
                coll.is_visible = True

        ## Cleanup Rigify Settings and Constrains
        for pose_bone in armature.pose.bones:
            pose_bone.rigify_type = " "
            for constraint in pose_bone.constraints:
                pose_bone.constraints.remove(constraint)

        bpy.ops.object.mode_set(mode='OBJECT')

        print(f"[AetherBlend] Clean Up rig: {time.time() - time_start:.3f}s")
        return {'FINISHED'}
    
class AETHER_OT_Reset_Rig(bpy.types.Operator):
    bl_idname = "aether.reset_rig"
    bl_label = "Reset FFXIV Rig"
    bl_description = ("Resets the armature to its original state (removes animation data)")
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            return {'CANCELLED'}
        
        result = bpy.ops.aether.clean_up_rig()
        if result != {'FINISHED'}:
            self.report({'ERROR'}, "Clean Up process Failed")
            return {'CANCELLED'}
        
        # Remove all animation data
        if armature.animation_data:
            armature.animation_data_clear()
        
        bpy.ops.object.mode_set(mode='OBJECT')
        return {'FINISHED'}

def register():
    bpy.utils.register_class(AETHER_OT_Clean_Up_Rig)
    bpy.utils.register_class(AETHER_OT_Reset_Rig)
    bpy.utils.register_class(AETHER_OT_Generate_Full_Rig)
    bpy.utils.register_class(AETHER_OT_Generate_Meta_Rig)

def unregister():
    bpy.utils.unregister_class(AETHER_OT_Generate_Meta_Rig)
    bpy.utils.unregister_class(AETHER_OT_Clean_Up_Rig)
    bpy.utils.unregister_class(AETHER_OT_Reset_Rig)
    bpy.utils.unregister_class(AETHER_OT_Generate_Full_Rig)