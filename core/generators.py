import bpy
import math
import mathutils  # type: ignore

from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .shared import PoseOperations

from .. import utils


class BoneGenerator(ABC):
    """Base interface for all bone generation types."""
    # These fields will be defined in child dataclasses
    name: str
    parent: str | None = None
    is_connected: bool = False
    roll: float = 0.0
    req_bones: list[str] | None = None
    pose_operations: 'PoseOperations | None' = None
    is_optional: bool = False
    
    @abstractmethod
    def generate(self, armature: bpy.types.Object, data: dict | None = None) -> list[str] | None:
        """Generates the bone and returns the created bone name(s)."""
        pass


@dataclass(frozen=True)
class ConnectBone(BoneGenerator):
    """Creates a bone connecting point A to point B."""
    name: str
    bone_a: str
    bone_b: str 
    start: str = "head"  # e.g., "head", "tail" - which end of bone_a to start from
    end: str = "head"    # e.g., "head", "tail" - which end of bone_b to connect to
    parent: str | None = None
    is_connected: bool = False
    roll: float = 0.0
    
    req_bones: list[str] | None = None
    pose_operations: 'PoseOperations | None' = None
    is_optional: bool = False

    def generate(self, armature: bpy.types.Object, data: dict | None = None) -> list[str] | None:
        """Generates the ConnectBone from bone_a to bone_b."""
        if not armature:
            print(f"[AetherBlend] Invalid armature provided for ConnectBone '{self.name}'.")
            return None
            
        edit_bones = armature.data.edit_bones
        bone_a_ref = edit_bones.get(self.bone_a)
        bone_b_ref = edit_bones.get(self.bone_b)

        if not bone_a_ref or not bone_b_ref:
            print(f"[AetherBlend] Cannot create ConnectBone '{self.name}': reference bones '{self.bone_a}' or '{self.bone_b}' not found.")
            return None
        
        if self.start == "tail":
            head_pos = bone_a_ref.tail.copy()
        else:  # "head"
            head_pos = bone_a_ref.head.copy()
        
        if self.end == "tail":
            tail_pos = bone_b_ref.tail.copy()
        else:  # "head"
            tail_pos = bone_b_ref.head.copy()
        
        if self.name in edit_bones:
            edit_bones.remove(edit_bones[self.name])

        new_bone = edit_bones.new(self.name)
        new_bone.head = head_pos
        new_bone.tail = tail_pos
        new_bone.roll = math.radians(self.roll) if self.roll != 0.0 else 0.0
        
        if self.parent:
            parent_bone = edit_bones.get(self.parent)
            if parent_bone:
                new_bone.parent = parent_bone
                new_bone.use_connect = self.is_connected
            else:
                print(f"[AetherBlend] Warning: Parent bone '{self.parent}' not found for ConnectBone '{self.name}'.")
        
        created_name = new_bone.name
        
        return [created_name]


