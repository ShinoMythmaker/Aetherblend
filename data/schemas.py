from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import math
import mathutils

import bpy

from .. import utils

@dataclass(frozen=True)
class MetaRigCollectionInfo:
    name: str
    color_type: str
    row_index: int
    title: str

@dataclass(frozen=True)
class RigifySettings:
    bone_name: str | None  = None
    rigify_type: str | None  = None
    fk_coll: str | None  = None
    tweak_coll: str | None  = None
    copy_rot_axes: dict[str, bool] | None = None
    make_extra_ik_control: bool | None = None
    super_copy_widget_type: str | None = None
    pivot_pos: int | None = None
    secondary_layer_extra: str | None  = None
    skin_chain_pivot_pos: int | None  = None
    skin_chain_falloff: list[float] | None = None
    skin_chain_falloff_length: bool | None = None
    skin_chain_falloff_spherical: list[bool] | None  = None
    skin_control_orientation_bone: str | None  = None

@dataclass(frozen=True)
class ExtensionBone:
    name: str 
    bone_a: str 
    size_factor: float = 1.0
    axis_type: str = "local"# e.g., "global", "local", "armature"
    axis: str  = "Y" # e.g., "X", "Y", "Z"
    start: str = "tail" # e.g., "head", "tail"
    is_connected: bool = False
    parent: str | None = None
    roll: float = 0.0

    def generate(self, ref: bpy.types.Armature, target: bpy.types.Armature, data: dict | None = None) -> list[str] | None:
        """Generates the ExtensionBone extending from bone_a in the target armature."""
        if not ref or not target:
            print(f"[AetherBlend] Invalid armatures provided for ExtensionBone '{self.name}'.")
            return None
        
        ref_bones = ref.data.bones
        bone_a_ref = ref_bones.get(self.bone_a)

        if not bone_a_ref:
            print(f"[AetherBlend] Reference bone '{self.bone_a}' not found in either armature for ExtensionBone '{self.name}'.")
            return None
        
        if self.start == "tail":
            start_pos = bone_a_ref.tail_local.copy()
        else:  # "head"
            start_pos = bone_a_ref.head_local.copy()

        direction_vector = None
        if self.axis_type == "local":
            local_bone_matrix = bone_a_ref.matrix_local.to_3x3().inverted()
            if self.axis == "X":
                direction_vector = local_bone_matrix[0]
            elif self.axis == "Y":
                direction_vector = local_bone_matrix[1] 
            elif self.axis == "Z":
                direction_vector = local_bone_matrix[2]
        elif self.axis_type == "armature":
            armature_matrix = target.matrix_world.to_3x3().inverted()
            if self.axis == "X":
                direction_vector = armature_matrix[0]
            elif self.axis == "Y":
                direction_vector = armature_matrix[1]
            elif self.axis == "Z":
                direction_vector = armature_matrix[2]
        elif self.axis_type == "global":
            if self.axis == "X":
                direction_vector = mathutils.Vector((1.0, 0.0, 0.0))
            elif self.axis == "Y":
                direction_vector = mathutils.Vector((0.0, 1.0, 0.0))
            elif self.axis == "Z":
                direction_vector = mathutils.Vector((0.0, 0.0, 1.0))
        
        if not direction_vector:
            print(f"[AetherBlend] Invalid axis configuration for ExtensionBone '{self.name}': axis_type='{self.axis_type}', axis='{self.axis}'.")
            return None
        
        ref_bone_length = bone_a_ref.length if bone_a_ref.length > 0 else 1.0
        extension_length = ref_bone_length * self.size_factor
        tail_pos = start_pos + direction_vector.normalized() * extension_length

        original_mode = bpy.context.object.mode
        bpy.context.view_layer.objects.active = target
        bpy.ops.object.mode_set(mode='EDIT')
        
        try:
            target_edit_bones = target.data.edit_bones
            
            if self.name in target_edit_bones:
                target_edit_bones.remove(target_edit_bones[self.name])

            new_bone = target_edit_bones.new(self.name)
            new_bone.head = start_pos
            new_bone.tail = tail_pos
            new_bone.roll = math.radians(self.roll) if self.roll != 0.0 else 0.0

            if self.parent:
                if isinstance(self.parent, list):
                    for bone_name in self.parent:
                        parent_bone = target_edit_bones.get(bone_name)
                        if parent_bone and parent_bone != new_bone:
                            break
                else :
                    parent_bone = target_edit_bones.get(self.parent)

                if parent_bone:
                    new_bone.parent = parent_bone
                    new_bone.use_connect = self.is_connected
                else:
                    print(f"[AetherBlend] Warning: Parent bone '{self.parent}' not found for ExtensionBone '{self.name}'.")
            
            created_name = new_bone.name  
            return [created_name]
            
        finally:
            bpy.ops.object.mode_set(mode=original_mode)

