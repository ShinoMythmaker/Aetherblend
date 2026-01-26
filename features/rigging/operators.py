import bpy
import time

from ... import utils
from .templates import HUMAN
from ...core.shared import PoseOperations
from ...core import rigify

class AETHER_OT_Generate_Meta_Rig(bpy.types.Operator):
    bl_idname = "aether.generate_meta_rig"
    bl_label = "Generate Meta Rig"
    bl_description = ("Generate a meta rig based on available bones")
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        time_start = time.time()
        bpy.context.window.cursor_set('WAIT') 
    
        bpy.ops.object.mode_set(mode='OBJECT')

        # Get Active Armature
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "Select an armature object")
            return {'CANCELLED'}
        
        armature.hide_set(False)
        bpy.ops.object.select_all(action='DESELECT')
        armature.select_set(True)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

        # Cleanup Before Meta Rig Generation
        bpy.ops.aether.clean_up_rig()

        if armature.aether_rig.rigified:
            self.report({'ERROR'}, "Cannot generate meta rig on an armature that is already rigified.")
            return {'CANCELLED'}
        
        # Get Generator Data 
        aether_rig_generator = HUMAN
        
        # Meta Rig Base Generation
        meta_rig = utils.armature.duplicate(armature)
        meta_rig.name = f"META_{armature.name}"

        ## This will make sure all FF bones will carry over to the rigify rig
        all_pose_operations: dict[str, list[PoseOperations]] = {}
        for bone in meta_rig.data.bones:
            ops_list = [
                PoseOperations(
                    rigify_settings=rigify.types.basic_raw_copy(True)
                )
            ]    
            all_pose_operations[bone.name] = ops_list

        # Preliminary MCH bone generation and joining
        mch_rig = utils.armature.duplicate(armature)
        utils.armature.add_bone_prefix(mch_rig, "MCH-")
        mch_ffxiv_coll = mch_rig.data.collections.get("FFXIV")
        if mch_ffxiv_coll:
            mch_rig.data.collections.remove(mch_rig.data.collections["FFXIV"])
        utils.armature.b_collection.assign_bones(mch_rig, list(mch_rig.data.bones.keys()), "MCH")

        utils.armature.join(src=mch_rig, target=meta_rig)


        # Rigify Settings and Collections
        bpy.context.view_layer.objects.active = meta_rig
        meta_rig.show_in_front = True 
        meta_rig.data.rigify_target_rig = armature
        
        armature_collection = utils.collection.get_collection(armature)
        if armature_collection:
            utils.collection.link_to_collection([meta_rig], armature_collection)

        ## Add Color Sets
        for color_set in aether_rig_generator.getColorSets().values():
            color_set.add(meta_rig)

        ## Add Bone Collections UI
        hide_collections = []
        for coll in aether_rig_generator.getUICollections().values():
            coll.create(meta_rig)
            coll, hide = coll.create_ui(meta_rig)
            if hide and coll:
                hide_collections.append(coll)

        
        # Populate Data needed for generation
        eye_occlusion_object = self._find_objects_with_armature_and_material_property(armature=armature, property_name="ShaderPackage", property_value="characterocclusion.shpk")

        data = {}
        if eye_occlusion_object:
            data["eye_occlusion"] = eye_occlusion_object[0]
            data["ffxiv_armature"] = armature

        if len(data) == 0:
            data = None

        # Loop through all bone groups
        for bone_group_handler in aether_rig_generator.getBoneGroups().values():
            for bone_group in bone_group_handler:
                bones, pose_ops = bone_group.execute(meta_rig, data)

                if not bones and not pose_ops:
                    continue # Skip if nothing to process
                
                # Merge operations, appending to existing lists
                for bone_name, ops_list in pose_ops.items():
                    # Since we store lists, if the bone doesnt exist yet, create an empty list, so we can use .extend()
                    if bone_name not in all_pose_operations:
                        all_pose_operations[bone_name] = []
                    all_pose_operations[bone_name].extend(ops_list)
                
                break  # Only process the first matching bone group

        # Now apply all operations per bone
        bpy.ops.object.mode_set(mode='POSE')
        for bone_name, ops_list in all_pose_operations.items():
            bone = meta_rig.pose.bones.get(bone_name)
            for ops in ops_list:
                ops.execute(bone, meta_rig)
                
        for hide_coll in hide_collections:
            hide_coll.is_visible = False

        # Finalize Meta Rig Assignment
        armature.aether_rig.meta_rig = meta_rig
        

        bpy.ops.object.mode_set(mode='OBJECT')
        meta_rig.parent = armature
        meta_rig.hide_set(True)
        #meta_rig.hide_viewport = True

        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = armature
        armature.select_set(True)

        bpy.context.window.cursor_set('DEFAULT')

        print(f"[AetherBlend] Meta rig generation: {time.time() - time_start:.3f}s")
        return {'FINISHED'}
    
    def _find_objects_with_armature_and_material_property(self, armature: bpy.types.Object, property_name: str, property_value=None) -> list[bpy.types.Object]:
        """Find all objects that have the specified armature as a constraint target and have materials with a specific custom property."""
        matching_objects = []
        
        for obj in bpy.data.objects:
            # Check if object has the armature as a constraint target
            has_armature_constraint = False
            
            # Check object-level constraints
            for constraint in obj.constraints:
                if hasattr(constraint, 'target') and constraint.target == armature:
                    has_armature_constraint = True
                    break
            
            # If not found in object constraints, check modifiers (like Armature modifier)
            if not has_armature_constraint: 
                for modifier in obj.modifiers:
                    if modifier.type == 'ARMATURE' and modifier.object == armature:
                        has_armature_constraint = True
                        break
            
            # If not found yet, check bone constraints (if object has pose bones)
            if not has_armature_constraint and obj.type == 'ARMATURE' and obj.pose:
                for pose_bone in obj.pose.bones:
                    for constraint in pose_bone.constraints:
                        if hasattr(constraint, 'target') and constraint.target == armature:
                            has_armature_constraint = True
                            break
                    if has_armature_constraint:
                        break
            
            # If object has armature constraint, check materials for custom property
            if has_armature_constraint and obj.data and hasattr(obj.data, 'materials'):
                for material_slot in obj.material_slots:
                    if material_slot.material:
                        material = material_slot.material
                        
                        # Check if material has the custom property
                        if property_name in material:
                            # If specific value is required, check it matches
                            if property_value is not None:
                                if material[property_name] == property_value:
                                    matching_objects.append(obj)
                                    break
                            else:
                                # Just checking for property existence
                                matching_objects.append(obj)
                                break
        
        return matching_objects


