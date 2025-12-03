import bpy
import time
from .. import utils
from ..data import *

def _cleanup_linked_rigify_bones(ffxiv_armature: bpy.types.Armature, rigify_rig: bpy.types.Armature) -> None:
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

def _find_objects_with_armature_and_material_property(armature: bpy.types.Armature, property_name: str, property_value=None) -> list[bpy.types.Object]:
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
            ## skip if genbone is a regex bone group if yes then return true 
            if isinstance(gen_bone.data, RegexBoneGroup):
                return True
            future_bones.append(gen_bone.data.name)
            if gen_bone.req_bones:
                for req_bone in gen_bone.req_bones:
                    if req_bone not in future_bones:
                        if req_bone not in armature_to_check.data.bones:
                            if gen_bone.is_optional:
                                future_bones.remove(gen_bone.data.name)
                                continue
                            return False
        return True
    
    def generateBones(self, data: dict | None = None) -> list[str]:
        """Generate the bones in the target armature based on the generative bones list."""
        generated_bones = []
        for gen_bone in self.generative_bones:
            ref = self.target_armature if gen_bone.ref == "tgt" else self.src_armature
            tgt = self.target_armature
            new_bone = gen_bone.generate(ref, tgt, data=data)
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

    def execute(self, data: dict | None = None) -> list[str]:
        """Execute the full generation process for this bone group."""
        verified = self.check()
        if not verified:
            return []

        bpy.ops.object.mode_set(mode='EDIT')
        generated_bones = self.generateBones(data=data)
        self.setRigifySettings()  ## 0.5 ms 
        return generated_bones

class AETHER_OT_Generate_Meta_Rig(bpy.types.Operator):
    bl_idname = "aether.generate_meta_rig"
    bl_label = "Generate Meta Rig"
    bl_description = ("Generate a meta rig based on available bones")
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        start_time = time.time()
        bpy.context.window.cursor_set('WAIT') 

        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "Select an armature object")
            return {'CANCELLED'}

        armature.hide_set(False)

        existing_meta_rig = armature.aether_rig.meta_rig
        
        if existing_meta_rig:
            existing_meta_rig.hide_set(False)
            bpy.data.objects.remove(existing_meta_rig, do_unlink=True)

        ## Creating Meta Rig and setting up basic Settings
        setup_start = time.time()
        meta_rig = utils.armature.create(location=armature.location, armature_name=f"META_{armature.name}")
        bpy.context.view_layer.objects.active = meta_rig
        meta_rig.show_in_front = True 
        bpy.ops.armature.rigify_use_standard_colors()
        bpy.ops.armature.rigify_add_color_sets()
        print(f"[AetherBlend] Meta rig creation: {time.time() - setup_start:.3f}s")

        ## Setup collections
        collection_start = time.time()
        hide_collections = []
        for collection in META_RIG_COLLECTIONS_INFO:
            coll = meta_rig.data.collections.new(collection.name)
            if coll:
                coll.rigify_color_set_name = collection.color_type
                coll.rigify_ui_row = collection.row_index
                coll.rigify_ui_title = collection.title
                if not collection.visible:
                    hide_collections.append(coll)
        print(f"[AetherBlend] Collection setup: {time.time() - collection_start:.3f}s")

        ## Propegate data 
        data_start = time.time()
        eye_occlusion_object = _find_objects_with_armature_and_material_property(armature=armature, property_name="ShaderPackage", property_value="characterocclusion.shpk")

        data = {}
        if eye_occlusion_object:
            data["eye_occlusion"] = eye_occlusion_object[0]

        if len(data) == 0:
            data = None
        print(f"[AetherBlend] Data propagation: {time.time() - data_start:.3f}s")

        ## Generate bones
        bone_gen_start = time.time()
        for bone_group_idx, bone_group in enumerate(HUMAN):
            for sub_group in bone_group:
                # Get the name from the first GenerativeBone's data if available
                group_name = "Unknown"
                if sub_group and len(sub_group) > 0:
                    first_bone = sub_group[0]
                    if hasattr(first_bone, 'data') and hasattr(first_bone.data, 'name'):
                        group_name = first_bone.data.name
                    elif hasattr(first_bone, 'name'):
                        group_name = first_bone.name
                
                group_start = time.time()
                gen_group = GenerativeMetaBoneGroup(src_armature=armature, target_armature=meta_rig, generative_bones=sub_group)
                gen_group.execute(data=data)
                print(f"[AetherBlend]   Group {bone_group_idx} ({group_name}): {time.time() - group_start:.3f}s")
        print(f"[AetherBlend] Bone generation: {time.time() - bone_gen_start:.3f}s")
                

        ## Hide Collections
        for hide_coll in hide_collections:
            hide_coll.is_visible = False

        ## Safe Rig Reference
        armature.aether_rig.meta_rig = meta_rig
        
        ## Parenting and context
        bpy.ops.object.mode_set(mode='OBJECT')
        meta_rig.parent = armature
        meta_rig.hide_set(True)

        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = armature
        armature.select_set(True)

        bpy.context.window.cursor_set('DEFAULT')
        print(f"[AetherBlend] Total meta rig generation time: {time.time() - start_time:.3f}s")
        return {'FINISHED'}