@dataclass(frozen=True)
class SkinBone:
    name: str
    bone_a: str
    parent: str | None = None
    size_factor: float = 1.0
    mesh_restriction: str | None = None

    def generate(self, ref: bpy.types.Armature, target: bpy.types.Armature, data: dict | None = None) -> list[str] | None:
        """Generates the SkinBone at the highest weighted vertex position for bone_a."""
        if not ref or not target:
            print(f"[AetherBlend] Invalid armatures provided for SkinBone '{self.name}'.")
            return None
        
        skin = None
        if data is not None:
            try:
                data_item = data.get(self.mesh_restriction)

                if data_item.type == 'MESH':
                    skin = data_item
            except Exception:
                pass
                
        ref_bones = ref.data.bones
        bone_a_ref = ref_bones.get(self.bone_a)

        if not bone_a_ref:
            print(f"[AetherBlend] Reference bone '{self.bone_a}' not found in source armature for SkinBone '{self.name}'.")
            return None
        
        world_co, weight = self._find_highest_weight_vertex_world_pos(self.bone_a, ref, mesh=skin)
        
        if world_co is None:
            print(f"[AetherBlend] No vertices found with weights for bone '{self.bone_a}'. Skipping SkinBone '{self.name}'.")
            return None     
        
        ref_bone_length = bone_a_ref.length if bone_a_ref.length > 0 else 0.3
    
        bone_length = ref_bone_length * self.size_factor
        
        original_mode = bpy.context.object.mode
        bpy.context.view_layer.objects.active = target
        bpy.ops.object.mode_set(mode='EDIT')
        
        try:
            target_edit_bones = target.data.edit_bones
            
            if self.name in target_edit_bones:
                target_edit_bones.remove(target_edit_bones[self.name])
            
            new_bone = target_edit_bones.new(self.name)
            
            local_co = target.matrix_world.inverted() @ world_co
            new_bone.head = local_co
            
            direction = mathutils.Vector((0.0, 0.0, bone_length))
            new_bone.tail = local_co + direction
            
            if self.parent:
                parent_bone = target_edit_bones.get(self.parent)
                if parent_bone:
                    new_bone.parent = parent_bone
                    new_bone.use_connect = False
                else:
                    print(f"[AetherBlend] Warning: Parent bone '{self.parent}' not found for SkinBone '{self.name}'.")
            
            created_name = new_bone.name
            return [created_name]
            
        finally:
            bpy.ops.object.mode_set(mode=original_mode)
    
    def _find_highest_weight_vertex_world_pos(self, bone_name: str, src_armature: bpy.types.Armature, mesh = None) -> tuple:
        """Optimized function to find the vertex with highest weight for given bone, accounting for modifiers and shapekeys."""
        depsgraph = bpy.context.evaluated_depsgraph_get()
        
        best_weight = 0.0
        best_world_co = None

        if mesh is not None:
            object_pool = [mesh]
        else:
            object_pool = [obj for obj in bpy.data.objects if obj.type == 'MESH']
            
        candidate_objects = []
        
        for obj in object_pool:
            if obj is None:
                continue
            if obj.type != 'MESH':
                continue
            
            has_armature_mod = False
            for modifier in obj.modifiers:
                if modifier.type == 'ARMATURE' and modifier.object == src_armature:
                    has_armature_mod = True
                    break
            
            if not has_armature_mod:
                continue
                
            vg = obj.vertex_groups.get(bone_name)
            if vg is not None:
                candidate_objects.append((obj, vg))
        
        if not candidate_objects:
            return (None, 0.0)
        
        for obj, vertex_group in candidate_objects:
            armature_mod = None
            for mod in obj.modifiers:
                if mod.type == 'ARMATURE' and mod.object == src_armature:
                    armature_mod = mod
                    break
            
            if not armature_mod:
                continue
            
            eval_obj = obj.evaluated_get(depsgraph)
            
            try:
                mesh_eval = eval_obj.to_mesh()
            except Exception as e:
                continue
            
            if mesh_eval is None:
                continue
            
            orig_verts = obj.data.vertices
            vg_index = vertex_group.index
            
            if len(mesh_eval.vertices) != len(orig_verts):
                eval_obj.to_mesh_clear()
                continue
            
            for v_idx, vertex in enumerate(orig_verts):
                for group in vertex.groups:
                    if group.group == vg_index and group.weight > best_weight:
                        eval_local_co = mesh_eval.vertices[v_idx].co.copy()
                        world_co = obj.matrix_world @ eval_local_co
                        
                        best_weight = group.weight
                        best_world_co = world_co.copy()
                        break
            
            eval_obj.to_mesh_clear()
        
        return (best_world_co, best_weight)

