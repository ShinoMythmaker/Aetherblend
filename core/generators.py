import bpy
import math
import mathutils 
import re

from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .operations import PoseOperations

from . import rigify
from .operations import ABOperation, ParentBoneOperation, PoseOperations, TransformLink
from .. import utils

@dataclass
class BoneGenerator(ABC):
    """Base interface for all bone generation types."""

    name: str
    parent: str | list[str] | None = field(default=None, kw_only=True)
    is_connected: bool = field(default=False, kw_only=True)
    roll: float = field(default=0.0, kw_only=True)
    req_bones: list[str] | None = field(default=None, kw_only=True)
    pose_operations: 'PoseOperations | None' = field(default=None, kw_only=True)
    operations: list[ABOperation] = field(default_factory=list, kw_only=True)
    is_optional: bool = field(default=False, kw_only=True)

    @abstractmethod
    def generate(self, armature: bpy.types.Object, data: dict | None = None) -> list[str] | None:
        """Generates the bone and returns the created bone name(s)."""
        return NotImplementedError
        
    def _set_parent(self, new_bone: bpy.types.EditBone, edit_bones: bpy.types.ArmatureEditBones, is_connected_overrite: bool | None = None) -> None:
        """Sets the parent bone for the generated bone. Override in subclasses if needed."""
        is_connected_overrite = is_connected_overrite if is_connected_overrite is not None else self.is_connected
        if self.parent:
            parent_names = self.parent if isinstance(self.parent, list) else [self.parent]
            parent_bone_name = parent_names[0]
            parent_bone = edit_bones.get(parent_bone_name)
            if parent_bone:
                new_bone.parent = parent_bone
                new_bone.use_connect = is_connected_overrite
            else:
                self.operations.append(ParentBoneOperation(new_bone.name, tuple(parent_names), is_connected_overrite))
        return 
    
    def get_dynamic_pose_operations(self) -> dict[str, list['PoseOperations']]:
        """Returns dynamically generated pose operations. Override in subclasses that need this."""
        return {}
    
    def get_dynamic_transform_links(self) -> list[TransformLink]:
        """Returns dynamically generated transform links. Override in subclasses that need this."""
        return []

