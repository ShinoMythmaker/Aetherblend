import bpy
from ...utils import armature as rig_utils
from ...data.constants import xiv_tail_bones, sb_tail_collection, spring_prefix, spring_bone_collection, sb_tail_parent_bone
from ..spring_bones_ot import end_spring_bone



class AETHER_OT_Generate_Spring_Tail(bpy.types.Operator):
    """Generates a spring tail for the selected armature"""
    bl_idname = "aether.generate_spring_tail"
    bl_label = "Generate Spring Tail"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.context.window.cursor_set('WAIT')  
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "[AetherBlend] Select an armature object")
            return {'CANCELLED'}
        
        context.scene.ab_sb_global_spring_frame = False 
        context.scene.ab_sb_global_spring = False 

        bpy.ops.object.mode_set(mode='EDIT')

        # Delete existing spring bones collection if it exists
        if armature.data.collections.get(sb_tail_collection):
            rig_utils.b_collection.delete_with_bones(armature, sb_tail_collection)

        # reset xiv_tail_bones
        original_visibility = rig_utils.bone.get_bone_visibility(armature, xiv_tail_bones)

        rig_utils.bone.delete_keyframes(armature, xiv_tail_bones)
        rig_utils.bone.reset_transforms(armature, xiv_tail_bones)
 
        # Create spring bones
        spring_bones = rig_utils.generate.bone_chain(armature, xiv_tail_bones, prefix=spring_prefix, parent_bone=sb_tail_parent_bone)

        # Check if spring bones is an empty array
        if not spring_bones:
            self.report({'ERROR'}, "[AetherBlend] No spring bones generated. Missing reference bones.")
            return {'CANCELLED'}

        rig_utils.b_collection.assign_bones(armature, spring_bones, f"{spring_bone_collection}/{sb_tail_collection}")

        # Apply Copy Rotation constraints to each reference bone except the last
        rig_utils.bone.add_constraint_copy_rotation(xiv_tail_bones[:-1], armature, spring_bones, overwrite=True)

        # Apply Spring Bones properties to each spring bone
        for index, spring_bone_name in enumerate(spring_bones):
            pb = armature.pose.bones[spring_bone_name]
            pb.ab_sb_bone_spring = True           
            pb.ab_sb_bone_rot = True              
            pb.ab_sb_collide = True               
            pb.ab_sb_lock_axis = 'NONE'           
            
            if index == 0:
                pb.ab_sb_stiffness = 0.20
                pb.ab_sb_damp = 0.40
                pb.ab_sb_gravity = 0.25
                pb.ab_sb_global_influence = 0.8
            elif index == 1:
                pb.ab_sb_stiffness = 0.20
                pb.ab_sb_damp = 0.40
                pb.ab_sb_gravity = 0.15
                pb.ab_sb_global_influence = 0.8
            elif index == 2:
                pb.ab_sb_stiffness = 0.20
                pb.ab_sb_damp = 0.40
                pb.ab_sb_gravity = (-0.15)
                pb.ab_sb_global_influence = 0.8
            elif index == 3:
                pb.ab_sb_stiffness = 0.20
                pb.ab_sb_damp = 0.40
                pb.ab_sb_gravity = (-0.20)
                pb.ab_sb_global_influence = 0.80
            else :
                pb.ab_sb_stiffness = 0.20
                pb.ab_sb_damp = 0.40
                pb.ab_sb_gravity = 0.20
                pb.ab_sb_global_influence = 0.8 


        # Restore original bone visibility
        rig_utils.bone.restore_visibility(armature, original_visibility)

        bpy.ops.object.mode_set(mode='POSE')   
        bpy.context.window.cursor_set('DEFAULT')  
        self.report({'INFO'}, "[AetherBlend] Spring tail generated and constraints set.")
        return {'FINISHED'}

class AETHER_OT_Delete_Spring_Tail(bpy.types.Operator):
    """Deletes the generated spring tail and removes constraints from reference bones"""
    bl_idname = "aether.delete_spring_tail"
    bl_label = "Delete Spring Tail"
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

        # Remove Copy Rotation constraints from reference bones
        rig_utils.bone.remove_copy_rotation_constraints(armature, xiv_tail_bones)

        bpy.ops.object.mode_set(mode='EDIT')

        # Delete the spring bone collection and all bones within
        rig_utils.b_collection.delete_with_bones(armature, sb_tail_collection)

        bpy.ops.object.mode_set(mode='POSE')
        self.report({'INFO'}, "[AetherBlend] Spring tail deleted.")
        return {'FINISHED'}

class AETHER_OT_Bake_Spring_Tail(bpy.types.Operator):
    """Bake the spring tail animation to keyframes"""
    bl_idname = "aether.bake_spring_tail"
    bl_label = "Bake Spring Tail"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "[AetherBlend] Select an armature object")
            return {'CANCELLED'}

        start_frame, end_frame = rig_utils.get_frame_range(armature)

        original_visibility = rig_utils.bone.get_bone_visibility(armature, xiv_tail_bones)

        # Select only the tail bones before baking
        rig_utils.bone.select_edit(armature, xiv_tail_bones)

        pre_roll = 50
        pre_roll_start = start_frame - pre_roll

        for f in range(pre_roll_start, start_frame):
            bpy.context.scene.frame_set(f)

        # Bake with only the tail bones selected
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
        self.report({'INFO'}, f"[AetherBlend] Spring tail baked from frame {start_frame} to {end_frame}.")
        return {'FINISHED'}



def register():
    bpy.utils.register_class(AETHER_OT_Generate_Spring_Tail)
    bpy.utils.register_class(AETHER_OT_Delete_Spring_Tail)
    bpy.utils.register_class(AETHER_OT_Bake_Spring_Tail)

def unregister():
    bpy.utils.unregister_class(AETHER_OT_Generate_Spring_Tail)
    bpy.utils.unregister_class(AETHER_OT_Delete_Spring_Tail)
    bpy.utils.unregister_class(AETHER_OT_Bake_Spring_Tail)