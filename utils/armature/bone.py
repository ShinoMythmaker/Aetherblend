import bpy

def add_constraint_track_to_after_original(armature: bpy.types.Armature, bone_map: dict[str, str]) -> list[bpy.types.Constraint]:
    """Adds a track to constraint to a bone in an armature, applied after the original rotation."""
    original_mode = armature.mode
    constraints = []
    for bone_name, target_bone_name in bone_map.items():
        bpy.ops.object.mode_set(mode='EDIT')
        edit_bones = armature.data.edit_bones


        base_bone = edit_bones.get(bone_name)
        base_bone_parent = edit_bones.get(base_bone.parent.name)
        target_bone = edit_bones.get(target_bone_name)

        if not base_bone or not target_bone:
            print(f"[AetherBlend] Bone '{bone_name}' or target bone '{target_bone_name}' not found in armature '{armature.name}'.")
            bpy.ops.object.mode_set(mode=original_mode)
            return

        new_bone_name = f"ORG_{bone_name}_to_{target_bone_name}"
        new_bone = edit_bones.new(new_bone_name)
        new_bone.head = base_bone.head.copy()
        new_bone.tail = target_bone.head.copy()
        new_bone.roll = 0.0
        new_bone.parent = base_bone_parent

        org_collection = armature.data.collections.get("ORG")
        if org_collection:
            org_collection.assign(new_bone)

        bpy.ops.object.mode_set(mode='POSE')
        pb = armature.pose.bones.get(bone_name)
        new_pb = armature.pose.bones.get(new_bone_name)

        if pb and new_pb:
            track_to = add_constraint_track_to(
                armature, {new_bone_name: [target_bone_name]}, overwrite=False)
            child_of = add_constraint_child_of(
                armature, {bone_name: [new_bone_name]}, overwrite=False, inverse=True, location=False, rotation=True, scale=False)
        else:
            print(f"[AetherBlend] Pose bone '{bone_name}' or new pose bone '{new_bone_name}' not found in armature '{armature.name}'.")

        constraints.append(track_to)
        constraints.append(child_of)

    bpy.ops.object.mode_set(mode=original_mode)
    return constraints


def add_constraint_track_to(armature: bpy.types.Armature, bone_map: dict[str, list[str]], overwrite: bool = False) -> list[bpy.types.Constraint]:
    """Adds Track To constraints to specified bones in an armature."""
    original_mode = armature.mode

    bpy.ops.object.mode_set(mode='POSE')
    constraints = []

    for bone_name, target_bone_names in bone_map.items():
        for target_bone_name in target_bone_names:
            bone = armature.pose.bones[bone_name]

            # Remove all existing constraints
            if overwrite:
                for con in list(bone.constraints):
                    bone.constraints.remove(con)

            track_to = bone.constraints.new('TRACK_TO')
            track_to.target = armature
            track_to.subtarget = target_bone_name
            track_to.track_axis = "TRACK_Y"
            track_to.up_axis = "UP_X"
            track_to.target_space = 'POSE'
            track_to.owner_space = 'POSE'
            track_to.name = f"AetherBlend_{track_to.name}"
            constraints.append(track_to)

    bpy.ops.object.mode_set(mode=original_mode)
    return constraints



def add_constraint_copy_rotation(armature: bpy.types.Armature, bone_map: dict[str, list[str]], overwrite: bool = False) -> list[bpy.types.Constraint]:
    """Adds Copy Rotation constraints to specified bones in an armature."""
    original_mode = armature.mode

    bpy.ops.object.mode_set(mode='POSE')
    constraints = []

    for bone_name, target_bone_names in bone_map.items():
        for target_bone_name in target_bone_names:
            bone = armature.pose.bones[bone_name]

            # Remove all existing constraints
            if overwrite:
                for con in list(bone.constraints):
                    bone.constraints.remove(con)

            copy_rot = bone.constraints.new('COPY_ROTATION')
            copy_rot.target = armature
            copy_rot.subtarget = target_bone_name
            copy_rot.euler_order = 'ZXY'
            copy_rot.use_x = True
            copy_rot.use_y = True
            copy_rot.use_z = True
            copy_rot.mix_mode = 'AFTER'
            copy_rot.target_space = 'LOCAL_OWNER_ORIENT'
            copy_rot.owner_space = 'LOCAL_WITH_PARENT'

            copy_rot.name = f"AetherBlend_{copy_rot.name}"
            constraints.append(copy_rot)

    bpy.ops.object.mode_set(mode=original_mode)
    return constraints

