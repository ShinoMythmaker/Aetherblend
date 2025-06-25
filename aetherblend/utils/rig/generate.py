import bpy
from .bone import bones_exist

def bone_chain(armature, reference_bone_names, prefix="gen_", suffix="", parent_bone=None):
    """Generates a chain of bones based on reference bone names."""

    if not armature or armature.type != 'ARMATURE':
        print(f"[AetherBlend] Object '{armature.name}' is not an armature.")
        return []
    
    if not bones_exist(armature, reference_bone_names):
        print(f"[AetherBlend] One or more reference bones do not exist in armature '{armature.name}'.")
        return []

    bpy.ops.object.mode_set(mode='EDIT')
    edit_bones = armature.data.edit_bones
    bone_chain = []

    for index, bone_name in enumerate(reference_bone_names[:-1]):
        new_bone_name = f"{prefix}{bone_name}{suffix}"

        # Delete existing bone if it exists
        if new_bone_name in edit_bones:
            edit_bones.remove(edit_bones[new_bone_name])
            
        new_bone = edit_bones.new(new_bone_name)
        new_bone.head = edit_bones[bone_name].head
        if index < len(reference_bone_names) - 2:  # Prevent out of range index for the last bone
            next_bone_name = reference_bone_names[index + 1]
            new_bone.tail = edit_bones[next_bone_name].head
        else:
            # Set the tail of the last bone using the last reference bone's head
            new_bone.tail = edit_bones[reference_bone_names[-1]].head

        if parent_bone and index == 0:
            if parent_bone in edit_bones:
                new_bone.parent = edit_bones[parent_bone]
                new_bone.use_connect = False
            else:
                print(f"[AetherBlend] Parent bone '{parent_bone}' not found in armature '{armature.name}'.")
        elif index > 0:
            new_bone.parent = edit_bones[bone_chain[index - 1]]
            new_bone.use_connect = True

        bone_chain.append(new_bone.name)

    bpy.ops.object.mode_set(mode='POSE')
    return bone_chain