class AETHER_OT_Generate_Rigify_Rig(bpy.types.Operator):

    bl_idname = "aether.generate_rigify_rig"
    bl_label = "Generate Rigify Rig"
    bl_description = ("Generate the rigify control rig from the meta rig")
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.context.window.cursor_set('WAIT') 

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
        
        bpy.context.window.cursor_set('DEFAULT') 
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
        start_time = time.time()
        bpy.context.window.cursor_set('WAIT') 

        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "Select an armature object")
            return {'CANCELLED'}

        if not armature.aether_rig.rigify_rig:
            self.report({'ERROR'}, "No Rigify Rig found. Generate a Rigify Rig first.")
            return {'CANCELLED'}

        rigify_rig = armature.aether_rig.rigify_rig
        rigify_rig.hide_set(False)

        cleanup_start = time.time()
        if armature.aether_rig.rigify_linked:
            _cleanup_linked_rigify_bones(armature, rigify_rig)
        print(f"[AetherBlend] Cleanup: {time.time() - cleanup_start:.3f}s")

        merge_start = time.time()
        self._merge_control_rig_bones(armature, rigify_rig)
        print(f"[AetherBlend] Merge control rig bones: {time.time() - merge_start:.3f}s")

        rename_start = time.time()
        self._rename_constraints(armature)
        print(f"[AetherBlend] Rename constraints: {time.time() - rename_start:.3f}s")

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

        bpy.context.window.cursor_set('DEFAULT')
        print(f"[AetherBlend] Total link time: {time.time() - start_time:.3f}s")
        return {'FINISHED'}

    def _rename_constraints(self, armature: bpy.types.Armature) -> None:
        """Rename constraints based on ConstraintUIController settings."""
        for controller in UI_CONTROLLERS.values():
            if controller.rename_constraint is not None:
                controller.name_change(armature)    

    def _merge_control_rig_bones(self, ffxiv_armature: bpy.types.Armature, rigify_rig: bpy.types.Armature) -> bool:
        """Duplicate the control rig and merge it with the FFXIV armature."""
        original_mode = bpy.context.object.mode
        
        duplicate_start = time.time()
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
        print(f"[AetherBlend]   Duplicate & join: {time.time() - duplicate_start:.3f}s")
        
        bpy.ops.object.mode_set(mode='OBJECT')
        
        props_start = time.time()
        self.copy_rigify_properties(ffxiv_armature, rigify_rig)
        self._override_property_values(ffxiv_armature)
        print(f"[AetherBlend]   Copy properties: {time.time() - props_start:.3f}s")


        link_edits_start = time.time()
        for operation in LINK_EDIT_OPERATIONS:
            operation.execute(ffxiv_armature)
        print(f"[AetherBlend]   Link edits: {time.time() - link_edits_start:.3f}s")


        bpy.ops.object.mode_set(mode='POSE')

        link_pose_start = time.time()
        for bone_name, constraints in LINK_POSE_OPERATIONS.items():
           # get pose bone in ffxiv armature
           pose_bone = ffxiv_armature.pose.bones.get(bone_name)
           if pose_bone:
               for constraint in constraints:
                   constraint.apply(pose_bone, ffxiv_armature)
        print(f"[AetherBlend]   New constraints: {time.time() - link_pose_start:.3f}s")


        ## implement regex constrainst 
        regex_start = time.time()
        for pattern, constraints in REGEX_CONSTRAINTS.items():
            for pose_bone in ffxiv_armature.pose.bones:
                match = re.match(pattern, pose_bone.name)
                if match:
                    owner_bone_name = match.group(1) if match.groups() else re.sub(pattern, '', pose_bone.name)
                    owner_bone = ffxiv_armature.pose.bones.get(owner_bone_name)
                    if owner_bone:
                        for constraint in constraints:
                            constraint.apply(owner_bone, ffxiv_armature, target_override=pose_bone.name)
        print(f"[AetherBlend]   Regex constraints: {time.time() - regex_start:.3f}s")

        pose_apply_start = time.time()
        bpy.ops.pose.armature_apply()
        print(f"[AetherBlend]   Apply pose: {time.time() - pose_apply_start:.3f}s")

                   
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
        
        return True
    
    def _override_property_values(self, armature: bpy.types.Armature) -> None:
        """Override specific custom property values based on PROP_OVERRIDES."""
        bpy.ops.object.mode_set(mode='POSE')
        
        for bone_name, properties in PROP_OVERRIDES.items():
            pose_bone = armature.pose.bones.get(bone_name)
            
            if pose_bone:
                for property_name, override_value in properties.items():
                    try:
                        pose_bone[property_name] = override_value
                    except Exception as e:
                        print(f"[AetherBlend] Failed to set {bone_name}['{property_name}'] = {override_value}: {e}")
            else:
                print(f"[AetherBlend] Pose bone not found: {bone_name}")

class AETHER_OT_Unlink_Rigify_Rig(bpy.types.Operator):
    bl_idname = "aether.unlink_rigify_rig"
    bl_label = "Unlink Rigify Rig"
    bl_description = ("Unlink the Rigify Rig from the FFXIV Rig by removing control bones and constraints")
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.context.window.cursor_set('WAIT') 
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "Select an armature object")
            bpy.context.window.cursor_set('DEFAULT')
            return {'CANCELLED'}
        
        rigify_rig = armature.aether_rig.rigify_rig
        if rigify_rig:
            rigify_rig.hide_set(False)
            _cleanup_linked_rigify_bones(armature, rigify_rig)
            armature.aether_rig.rigify_linked = False
            bpy.context.window.cursor_set('DEFAULT')
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "No Rigify Rig found to unlink.")
            bpy.context.window.cursor_set('DEFAULT')
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