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
            copy_rot.euler_order = 'ZXY'
            copy_rot.use_x = True
            copy_rot.use_y = True
            copy_rot.use_z = True
            copy_rot.mix_mode = 'AFTER'
            copy_rot.target_space = 'LOCAL_OWNER_ORIENT'
            copy_rot.owner_space = 'LOCAL_WITH_PARENT'


def assign_bones_to_collection(armature, bone_names, collection_path):
    """Assigns specified bones to a nested collection in the armature's data (Blender 4.x+)."""
    if armature.type != 'ARMATURE':
        print(f"[AetherBlend] Object '{armature.name}' is not an armature.")
        return

    bone_collections = armature.data.collections
    current_parent = None

    # Traverse or create nested collections
    for name in collection_path.split('/'):
        existing = None
        for coll in armature.data.collections_all:
            if coll.name == name and coll.parent == current_parent:
                existing = coll
                break
        if existing:
            current_parent = existing
        else:
            new_coll = bone_collections.new(name=name, parent=current_parent)
            current_parent = new_coll

    # Assign bones to the final collection
    for bone_name in bone_names:
        bone = armature.data.bones.get(bone_name)
        if bone:
            current_parent.assign(bone)
        else:
            print(f"[AetherBlend] Bone '{bone_name}' not found in armature '{armature.name}'")


def collection_exists(armature, collection_name):
    """Checks if a specified collection exists in the armature's data."""
    if armature.type != 'ARMATURE':
        print(f"[AetherBlend] Object '{armature.name}' is not an armature.")
        return False

    for coll in armature.data.collections_all:
        if coll.name == collection_name:
            return True
    return False

def delete_bone_collection_and_bones(armature, collection_name):
    """Deletes a specified collection and all bones within it from the armature."""
    if armature.type != 'ARMATURE':
        print(f"[AetherBlend] Object '{armature.name}' is not an armature.")
        return

    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='EDIT')
    edit_bones = armature.data.edit_bones

    # Find the collection
    target_coll = None
    for coll in armature.data.collections_all:
        if coll.name == collection_name:
            target_coll = coll
            break

    if not target_coll:
        print(f"[AetherBlend] Collection '{collection_name}' not found.")
        return

    # Gather all bones recursively
    bpy.ops.object.mode_set(mode='POSE')
    bones_to_delete = set()
    def gather_bones(coll):
        bones_to_delete.update(b.name for b in coll.bones)
        for child in coll.children:
            gather_bones(child)

    gather_bones(target_coll)

    bpy.ops.object.mode_set(mode='EDIT')

    # Delete bones
    for bone_name in bones_to_delete:
        if bone_name in edit_bones:
            edit_bones.remove(edit_bones[bone_name])

    # Delete the collection
    armature.data.collections.remove(target_coll)

    bpy.ops.object.mode_set(mode='OBJECT')
    print(f"[AetherBlend] Deleted collection '{collection_name}' and its bones from armature '{armature.name}'.")



def remove_copy_rotation_constraints(armature, bone_names):
    """Removes all Copy Rotation constraints from the specified bones in the given armature."""
    bpy.ops.object.mode_set(mode='POSE')
    for bone_name in bone_names:
        pb = armature.pose.bones.get(bone_name)
        if pb:
            for con in list(pb.constraints):
                if con.type == 'COPY_ROTATION':
                    pb.constraints.remove(con)

def select_bones(armature, bone_names):
    """Selects the specified bones in the armature."""
    bpy.ops.object.mode_set(mode='POSE')
    for bone_name in bone_names:
        pb = armature.pose.bones.get(bone_name)
        if pb:
            pb.bone.select = True
        else:
            print(f"[AetherBlend] Bone '{bone_name}' not found in armature '{armature.name}'.")

def get_collectiion(armature, collection_name):
    """Returns the specified collection from the armature's data."""
    return armature.data.collections_all.get(collection_name)


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

def reset_bone_transforms(armature, bone_names):
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
    # Deselect all again (optional)
    for pb in armature.pose.bones:
        pb.bone.select = False

def bone_exists(armature, bone_name):
    """Checks if a bone exists in the armature."""
    return bone_name in armature.data.bones

def bones_exist(armature, bone_names):
    """Checks if all specified bones exist in the armature."""
    return all(bone_exists(armature, bone_name) for bone_name in bone_names)