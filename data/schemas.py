from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import math
import mathutils
import re

import bpy

from .. import utils

@dataclass(frozen=True)
class MetaRigCollectionInfo:
    name: str
    color_type: str
    row_index: int
    title: str
    visible: bool = True

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
    primary_layer_extra: str | None = None
    secondary_layer_extra: str | None  = None
    jaw_mouth_influence: str | None = None
    relink_constraints: bool | None = None
    skin_glue_use_tail: bool | None = None
    skin_glue_tail_reparent: bool | None = None
    skin_glue_add_constraint: str | None = None
    skin_glue_add_constraint_influence: float | None = None
    skin_chain_pivot_pos: int | None  = None
    skin_chain_falloff: list[float] | None = None
    skin_chain_falloff_length: bool | None = None
    skin_chain_falloff_spherical: list[bool] | None  = None
    skin_chain_priority: int | None = None
    skin_control_orientation_bone: str | None  = None
    pivot_master_widget_type: str | None = None

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
        if bpy.context.object.mode != 'EDIT':
            bpy.ops.object.mode_set(mode='EDIT')

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

        bpy.context.view_layer.objects.active = target
        
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
            

@dataclass(frozen=True)
class RegexBoneGroup:
    pattern: str
    prefix: str = "RegexBoneGroup"
    extension_size_factor: float = 1.0
    extension_axis_type: str = "local"  # e.g., "global", "local", "armature"
    extension_axis: str  = "Y"  # e.g., "X", "Y", "Z"
    standalone_widget: str | None = None 
    parent: str | None = None
    is_connected: bool = False
    rigify_type_standalone: str | None = "basic.super_copy"
    rigify_type_chain: str | None = "skin.stretchy_chain" 

    def generate(self, ref: bpy.types.Armature, target: bpy.types.Armature, data: dict | None = None) -> list[str] | None:
        """Generates bone chains for pattern-matched bones in the target armature."""
        import re

        if not ref or not target:
            print(f"[AetherBlend] Invalid armatures provided for RegexBoneGroup with pattern '{self.pattern}'.")
            return None
        
        ref_bones = ref.data.bones
        matched_bones = [bone for bone in ref_bones if re.match(self.pattern, bone.name)]

        created_bones = []
        processed_bones = set()  
        root_chain_bones = [] 

        for bone in matched_bones:
            if bone.name in processed_bones:
                continue

            children = [child for child in bone.children if re.match(self.pattern, child.name)]

            if not children:
                extension_bone = ExtensionBone(
                    name=f"{self.prefix}_{bone.name}",
                    bone_a=bone.name,
                    size_factor=self.extension_size_factor,
                    axis_type=self.extension_axis_type,
                    axis=self.extension_axis,
                    parent=self.parent,
                    is_connected=self.is_connected,
                    start="head"
                )
                result = extension_bone.generate(ref, target, data)
                if result:
                    created_bones.extend(result)
                    
                    if self.rigify_type_standalone:
                        self._apply_rigify_to_bone(target, result[-1], self.rigify_type_standalone, self.standalone_widget)
                
                processed_bones.add(bone.name)
            else:
                chain_bones = self._build_chain(bone, ref_bones)
                processed_bones.update(chain_bones)
                
                is_valid_chain = len(chain_bones) >= 3
                chain_connect_bones = []  
                
                for i in range(len(chain_bones) - 1):
                    connect_bone_name = f"{self.prefix}_{chain_bones[i]}"
                    connect_bone = ConnectBone(
                        name=connect_bone_name,
                        bone_a=chain_bones[i],
                        bone_b=chain_bones[i+1],
                        parent=self.parent if i == 0 else created_bones[-1],
                        start="head",
                        end="head",
                        is_connected=self.is_connected if i == 0 else True
                    )
                    result = connect_bone.generate(ref, target, data)
                    if result:
                        created_bone_name = result[-1]
                        created_bones.extend(result)
                        chain_connect_bones.append(created_bone_name)
                
                if is_valid_chain and self.rigify_type_chain:
                    if chain_connect_bones:
                        root_chain_bones.append(chain_connect_bones[0])
                elif not is_valid_chain and self.rigify_type_standalone:
                    for connect_bone_name in chain_connect_bones:
                        self._apply_rigify_to_bone(target, connect_bone_name, self.rigify_type_standalone, self.standalone_widget)
                
                last_bone = created_bones[-1]
                extension_bone = ExtensionBone(
                    name=f"{self.prefix}_{chain_bones[-1]}",
                    bone_a=last_bone,
                    size_factor=1.0,
                    axis_type="local",
                    axis="Y",
                    parent=created_bones[-1],
                    is_connected=True,
                    start="tail"
                )
                result = extension_bone.generate(target, target, data)
                if result:
                    created_bones.extend(result)
                    if not is_valid_chain and self.rigify_type_standalone:
                        self._apply_rigify_to_bone(target, result[-1], self.rigify_type_standalone, self.standalone_widget)

        if root_chain_bones and self.rigify_type_chain:
            for root_bone_name in root_chain_bones:
                self._apply_rigify_to_bone(target, root_bone_name, self.rigify_type_chain)

        return created_bones if created_bones else None

    def _build_chain(self, start_bone: bpy.types.Bone, ref_bones) -> list[str]:
        """Recursively builds a chain of bones following the hierarchy."""
        chain = [start_bone.name]
        current = start_bone
        
        while True:
            children = [child for child in current.children if re.match(self.pattern, child.name)]   
            if not children:
                break
            current = children[0]
            chain.append(current.name)
        
        return chain

    def _apply_rigify_to_bone(self, target: bpy.types.Armature, bone_name: str, rigify_type: str, widget: str | None = None) -> None:
        """Applies rigify type to a specific bone using the utility function."""
        settings = RigifySettings(
            bone_name=bone_name,
            rigify_type=rigify_type,
            super_copy_widget_type=widget
        )    
        utils.armature.rigify.set_rigify_properties(
            armature=target,
            settings=settings,
            bone_name=bone_name,   
        )

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
    start: str = "head"  # e.g., "head", "tail" - which end of bone_a to start from
    end: str = "head"    # e.g., "head", "tail" - which end of bone_b to connect to

    def generate(self, ref: bpy.types.Armature, target: bpy.types.Armature, data: dict | None = None) -> list[str] | None:
        """Generates the ConnectBone from bone_a to bone_b in target armature."""
        if bpy.context.object.mode != 'EDIT':
            bpy.ops.object.mode_set(mode='EDIT')

        if not ref or not target:
            print(f"[AetherBlend] Invalid armatures provided for ConnectBone '{self.name}'.")
            return None
            
        ref_bones = ref.data.bones
        bone_a_ref = ref_bones.get(self.bone_a)
        bone_b_ref = ref_bones.get(self.bone_b)

        if not bone_a_ref or not bone_b_ref:
            print(f"[AetherBlend] Cannot create ConnectBone '{self.name}': reference bones '{self.bone_a}' or '{self.bone_b}' not found in source armature.")
            return None
        
        if self.start == "tail":
            head_pos = bone_a_ref.tail_local.copy()
        else:  # "head"
            head_pos = bone_a_ref.head_local.copy()
        
        if self.end == "tail":
            tail_pos = bone_b_ref.tail_local.copy()
        else:  # "head"
            tail_pos = bone_b_ref.head_local.copy()
        
        bpy.context.view_layer.objects.active = target

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
            

