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

def meta_rig_bone_chain(source_armature, target_armature, reference_bones, meta_bone_names, prefix="META_", parent_bone=None, extend_last=True, extension_factor=0.5):
    """
    Generates a meta rig bone chain with proper naming and optional extension of the last bone.
    
    Args:
        source_armature: Armature to read reference bone positions from (FFXIV rig)
        target_armature: Armature to create new bones in (Meta rig)
        reference_bones: List of reference bone names from source armature
        meta_bone_names: List of corresponding meta rig bone names
        prefix: Prefix for generated bones
        parent_bone: Optional parent bone for the first bone in chain
        extend_last: Whether to extend the last bone beyond its reference
        extension_factor: Factor to extend the last bone (relative to bone length)
    """
    if not source_armature or source_armature.type != 'ARMATURE':
        print(f"[AetherBlend] Source object '{source_armature.name}' is not an armature.")
        return []
        
    if not target_armature or target_armature.type != 'ARMATURE':
        print(f"[AetherBlend] Target object '{target_armature.name}' is not an armature.")
        return []
    
    if not bones_exist(source_armature, reference_bones):
        print(f"[AetherBlend] One or more reference bones do not exist in source armature '{source_armature.name}'.")
        return []

    # Read reference positions from source armature
    source_bones = source_armature.data.bones
    
    # Create bones in target armature
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.context.view_layer.objects.active = target_armature
    target_edit_bones = target_armature.data.edit_bones
    created_bones = []

    for index, (ref_bone, meta_name) in enumerate(zip(reference_bones, meta_bone_names)):
        new_bone_name = f"{prefix}{meta_name}"

        # Delete existing bone if it exists
        if new_bone_name in target_edit_bones:
            target_edit_bones.remove(target_edit_bones[new_bone_name])
            
        new_bone = target_edit_bones.new(new_bone_name)
        source_bone = source_bones[ref_bone]
        
        # Set bone head position from source armature
        new_bone.head = source_bone.head_local.copy()
        
        # Set bone tail position
        if index < len(reference_bones) - 1:
            # Normal bone - tail points to next reference bone's head
            next_ref_bone = reference_bones[index + 1]
            next_source_bone = source_bones[next_ref_bone]
            new_bone.tail = next_source_bone.head_local.copy()
        else:
            # Last bone - extend beyond the chain in the direction of the bone chain
            if extend_last and len(reference_bones) >= 2:
                # Calculate direction from second-to-last bone to last bone
                prev_ref_bone = reference_bones[index - 1]
                prev_source_bone = source_bones[prev_ref_bone]
                
                # Direction vector from previous bone head to current bone head
                chain_direction = (source_bone.head_local - prev_source_bone.head_local).normalized()
                
                # Extension length should be reasonable - use average bone length in chain
                if index > 0:
                    prev_bone_length = (source_bone.head_local - prev_source_bone.head_local).length
                    extension_length = prev_bone_length * extension_factor
                else:
                    extension_length = source_bone.length * extension_factor
                
                new_bone.tail = source_bone.head_local + chain_direction * extension_length
            else:
                new_bone.tail = source_bone.tail_local.copy()

        # Set parent relationship
        if parent_bone and index == 0:
            if parent_bone in target_edit_bones:
                new_bone.parent = target_edit_bones[parent_bone]
                new_bone.use_connect = False
            else:
                print(f"[AetherBlend] Parent bone '{parent_bone}' not found in target armature '{target_armature.name}'.")
        elif index > 0:
            new_bone.parent = target_edit_bones[created_bones[index - 1]]
            new_bone.use_connect = True

        created_bones.append(new_bone.name)

    bpy.ops.object.mode_set(mode='OBJECT')
    return created_bones