class AETHER_OT_Generate_Rigify_Rig(bpy.types.Operator):
    bl_idname = "aether.generate_rigify_rig"
    bl_label = "Generate Rigify Rig"
    bl_description = ("Generate the rigify control rig from the meta rig")
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        time_start = time.time()
        bpy.context.window.cursor_set('WAIT') 

        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            return {'CANCELLED'}
        
        if not armature.aether_rig.meta_rig:
            self.report({'ERROR'}, "No meta rig found. Generate a meta rig first.")
            return {'CANCELLED'}

        # Make sure Meta Rig is available
        meta_rig = armature.aether_rig.meta_rig
        meta_rig.hide_set(False)
        meta_rig.hide_viewport = False

        bpy.context.view_layer.objects.active = meta_rig
        bpy.ops.object.select_all(action='DESELECT')
        meta_rig.select_set(True)
    
        result = bpy.ops.pose.rigify_generate()

        if result == {"FINISHED"}:
            aether_rig_generator = HUMAN

            ## Execute Post Generation Steps
            ffxiv_data_bones = utils.armature.b_collection.get_bones(armature, "FFXIV")
            for bone in ffxiv_data_bones.values():
                if bone:
                    bone.use_deform = True

            ## Widget Overrides
            bpy.ops.object.mode_set(mode='POSE')
            for widget in aether_rig_generator.getWidgetOverrides().values():
                widget.execute(armature)
            
            bpy.ops.object.mode_set(mode='OBJECT')
            armature.aether_rig.rigified = True

        meta_rig.hide_set(True)
        meta_rig.hide_viewport = True

        bpy.context.window.cursor_set('DEFAULT') 
        print(f"[AetherBlend] Rigify rig generation: {time.time() - time_start:.3f}s")
        return {'FINISHED'}
            
    
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
        coll_to_delete = []
        bpy.ops.object.mode_set(mode='EDIT')
        for collection in armature.data.collections_all:
            if collection.name == "FFXIV":
                collection.is_visible = False
            else:
                collection.is_visible = True
                coll_to_delete.append(collection.name)

        bpy.ops.armature.select_all(action='DESELECT')
        bpy.ops.armature.reveal()
        bpy.ops.armature.select_all(action='SELECT')
        bpy.ops.armature.delete()

        ## Deep Cleanup
        root_level_bones = [bone for bone in armature.data.edit_bones if bone.parent is None]
        for root_bone in root_level_bones:
            if root_bone.name != "n_root":      ## whack
                for child_bone in root_bone.children_recursive:
                    armature.data.edit_bones.remove(child_bone)

                armature.data.edit_bones.remove(root_bone)

        # Cleanup Collections
        for coll_name in coll_to_delete:
            coll = armature.data.collections.get(coll_name)
            if coll:
                armature.data.collections.remove(coll)

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

class AETHER_OT_Generate_Full_Rig(bpy.types.Operator):
    bl_idname = "aether.generate_full_rig"
    bl_label = "Generate Full Rig"
    bl_description = ("Generate meta rig, rigify rig, and link them in one operation")
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        time_start = time.time()
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "Select an armature object")
            return {'CANCELLED'}
        
        result = bpy.ops.aether.generate_meta_rig()
        if result != {'FINISHED'}:
            self.report({'ERROR'}, "Meta rig generation failed")
            return {'CANCELLED'}
        
        result = bpy.ops.aether.generate_rigify_rig()
        if result != {'FINISHED'}:
            self.report({'ERROR'}, "Rigify rig generation failed")
            return {'CANCELLED'}
        
        print(f"[AetherBlend] Full rig generation: {time.time() - time_start:.3f}s")
        return {'FINISHED'}
    



    
def register():
    bpy.utils.register_class(AETHER_OT_Generate_Meta_Rig)
    bpy.utils.register_class(AETHER_OT_Generate_Rigify_Rig)
    bpy.utils.register_class(AETHER_OT_Clean_Up_Rig)
    bpy.utils.register_class(AETHER_OT_Reset_Rig)
    bpy.utils.register_class(AETHER_OT_Generate_Full_Rig)

def unregister():
    bpy.utils.unregister_class(AETHER_OT_Generate_Meta_Rig)
    bpy.utils.unregister_class(AETHER_OT_Generate_Rigify_Rig)
    bpy.utils.unregister_class(AETHER_OT_Clean_Up_Rig)
    bpy.utils.unregister_class(AETHER_OT_Reset_Rig)
    bpy.utils.unregister_class(AETHER_OT_Generate_Full_Rig)