@dataclass
class RegexBoneGroup(BoneGenerator):
    pattern: str
    prefix: str = "HAIR"
    extension_size_factor: float = 1.0
    extension_axis_type: str = "local"
    extension_axis: str = "Y"
    b_collection: str | None = None
    _dynamic_pose_operations: dict[str, list['PoseOperations']] = field(default_factory=dict, init=False, repr=False)
    _dynamic_transform_links: list['TransformLink'] = field(default_factory=list, init=False, repr=False)

    def generate(self, armature: bpy.types.Object, data: dict | None = None) -> list[str] | None:
        """Generates bone chains for pattern-matched bones in the target armature."""

        if not armature:
            print(f"[AetherBlend] Invalid armatures provided for RegexBoneGroup with pattern '{self.pattern}'.")
            return None
        
        # Reset dynamic tracking for each generate() call
        self._dynamic_pose_operations = {}
        self._dynamic_transform_links = []
        
        ref_bones = armature.data.bones
        matched_bones = [bone for bone in ref_bones if re.match(self.pattern, bone.name)]

        created_bones = []
        processed_bones = set()

        for bone in matched_bones:
            if bone.name in processed_bones:
                continue

            children = [child for child in bone.children if re.match(self.pattern, child.name)]

            if not children:
                # Single bone without children - create extension bone
                bone_name = f"{self.prefix}_{bone.name}"
                extension_bone = ExtensionBone(
                    name=bone_name,
                    bone_a=bone.name,
                    size_factor=self.extension_size_factor,
                    axis_type=self.extension_axis_type,
                    axis=self.extension_axis,
                    parent=self.parent,
                    is_connected=self.is_connected,
                    start="head"
                )
                result = extension_bone.generate(armature, data)
                if result:
                    created_bones.extend(result)
                    # Add pose operations and transform link
                    self._dynamic_pose_operations[bone_name] = [
                        PoseOperations(
                            rigify_settings=rigify.types.basic_super_copy(widget_type="bone"),
                            b_collection=self.b_collection
                        )
                    ]
                    self._dynamic_transform_links.append(
                        TransformLink(target=f"DEF-{bone_name}", bone=bone.name)
                    )
                
                processed_bones.add(bone.name)
            else:
                # Chain of bones - create connect bones for each
                chain_bones = self._build_chain(bone, ref_bones)
                processed_bones.update(chain_bones)
                
                # Create ConnectBones for all bones in chain including last
                for i in range(len(chain_bones)):
                    source_bone_name = chain_bones[i]
                    connect_bone_name = f"{self.prefix}_{source_bone_name}"
                    
                    if i < len(chain_bones) - 1:
                        # Connect to next bone in chain
                        connect_bone = ConnectBone(
                            name=connect_bone_name,
                            bone_a=chain_bones[i],
                            bone_b=chain_bones[i+1],
                            parent=self.parent if i == 0 else created_bones[-1],
                            start="head",
                            end="head",
                            is_connected=self.is_connected if i == 0 else True
                        )
                    else:
                        # Last bone - extend from its own tail
                        connect_bone = ExtensionBone(
                            name=connect_bone_name,
                            bone_a=chain_bones[i],
                            size_factor=1.0,
                            axis_type="local",
                            axis="Y",
                            parent=list(created_bones[-1]) if created_bones else self.parent,
                            is_connected=True,
                            start="head"
                        )
                    
                    result = connect_bone.generate(armature, data)
                    if result:
                        created_bones.extend(result)
                        # Add pose operations and transform link for this bone
                        self._dynamic_pose_operations[connect_bone_name] = [
                            PoseOperations(
                                rigify_settings=rigify.types.basic_super_copy(widget_type="bone"),
                                b_collection=self.b_collection
                            )
                        ]
                        self._dynamic_transform_links.append(
                            TransformLink(target=f"DEF-{connect_bone_name}", bone=source_bone_name)
                        )
                        
        return created_bones if created_bones else None
    
    def _build_chain(self, start_bone, ref_bones) -> list[str]:
        """Build a chain of bones starting from start_bone following the pattern."""
        chain = [start_bone.name]
        current = start_bone
        
        while True:
            children = [child for child in current.children if re.match(self.pattern, child.name)]
            if not children:
                break
            # Follow the first matching child
            current = children[0]
            chain.append(current.name)
        
        return chain
    
    def get_dynamic_pose_operations(self) -> dict[str, list['PoseOperations']]:
        """Returns the dynamically generated pose operations after generate() is called."""
        return self._dynamic_pose_operations if self._dynamic_pose_operations else {}
    
    def get_dynamic_transform_links(self) -> list['TransformLink']:
        """Returns the dynamically generated transform links after generate() is called."""
        return self._dynamic_transform_links if self._dynamic_transform_links else []

@dataclass
class ConnectBone(BoneGenerator):
    """Creates a bone connecting point A to point B."""
    bone_a: str
    bone_b: str
    start: str = "head"
    end: str = "head"

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
        
        self._set_parent(new_bone, edit_bones)
        
        created_name = new_bone.name
        
        return [created_name]

@dataclass
class ExtensionBone(BoneGenerator):
    """Creates a bone extending from a source bone in a given direction."""
    bone_a: str
    size_factor: float = 1.0
    axis_type: str = "local"
    axis: str = "Y"
    start: str = "tail"

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

        self._set_parent(new_bone, edit_bones)
        
        created_name = new_bone.name
        
        return [created_name]

@dataclass
class CopyBone(BoneGenerator):
    """Creates a bone by copying the transform of an existing bone."""
    source_bone: str

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

        self._set_parent(new_bone, edit_bones)
        
        created_name = new_bone.name
        return [created_name]
    