@dataclass(frozen=True)
class ConnectBone:
    name: str
    bone_a: str
    bone_b: str 
    parent: str | None = None
    is_connected: bool = False
    roll: float = 0.0

    def generate(self, ref: bpy.types.Armature, target: bpy.types.Armature, data: dict | None = None) -> list[str] | None:
        """Generates the ConnectBone from bone_a.head to bone_b.head in target armature."""
        if not ref or not target:
            print(f"[AetherBlend] Invalid armatures provided for ConnectBone '{self.name}'.")
            return None
            
        ref_bones = ref.data.bones
        bone_a_ref = ref_bones.get(self.bone_a)
        bone_b_ref = ref_bones.get(self.bone_b)

        if not bone_a_ref or not bone_b_ref:
            print(f"[AetherBlend] Cannot create ConnectBone '{self.name}': reference bones '{self.bone_a}' or '{self.bone_b}' not found in source armature.")
            return None
        
        head_pos = bone_a_ref.head_local.copy()
        tail_pos = bone_b_ref.head_local.copy()
        
        original_mode = bpy.context.object.mode
        bpy.context.view_layer.objects.active = target
        bpy.ops.object.mode_set(mode='EDIT')
        
        try:
            target_edit_bones = target.data.edit_bones
            
            if self.name in target_edit_bones:
                target_edit_bones.remove(target_edit_bones[self.name])

            new_bone = target_edit_bones.new(self.name)
            new_bone.head = head_pos
            new_bone.tail = tail_pos
            new_bone.roll = math.radians(self.roll) if self.roll != 0.0 else 0.0
            
            if self.parent:
                parent_bone = target_edit_bones.get(self.parent)
                if parent_bone:
                    new_bone.parent = parent_bone
                    new_bone.use_connect = self.is_connected
                else:
                    print(f"[AetherBlend] Warning: Parent bone '{self.parent}' not found for ConnectBone '{self.name}'.")
            
            created_name = new_bone.name  
            return [created_name]
            
        finally:
            bpy.ops.object.mode_set(mode=original_mode)

@dataclass(frozen=True)
class BridgeBone:
    name: str
    bone_a: str
    bone_b: str
    offset_factor: mathutils.Vector = mathutils.Vector((0.0, 0.0, 0.0))
    is_connected: bool = True #Unlike ExtensionBone and SkinBone, BridgeBones is_connect defines weither the last bone is connected to bone_b
    parent : str | None = None

    def generate(self, ref: bpy.types.Armature, target: bpy.types.Armature, data: dict | None = None) -> list[str] | None:
        """Generates the BridgeBone from bone_a to bone_b with curved offset in target armature."""
        if not ref or not target:
            print(f"[AetherBlend] Invalid armatures provided for BridgeBone '{self.name}'.")
            return None
            
        ref_bones = ref.data.bones
        bone_a_ref = ref_bones.get(self.bone_a)
        bone_b_ref = ref_bones.get(self.bone_b)

        if not bone_a_ref or not bone_b_ref:
            print(f"[AetherBlend] Cannot create BridgeBone '{self.name}': reference bones '{self.bone_a}' or '{self.bone_b}' not found in source armature.")
            return None
        
        start_pos = bone_a_ref.head_local.copy()
        end_pos = bone_b_ref.head_local.copy()
        
        midpoint = (start_pos + end_pos) / 2.0
        curve_factor = math.sin(math.pi * 0.5)  # Maximum curve at t=0.5
        bridge_head = midpoint + (self.offset_factor * curve_factor)
        
        original_mode = bpy.context.object.mode
        bpy.context.view_layer.objects.active = target
        bpy.ops.object.mode_set(mode='EDIT')
        
        try:
            target_edit_bones = target.data.edit_bones
            
            if self.name in target_edit_bones:
                target_edit_bones.remove(target_edit_bones[self.name])

            new_bone = target_edit_bones.new(self.name)
            new_bone.head = bridge_head
            new_bone.tail = end_pos
            
            bone_a_target = target_edit_bones.get(self.bone_a)
            if bone_a_target:
                bone_a_target.tail = bridge_head
                new_bone.parent = bone_a_target
                new_bone.use_connect = True
                
                # Set bone_a's parent if parent parameter is provided
                if self.parent:
                    parent_bone = target_edit_bones.get(self.parent)
                    if parent_bone:
                        bone_a_target.parent = parent_bone
                        bone_a_target.use_connect = False
                    else:
                        print(f"[AetherBlend] Warning: Parent bone '{self.parent}' not found for bone_a '{self.bone_a}' in BridgeBone '{self.name}'.")
            else:
                print(f"[AetherBlend] Warning: Parent bone '{self.bone_a}' not found in target armature for BridgeBone '{self.name}'.")
            
            if self.is_connected:
                bone_b_target = target_edit_bones.get(self.bone_b)
                if bone_b_target:
                    bone_b_target.parent = new_bone
                    bone_b_target.use_connect = True
                else:
                    print(f"[AetherBlend] Warning: Target bone '{self.bone_b}' not found for connection in BridgeBone '{self.name}'.")
            
            created_name = new_bone.name  
            return [created_name]
            
        finally:
            bpy.ops.object.mode_set(mode=original_mode)