@dataclass(frozen=True)
class BridgeBone:
    name: str
    bone_a: str
    bone_b: str
    offset_factor: mathutils.Vector = mathutils.Vector((0.0, 0.0, 0.0))
    is_connected: bool = True #Unlike ExtensionBone and SkinBone, BridgeBones is_connect defines wether the last bone is connected to bone_b
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
class CenterBone:
    name: str
    ref_bones: list[str]
    size_factor: float = 1.0
    parent: str | None = None
    axis: str = "Z"  # e.g., "X", "Y", "Z" - axis direction for bone extension
    inverted: bool = False  # True: tail to head, False: head to tail

    def generate(self, ref: bpy.types.Armature, target: bpy.types.Armature, data: dict | None = None) -> list[str] | None:
        """Generates the CenterBone at the center position of reference bones in target armature."""
        if not ref or not target:
            print(f"[AetherBlend] Invalid armatures provided for CenterBone '{self.name}'.")
            return None
        
        ref_bones_data = ref.data.bones
        valid_ref_bones = []
        
        for bone_name in self.ref_bones:
            bone_ref = ref_bones_data.get(bone_name)
            if bone_ref:
                valid_ref_bones.append(bone_ref)
            else:
                print(f"[AetherBlend] Warning: Reference bone '{bone_name}' not found in source armature for CenterBone '{self.name}'.")
        
        if not valid_ref_bones:
            print(f"[AetherBlend] Error: No valid reference bones found for CenterBone '{self.name}'. Cannot create center bone.")
            return None
        
        total_position = mathutils.Vector((0.0, 0.0, 0.0))
        total_length = 0.0
        for bone_ref in valid_ref_bones:
            total_position += bone_ref.head_local
            total_length += bone_ref.length
        
        center_position = total_position / len(valid_ref_bones)
        avg_length = total_length / len(valid_ref_bones) if total_length > 0 else 0.3
        eye_bone_length = avg_length * self.size_factor
        
        if self.axis == "X":
            direction_vector = mathutils.Vector((eye_bone_length, 0.0, 0.0))
        elif self.axis == "Y":
            direction_vector = mathutils.Vector((0.0, eye_bone_length, 0.0))
        elif self.axis == "Z":
            direction_vector = mathutils.Vector((0.0, 0.0, eye_bone_length))
        else:
            # Default to Y axis if invalid
            direction_vector = mathutils.Vector((0.0, eye_bone_length, 0.0))
        
        original_mode = bpy.context.object.mode
        bpy.context.view_layer.objects.active = target
        bpy.ops.object.mode_set(mode='EDIT')
        
        try:
            target_edit_bones = target.data.edit_bones
            
            if self.name in target_edit_bones:
                target_edit_bones.remove(target_edit_bones[self.name])
            
            new_bone = target_edit_bones.new(self.name)
            
            if self.inverted:
                new_bone.tail = center_position.copy()
                new_bone.head = center_position + direction_vector
            else:
                new_bone.head = center_position.copy()
                new_bone.tail = center_position + direction_vector
            
            if self.parent:
                parent_bone = target_edit_bones.get(self.parent)
                if parent_bone:
                    new_bone.parent = parent_bone
                    new_bone.use_connect = False
                else:
                    print(f"[AetherBlend] Warning: Parent bone '{self.parent}' not found for CenterBone '{self.name}'.")
            
            created_name = new_bone.name
            return [created_name]
            
        finally:
            bpy.ops.object.mode_set(mode=original_mode)
        
