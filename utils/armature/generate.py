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

def skin_bone(src: bpy.types.Armature, target: bpy.types.Armature, skin_bone_info: constants.SkinBone) -> list[str]:
    """Generate skin bones in target armature based on skin_bone_info."""
    original_mode = bpy.context.object.mode
    created_bones = []
    
    try:
        world_co, weight = _find_highest_weight_vertex_world_pos(skin_bone_info.org_bone, src)
        
        if world_co is None:
            print(f"[AetherBlend] No vertices found with weights for bone '{skin_bone_info.org_bone}'. Skipping skin bone creation.")
            return created_bones
        
        bpy.context.view_layer.objects.active = target
        bpy.ops.object.mode_set(mode='EDIT')
        target_edit_bones = target.data.edit_bones
        
        if skin_bone_info.name in target_edit_bones:
            target_edit_bones.remove(target_edit_bones[skin_bone_info.name])
        
        new_bone = target_edit_bones.new(skin_bone_info.name)
        
        local_co = target.matrix_world.inverted() @ world_co
        new_bone.head = local_co
        
        org_bone = src.data.bones.get(skin_bone_info.org_bone)
        if org_bone:
            org_bone_length = org_bone.length
        else:
            org_bone_length = 0.3 
        
        bone_length = org_bone_length * skin_bone_info.size_factor
        direction = mathutils.Vector((0, 0, bone_length))
        new_bone.tail = local_co + direction
        
        print(f"[AetherBlend] Created skin bone '{new_bone.name}' at vertex position (weight: {weight:.6f})")
        created_bones.append(new_bone.name)
        
    finally:
        bpy.ops.object.mode_set(mode=original_mode)
    
    return created_bones

def _find_highest_weight_vertex_world_pos(bone_name: str, src_armature: bpy.types.Armature) -> tuple:
    """Find the vertex with the highest weight for the given bone name across meshes with armature modifiers."""
    depsgraph = bpy.context.evaluated_depsgraph_get()
    
    best_weight = 0.0
    best_world_co = None
    
    for obj in bpy.data.objects:
        if obj.type != 'MESH':
            continue
        
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
        
        eval_obj = obj.evaluated_get(depsgraph)
        try:
            mesh_eval = eval_obj.to_mesh()
        except Exception:
            mesh_eval = None
        
        orig_verts = obj.data.vertices
        
        if mesh_eval is None or len(mesh_eval.vertices) != len(orig_verts):
            if mesh_eval is not None:
                eval_obj.to_mesh_clear()
            continue
        
        for v_idx, v in enumerate(orig_verts):
            weight = 0.0
            for g in v.groups:
                if g.group == vg.index:
                    weight = g.weight
                    break
            
            if weight > best_weight:
                ev_co = mesh_eval.vertices[v_idx].co
                world_co = eval_obj.matrix_world @ ev_co
                best_weight = weight
                best_world_co = world_co.copy()
        
        eval_obj.to_mesh_clear()
    
    return (best_world_co, best_weight)

def bridge_bones(armature: bpy.types.Armature, bridge_info: constants.BridgeBone) -> list[str]:
    """Creates a chain of bones bridging from bone_a to bone_b with curved path."""
    original_mode = bpy.context.object.mode
    created_bones = []
    
    def _get_next_bone_name(base_name: str, start_index: int = 1) -> str:
        """Generate the next available bone name with proper numbering."""
        import re
        match = re.match(r'^(.+)\.(\d+)$', base_name)
        
        if match:
            name_part = match.group(1)
            current_num = int(match.group(2))
            next_num = current_num + start_index
            return f"{name_part}.{next_num:03d}"
        else:
            return f"{base_name}.{start_index:03d}"
    
    try:
        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='EDIT')
        edit_bones = armature.data.edit_bones

        bone_a = edit_bones.get(bridge_info.bone_a)
        bone_b = edit_bones.get(bridge_info.bone_b)

        if not bone_a or not bone_b:
            print(f"[AetherBlend] One or both bones '{bridge_info.bone_a}' and '{bridge_info.bone_b}' not found in armature '{armature.name}'.")
            return created_bones

        original_bone_a_head = bone_a.head.copy()
        original_bone_b_head = bone_b.head.copy()
        
        start_pos = original_bone_a_head
        end_pos = original_bone_b_head
        
        offset_vector = mathutils.Vector(bridge_info.offset_factor)
        

        total_bones = bridge_info.segments + 1

        positions = []
        total_distance = (end_pos - start_pos).length
        segment_length = total_distance / total_bones
        direction = (end_pos - start_pos).normalized()
        
        for i in range(total_bones + 1):  
            t = i / total_bones 
            
            linear_pos = start_pos + (direction * segment_length * i)
            
            curve_factor = math.sin(math.pi * t)
            final_pos = linear_pos + (offset_vector * curve_factor)
            
            positions.append(final_pos)

        current_parent = bone_a
        for i in range(bridge_info.segments):
            bone_name = _get_next_bone_name(bridge_info.bone_a, i + 1)
            
            if bone_name in edit_bones:
                edit_bones.remove(edit_bones[bone_name])
            
            new_bone = edit_bones.new(bone_name)
            new_bone.head = positions[i+1].copy()  
            new_bone.tail = positions[i + 2].copy()  
            
            new_bone.parent = current_parent
            new_bone.use_connect = True
            
            created_bones.append(new_bone.name)
            current_parent = new_bone
        
        if bridge_info.segments > 0:
            bone_a.tail = positions[1].copy()
            
            if bridge_info.connected:
                bone_b.parent = current_parent
                bone_b.use_connect = True
            
        else:
            bone_a.tail = original_bone_b_head.copy()
            
            if bridge_info.connected:
                bone_b.parent = bone_a
                bone_b.use_connect = True

        print(f"[AetherBlend] Created bridge with {bridge_info.segments} segments between '{bridge_info.bone_a}' and '{bridge_info.bone_b}'")
        if created_bones:
            print(f"[AetherBlend] Intermediate bones created: {created_bones}")

    finally:
        bpy.ops.object.mode_set(mode=original_mode)
    
    return created_bones

def eye_bone(armature: bpy.types.Armature, outer_bones: list[str], name: str, length: float) -> list[str]:
    """Creates an eye bone by finding the center between given bones and extending in Y direction."""
    original_mode = bpy.context.object.mode
    created_bone_name = ""
    
    try:
        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='EDIT')
        edit_bones = armature.data.edit_bones

        valid_bones = []
        for bone_name in outer_bones:
            bone = edit_bones.get(bone_name)
            if bone:
                valid_bones.append(bone)
            else:
                print(f"[AetherBlend] Warning: Bone '{bone_name}' not found in armature '{armature.name}'.")
        
        if not valid_bones:
            print(f"[AetherBlend] Error: No valid bones found from list {outer_bones}")
            return ""
        
        total_position = mathutils.Vector((0.0, 0.0, 0.0))
        for bone in valid_bones:
            total_position += bone.head
        
        center_position = total_position / len(valid_bones)
        
        if name in edit_bones:
            edit_bones.remove(edit_bones[name])
        
        new_bone = edit_bones.new(name)
        
        new_bone.tail = center_position.copy()
        new_bone.head = center_position + mathutils.Vector((0.0, length, 0.0))
        
        created_bone_name = new_bone.name
        print(f"[AetherBlend] Created eye bone '{new_bone.name}' from {len(valid_bones)} bones, center at {center_position}, length {length}")
    
    finally:
        bpy.ops.object.mode_set(mode=original_mode)

    return [created_bone_name]