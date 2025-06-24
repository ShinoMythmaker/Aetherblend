import bpy
from ..utils import rig as rig_utils

class AETHER_OT_Generate_Spring_Tail(bpy.types.Operator):
    """Generates a spring tail for the selected armature"""
    bl_idname = "aether.generate_spring_tail"
    bl_label = "Generate Spring Tail"
    bl_options = {'REGISTER', 'UNDO'}

    bone_names = ["n_sippo_a", "n_sippo_b", "n_sippo_c", "n_sippo_d", "n_sippo_e"]

    def execute(self, context):
        armature_obj = context.active_object
        if not armature_obj or armature_obj.type != 'ARMATURE':
            self.report({'ERROR'}, "[AetherBlend] Select an armature object")
            return {'CANCELLED'}

        bpy.ops.object.mode_set(mode='EDIT')
 
        # Create spring bones
        spring_bones = rig_utils.generate.bone_chain(armature_obj, self.bone_names, prefix="sb_", parent_bone="j_kosi")

        # Apply Copy Rotation constraints to each reference bone except the last
        rig_utils.bone.add_constraint_copy_rotation(self.bone_names[:-1], armature_obj, spring_bones)

        # Apply Spring Bones properties to each spring bone
        for index, spring_bone_name in enumerate(spring_bones):
            pb = armature_obj.pose.bones[spring_bone_name]
            pb.sb_bone_spring = True           
            pb.sb_bone_rot = True              
            pb.sb_collide = True               
            pb.sb_lock_axis = 'NONE'           
            
            if index == 0:
                pb.sb_stiffness = 0.20             
                pb.sb_damp = 0.40                  
                pb.sb_gravity = 0.25               
                pb.sb_global_influence = 0.8       
            elif index == 1:
                pb.sb_stiffness = 0.20             
                pb.sb_damp = 0.40                  
                pb.sb_gravity = 0.15               
                pb.sb_global_influence = 0.8       
            elif index == 2:
                pb.sb_stiffness = 0.20             
                pb.sb_damp = 0.40                  
                pb.sb_gravity = (-0.15)            
                pb.sb_global_influence = 0.8       
            elif index == 3:
                pb.sb_stiffness = 0.20             
                pb.sb_damp = 0.40                  
                pb.sb_gravity = (-0.20)            
                pb.sb_global_influence = 0.80      
            else :
                pb.sb_stiffness = 0.20             
                pb.sb_damp = 0.40                  
                pb.sb_gravity = 0.20               
                pb.sb_global_influence = 0.8       

        self.report({'INFO'}, "[AetherBlend] Spring tail generated and constraints set.")
        return {'FINISHED'}


def register():
    bpy.utils.register_class(AETHER_OT_Generate_Spring_Tail)

def unregister():
    bpy.utils.unregister_class(AETHER_OT_Generate_Spring_Tail)