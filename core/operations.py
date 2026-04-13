import bpy

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import ClassVar, Literal

from .constraints import Constraint
from . import rigify
from .. import utils

Mode = Literal["POSE", "EDIT"]
Time = Literal["Pre", "Post"]

@dataclass
class PoseOperations:
    """Groups all pose mode operations for a single bone."""
    rigify_settings: 'rigify.types.rigify_type | None' = None
    constraints: 'list[Constraint] | None' = None
    b_collection: str | None = None

    def execute(self, pose_bone: bpy.types.PoseBone, armature: bpy.types.Object):
        """Executes all pose operations on the given pose bone."""
        try:
            if self.rigify_settings:
                self.rigify_settings.apply(pose_bone, armature)
            
            if self.constraints:
                for constraint in self.constraints:
                    constraint.apply(pose_bone, armature)
            
            if self.b_collection:
                utils.armature.b_collection.assign_bones(armature, [pose_bone.name], self.b_collection)
        except Exception as e:
            print(f"[AetherBlend] Error executing PoseOperations for bone: {e}")

class PoseOperationsStack:
    """Holds function for merging multiple PoseOperations into one dictionary"""

    stack: dict[str, list[PoseOperations]]
    
    def __init__(self, stack: dict[str, list[PoseOperations]] | None = None):
        self.stack = stack if stack is not None else {}

    def add(self, bone_name: str, operations: PoseOperations):
        """Adds PoseOperations to the stack for a specific bone."""
        if bone_name not in self.stack:
            self.stack[bone_name] = []
        self.stack[bone_name].append(operations)

    def merge(self, diff: 'PoseOperationsStack'):
        """Merges multiple PoseOperations into one dictionary"""
        for bone_name, ops_list in diff.stack.items():
            if bone_name not in self.stack:
                self.stack[bone_name] = []
            self.stack[bone_name].extend(ops_list)

    def execute(self, armature: bpy.types.Object):
        """Executes all PoseOperations in the stack on the corresponding bones."""
        for bone_name, ops_list in self.stack.items():
            pose_bone = armature.pose.bones.get(bone_name)
            if pose_bone:
                for ops in ops_list:
                    ops.execute(pose_bone, armature)
            else:
                print(f"[AetherBlend] PoseOperationsStack: Bone '{bone_name}' not found in armature.")

@dataclass(frozen=True)
class ABOperation(ABC):
    mode: ClassVar[Mode] = "POSE"
    time: Time = field(default="Pre", kw_only=True)

    @abstractmethod
    def apply(self, armature: bpy.types.Object):
        """Apply the operation to the given bone."""
        raise NotImplementedError

    def _switch_mode(self) -> bool:
        """Switches the current mode to the operation's mode if necessary."""
        current_mode = bpy.context.mode.upper()
        if current_mode.startswith("EDIT"):
            current_mode = "EDIT"
        elif current_mode.startswith("POSE"):
            current_mode = "POSE"

        if current_mode != self.mode:
            try:
                bpy.ops.object.mode_set(mode=self.mode)
                return True
            except Exception as e:
                print(f"[AetherBlend] Error switching to {self.mode} mode: {e}")
                return False
        return True

    def _getPoseBone(self, bone_name: str, armature: bpy.types.Object) -> bpy.types.PoseBone | None:
        """Gets the corresponding pose bone for the given data bone."""
        try:
            pose_bone = armature.pose.bones.get(bone_name)
            if not pose_bone:
                print(f"[AetherBlend] Pose bone '{bone_name}' not found in armature '{armature.name}'.")
                return None
            return pose_bone
        except Exception as e:
            print(f"[AetherBlend] Error getting pose bone for '{bone_name}': {e}")
            return None

    def _getEditBone(self, bone_name: str, armature: bpy.types.Object) -> bpy.types.EditBone | None:
        """Gets the corresponding edit bone for the given data bone."""
        try:
            edit_bone = armature.data.edit_bones.get(bone_name)
            if not edit_bone:
                print(f"[AetherBlend] Edit bone '{bone_name}' not found in armature '{armature.name}'.")
                return None
            return edit_bone
        except Exception as e:
            print(f"[AetherBlend] Error getting edit bone for '{bone_name}': {e}")
            return None

