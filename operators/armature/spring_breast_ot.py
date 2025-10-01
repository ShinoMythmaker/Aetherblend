import bpy
import mathutils
from ...utils import rig as rig_utils
from ...data.constants import xiv_breast_bone_r, xiv_breast_bone_l, sb_breast_collection, sb_breast_parent_bone, spring_prefix, spring_bone_collection
from ..spring_bones_ot import end_spring_bone

class AETHER_OT_Generate_Spring_Breasts(bpy.types.Operator):
    """Generate spring breast bones for the active armature object."""
    bl_idname = "aether.generate_spring_breasts"
    bl_label = "Generate Spring Breasts"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "[AetherBlend] Select an armature object")
            return {'CANCELLED'}

        bpy.ops.object.mode_set(mode='EDIT')

        # store visibility state of xiv_breast_bones
        original_visibility = rig_utils.bone.get_bone_visibility(armature, xiv_breast_bone_r + xiv_breast_bone_l)


        # Delete existing spring breast collection if it exists
        if rig_utils.bone.collection_exists(armature, sb_breast_collection):
            rig_utils.bone.delete_bone_collection_and_bones(armature, sb_breast_collection)

        # reset xiv_breast_bones
        rig_utils.bone.delete_keyframes(armature, xiv_breast_bone_r)
        rig_utils.bone.reset_bone_transforms(armature, xiv_breast_bone_r)

        rig_utils.bone.delete_keyframes(armature, xiv_breast_bone_l)
        rig_utils.bone.reset_bone_transforms(armature, xiv_breast_bone_l)

        # check if xiv_breast_bones exist
        if not rig_utils.bone.bones_exist(armature, xiv_breast_bone_r + xiv_breast_bone_l):
            self.report({'ERROR'}, "[AetherBlend] Missing reference bones for spring breasts.")
            return {'CANCELLED'}

        spring_bone_r = rig_utils.generate.bone_on_local_axis_x(armature, xiv_breast_bone_r[0], parent_bone=sb_breast_parent_bone, prefix=spring_prefix)
        spring_bone_l = rig_utils.generate.bone_on_local_axis_x(armature, xiv_breast_bone_l[0], parent_bone=sb_breast_parent_bone, prefix=spring_prefix)

        print(f"[AetherBlend] Generating spring breasts for {xiv_breast_bone_r} and {spring_bone_r}")
        print(f"[AetherBlend] Generating spring breasts for {xiv_breast_bone_l} and {spring_bone_l}")


        # Assign to collection
        rig_utils.bone.assign_bones_to_collection(armature, [spring_bone_r, spring_bone_l], f"{spring_bone_collection}/{sb_breast_collection}")

        bpy.ops.object.mode_set(mode='POSE')

        # Apply Copy Rotation constraints and spring bone parameters
        rig_utils.bone.add_constraint_copy_rotation(xiv_breast_bone_r, armature, [spring_bone_r], overwrite=True)
        rig_utils.bone.add_constraint_copy_rotation(xiv_breast_bone_l, armature, [spring_bone_l], overwrite=True)

        for spring_bone_name in [spring_bone_r, spring_bone_l]:
            pb = armature.pose.bones[spring_bone_name]
            pb.ab_sb_bone_spring = True
            pb.ab_sb_bone_rot = True
            pb.ab_sb_collide = True
            pb.ab_sb_lock_axis = 'NONE'
            pb.ab_sb_stiffness = 0.1
            pb.ab_sb_damp = 0.9
            pb.ab_sb_gravity = 0
            pb.ab_sb_global_influence = 0.9


        # Restore original bone visibility
        rig_utils.bone.restore_visibility(armature, original_visibility)

        bpy.ops.object.mode_set(mode='POSE')
        self.report({'INFO'}, "[AetherBlend] Spring breasts generated and constraints set.")
        return {'FINISHED'}
    

class AETHER_OT_Bake_Spring_Breasts(bpy.types.Operator):
    """Bake spring breast bones for the active armature object."""
    bl_idname = "aether.bake_spring_breasts"
    bl_label = "Bake Spring Breasts"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.context.window.cursor_set('WAIT')  
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "[AetherBlend] Select an armature object")
            return {'CANCELLED'}
        
        context.scene.ab_sb_global_spring_frame = False 
        context.scene.ab_sb_global_spring = False 

        start_frame, end_frame = rig_utils.armature.get_frame_range(armature)
        reference_bones = xiv_breast_bone_r + xiv_breast_bone_l

        original_visibility = rig_utils.bone.get_bone_visibility(armature, reference_bones)

        # Select only the reference bones before baking
        rig_utils.bone.select_bones(armature, reference_bones)

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

        self.report({'INFO'}, f"[AetherBlend] Spring breasts baked from frame {start_frame} to {end_frame}.")
        return {'FINISHED'}
    

class AETHER_OT_Delete_Spring_Breasts(bpy.types.Operator):
    """Delete spring breast bones for the active armature object."""
    bl_idname = "aether.delete_spring_breasts"
    bl_label = "Delete Spring Breasts"
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

        reference_bones = xiv_breast_bone_r + xiv_breast_bone_l

        # Remove Copy Rotation constraints from reference bones
        rig_utils.bone.remove_copy_rotation_constraints(armature, reference_bones)

        bpy.ops.object.mode_set(mode='EDIT')

        # Delete the spring bone collection and all bones within
        rig_utils.bone.delete_bone_collection_and_bones(armature, sb_breast_collection)

        bpy.ops.object.mode_set(mode='POSE')
        self.report({'INFO'}, "[AetherBlend] Spring breasts deleted.")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(AETHER_OT_Generate_Spring_Breasts)
    bpy.utils.register_class(AETHER_OT_Bake_Spring_Breasts)
    bpy.utils.register_class(AETHER_OT_Delete_Spring_Breasts)

def unregister():
    bpy.utils.unregister_class(AETHER_OT_Generate_Spring_Breasts)
    bpy.utils.unregister_class(AETHER_OT_Bake_Spring_Breasts)
    bpy.utils.unregister_class(AETHER_OT_Delete_Spring_Breasts)
