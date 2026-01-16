import bpy
import math
import mathutils # type: ignore

from dataclasses import dataclass, field
from abc import ABC, abstractmethod

from .. import utils
from . import rigify

@dataclass
class PoseOperations:
    """Groups all pose mode operations for a single bone."""
    rigify_settings: rigify.types.rigify_type | None = None
    b_collection: str | None = None

class BoneGenerator(ABC):
    """Base interface for all bone generation types."""
    # These fields will be defined in child dataclasses
    name: str
    parent: str | None = None
    is_connected: bool = False
    roll: float = 0.0
    req_bones: list[str] | None = None
    pose_operations: PoseOperations | None = None
    is_optional: bool = False
    
    @abstractmethod
    def generate(self, armature: bpy.types.Object, data: dict | None = None) -> list[str] | None:
        """Generates the bone and returns the created bone name(s)."""
        pass


@dataclass
class BoneGroup:
    """A group of bone generators that can be executed together."""
    name: str
    bones: list[BoneGenerator]
    description: str = ""
    
    def check(self, armature: bpy.types.Object) -> bool:
        """Check if all required bones exist in the armature for this bone group."""
        future_bones = []
        
        for bone_gen in self.bones:
            future_bones.append(bone_gen.name)
            
            if bone_gen.req_bones:
                for req_bone in bone_gen.req_bones:
                    # Check if bone will be created in this group or already exists
                    if req_bone not in future_bones:
                        if req_bone not in armature.data.bones:
                            if bone_gen.is_optional:
                                future_bones.remove(bone_gen.name)
                                continue
                            return False
        return True
    
    def generate(self, armature: bpy.types.Object, data: dict | None = None) -> list[str]:
        """Generate all bones in this group."""
        generated_bones = []
        
        for bone_gen in self.bones:
            new_bones = bone_gen.generate(armature, data=data)
            if new_bones:
                generated_bones.extend(new_bones)
        
        return generated_bones
    
    def execute(self, armature: bpy.types.Object, data: dict | None = None) -> tuple[list[str], dict[str, list[PoseOperations]]]:
        """Execute the full generation process for this bone group."""
        # Check if all required bones exist
        if not self.check(armature):
            print(f"[AetherBlend] BoneGroup '{self.name}' check failed - missing required bones")
            return [], {}
        
        # Switch to edit mode if needed
        current_mode = bpy.context.object.mode if bpy.context.object else None
        if current_mode != 'EDIT':
            bpy.ops.object.mode_set(mode='EDIT')
        
        # Generate bones
        generated_bones = self.generate(armature, data=data)
        
        # Collect pose operations by bone name (allowing multiple operations per bone)
        pose_operations_dict: dict[str, list[PoseOperations]] = {}
        
        for bone_gen in self.bones:
            # Only add to dict if there are operations to perform
            if bone_gen.pose_operations:
                if bone_gen.name not in pose_operations_dict:
                    pose_operations_dict[bone_gen.name] = []
                pose_operations_dict[bone_gen.name].append(bone_gen.pose_operations)
        
        return generated_bones, pose_operations_dict


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
    pose_operations: PoseOperations | None = None
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
    pose_operations: PoseOperations | None = None
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
        
        print(f"[DEBUG] direction_vector: {direction_vector}")
        
        ref_bone_length = bone_a_ref.length if bone_a_ref.length > 0 else 1.0
        extension_length = ref_bone_length * self.size_factor
        tail_pos = start_pos + direction_vector.normalized() * extension_length
        
        print(f"[DEBUG] Creating bone with head={start_pos}, tail={tail_pos}, roll={self.roll}")
        
        if self.name in edit_bones:
            edit_bones.remove(edit_bones[self.name])

        new_bone = edit_bones.new(self.name)
        new_bone.head = start_pos
        new_bone.tail = tail_pos
        new_bone.roll = math.radians(self.roll) if self.roll != 0.0 else 0.0

        print(f"[DEBUG] Bone created successfully, setting parent to '{self.parent}'")

        if self.parent:
            if isinstance(self.parent, list):
                for bone_name in self.parent:
                    parent_bone = edit_bones.get(bone_name)
                    if parent_bone and parent_bone != new_bone:
                        break
            else :
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
    pose_operations: PoseOperations | None = None
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
