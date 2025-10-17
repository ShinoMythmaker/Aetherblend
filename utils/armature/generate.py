import bpy

from ...data import constants

def bone_on_local_axis_x(armature, bone_name, parent_bone=None, prefix="gen_", suffix=""):
    """Generates a new bone on the local +X axis of a reference bone."""
    
    if not armature or armature.type != 'ARMATURE':
        print(f"[AetherBlend] Object '{armature.name}' is not an armature.")
        return None

    bpy.ops.object.mode_set(mode='EDIT')
    edit_bones = armature.data.edit_bones

    new_bone_name = f"{prefix}{bone_name}{suffix}"

    # Delete existing bone if it exists
    if new_bone_name in edit_bones:
        edit_bones.remove(edit_bones[new_bone_name])

    ref_bone = edit_bones.get(bone_name)
    if not ref_bone:
        print(f"[AetherBlend] Reference bone '{bone_name}' not found in armature '{armature.name}'.")
        return None

    length = ref_bone.length if ref_bone.length > 0 else 1.0  # Default length if zero

    new_bone = edit_bones.new(new_bone_name)
    new_bone.head = ref_bone.head.copy()
    new_bone.tail = ref_bone.head + ref_bone.x_axis * length

    if parent_bone and parent_bone in edit_bones:
        new_bone.parent = edit_bones[parent_bone]
        new_bone.use_connect = False
    else:
        new_bone.parent = ref_bone.parent
        new_bone.use_connect = True

    created_bone_name = new_bone.name
    bpy.ops.object.mode_set(mode='POSE')
    
    return created_bone_name

def bone_chain(src: bpy.types.Armature, target: bpy.types.Armature, chain_info: constants.BoneChainInfo) -> list[str]:
    """Generate a bone chain based on info from chain_info"""
    original_mode = bpy.context.object.mode

    source_bones = src.data.bones
    reference_bones = chain_info.ffxiv_bones
    meta_bone_names = chain_info.gen_bones.keys()
    parent_bone = chain_info.parent_bone
    extend_last = chain_info.extend_last
    extension_factor = chain_info.extension_factor

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.context.view_layer.objects.active = target
    target_edit_bones = target.data.edit_bones
    created_bones = []

    for index, (ref_bone, meta_name) in enumerate(zip(reference_bones, meta_bone_names)):
        new_bone_name = meta_name

        if new_bone_name in target_edit_bones:
            target_edit_bones.remove(target_edit_bones[new_bone_name])
            
        new_bone = target_edit_bones.new(new_bone_name)
        source_bone = source_bones[ref_bone]
        
        new_bone.head = source_bone.head_local.copy()

        if index < len(reference_bones) - 1:
            next_ref_bone = reference_bones[index + 1]
            next_source_bone = source_bones[next_ref_bone]
            new_bone.tail = next_source_bone.head_local.copy()
        else:
            if extend_last and len(reference_bones) >= 2:
                prev_ref_bone = reference_bones[index - 1]
                prev_source_bone = source_bones[prev_ref_bone]
                
                chain_direction = (source_bone.head_local - prev_source_bone.head_local).normalized()
                
                if index > 0:
                    prev_bone_length = (source_bone.head_local - prev_source_bone.head_local).length
                    extension_length = prev_bone_length * extension_factor
                else:
                    extension_length = source_bone.length * extension_factor
                
                new_bone.tail = source_bone.head_local + chain_direction * extension_length
            else:
                new_bone.tail = source_bone.tail_local.copy()

        if parent_bone and index == 0:
            if parent_bone in target_edit_bones:
                new_bone.parent = target_edit_bones[parent_bone]
                new_bone.use_connect = False
            else:
                print(f"[AetherBlend] Parent bone '{parent_bone}' not found in target armature '{target.name}'.")
        elif index > 0:
            new_bone.parent = target_edit_bones[created_bones[index - 1]]
            new_bone.use_connect = True

        created_bones.append(new_bone.name)

    bpy.ops.object.mode_set(mode=original_mode)
    return created_bones