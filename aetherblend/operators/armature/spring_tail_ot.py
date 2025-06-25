import bpy
from ...utils import rig as rig_utils
from ...data.constants import xiv_tail_bones, sb_tail_collection, spring_prefix
from ..spring_bones_ot import end_spring_bone



class AETHER_OT_Generate_Spring_Tail(bpy.types.Operator):
    """Generates a spring tail for the selected armature"""
    bl_idname = "aether.generate_spring_tail"
    bl_label = "Generate Spring Tail"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "[AetherBlend] Select an armature object")
            return {'CANCELLED'}

        bpy.ops.object.mode_set(mode='EDIT')

        # Delete existing spring bones collection if it exists
        rig_utils.bone.delete_bone_collection_and_bones(armature, "SB_Tail")

        # reset xiv_tail_bones
        rig_utils.bone.delete_keyframes(armature, xiv_tail_bones)
        rig_utils.bone.reset_bone_transforms(armature, xiv_tail_bones)
 
        # Create spring bones
        spring_bones = rig_utils.generate.bone_chain(armature, xiv_tail_bones, prefix=spring_prefix, parent_bone="j_kosi")

        rig_utils.bone.assign_bones_to_collection(armature, spring_bones, "Spring Bones/SB_Tail")

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

        bpy.ops.object.mode_set(mode='POSE')   

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
        end_spring_bone(context, self)

        bpy.ops.object.mode_set(mode='POSE')

        # Remove Copy Rotation constraints from reference bones
        rig_utils.bone.remove_copy_rotation_constraints(armature, xiv_tail_bones)

        bpy.ops.object.mode_set(mode='EDIT')

        # Delete the spring bone collection and all bones within
        rig_utils.bone.delete_bone_collection_and_bones(armature, sb_tail_collection)

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

        start_frame, end_frame = rig_utils.armature.get_frame_range(armature)

        # Select only the tail bones before baking
        rig_utils.bone.select_bones(armature, xiv_tail_bones)

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