def add_constraint_copy_location(armature: bpy.types.Armature, bone_map: dict[str, list[str]], overwrite: bool = False) -> list[bpy.types.Constraint]:
    """Adds Copy Location constraints to specified bones in an armature."""
    original_mode = armature.mode

    bpy.ops.object.mode_set(mode='POSE')
    constraints = []

    for bone_name, target_bone_names in bone_map.items():
        for target_bone_name in target_bone_names:
            bone = armature.pose.bones[bone_name]

            # Remove all existing constraints
            if overwrite:
                for con in list(bone.constraints):
                    bone.constraints.remove(con)

            copy_loc = bone.constraints.new('COPY_LOCATION')
            copy_loc.target = armature
            copy_loc.subtarget = target_bone_name
            copy_loc.use_x = True
            copy_loc.use_y = True
            copy_loc.use_z = True
            copy_loc.target_space = 'POSE'
            copy_loc.owner_space = 'POSE'

            copy_loc.name = f"AetherBlend_{copy_loc.name}"
            constraints.append(copy_loc)

    bpy.ops.object.mode_set(mode=original_mode)
    return constraints

def add_constraint_child_of(armature: bpy.types.Armature, bone_map: dict[str, list[str]], overwrite: bool = False, inverse: bool = False, location: bool = True, rotation: bool = True, scale: bool = True) -> list[bpy.types.Constraint]:
    """Adds Child Of constraints to specified bones in an armature."""
    original_mode = armature.mode

    bpy.ops.object.mode_set(mode='POSE')
    constraints = []

    for bone_name, target_bone_names in bone_map.items():
        for target_bone_name in target_bone_names:
            bone = armature.pose.bones[bone_name]

            # Remove all existing constraints
            if overwrite:
                for con in list(bone.constraints):
                    bone.constraints.remove(con)

            child_of = bone.constraints.new('CHILD_OF')
            child_of.target = armature
            child_of.subtarget = target_bone_name
            child_of.name = f"AetherBlend_{child_of.name}"

            if not location:
                child_of.use_location_x = False
                child_of.use_location_y = False
                child_of.use_location_z = False
            
            if not rotation:
                child_of.use_rotation_x = False
                child_of.use_rotation_y = False
                child_of.use_rotation_z = False
            
            if not scale:
                child_of.use_scale_x = False
                child_of.use_scale_y = False
                child_of.use_scale_z = False


            if inverse:
                bpy.context.active_object.data.bones.active = bone.bone

                bpy.ops.constraint.childof_set_inverse(constraint=child_of.name, owner='BONE')

            constraints.append(child_of)

    bpy.ops.object.mode_set(mode=original_mode)
    return constraints

def remove_copy_rotation_constraints(armature, bone_names):
    """Removes all Copy Rotation constraints from the specified bones in the given armature."""
    bpy.ops.object.mode_set(mode='POSE')
    for bone_name in bone_names:
        pb = armature.pose.bones.get(bone_name)
        if pb:
            for con in list(pb.constraints):
                if con.type == 'COPY_ROTATION':
                    pb.constraints.remove(con)

def remove_constraint_by_name_contains(armature: bpy.types.Armature, bone_name: str, substring: str) -> None:
    """Removes a specific constraint that contains name from a given bone in the armature."""
    original_mode = armature.mode

    bpy.ops.object.mode_set(mode='POSE')
    pb = armature.pose.bones.get(bone_name)
    if pb:
        for con in list(pb.constraints):
            if substring in con.name:
                pb.constraints.remove(con)
    else:
        print(f"[AetherBlend] Bone '{bone_name}' not found in armature '{armature.name}'")

    bpy.ops.object.mode_set(mode=original_mode)

def select_edit(armature, bone_names):
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

def copy_to(src_armature: bpy.types.Armature, target_armature: bpy.types.Armature, bone_name: str, new_bone_name: str) -> str | None:
    """Copy a bone from src_armature to target_armature."""
    
    src_bones = src_armature.data.bones
    target_edit_bones = target_armature.data.edit_bones
        
    ref_bone = src_bones.get(bone_name)
    if not ref_bone:
        print(f"[AetherBlend] Reference bone '{bone_name}' not found in armature '{src_armature.name}'.")
        return None
    
    bone_copy = target_edit_bones.new(new_bone_name)
    bone_copy.head = ref_bone.head_local.copy()
    bone_copy.tail = ref_bone.tail_local.copy()
    bone_copy.roll = get_roll(ref_bone)

    return bone_copy.name

def get_roll(bone: bpy.types.Bone) -> float:
    """Gets the roll of a data Bone"""
    axis, roll = bone.AxisRollFromMatrix(bone.matrix, axis=bone.y_axis)
    return roll

def set_parent(armature: bpy.types.Armature, bone_name: str, parent_bone_name: str) -> None:
    """Sets the parent of a bone in the armature."""
    bpy.ops.object.mode_set(mode='EDIT')
    edit_bones = armature.data.edit_bones
    bone = edit_bones.get(bone_name)
    parent_bone = edit_bones.get(parent_bone_name)
    if bone and parent_bone:
        bone.parent = parent_bone
    else:
        if not bone:
            print(f"[AetherBlend] Bone '{bone_name}' not found in armature '{armature.name}'.")
        if not parent_bone:
            print(f"[AetherBlend] Parent bone '{parent_bone_name}' not found in armature '{armature.name}'.")