class ABOperationStack:
    STACK_KEYS : ClassVar[tuple[str, ...]] = ('prePOSE', 'postPOSE', 'preEDIT', 'postEDIT')

    def __init__(self):
        self.stack: dict[str, list[ABOperation]] = {
            key: [] for key in self.STACK_KEYS
        }

    def add_operation(self, operation: ABOperation):
        operationMode = operation.mode
        operationTime = operation.time

        key = f"{operationTime.lower()}{operationMode.upper()}"
        self.stack[key].append(operation)

    def merge(self, other_stack: 'ABOperationStack'):
        for key in self.stack.keys():
            self.stack[key].extend(other_stack.stack[key])

    def applyPrePoseOperations(self, armature: bpy.types.Object):
        self._apply_operations(self.stack['prePOSE'], armature)

    def applyPostPoseOperations(self, armature: bpy.types.Object):
        self._apply_operations(self.stack['postPOSE'], armature)

    def applyPreEditOperations(self, armature: bpy.types.Object):
        self._apply_operations(self.stack['preEDIT'], armature)

    def applyPostEditOperations(self, armature: bpy.types.Object):
        self._apply_operations(self.stack['postEDIT'], armature)

    def _addPoseOperationStack(self, pose_ops_stack: PoseOperationsStack):
        for bone_name, operations in pose_ops_stack.stack.items():
            for operation in operations:
                if operation.rigify_settings:
                    rigify_op = RigifyTypeOperation(bone_name, operation.rigify_settings)
                    self.add_operation(rigify_op)
                
                if operation.constraints:
                    constraintList = operation.constraints
                    for constraint in constraintList:
                        constraint_op = ConstraintOperation(bone_name, constraint)
                        self.add_operation(constraint_op)
                
                if operation.b_collection:
                    collection_op = CollectionOperation(bone_name, operation.b_collection)
                    self.add_operation(collection_op)

    def _apply_operations(self, operations: list[ABOperation], armature: bpy.types.Object):
        if not operations:
            return

        for operation in operations:
            operation.apply(armature)

@dataclass(frozen=True)
class ConstraintOperation(ABOperation):
    mode: ClassVar[Mode] = "POSE"

    bone_name: str
    constraint: Constraint

    def apply(self, armature: bpy.types.Object):
        """Applies the constraint operation to the given pose bone."""
        if not self._switch_mode():
            return
        poseBone = self._getPoseBone(self.bone_name, armature)
        if not poseBone:
            return
        try:
            self.constraint.apply(poseBone, armature)
        except Exception as e:
            print(f"[AetherBlend] Error applying ConstraintOperation for bone '{self.bone_name}': {e}")

@dataclass(frozen=True)
class RigifyTypeOperation(ABOperation):
    mode: ClassVar[Mode] = "POSE"

    bone_name: str
    rigify_type: rigify.types.rigify_type

    def apply(self, armature: bpy.types.Object):
        """Applies the Rigify type operation to the given pose bone."""
        if not self._switch_mode():
            return
        poseBone = self._getPoseBone(self.bone_name, armature)
        if not poseBone:
            return
        try:
            self.rigify_type.apply(poseBone, armature)
        except Exception as e:
            print(f"[AetherBlend] Error applying RigifyTypeOperation for bone '{self.bone_name}': {e}")

@dataclass(frozen=True)
class CollectionOperation(ABOperation):
    mode: ClassVar[Mode] = "POSE"

    bone_name: str
    collection_name: str

    def apply(self, armature: bpy.types.Object):
        """Applies the collection operation to the given pose bone."""
        if not self._switch_mode():
            return
        poseBone = self._getPoseBone(self.bone_name, armature)
        if not poseBone:
            return
        try:
            utils.armature.b_collection.assign_bones(armature, [poseBone.name], self.collection_name)
        except Exception as e:
            print(f"[AetherBlend] Error applying CollectionOperation for bone '{self.bone_name}': {e}")

@dataclass(frozen=True)
class ParentBoneOperation(ABOperation):
    bone_name: str
    parent: tuple[str, ...]
    is_connected: bool = False
    
    mode: ClassVar[Mode] = "EDIT"

    def apply(self, armature: bpy.types.Object):
        """Applies the parent bone operation to the given edit bone."""
        if not self._switch_mode():
            return
        editBone = self._getEditBone(self.bone_name, armature)
        if not editBone:
            return
        parent_bone = None 
        for parent_name in self.parent:
                parent_bone = self._getEditBone(parent_name, armature)
                if parent_bone:
                    break
                
        if not parent_bone:
            parent_names_str = ", ".join(self.parent)
            print(f"[AetherBlend] ParentBoneOperation: None of the specified parent bones '{parent_names_str}' were found for bone '{self.bone_name}' in armature '{armature.name}'.")
            return

        try:
            editBone.parent = parent_bone
            editBone.use_connect = self.is_connected
        except Exception as e:
            print(f"[AetherBlend] Error applying ParentBoneOperation for bone '{self.bone_name}': {e}")


    

