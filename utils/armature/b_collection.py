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


def unassign_bones(armature, bone_names, collection_name) -> None:
    """Unassigns the specified bones from the given collection in the armature."""
    original_mode = armature.mode
    target_coll = armature.data.collections.get(collection_name)
    if not target_coll:
        print(f"[AetherBlend] Collection '{collection_name}' not found in armature '{armature.name}'")
        return

    bpy.ops.object.mode_set(mode='POSE')

    for bone_name in bone_names:
        bone = armature.data.bones.get(bone_name)
        if bone:
            target_coll.unassign(bone)
        else:
            print(f"[AetherBlend] Bone '{bone_name}' not found in armature '{armature.name}'")

    bpy.ops.object.mode_set(mode=original_mode)

def assign_bones(armature, bone_names, collection_name, clear=False) -> None:
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
    """Deletes the specified collection and all bones contained within it from the armature."""
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='POSE')
    target_coll = armature.data.collections.get(collection_name)

    if len(target_coll.bones) > 0: 
        armature.data.collections.active = target_coll
        target_coll.is_visible = True
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.armature.collection_select()
        bpy.ops.armature.delete()

    armature.data.collections.remove(target_coll)

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