@dataclass(frozen=True)
class TrackToBone:
    origin_name: str 
    target_name: str
    custom_space: str
    parent_name: str | None

@dataclass(frozen=True)
class EyeBone:
    name: str
    ref_bones: list[str]
    size_factor: float = 1.0
    parent: str | None = None

    def generate(self, ref: bpy.types.Armature, target: bpy.types.Armature, data: dict | None = None) -> list[str] | None:
        """Generates the EyeBone at the center position of reference bones in target armature."""
        if not ref or not target:
            print(f"[AetherBlend] Invalid armatures provided for EyeBone '{self.name}'.")
            return None
        
        ref_bones_data = ref.data.bones
        valid_ref_bones = []
        
        for bone_name in self.ref_bones:
            bone_ref = ref_bones_data.get(bone_name)
            if bone_ref:
                valid_ref_bones.append(bone_ref)
            else:
                print(f"[AetherBlend] Warning: Reference bone '{bone_name}' not found in source armature for EyeBone '{self.name}'.")
        
        if not valid_ref_bones:
            print(f"[AetherBlend] Error: No valid reference bones found for EyeBone '{self.name}'. Cannot create eye bone.")
            return None
        
        total_position = mathutils.Vector((0.0, 0.0, 0.0))
        total_length = 0.0
        for bone_ref in valid_ref_bones:
            total_position += bone_ref.head_local
            total_length += bone_ref.length
        
        center_position = total_position / len(valid_ref_bones)
        avg_length = total_length / len(valid_ref_bones) if total_length > 0 else 0.3
        eye_bone_length = avg_length * self.size_factor
        
        original_mode = bpy.context.object.mode
        bpy.context.view_layer.objects.active = target
        bpy.ops.object.mode_set(mode='EDIT')
        
        try:
            target_edit_bones = target.data.edit_bones
            
            if self.name in target_edit_bones:
                target_edit_bones.remove(target_edit_bones[self.name])
            
            new_bone = target_edit_bones.new(self.name)
            
            new_bone.tail = center_position.copy()
            new_bone.head = center_position + mathutils.Vector((0.0, eye_bone_length, 0.0))
            
            if self.parent:
                parent_bone = target_edit_bones.get(self.parent)
                if parent_bone:
                    new_bone.parent = parent_bone
                    new_bone.use_connect = False
                else:
                    print(f"[AetherBlend] Warning: Parent bone '{self.parent}' not found for EyeBone '{self.name}'.")
            
            created_name = new_bone.name
            print(f"[AetherBlend] Created eye bone '{created_name}' from {len(valid_ref_bones)} reference bones, center at {center_position}, length {eye_bone_length:.3f}")
            return [created_name]
            
        finally:
            bpy.ops.object.mode_set(mode=original_mode)
        
@dataclass(frozen=True)
class GenerativeBone:
    ref: str # e.g. "src" or "tgt"
    data: ConnectBone | ExtensionBone
    req_bones: list[str] | None = None
    settings: RigifySettings | None = None
    b_collection: str | None = None
    is_optional: bool = False


    def generate(self, ref: bpy.types.Armature, tgt: bpy.types.Armature, data: dict | None = None) -> list[str] | None:
        """Generates the bone in the given armature and returns the new bone's name."""
        generated_bones = self.data.generate(ref, tgt, data=data)

        if generated_bones and self.b_collection:
           utils.armature.b_collection.assign_bones(tgt, generated_bones, self.b_collection)

        return generated_bones