@dataclass
class ParallelBone(BoneGenerator):
    """Creates a bone extending from a source bone along an axis until it reaches a target coordinate."""
    bone_a: str
    bone_b: str
    axis_type: str = "local"
    axis: str = "Y"
    coordinate: str = "Y"
    start: str = "tail"
    end: str = "head"

    def generate(self, armature: bpy.types.Object, data: dict | None = None) -> list[str] | None:
        """Generates the ParallelBone extending from bone_a until reaching bone_b's coordinate."""
        if not armature:
            print(f"[AetherBlend] Invalid armature provided for ParallelBone '{self.name}'.")
            return None
        
        edit_bones = armature.data.edit_bones
        bone_a_ref = edit_bones.get(self.bone_a)
        bone_b_ref = edit_bones.get(self.bone_b)

        if not bone_a_ref:
            print(f"[AetherBlend] Reference bone '{self.bone_a}' not found for ParallelBone '{self.name}'.")
            return None
        
        if not bone_b_ref:
            print(f"[AetherBlend] Target bone '{self.bone_b}' not found for ParallelBone '{self.name}'.")
            return None
        
        # Get start position from bone_a
        if self.start == "tail":
            start_pos = bone_a_ref.tail.copy()
        else:  # "head"
            start_pos = bone_a_ref.head.copy()

        # Get target coordinate from bone_b
        if self.end == "tail":
            target_pos = bone_b_ref.tail.copy()
        else:  # "head"
            target_pos = bone_b_ref.head.copy()
        
        # Get the target coordinate value
        coord_index = {"X": 0, "Y": 1, "Z": 2}.get(self.coordinate.upper(), 1)
        target_coord_value = target_pos[coord_index]

        # Calculate direction vector
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
            print(f"[AetherBlend] Invalid axis configuration for ParallelBone '{self.name}': axis_type='{self.axis_type}', axis='{self.axis}'.")
            return None
        
        direction_vector = direction_vector.normalized()
        
        # Calculate the length needed to reach the target coordinate
        # We need to solve: start_pos[coord_index] + t * direction_vector[coord_index] = target_coord_value
        if abs(direction_vector[coord_index]) < 0.0001:
            print(f"[AetherBlend] Direction vector has no component along coordinate '{self.coordinate}' for ParallelBone '{self.name}'. Cannot reach target.")
            return None
        
        t = (target_coord_value - start_pos[coord_index]) / direction_vector[coord_index]
        
        if t < 0:
            print(f"[AetherBlend] Warning: ParallelBone '{self.name}' requires negative extension (t={t}). This may result in unexpected bone direction.")
        
        tail_pos = start_pos + direction_vector * t
        
        if self.name in edit_bones:
            edit_bones.remove(edit_bones[self.name])

        new_bone = edit_bones.new(self.name)
        new_bone.head = start_pos
        new_bone.tail = tail_pos
        new_bone.roll = math.radians(self.roll) if self.roll != 0.0 else 0.0

        self._set_parent(new_bone, edit_bones)

        created_name = new_bone.name
        
        return [created_name]

@dataclass
class SkinBone(BoneGenerator):
    bone_a: str
    size_factor: float = 1.0
    mesh_restriction: str | None = None

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
        
        edit_bones = armature.data.edit_bones
        
        if self.name in edit_bones:
            edit_bones.remove(edit_bones[self.name])
        
        new_bone = edit_bones.new(self.name)
        
        local_co = armature.matrix_world.inverted() @ world_co
        new_bone.head = local_co
        
        direction = mathutils.Vector((0.0, 0.0, bone_length))
        new_bone.tail = local_co + direction
        
        self._set_parent(new_bone, edit_bones)

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
    
@dataclass
class BridgeBone(BoneGenerator):
    #Unlike other generators, BridgeBone's is_connected defines whether the last bone is connected to bone_b
    bone_a: str
    bone_b: str
    offset_factor: mathutils.Vector = field(default_factory=lambda: mathutils.Vector((0.0, 0.0, 0.0)))
    is_connected: bool = field(default=True, kw_only=True)

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
        
        if self.name in edit_bones:
            edit_bones.remove(edit_bones[self.name])

        new_bone = edit_bones.new(self.name)
        new_bone.head = bridge_head
        new_bone.tail = end_pos
        
        bone_a_ref.tail = bridge_head
        new_bone.parent = bone_a_ref
        new_bone.use_connect = True    
            
        self._set_parent(bone_a_ref, edit_bones, is_connected_overrite=False)
        
        if self.is_connected:
            bone_b_ref = edit_bones.get(self.bone_b)
            if bone_b_ref:
                bone_b_ref.parent = new_bone
                bone_b_ref.use_connect = True
            else:
                print(f"[AetherBlend] Warning: Target bone '{self.bone_b}' not found for connection in BridgeBone '{self.name}'.")
        
        created_name = new_bone.name  
        return [created_name]

@dataclass
class CenterBone(BoneGenerator):
    ref_bones: list[str]
    size_factor: float = 1.0
    axis: str = "Z"
    inverted: bool = False

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
        
        self._set_parent(new_bone, edit_bones)

        created_name = new_bone.name
        return [created_name]
