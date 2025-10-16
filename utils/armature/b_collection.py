import bpy


def unassign_bones(armature, bone_names, collection_name):
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


def assign_bones(armature, bone_names, collection_name):
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


def delete_with_bones(armature, collection_name):

    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='EDIT')
    edit_bones = armature.data.edit_bones

    target_coll = armature.data.collections.get(collection_name)

    if not target_coll:
        print(f"[AetherBlend] Collection '{collection_name}' not found.")
        return
    
    bpy.ops.object.mode_set(mode='POSE')
    bones_to_delete = set()
    def gather_bones(coll):
        bones_to_delete.update(b.name for b in coll.bones)
        for child in coll.children:
            gather_bones(child)

    gather_bones(target_coll)

    bpy.ops.object.mode_set(mode='EDIT')

    for bone_name in bones_to_delete:
        if bone_name in edit_bones:
            edit_bones.remove(edit_bones[bone_name])

    armature.data.collections.remove(target_coll)

    bpy.ops.object.mode_set(mode='OBJECT')



# it needs to return a dictionary of bone names to pose bones
def get_pose_bones(armature, collection_name) -> dict[str, bpy.types.PoseBone]:
    """Returns a dictionary of bone names to pose bones contained within a collection"""
    target_coll = armature.data.collections.get(collection_name)
    if not target_coll:
        print(f"[AetherBlend] Collection '{collection_name}' not found in armature '{armature.name}'")
        return {}

    pose_bones = {b.name: armature.pose.bones.get(b.name) for b in target_coll.bones if b.name in armature.pose.bones}
    return pose_bones