@dataclass(frozen=True)
class GenerativeBone:
    ref: str # e.g. "src" or "tgt"
    data: ConnectBone | ExtensionBone | SkinBone | BridgeBone | CenterBone | RegexBoneGroup
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


@dataclass(frozen=True)
class CopyTransformsConstraint(Constraint):
    target_bone: str | None = None
    head_tail: float = 0.0
    remove_target_shear: bool = False
    mix_mode: str = "REPLACE"
    target_space: str = "LOCAL_OWNER_ORIENT"
    owner_space: str = "LOCAL_WITH_PARENT"
    influence: float = 1.0
    name: str = "AetherBlend_CopyTransform"

    def apply(self, bone: bpy.types.PoseBone, armature: bpy.types.Armature) -> None:
        """Applies the Copy Transforms constraint to the given bone."""
        constraint = bone.constraints.new(type='COPY_TRANSFORMS')
        constraint.name = self.name
        target_obj = armature
        if not target_obj:
            print(f"[AetherBlend] Target object '{self.target_object}' not found for Copy Transforms constraint.")
            return
        constraint.target = target_obj
        constraint.subtarget = self.target_bone
        constraint.head_tail = self.head_tail
        constraint.remove_target_shear = self.remove_target_shear
        constraint.mix_mode = self.mix_mode
        constraint.target_space = self.target_space
        constraint.owner_space = self.owner_space
        constraint.influence = self.influence


@dataclass(frozen=True)
class UnmapConstraint(Constraint):
    """Pseudo-constraint that moves bones to an 'Unmapped Bones' collection."""
    name: str = "AetherBlend_Unmap"

    def apply(self, bone: bpy.types.PoseBone, armature: bpy.types.Armature) -> None:
        """Moves the bone to the 'Unmapped Bones' collection."""
        collection_name = "Unmapped Bones"
        
        bone_collections = armature.data.collections
        unmapped_collection = bone_collections.get(collection_name)
        
        if unmapped_collection is None:
            unmapped_collection = bone_collections.new(collection_name)
            unmapped_collection.is_visible = False
        
        for collection in bone.bone.collections:
            collection.unassign(bone.bone)
        
        unmapped_collection.assign(bone.bone)


