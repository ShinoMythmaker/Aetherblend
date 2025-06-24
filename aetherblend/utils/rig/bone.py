import bpy

def add_constraint_copy_rotation(bone_names, armature, target_bone_names, euler_order='ZXY', use_x=True, use_y=True, use_z=True, mix_mode='AFTER', target_space='LOCAL_OWNER_ORIENT', owner_space='LOCAL_WITH_PARENT'):
        """Adds Copy Rotation constraints to specified bones in an armature."""
        bpy.ops.object.mode_set(mode='POSE')
        for index, bone_name in enumerate(bone_names):
            ref_bone = armature.pose.bones[bone_name]
            spring_bone_name = target_bone_names[index]
            
            copy_rot = ref_bone.constraints.new('COPY_ROTATION')
            copy_rot.target = armature
            copy_rot.subtarget = spring_bone_name
            copy_rot.euler_order = 'ZXY'
            copy_rot.use_x = True
            copy_rot.use_y = True
            copy_rot.use_z = True
            copy_rot.mix_mode = 'AFTER'
            copy_rot.target_space = 'LOCAL_OWNER_ORIENT'
            copy_rot.owner_space = 'LOCAL_WITH_PARENT'