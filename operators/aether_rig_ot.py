import bpy
import time
from bpy.props import IntProperty
from .. import utils
from ..data import *
from ..preferences import get_preferences

def _find_objects_with_armature_and_material_property(armature: bpy.types.Object, property_name: str, property_value=None) -> list[bpy.types.Object]:
    """Find all objects that have the specified armature as a constraint target and have materials with a specific custom property.
    
    Args:
        armature: The armature object to search for in constraints
        property_name: The name of the custom property to look for in materials
        property_value: Optional specific value the property should have. If None, just checks for property existence
        
    Returns:
        List of objects that meet both criteria
    """
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

class AETHER_OT_Generate_Meta_Rig(bpy.types.Operator):
    bl_idname = "aether.generate_meta_rig"
    bl_label = "Generate Meta Rig"
    bl_description = ("Generate a meta rig based on available bones")
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        bpy.context.window.cursor_set('WAIT') 
        bpy.ops.object.mode_set(mode='OBJECT')

        # Get Active Armature
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "Select an armature object")
            return {'CANCELLED'}
        
        armature.hide_set(False)

        # Check if rig is Linked
        if armature.aether_rig.rigify_linked:
            bpy.ops.aether.unlink_rigify_rig()
        
        # Remove Existing Rigs
        existing_meta_rig = armature.aether_rig.meta_rig
        existing_rigify_rig = armature.aether_rig.rigify_rig
        
        if existing_meta_rig:
            if hasattr(existing_meta_rig.data, 'rigify_rig_ui') and existing_meta_rig.data.rigify_rig_ui:
                script = existing_meta_rig.data.rigify_rig_ui
                if script and script.name in bpy.data.texts:
                    bpy.data.texts.remove(script)
            bpy.data.objects.remove(existing_meta_rig, do_unlink=True)
        
        if existing_rigify_rig:
            bpy.data.objects.remove(existing_rigify_rig, do_unlink=True)
            armature.aether_rig.rigify_rig = None


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

        utils.armature.join(src=mch_rig, target=meta_rig)


        # Rigify Settings and Collections
        bpy.context.view_layer.objects.active = meta_rig
        meta_rig.show_in_front = True 
        bpy.ops.armature.rigify_use_standard_colors()
        bpy.ops.armature.rigify_add_color_sets()
        
        armature_collection = utils.collection.get_collection(armature)
        if armature_collection:
            utils.collection.link_to_collection([meta_rig], armature_collection)
        
        hide_collections = []
        for collection in META_RIG_COLLECTIONS_INFO:
            coll = meta_rig.data.collections.new(collection.name)
            if coll:
                coll.rigify_color_set_name = collection.color_type
                coll.rigify_ui_row = collection.row_index
                coll.rigify_ui_title = collection.title
                if not collection.visible:
                    hide_collections.append(coll)


        # Populate Data needed for generation
        eye_occlusion_object = _find_objects_with_armature_and_material_property(armature=armature, property_name="ShaderPackage", property_value="characterocclusion.shpk")

        data = {}
        if eye_occlusion_object:
            data["eye_occlusion"] = eye_occlusion_object[0]

        if len(data) == 0:
            data = None

        # Loop through all bone groups
        for bone_group_handler in HUMAN:
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
        return {'FINISHED'}

class AETHER_OT_Generate_Rigify_Rig(bpy.types.Operator):

    bl_idname = "aether.generate_rigify_rig"
    bl_label = "Generate Rigify Rig"
    bl_description = ("Generate the rigify control rig from the meta rig")
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        return {'FINISHED'}
            
class AETHER_OT_Link_Rigify_Rig(bpy.types.Operator):
    bl_idname = "aether.link_rigify_rig"
    bl_label = "Link Rigify Rig"
    bl_description = ("Link the Rigify Rig to the FFXIV Rig by merging control bones and setting up constraints")
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        return {'FINISHED'}
    
class AETHER_OT_Unlink_Rigify_Rig(bpy.types.Operator):
    bl_idname = "aether.unlink_rigify_rig"
    bl_label = "Unlink Rigify Rig"
    bl_description = ("Unlink the Rigify Rig from the FFXIV Rig by restoring from backup")
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        return {'FINISHED'}

class AETHER_OT_Generate_Full_Rig(bpy.types.Operator):
    bl_idname = "aether.generate_full_rig"
    bl_label = "Generate Full Rig"
    bl_description = ("Generate meta rig, rigify rig, and link them in one operation")
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        return {'FINISHED'}
    
def register():
    bpy.utils.register_class(AETHER_OT_Generate_Meta_Rig)
    bpy.utils.register_class(AETHER_OT_Generate_Rigify_Rig)
    bpy.utils.register_class(AETHER_OT_Link_Rigify_Rig)
    bpy.utils.register_class(AETHER_OT_Unlink_Rigify_Rig)
    bpy.utils.register_class(AETHER_OT_Generate_Full_Rig)

def unregister():
    bpy.utils.unregister_class(AETHER_OT_Generate_Meta_Rig)
    bpy.utils.unregister_class(AETHER_OT_Generate_Rigify_Rig)
    bpy.utils.unregister_class(AETHER_OT_Link_Rigify_Rig)
    bpy.utils.unregister_class(AETHER_OT_Unlink_Rigify_Rig)
    bpy.utils.unregister_class(AETHER_OT_Generate_Full_Rig)