@dataclass(frozen=True)
class ExtensionBone(BoneGenerator):
    """Creates a bone extending from a source bone in a given direction."""
    name: str
    bone_a: str 
    size_factor: float = 1.0
    axis_type: str = "local"  # e.g., "global", "local", "armature"
    axis: str = "Y"  # e.g., "X", "Y", "Z"
    start: str = "tail"  # e.g., "head", "tail"
    parent: str | None = None
    is_connected: bool = False
    roll: float = 0.0

    req_bones: list[str] | None = None
    pose_operations: 'PoseOperations | None' = None
    is_optional: bool = False

    def generate(self, armature: bpy.types.Object, data: dict | None = None) -> list[str] | None:
        """Generates the ExtensionBone extending from bone_a."""
        if not armature:
            print(f"[AetherBlend] Invalid armature provided for ExtensionBone '{self.name}'.")
            return None
        
        edit_bones = armature.data.edit_bones
        bone_a_ref = edit_bones.get(self.bone_a)

        if not bone_a_ref:
            print(f"[AetherBlend] Reference bone '{self.bone_a}' not found for ExtensionBone '{self.name}'.")
            return None
        
        if self.start == "tail":
            start_pos = bone_a_ref.tail.copy()
        else:  # "head"
            start_pos = bone_a_ref.head.copy()

        direction_vector = None
        if self.axis_type == "local":
            local_bone_matrix = bone_a_ref.matrix.to_3x3().inverted()
            if self.axis == "X":
                direction_vector = local_bone_matrix[0]
            elif self.axis == "Y":
                direction_vector = local_bone_matrix[1] 
            elif self.axis == "Z":
                direction_vector = local_bone_matrix[2]
        elif self.axis_type == "armature":
            if self.axis == "X":
                direction_vector = mathutils.Vector((1.0, 0.0, 0.0))
            elif self.axis == "Y":
                direction_vector = mathutils.Vector((0.0, 1.0, 0.0))
            elif self.axis == "Z":
                direction_vector = mathutils.Vector((0.0, 0.0, 1.0))
        elif self.axis_type == "global":
            if self.axis == "X":
                world_direction = mathutils.Vector((1.0, 0.0, 0.0))
            elif self.axis == "Y":
                world_direction = mathutils.Vector((0.0, 1.0, 0.0))
            elif self.axis == "Z":
                world_direction = mathutils.Vector((0.0, 0.0, 1.0))
            
            armature_matrix_inv = armature.matrix_world.to_3x3().inverted()
            direction_vector = armature_matrix_inv @ world_direction
        
        if not direction_vector:
            print(f"[AetherBlend] Invalid axis configuration for ExtensionBone '{self.name}': axis_type='{self.axis_type}', axis='{self.axis}'.")
            return None
        
        ref_bone_length = bone_a_ref.length if bone_a_ref.length > 0 else 1.0
        extension_length = ref_bone_length * self.size_factor
        tail_pos = start_pos + direction_vector.normalized() * extension_length
        
        
        if self.name in edit_bones:
            edit_bones.remove(edit_bones[self.name])

        new_bone = edit_bones.new(self.name)
        new_bone.head = start_pos
        new_bone.tail = tail_pos
        new_bone.roll = math.radians(self.roll) if self.roll != 0.0 else 0.0

        if self.parent:
            if isinstance(self.parent, list):
                for bone_name in self.parent:
                    parent_bone = edit_bones.get(bone_name)
                    if parent_bone and parent_bone != new_bone:
                        break
            else:
                parent_bone = edit_bones.get(self.parent)

            if parent_bone:
                new_bone.parent = parent_bone
                new_bone.use_connect = self.is_connected
            else:
                print(f"[AetherBlend] Warning: Parent bone '{self.parent}' not found for ExtensionBone '{self.name}'.")
        
        created_name = new_bone.name
        
        if self.pose_operations and self.pose_operations.b_collection:
            utils.armature.b_collection.assign_bones(armature, [created_name], self.pose_operations.b_collection)
        
        return [created_name]


