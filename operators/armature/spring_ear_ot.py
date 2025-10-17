import bpy
from ...utils import armature as rig_utils
from ...data.constants import xiv_ear_bone_l, xiv_ear_bone_r, sb_ear_target_bone_l, sb_ear_target_bone_r, sb_ear_parent_bone, sb_ears_collection, spring_prefix, spring_bone_collection
from ..spring_bones_ot import end_spring_bone

class AETHER_OT_Generate_Spring_Ears(bpy.types.Operator):
    """Generate spring ear bones for the active armature object."""
    bl_idname = "aether.generate_spring_ears"
    bl_label = "Generate Spring Ears"
    bl_options = {'REGISTER', 'UNDO'}

    
    def execute(self, context):
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "[AetherBlend] Select an armature object")
            return {'CANCELLED'}
        
        context.scene.ab_sb_global_spring_frame = False 
        context.scene.ab_sb_global_spring = False 

        referenece_bones_l = xiv_ear_bone_l + sb_ear_target_bone_l
        referenece_bones_r = xiv_ear_bone_r + sb_ear_target_bone_r


        bpy.ops.object.mode_set(mode='EDIT')

        # store visibility state of xiv_ear_bones
        original_visibility = rig_utils.bone.get_bone_visibility(armature, referenece_bones_l + referenece_bones_r)

        # Delete existing spring bones collection if it exists
        if armature.data.collections.get(sb_ears_collection):
            rig_utils.b_collection.delete_with_bones(armature, sb_ears_collection)

        # reset xiv_ear_bones
        rig_utils.bone.delete_keyframes(armature, xiv_ear_bone_l)
        rig_utils.bone.reset_transforms(armature, xiv_ear_bone_l)

        rig_utils.bone.delete_keyframes(armature, xiv_ear_bone_r)
        rig_utils.bone.reset_transforms(armature, xiv_ear_bone_r)

        # Create spring bones
        print(f"[AetherBlend] Generating spring ears for {referenece_bones_l}...")
        spring_bones_l = rig_utils.generate.bone_chain(armature, referenece_bones_l, prefix=spring_prefix, parent_bone=sb_ear_parent_bone)
        spring_bones_r = rig_utils.generate.bone_chain(armature, referenece_bones_r, prefix=spring_prefix, parent_bone=sb_ear_parent_bone)

        # Check if spring bones is an empty array
        if not spring_bones_l or not spring_bones_r:
            self.report({'ERROR'}, "[AetherBlend] No spring bones generated. Missing reference bones.")
            return {'CANCELLED'}

        rig_utils.b_collection.assign_bones(armature, spring_bones_l, f"{spring_bone_collection}/{sb_ears_collection}")
        rig_utils.b_collection.assign_bones(armature, spring_bones_r, f"{spring_bone_collection}/{sb_ears_collection}")

        # Apply Copy Rotation constraints to each reference bone except the last
        rig_utils.bone.add_constraint_copy_rotation(xiv_ear_bone_l, armature, spring_bones_l, overwrite=True)
        rig_utils.bone.add_constraint_copy_rotation(xiv_ear_bone_r, armature, spring_bones_r, overwrite=True)

        # Merge both spring bone lists 
        spring_bones = spring_bones_l +spring_bones_r

        # Apply Spring Bones properties to each spring bone
        for index, spring_bone_name in enumerate(spring_bones):
            pb = armature.pose.bones[spring_bone_name]
            pb.ab_sb_bone_spring = True           
            pb.ab_sb_bone_rot = True              
            pb.ab_sb_collide = True               
            pb.ab_sb_lock_axis = 'NONE'           
            pb.ab_sb_stiffness = 0.15
            pb.ab_sb_damp = 0.70
            pb.ab_sb_gravity = 0
            pb.ab_sb_global_influence = 0.8

        # Restore original bone visibility
        rig_utils.bone.restore_visibility(armature, original_visibility)

        bpy.ops.object.mode_set(mode='POSE')   

        self.report({'INFO'}, "[AetherBlend] Spring ears generated and constraints set.")
        return {'FINISHED'}
    

class AETHER_OT_Bake_Spring_Ears(bpy.types.Operator):
    """Bake spring ear bones for the active armature object."""
    bl_idname = "aether.bake_spring_ears"
    bl_label = "Bake Spring Ears"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.context.window.cursor_set('WAIT')  
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "[AetherBlend] Select an armature object")
            return {'CANCELLED'}

        start_frame, end_frame = rig_utils.get_frame_range(armature)

        reference_bones = xiv_ear_bone_r + xiv_ear_bone_l

        original_visibility = rig_utils.bone.get_bone_visibility(armature, reference_bones)

        # Select only the reference bones before baking
        rig_utils.bone.select_edit(armature, reference_bones)

        pre_roll = 50
        pre_roll_start = start_frame - pre_roll

        for f in range(pre_roll_start, start_frame):
            bpy.context.scene.frame_set(f)

        # Bake with only the reference bones selected
        bpy.ops.nla.bake(
            frame_start=start_frame,
            frame_end=end_frame,
            only_selected=True,
            visual_keying=True,
            clear_constraints=True,
            use_current_action=True,
            bake_types={'POSE'},
            step=1,
        )

        # Restore original bone visibility
        rig_utils.bone.restore_visibility(armature, original_visibility)

        bpy.ops.object.mode_set(mode='POSE')
        bpy.context.window.cursor_set('DEFAULT')  
        self.report({'INFO'}, f"[AetherBlend] Spring ears baked from frame {start_frame} to {end_frame}.")
        return {'FINISHED'}
    

class AETHER_OT_Delete_Spring_Ears(bpy.types.Operator):
    """Delete spring ear bones for the active armature object."""
    bl_idname = "aether.delete_spring_ears"
    bl_label = "Delete Spring Ears"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "[AetherBlend] Select an armature object")
            return {'CANCELLED'}
        
        # Disable Spring Bones
        context.scene.ab_sb_global_spring_frame = False 
        context.scene.ab_sb_global_spring = False 
        end_spring_bone(context, self)

        bpy.ops.object.mode_set(mode='POSE')

        reference_bones = xiv_ear_bone_r + xiv_ear_bone_l

        # Remove Copy Rotation constraints from reference bones
        rig_utils.bone.remove_copy_rotation_constraints(armature, reference_bones)

        bpy.ops.object.mode_set(mode='EDIT')

        # Delete the spring bone collection and all bones within
        rig_utils.b_collection.delete_with_bones(armature, sb_ears_collection)

        bpy.ops.object.mode_set(mode='POSE')
        self.report({'INFO'}, "[AetherBlend] Spring ears deleted.")
        return {'FINISHED'}
    

def register():
    bpy.utils.register_class(AETHER_OT_Generate_Spring_Ears)
    bpy.utils.register_class(AETHER_OT_Bake_Spring_Ears)
    bpy.utils.register_class(AETHER_OT_Delete_Spring_Ears)

def unregister():
    bpy.utils.unregister_class(AETHER_OT_Generate_Spring_Ears)
    bpy.utils.unregister_class(AETHER_OT_Bake_Spring_Ears)
    bpy.utils.unregister_class(AETHER_OT_Delete_Spring_Ears)
    
