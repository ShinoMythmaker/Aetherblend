import bpy


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

def assign_bones(armature, bone_names, collection_name) -> None:
    """Assigns the specified bones to the given collection in the armature."""
    original_mode = armature.mode
    target_coll = armature.data.collections.get(collection_name)
    if not target_coll:
        print(f"[AetherBlend] Collection '{collection_name}' not found in armature '{armature.name}'")
        return

    bpy.ops.object.mode_set(mode='POSE')

    for bone_name in bone_names:
        bone = armature.data.bones.get(bone_name)
        if bone:
            target_coll.assign(bone)
        else:
            print(f"[AetherBlend] Bone '{bone_name}' not found in armature '{armature.name}'")

    bpy.ops.object.mode_set(mode=original_mode)

def delete_with_bones(armature: bpy.types.Armature, collection_name: str) -> None:
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

def get_pose_bones(armature, collection_name) -> dict[str, bpy.types.PoseBone]:
    """Returns a dictionary of bone names to pose bones contained within a collection"""
    target_coll = armature.data.collections.get(collection_name)
    if not target_coll:
        print(f"[AetherBlend] Collection '{collection_name}' not found in armature '{armature.name}'")
        return {}
    
    pose_bones = {b.name: armature.pose.bones.get(b.name) for b in target_coll.bones if b.name in armature.pose.bones}
    return pose_bones