## Constraints 

class Constraint(ABC):
    """Abstract base class for all bone constraints."""
    
    @abstractmethod
    def apply(self, bone: bpy.types.PoseBone, armature: bpy.types.Armature) -> None:
        """Applies the constraint to the given bone."""
        pass

@dataclass(frozen=True)
class CopyScaleConstraint(Constraint):
    target_bone: str | None = None
    axis: tuple[bool, bool, bool] = (True, True, True) 
    power: float = 1.0
    uniform_scale: bool = False
    offset: bool = False
    additive: bool = False
    target_space: str = "LOCAL_OWNER_ORIENT"
    owner_space: str = "LOCAL_WITH_PARENT"
    influence: float = 1.0
    name: str = "AetherBlend_CopyScale"

    def apply(self, bone: bpy.types.PoseBone, armature: bpy.types.Armature) -> None:
        """Applies the Copy Scale constraint to the given bone."""
        constraint = bone.constraints.new(type='COPY_SCALE')
        constraint.name = self.name
        target_obj = armature
        if not target_obj:
            print(f"[AetherBlend] Target object '{self.target_object}' not found for Copy Scale constraint.")
            return
        constraint.target = target_obj
        constraint.subtarget = self.target_bone
        constraint.use_x = self.axis[0]
        constraint.use_y = self.axis[1]
        constraint.use_z = self.axis[2]
        constraint.use_make_uniform = self.uniform_scale
        constraint.use_offset = self.offset
        constraint.use_add = self.additive
        constraint.target_space = self.target_space
        constraint.owner_space = self.owner_space
        constraint.influence = self.influence


@dataclass(frozen=True)
class CopyLocationConstraint(Constraint):
    target_bone: str | None = None
    head_tail: float = 0.0
    axis: tuple[bool, bool, bool] = (True, True, True) 
    invert_axis: tuple[bool, bool, bool] = (False, False, False)
    offset: bool = False
    target_space: str = "POSE"
    owner_space: str = "POSE"
    influence: float = 1.0
    name: str = "AetherBlend_CopyLocation"

    def apply(self, bone: bpy.types.PoseBone, armature: bpy.types.Armature) -> None:
        """Applies the Copy Location constraint to the given bone."""
        constraint = bone.constraints.new(type='COPY_LOCATION')
        constraint.name = self.name
        target_obj = armature
        if not target_obj:
            print(f"[AetherBlend] Target object '{self.target_object}' not found for Copy Location constraint.")
            return
        constraint.target = target_obj
        constraint.subtarget = self.target_bone
        constraint.head_tail = self.head_tail
        constraint.use_x = self.axis[0]
        constraint.use_y = self.axis[1]
        constraint.use_z = self.axis[2]
        constraint.invert_x = self.invert_axis[0]
        constraint.invert_y = self.invert_axis[1]
        constraint.invert_z = self.invert_axis[2]
        constraint.use_offset = self.offset
        constraint.target_space = self.target_space
        constraint.owner_space = self.owner_space
        constraint.influence = self.influence


@dataclass(frozen=True)
class CopyRotationConstraint(Constraint):
    target_bone: str | None = None
    euler_order: str = "ZXY"
    axis: tuple[bool, bool, bool] = (True, True, True) 
    invert_axis: tuple[bool, bool, bool] = (False, False, False)
    mix_mode: str = "AFTER"
    target_space: str = "LOCAL_OWNER_ORIENT"
    owner_space: str = "LOCAL_WITH_PARENT"
    influence: float = 1.0
    name: str = "AetherBlend_CopyRotation"

    def apply(self, bone: bpy.types.PoseBone, armature: bpy.types.Armature) -> None:
        """Applies the Copy Rotation constraint to the given bone."""
        constraint = bone.constraints.new(type='COPY_ROTATION')
        constraint.name = self.name
        target_obj = armature
        if not target_obj:
            print(f"[AetherBlend] Target object '{self.target_object}' not found for Copy Rotation constraint.")
            return
        constraint.target = target_obj
        constraint.subtarget = self.target_bone
        constraint.euler_order = self.euler_order
        constraint.use_x = self.axis[0]
        constraint.use_y = self.axis[1]
        constraint.use_z = self.axis[2]
        constraint.invert_x = self.invert_axis[0]
        constraint.invert_y = self.invert_axis[1]
        constraint.invert_z = self.invert_axis[2]
        constraint.mix_mode = self.mix_mode
        constraint.target_space = self.target_space
        constraint.owner_space = self.owner_space
        constraint.influence = self.influence