import bpy
import time

from ... import utils
from ...core.shared import PoseOperations, PoseOperationsStack
from ...core import rigify
from . import template_manager



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
        aether_rig_generator = template_manager.get_rig_generator(armature.aether_rig)
        
        # Meta Rig Base Generation
        meta_rig = utils.armature.duplicate(armature)
        meta_rig.name = f"META_{armature.name}"

        linked_coll = meta_rig.data.collections.get("Linked")
        unlinked_coll = meta_rig.data.collections.get("Unlinked")
        ffxiv_coll = meta_rig.data.collections.get("FFXIV")

        ## Setup for mendatory collections 
        if not linked_coll:
            linked_coll=meta_rig.data.collections.new("Linked")
        if not unlinked_coll:
            unlinked_coll=meta_rig.data.collections.new("Unlinked")
        if not ffxiv_coll:
            ffxiv_coll=meta_rig.data.collections.new("FFXIV")
        
        meta_rig_collections = meta_rig.data.collections
        meta_rig_collections.move(linked_coll.index, 0)  # Move Linked to the top
        meta_rig_collections.move(unlinked_coll.index, 1)  # Move Unlinked to the second position
        meta_rig_collections.move(ffxiv_coll.index, 2)  # Move FFXIV to the third position
        
        ## This will make sure all FF bones will carry over to the rigify rig
        pose_ops_stack = PoseOperationsStack()
        for bone in meta_rig.data.bones:
            pose_ops_stack.add(bone.name, PoseOperations(rigify_settings=rigify.types.basic_raw_copy(True)))

        # Preliminary LINK bone generation and joining
        link_rig = utils.armature.duplicate(armature)
        utils.armature.add_bone_prefix(link_rig, "LINK-")
        link_ffxiv_coll = link_rig.data.collections.get("FFXIV")
        if link_ffxiv_coll:
            link_rig.data.collections.remove(link_rig.data.collections["FFXIV"])
        utils.armature.b_collection.assign_bones(link_rig, list(link_rig.data.bones.keys()), "LINK", clear=True)

        utils.armature.join(src=link_rig, target=meta_rig)


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

        
        # Populate Data needed for generation
        eye_occlusion_object = self._find_objects_with_armature_and_material_property(armature=armature, property_name="ShaderPackage", property_value="characterocclusion.shpk")

        data = {}
        if eye_occlusion_object:
            data["eye_occlusion"] = eye_occlusion_object[0]
            data["ffxiv_armature"] = armature

        if len(data) == 0:
            data = None

        ui = rigify.settings.UI_Collections()

        for modules in aether_rig_generator.modules.values():
            for module in modules:
                integrity, module_pose_ops, module_ui_collections = module.execute(meta_rig, data)
                pose_ops_stack.merge(module_pose_ops)
                if module_ui_collections:
                    ui.add(module_ui_collections)
                if integrity:
                    break 

        ## Cleanup unlinked Bones and assign Collection to FFXIV bones
        data_bones = meta_rig.data.bones
        bones_to_delete = []
        for bone in data_bones.values():
            ffxiv_coll = meta_rig.data.collections.get("FFXIV")
            if ffxiv_coll and bone.name in ffxiv_coll.bones:
                if not bone.get("ab_linked", False):
                    pose_ops_stack.add(bone.name, PoseOperations(
                        b_collection="Unlinked",
                    ))
                    link_bone = meta_rig.data.bones.get(f"LINK-{bone.name}")
                    if link_bone:
                        bones_to_delete.append(link_bone.name)
                else:
                    pose_ops_stack.add(bone.name, PoseOperations(
                        b_collection="Linked",
                    ))
        
        
        bpy.ops.object.mode_set(mode='EDIT')
        for bone_name in bones_to_delete:
            bone = meta_rig.data.edit_bones.get(bone_name)
            if bone:
                meta_rig.data.edit_bones.remove(bone)


        ## Add Bone Collections UI
        hide_collections = []
        for coll in ui.collections:
            coll.create(meta_rig)
            coll, hide = coll.create_ui(meta_rig)
            if hide and coll:
                hide_collections.append(coll)
                

        # Now apply all operations per bone
        bpy.ops.object.mode_set(mode='POSE')
        pose_ops_stack.execute(meta_rig)
       
                
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
            aether_rig_generator = template_manager.get_rig_generator(armature.aether_rig)

            ## Execute Post Generation Steps
            data_bones = armature.data.bones
            ffxiv_data_bones = utils.armature.b_collection.get_bones(armature, "FFXIV")
            for bone in data_bones.values():
                if bone in ffxiv_data_bones.values():
                    bone.use_deform = True
                else:
                    bone.use_deform = False

            ## Widget Overrides
            bpy.ops.object.mode_set(mode='POSE')
            for widget in aether_rig_generator.getOverrides().values():
                widget.execute(armature)
            
            ffxiv_coll = armature.data.collections.get("FFXIV")
            linked_coll = armature.data.collections.get("Linked")
            unlinked_coll = armature.data.collections.get("Unlinked")
            if ffxiv_coll:
                ffxiv_coll.is_visible = False
            if linked_coll:
                linked_coll.is_visible = False
            if unlinked_coll:
                unlinked_coll.is_visible = False
                
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