@dataclass(frozen=True)
class TrackToConstraint(Constraint):
    target_bone: str
    track_axis: str = "TRACK_Y"
    up_axis: str = "UP_X"
    target_z: bool = False 
    target_space: str = "LOCAL_OWNER_ORIENT"
    owner_space: str = "LOCAL_WITH_PARENT"
    space_object: str | None = None
    space_subtarget: str | None = None
    influence: float = 1.0
    name: str = "AetherBlend_TrackTo"

    def apply(self, bone: bpy.types.PoseBone, armature: bpy.types.Armature) -> None:
        """Applies the Track To constraint to the given bone."""
        constraint = bone.constraints.new(type='TRACK_TO')
        constraint.name = self.name
        target_obj = armature
        if not target_obj:
            print(f"[AetherBlend] Target object '{self.target_object}' not found for Track To constraint.")
            return
        constraint.target = target_obj
        constraint.subtarget = self.target_bone
        constraint.track_axis = self.track_axis
        constraint.up_axis = self.up_axis
        constraint.use_target_z = self.target_z
        constraint.target_space = self.target_space
        constraint.owner_space = self.owner_space

        if self.owner_space == 'CUSTOM' or self.target_space == 'CUSTOM':
            space_object = bpy.data.objects.get(self.space_object) if self.space_object else armature
            if space_object:
                constraint.space_object = space_object
                constraint.space_subtarget = self.space_subtarget
            else:
                print(f"[AetherBlend] Warning: Space object '{self.space_object}' not found for Track To constraint.")
        constraint.influence = self.influence

        # utils.armature.rigify._select_pose_bone(bone, True)
        # bpy.ops.pose.armature_apply(selected=True)
        # utils.armature.rigify._select_pose_bone(bone, False)


@dataclass(frozen=True)
class OffsetTransformConstraint(Constraint):
    """Pseudo-constraint that creates a mechanism bone to properly handle world-to-local transforms."""
    target_bone: str | None = None
    name: str = "AetherBlend_OffsetTransform"

    def apply(self, bone: bpy.types.PoseBone, armature: bpy.types.Armature, target_override: str | None = None) -> None:
        """Creates a MCH bone copy and sets up proper transform inheritance."""
        if not self.target_bone and not target_override:
            print(f"[AetherBlend] No target bone specified for OffsetTransform constraint on '{bone.name}'")
            return
        
        target_bone = target_override if target_override else self.target_bone
        
        mch_bone_name = f"MCH-{bone.name}"
        collection_name = "MCH"
        
        original_mode = bpy.context.object.mode
        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='EDIT')
        
        try:
            edit_bones = armature.data.edit_bones
            
            if mch_bone_name in edit_bones:
                edit_bones.remove(edit_bones[mch_bone_name])
            
            original_edit_bone = edit_bones.get(bone.name)
            if not original_edit_bone:
                print(f"[AetherBlend] Could not find bone '{bone.name}' in edit mode")
                return
            
            mch_bone = edit_bones.new(mch_bone_name)
            mch_bone.head = original_edit_bone.head.copy()
            mch_bone.tail = original_edit_bone.tail.copy()
            mch_bone.roll = original_edit_bone.roll
            
            target_edit_bone = edit_bones.get(target_bone)
            if target_edit_bone:
                mch_bone.parent = target_edit_bone
                mch_bone.use_connect = False
            else:
                print(f"[AetherBlend] Warning: Target bone '{target_bone}' not found for OffsetTransform")
            
            bone_collections = armature.data.collections
            mch_collection = bone_collections.get(collection_name)
            
            if mch_collection is None:
                mch_collection = bone_collections.new(collection_name)
                print(f"[AetherBlend] Created bone collection '{collection_name}'")
            
        finally:
            bpy.ops.object.mode_set(mode='POSE')
        
        mch_pose_bone = armature.pose.bones.get(mch_bone_name)
        if mch_pose_bone and bone:
            mch_collection.assign(mch_pose_bone.bone)
            
            copy_transform = CopyTransformsConstraint(
                target_bone=mch_pose_bone.name,
                mix_mode="REPLACE",
                target_space="WORLD",
                owner_space="WORLD",
                name="AetherBlend_OffsetTransform_Copy"
            )
            copy_transform.apply(bone, armature)
        
        if original_mode != 'POSE':
            bpy.ops.object.mode_set(mode=original_mode)


## LINK Edit Operations 

class LinkEditOperation(ABC):
    """Abstract base class for all link edit operations."""
    
    @abstractmethod
    def execute(self, armature: bpy.types.Armature) -> None:
        """Executes the link edit operation on the given armature."""
        pass