@dataclass(frozen=True)
class CopyBone(BoneGenerator):
    """Creates a bone by copying the transform of an existing bone."""
    name: str
    source_bone: str
    parent: str | None = None
    is_connected: bool = False
    roll: float = 0.0

    req_bones: list[str] | None = None
    pose_operations: 'PoseOperations | None' = None
    is_optional: bool = False
    
    def generate(self, armature: bpy.types.Object, data: dict | None = None) -> list[str] | None:
        """Generates a copy of the source bone."""
        if not armature:
            print(f"[AetherBlend] Invalid armature provided for CopyBone '{self.name}'.")
            return None
        
        edit_bones = armature.data.edit_bones
        source_bone_ref = edit_bones.get(self.source_bone)

        if not source_bone_ref:
            print(f"[AetherBlend] Source bone '{self.source_bone}' not found for CopyBone '{self.name}'.")
            return None
        
        if self.name in edit_bones:
            edit_bones.remove(edit_bones[self.name])

        new_bone = edit_bones.new(self.name)
        new_bone.head = source_bone_ref.head.copy()
        new_bone.tail = source_bone_ref.tail.copy()
        new_bone.roll = math.radians(self.roll) if self.roll != 0.0 else source_bone_ref.roll

        if self.parent:
            parent_bone = edit_bones.get(self.parent)
            if parent_bone:
                new_bone.parent = parent_bone
                new_bone.use_connect = self.is_connected
            else:
                print(f"[AetherBlend] Warning: Parent bone '{self.parent}' not found for CopyBone '{self.name}'.")
        
        created_name = new_bone.name
        
        if self.pose_operations and self.pose_operations.b_collection:
            utils.armature.b_collection.assign_bones(armature, [created_name], self.pose_operations.b_collection)
        
        return [created_name]
    
@dataclass(frozen=True)
class SkinBone:
    name: str
    bone_a: str
    parent: str | None = None
    size_factor: float = 1.0
    mesh_restriction: str | None = None

    req_bones: list[str] | None = None
    pose_operations: 'PoseOperations | None' = None
    is_optional: bool = False

    def generate(self, armature: bpy.types.Object, data: dict | None = None) -> list[str] | None:
        """Generates the SkinBone at the highest weighted vertex position for bone_a."""
        if not armature:
            print(f"[AetherBlend] Invalid armature provided for SkinBone '{self.name}'.")
            return None
        
        skin = None
        ffxiv_armature = None
        if data is not None:
            try:
                skin_data_item = data.get(self.mesh_restriction)
                if skin_data_item.type == 'MESH':
                    skin = skin_data_item

                ffxiv_armature = data.get("ffxiv_armature")
            except Exception:
                pass
                
        bones = armature.data.bones
        bone_a_ref = bones.get(self.bone_a)

        if not bone_a_ref:
            print(f"[AetherBlend] Reference bone '{self.bone_a}' not found in source armature for SkinBone '{self.name}'.")
            return None
        
        world_co, weight = self._find_highest_weight_vertex_world_pos(self.bone_a, ffxiv_armature, mesh=skin)
        
        if world_co is None:
            print(f"[AetherBlend] No vertices found with weights for bone '{self.bone_a}'. Skipping SkinBone '{self.name}'.")
            return None     
        
        ref_bone_length = bone_a_ref.length if bone_a_ref.length > 0 else 0.3
    
        bone_length = ref_bone_length * self.size_factor
        
        bpy.context.view_layer.objects.active = armature
        
        target_edit_bones = armature.data.edit_bones
        
        if self.name in target_edit_bones:
            target_edit_bones.remove(target_edit_bones[self.name])
        
        new_bone = target_edit_bones.new(self.name)
        
        local_co = armature.matrix_world.inverted() @ world_co
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
    
    def _find_highest_weight_vertex_world_pos(self, bone_name: str, armature: bpy.types.Object, mesh = None) -> tuple:
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
                if modifier.type == 'ARMATURE' and modifier.object == armature:
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
                if mod.type == 'ARMATURE' and mod.object == armature:
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
class BridgeBone:
    name: str
    bone_a: str
    bone_b: str
    offset_factor: mathutils.Vector = mathutils.Vector((0.0, 0.0, 0.0))
    is_connected: bool = True #Unlike ExtensionBone and SkinBone, BridgeBones is_connect defines wether the last bone is connected to bone_b
    parent : str | None = None

    req_bones: list[str] | None = None
    pose_operations: 'PoseOperations | None' = None
    is_optional: bool = False

    def generate(self, armature: bpy.types.Object, data: dict | None = None) -> list[str] | None:
        """Generates the BridgeBone from bone_a to bone_b with curved offset in target armature."""
        if not armature:
            print(f"[AetherBlend] Invalid armatures provided for BridgeBone '{self.name}'.")
            return None
            
        edit_bones = armature.data.edit_bones
        bone_a_ref = edit_bones.get(self.bone_a)
        bone_b_ref = edit_bones.get(self.bone_b)

        if not bone_a_ref or not bone_b_ref:
            print(f"[AetherBlend] Cannot create BridgeBone '{self.name}': reference bones '{self.bone_a}' or '{self.bone_b}' not found in source armature.")
            return None
        
        start_pos = bone_a_ref.head.copy()
        end_pos = bone_b_ref.head.copy()
        
        midpoint = (start_pos + end_pos) / 2.0
        curve_factor = math.sin(math.pi * 0.5)  # Maximum curve at t=0.5
        bridge_head = midpoint + (self.offset_factor * curve_factor)
        
        edit_bones = armature.data.edit_bones
        
        if self.name in edit_bones:
            edit_bones.remove(edit_bones[self.name])

        new_bone = edit_bones.new(self.name)
        new_bone.head = bridge_head
        new_bone.tail = end_pos
        
        bone_a_target = edit_bones.get(self.bone_a)
        if bone_a_target:
            bone_a_target.tail = bridge_head
            new_bone.parent = bone_a_target
            new_bone.use_connect = True
            
            # Set bone_a's parent if parent parameter is provided
            if self.parent:
                parent_bone = edit_bones.get(self.parent)
                if parent_bone:
                    bone_a_target.parent = parent_bone
                    bone_a_target.use_connect = False
                else:
                    print(f"[AetherBlend] Warning: Parent bone '{self.parent}' not found for bone_a '{self.bone_a}' in BridgeBone '{self.name}'.")
        else:
            print(f"[AetherBlend] Warning: Parent bone '{self.bone_a}' not found in target armature for BridgeBone '{self.name}'.")
        
        if self.is_connected:
            bone_b_target = edit_bones.get(self.bone_b)
            if bone_b_target:
                bone_b_target.parent = new_bone
                bone_b_target.use_connect = True
            else:
                print(f"[AetherBlend] Warning: Target bone '{self.bone_b}' not found for connection in BridgeBone '{self.name}'.")
        
        created_name = new_bone.name  
        return [created_name]


