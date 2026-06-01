import bpy


def _get_collection_bone_names(armature: bpy.types.Object, collection_name: str) -> set[str]:
    """Returns the names of bones assigned to a collection, with edit-mode fallback."""
    target_coll = armature.data.collections.get(collection_name)
    if not target_coll:
        print(f"[AetherBlend] Collection '{collection_name}' not found in armature '{armature.name}'")
        return set()

    bone_names = {bone.name for bone in target_coll.bones}
    if bone_names:
        return bone_names

    if armature.mode.startswith('EDIT'):
        return {
            bone.name
            for bone in armature.data.edit_bones
            if any(coll.name == collection_name for coll in bone.collections)
        }

    return set()
def assign_bones(armature: bpy.types.Object, bone_names: list[str], collection_name: str, clear: bool = False) -> None:
    """Assigns the specified bones to the given collection in the armature."""
    target_coll = armature.data.collections.get(collection_name)

    if not target_coll:
        target_coll = armature.data.collections.new(collection_name)

    
    for bone_name in bone_names:
        bone = armature.data.bones.get(bone_name)
        if bone:
            if clear:
                bone.collections.clear()
            target_coll.assign(bone)
        else:
            print(f"[AetherBlend] Bone '{bone_name}' not found in armature '{armature.name}'")


def delete_with_bones(armature: bpy.types.Object, collection_name: str) -> None:
    """Deletes all bones assigned to a collection and removes the collection itself."""
    target_coll = armature.data.collections.get(collection_name)
    if not target_coll:
        print(f"[AetherBlend] Collection '{collection_name}' not found in armature '{armature.name}'")
        return

    bone_names = _get_collection_bone_names(armature, collection_name)
    original_mode = armature.mode

    try:
        if original_mode != 'EDIT':
            bpy.ops.object.mode_set(mode='EDIT')

        for bone_name in bone_names:
            edit_bone = armature.data.edit_bones.get(bone_name)
            if edit_bone:
                armature.data.edit_bones.remove(edit_bone)

        armature.data.collections.remove(target_coll)
    finally:
        if armature.mode != original_mode:
            bpy.ops.object.mode_set(mode=original_mode)

def get_pose_bones(armature: bpy.types.Object, collection_name: str) -> dict[str, bpy.types.PoseBone]:
    """Returns a dictionary of bone names to pose bones contained within a collection."""
    bone_names = _get_collection_bone_names(armature, collection_name)
    return {
        bone_name: armature.pose.bones.get(bone_name)
        for bone_name in bone_names
        if bone_name in armature.pose.bones
    }


def get_bones(armature: bpy.types.Object, collection_name: str) -> dict[str, bpy.types.Bone]:
    """Returns a dictionary of bone names to data bones contained within a collection."""
    bone_names = _get_collection_bone_names(armature, collection_name)
    return {
        bone_name: armature.data.bones.get(bone_name)
        for bone_name in bone_names
        if bone_name in armature.data.bones
    }