@dataclass(frozen=True)
class copyBone(LinkEditOperation):
    bone_name: str
    src_bone_name: str
    parent_bone_name: str | None = None

    def execute(self, armature: bpy.types.Armature) -> None:
        """Executes the link edit operation on the given armature."""
        if bpy.context.object.mode != 'EDIT':
            bpy.ops.object.mode_set(mode='EDIT')

        edit_bones = armature.data.edit_bones
        
        src_bone = edit_bones.get(self.src_bone_name)
        if not src_bone:
            print(f"[AetherBlend] Source bone '{self.src_bone_name}' not found in armature for copyBone operation.")
            return
        
        new_bone = edit_bones.new(self.bone_name)
        new_bone.head = src_bone.head.copy()
        new_bone.tail = src_bone.tail.copy()
        new_bone.roll = src_bone.roll
        
        if self.parent_bone_name:
            parent_bone = edit_bones.get(self.parent_bone_name)
            if parent_bone:
                new_bone.parent = parent_bone
                new_bone.use_connect = False
            else:
                print(f"[AetherBlend] Warning: Parent bone '{self.parent_bone_name}' not found for copyBone operation.")

@dataclass(frozen=True)
class connectBone(LinkEditOperation):
    bone_name: str
    bone_a: str
    bone_b: str
    start: str = "head"
    end: str = "head"
    is_connected: bool = False
    parent_bone_name: str | None = None

    ## a bone that is created from head of bone_a to head or tail of bone B
    def execute(self, armature: bpy.types.Armature) -> None:
        """Executes the link edit operation on the given armature."""
        if bpy.context.object.mode != 'EDIT':
            bpy.ops.object.mode_set(mode='EDIT')

        ref_bones = armature.data.bones
        bone_a_ref = ref_bones.get(self.bone_a)
        bone_b_ref = ref_bones.get(self.bone_b)

        if not bone_a_ref or not bone_b_ref:
            print(f"[AetherBlend] Cannot execute connectBone '{self.bone_name}': reference bones '{self.bone_a}' or '{self.bone_b}' not found in armature.")
            return
        
        if self.start == "tail":
            head_pos = bone_a_ref.tail_local.copy()
        else:  # "head"
            head_pos = bone_a_ref.head_local.copy()
        
        if self.end == "tail":
            tail_pos = bone_b_ref.tail_local.copy()
        else:  # "head"
            tail_pos = bone_b_ref.head_local.copy()
        
        edit_bones = armature.data.edit_bones
        
        new_bone = edit_bones.new(self.bone_name)
        new_bone.head = head_pos
        new_bone.tail = tail_pos
        
        if self.parent_bone_name:
            parent_bone = edit_bones.get(self.parent_bone_name)
            if parent_bone:
                new_bone.parent = parent_bone
                new_bone.use_connect = False
            else:
                print(f"[AetherBlend] Warning: Parent bone '{self.parent_bone_name}' not found for connectBone operation.")

## UI Controller 
@dataclass(frozen=True)
class ConstraintUIController:
    name: str
    target_bone: str
    target_constraint: str
    property_name: str
    title: str
    ui_element: str  # e.g., "checkbox", "slider", "dropdown"
    ui_params: dict | None = None  # Additional parameters for the UI element
    rename_constraint: str | None = None

    def create_ui(self, layout: bpy.types.UILayout, armature: bpy.types.Object) -> None:
        """Creates the UI element for controlling the constraint property."""
        if self.target_bone not in armature.pose.bones:
            return
        
        bone = armature.pose.bones[self.target_bone]
        constraint_name = self.rename_constraint if self.rename_constraint is not None else self.target_constraint
        constraint = bone.constraints.get(constraint_name)
        
        if not constraint:
            return
        
        col = layout.column(align=True)
        if self.ui_element == "checkbox":
            col.prop(constraint, "mute", text=self.title)
        elif self.ui_element == "slider":
            col.prop(constraint, self.property_name, text=self.title, slider=True, **(self.ui_params or {}))
        elif self.ui_element == "dropdown":
            col.prop(constraint, self.property_name, text=self.title, **(self.ui_params or {}))
        else:
            print(f"[AetherBlend] Unknown UI element type '{self.ui_element}' for ConstraintUIController '{self.name}'")
    
    def name_change(self, armature: bpy.types.Object) -> bool:
        """Renames the target constraint to a new name."""
        if self.rename_constraint is None:
            return False
        
        if self.target_bone not in armature.pose.bones:
            print(f"[AetherBlend] Bone '{self.target_bone}' not found in armature for ConstraintUIController '{self.name}'")
            return False
        
        bone = armature.pose.bones[self.target_bone]
        constraint = bone.constraints.get(self.target_constraint)
        
        if not constraint:
            print(f"[AetherBlend] Constraint '{self.target_constraint}' not found on bone '{self.target_bone}' for ConstraintUIController '{self.name}'")
            return False
        
        constraint.name = self.rename_constraint
        return True