@dataclass(frozen=True)
class CenterBone:
    name: str
    ref_bones: list[str]
    size_factor: float = 1.0
    parent: str | None = None
    axis: str = "Z"  # e.g., "X", "Y", "Z" - axis direction for bone extension
    inverted: bool = False  # True: tail to head, False: head to tail

    req_bones: list[str] | None = None
    pose_operations: 'PoseOperations | None' = None
    is_optional: bool = False

    def generate(self, armature: bpy.types.Object ,data: dict | None = None) -> list[str] | None:
        """Generates the CenterBone at the center position of reference bones in target armature."""
        if not armature:
            print(f"[AetherBlend] Invalid armatures provided for CenterBone '{self.name}'.")
            return None
        
        edit_bones = armature.data.edit_bones
        valid_ref_bones = list[bpy.types.EditBone]()
        
        for bone_name in self.ref_bones:
            bone_ref = edit_bones.get(bone_name)
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
            total_position += bone_ref.head
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
        
        if self.name in edit_bones:
            edit_bones.remove(edit_bones[self.name])
        
        new_bone = edit_bones.new(self.name)
        
        if self.inverted:
            new_bone.tail = center_position.copy()
            new_bone.head = center_position + direction_vector
        else:
            new_bone.head = center_position.copy()
            new_bone.tail = center_position + direction_vector
        
        if self.parent:
            parent_bone = edit_bones.get(self.parent)
            if parent_bone:
                new_bone.parent = parent_bone
                new_bone.use_connect = False
            else:
                print(f"[AetherBlend] Warning: Parent bone '{self.parent}' not found for CenterBone '{self.name}'.")
        
        created_name = new_bone.name
        return [created_name]
