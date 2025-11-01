import bpy
import math
import mathutils

from . import bone as bone_utils
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

    valid_reference_bones = []
    valid_meta_bone_names = []
    for ref_bone, meta_name in zip(reference_bones, meta_bone_names):
        if ref_bone in source_bones:
            valid_reference_bones.append(ref_bone)
            valid_meta_bone_names.append(meta_name)
        else:
            print(f"[AetherBlend] Reference bone '{ref_bone}' not found in source armature '{src.name}'. Skipping this bone.")

    for index, (ref_bone, meta_name) in enumerate(zip(valid_reference_bones, valid_meta_bone_names)):
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
                new_parent = bone_utils.copy_to(src, target, parent_bone, parent_bone)

                new_bone.parent = target_edit_bones[new_parent]
                new_bone.use_connect = False
                print(f"New parent bone created: {new_parent}")
        elif index > 0:
            new_bone.parent = target_edit_bones[created_bones[index - 1]]
            new_bone.use_connect = True

        if chain_info.roll:
            new_bone.roll = math.radians(chain_info.roll)

        print(f"Created new bone: {new_bone.name}")
        created_bones.append(new_bone.name)

    bpy.ops.object.mode_set(mode=original_mode)
    return created_bones

def bone_extensions(target: bpy.types.Armature, extension_info: list[constants.BoneExtensionInfo]) -> list[str]:
    """Generate bone extension in target armature based on extension_info"""
    if extension_info is None or len(extension_info) == 0:
        return []

    original_mode = bpy.context.object.mode
    source_bones = target.data.bones

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.context.view_layer.objects.active = target
    target_edit_bones = target.data.edit_bones
    created_bones = []

    for ext_info in extension_info:
        ref_bone_name = ext_info.org_bone
        new_bone_name = ext_info.name

        if new_bone_name in target_edit_bones:
            target_edit_bones.remove(target_edit_bones[new_bone_name])
            
        new_bone = target_edit_bones.new(new_bone_name)
        source_bone = source_bones[ref_bone_name]
        
        start = source_bone.tail_local.copy() if ext_info.start == "tail" else source_bone.head_local.copy()

        new_bone.head = start

        direction_vector = None
        if ext_info.axis_type == "local":
            if ext_info.axis == "X":
                direction_vector = source_bone.x_axis
            elif ext_info.axis == "Y":
                direction_vector = source_bone.y_axis
            elif ext_info.axis == "Z":
                direction_vector = source_bone.z_axis
        elif ext_info.axis_type == "armature":
            armature_matrix = target.matrix_world.to_3x3().inverted()
            if ext_info.axis == "X":
                direction_vector = armature_matrix[0]
            elif ext_info.axis == "Y":
                direction_vector = armature_matrix[1]
            elif ext_info.axis == "Z":
                direction_vector = armature_matrix[2]

        if direction_vector:
            new_bone.tail = new_bone.head + direction_vector.normalized() * ext_info.extension_factors
        else:
            new_bone.tail = source_bone.tail_local.copy()

        if ext_info.is_connected:
            new_bone.parent = target_edit_bones[ref_bone_name]
            new_bone.use_connect = True
        else:
            new_bone.parent = target_edit_bones[ref_bone_name]
            new_bone.use_connect = False

        print(f"Created extension bone: {new_bone.name}")
        created_bones.append(new_bone.name)

    bpy.ops.object.mode_set(mode=original_mode)
    return created_bones


