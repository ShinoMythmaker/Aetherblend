import bpy

def add_constraint_copy_rotation(bone_names, armature, target_bone_names, euler_order='ZXY', use_x=True, use_y=True, use_z=True, mix_mode='AFTER', target_space='LOCAL_OWNER_ORIENT', owner_space='LOCAL_WITH_PARENT', overwrite=False):
        """Adds Copy Rotation constraints to specified bones in an armature."""
        bpy.ops.object.mode_set(mode='POSE')
        for index, bone_name in enumerate(bone_names):
            ref_bone = armature.pose.bones[bone_name]
            spring_bone_name = target_bone_names[index]

            # Remove all existing constraints
            if overwrite:
                for con in list(ref_bone.constraints):
                    ref_bone.constraints.remove(con)
            
            copy_rot = ref_bone.constraints.new('COPY_ROTATION')
            copy_rot.target = armature
            copy_rot.subtarget = spring_bone_name
            copy_rot.euler_order = euler_order
            copy_rot.use_x = use_x
            copy_rot.use_y = use_y
            copy_rot.use_z = use_z
            copy_rot.mix_mode = mix_mode
            copy_rot.target_space = target_space
            copy_rot.owner_space = owner_space

def remove_copy_rotation_constraints(armature, bone_names):
    """Removes all Copy Rotation constraints from the specified bones in the given armature."""
    bpy.ops.object.mode_set(mode='POSE')
    for bone_name in bone_names:
        pb = armature.pose.bones.get(bone_name)
        if pb:
            for con in list(pb.constraints):
                if con.type == 'COPY_ROTATION':
                    pb.constraints.remove(con)

def select(armature, bone_names):
    """Selects the specified bones in the armature."""
    original_mode = armature.mode

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.armature.select_all(action='DESELECT')

    for bone_name in bone_names:
        b = armature.data.edit_bones[bone_name]
        if b:
            b.select = True
            b.select_head = True
            b.select_tail = True
        else:
            print(f"[AetherBlend] Bone '{bone_name}' not found in armature '{armature.name}'.")
    
    bpy.ops.object.mode_set(mode=original_mode)

def delete_keyframes(armature, bone_names):
    """Deletes all keyframes for the specified bones in the armature."""
    action = getattr(getattr(armature.animation_data, "action", None), "fcurves", None)
    if not action:
        print(f"[AetherBlend] No action or fcurves found on armature '{armature.name}'.")
        return

    # Build all relevant data paths for each bone
    props = [
        "location",
        "rotation_euler",
        "rotation_quaternion",
        "scale"
    ]
    data_paths = set()
    for bone_name in bone_names:
        for prop in props:
            data_paths.add(f'pose.bones["{bone_name}"].{prop}')

    # Remove matching fcurves
    for fcurve in list(action):
        if fcurve.data_path in data_paths:
            action.remove(fcurve)

def reset_transforms(armature, bone_names):
    """Resets the transforms of the specified bones in the armature using Blender's operator."""
    bpy.ops.object.mode_set(mode='POSE')
    # Deselect all bones first
    for pb in armature.pose.bones:
        pb.bone.select = False
    # Select only the bones you want to reset
    for name in bone_names:
        pb = armature.pose.bones.get(name)
        if pb:
            pb.bone.select = True
    # Call the operator
    bpy.ops.pose.transforms_clear()
    # Deselect all again 
    for pb in armature.pose.bones:
        pb.bone.select = False


def exist(armature, bone_names):
    """Checks if the specified bone(s) exist in the armature."""
    return all(isinstance(b, str) and b in armature.data.bones for b in bone_names)

def get_bone_visibility(armature, bone_list):
    """Returns a dictionary of bone names and their visibility status."""
    bpy.ops.object.mode_set(mode='POSE')
    pbones = armature.pose.bones
    original_visibility = {}
    for bone_name in bone_list:
        pb = pbones.get(bone_name)
        if pb:
            original_visibility[bone_name] = pb.bone.hide
            pb.bone.hide = False
    return original_visibility

def restore_visibility(armature, original_visibility):
    """Restores the visibility of bones based on the provided dictionary."""
    bpy.ops.object.mode_set(mode='POSE')
    pbones = armature.pose.bones
    for bone_name, was_hidden in original_visibility.items():
        pb = pbones.get(bone_name)
        if pb:
            pb.bone.hide = was_hidden