def skin_bone(src: bpy.types.Armature, target: bpy.types.Armature, skin_bone_info: constants.SkinBoneInfo) -> list[str]:
    """Generate skin bones in target armature based on skin_bone_info.
    
    Finds the vertex with the highest weight for the specified bone and creates 
    a new bone at that position with the given size factor.
    """
    original_mode = bpy.context.object.mode
    created_bones = []
    
    try:
        # Find the highest weighted vertex position for the target bone
        world_co, weight = _find_highest_weight_vertex_world_pos(skin_bone_info.org_bone, src)
        
        if world_co is None:
            print(f"[AetherBlend] No vertices found with weights for bone '{skin_bone_info.org_bone}'. Skipping skin bone creation.")
            return created_bones
        
        # Switch to edit mode and create the skin bone
        bpy.context.view_layer.objects.active = target
        bpy.ops.object.mode_set(mode='EDIT')
        target_edit_bones = target.data.edit_bones
        
        # Remove existing bone if it exists
        if skin_bone_info.name in target_edit_bones:
            target_edit_bones.remove(target_edit_bones[skin_bone_info.name])
        
        # Create new bone at the highest weighted vertex position
        new_bone = target_edit_bones.new(skin_bone_info.name)
        
        # Convert world position to armature local space
        local_co = target.matrix_world.inverted() @ world_co
        new_bone.head = local_co
        
        # Get original bone length from source armature and calculate size based on factor
        org_bone = src.data.bones.get(skin_bone_info.org_bone)
        if org_bone:
            org_bone_length = org_bone.length
        else:
            org_bone_length = 0.3  # Fallback if original bone not found
        
        # Set tail based on size factor relative to original bone length
        bone_length = org_bone_length * skin_bone_info.size_factor
        direction = mathutils.Vector((0, 0, bone_length))
        new_bone.tail = local_co + direction
        
        # # Set parent if specified
        # if skin_bone_info.parent_bone and skin_bone_info.parent_bone in target_edit_bones:
        #     new_bone.parent = target_edit_bones[skin_bone_info.parent_bone]
        #     new_bone.use_connect = False
        
        print(f"[AetherBlend] Created skin bone '{new_bone.name}' at vertex position (weight: {weight:.6f})")
        created_bones.append(new_bone.name)
        
    finally:
        bpy.ops.object.mode_set(mode=original_mode)
    
    return created_bones


def _find_highest_weight_vertex_world_pos(bone_name: str, src_armature: bpy.types.Armature) -> tuple:
    """Find the vertex with the highest weight for the given bone name across meshes with armature modifiers.
    
    Only checks meshes that have an armature modifier targeting the source armature.
    Returns (world_location, weight) or (None, 0.0) if no vertices found.
    """
    depsgraph = bpy.context.evaluated_depsgraph_get()
    
    best_weight = 0.0
    best_world_co = None
    
    for obj in bpy.data.objects:
        if obj.type != 'MESH':
            continue
        
        # Check if this mesh has an armature modifier targeting our source armature
        has_armature_modifier = False
        for modifier in obj.modifiers:
            if modifier.type == 'ARMATURE' and modifier.object == src_armature:
                has_armature_modifier = True
                break
        
        if not has_armature_modifier:
            continue
            
        vg = obj.vertex_groups.get(bone_name)
        if vg is None:
            continue
        
        # Get evaluated mesh to account for modifiers
        eval_obj = obj.evaluated_get(depsgraph)
        try:
            mesh_eval = eval_obj.to_mesh()
        except Exception:
            mesh_eval = None
        
        # Use original mesh vertices to read vertex group weights
        orig_verts = obj.data.vertices
        
        if mesh_eval is None or len(mesh_eval.vertices) != len(orig_verts):
            if mesh_eval is not None:
                eval_obj.to_mesh_clear()
            continue
        
        for v_idx, v in enumerate(orig_verts):
            # Find weight for this vertex in the target group
            weight = 0.0
            for g in v.groups:
                if g.group == vg.index:
                    weight = g.weight
                    break
            
            if weight > best_weight:
                # Get world location of evaluated vertex
                ev_co = mesh_eval.vertices[v_idx].co
                world_co = eval_obj.matrix_world @ ev_co
                best_weight = weight
                best_world_co = world_co.copy()
        
        # Clean up evaluated mesh
        eval_obj.to_mesh_clear()
    
    return (best_world_co, best_weight)