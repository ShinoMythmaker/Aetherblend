import bpy

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar, Literal

from .shared import PoseOperationsStack

from .constraints import Constraint
from . import rigify
from .. import utils

Mode = Literal["POSE", "EDIT"]
Time = Literal["Pre", "Post"]

class ABOperation(ABC):
    mode: ClassVar[Mode]
    time: Time = "Pre"

    @abstractmethod
    def apply(self, data_bone: bpy.types.Bone, armature: bpy.types.Object):
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

    def _getPoseBone(self, data_bone: bpy.types.Bone, armature: bpy.types.Object) -> bpy.types.PoseBone | None:
        """Gets the corresponding pose bone for the given data bone."""
        try:
            pose_bone = armature.pose.bones.get(data_bone.name)
            if not pose_bone:
                print(f"[AetherBlend] Pose bone '{data_bone.name}' not found in armature '{armature.name}'.")
                return None
            return pose_bone
        except Exception as e:
            print(f"[AetherBlend] Error getting pose bone for '{data_bone.name}': {e}")
            return None

    def _getEditBone(self, data_bone: bpy.types.Bone, armature: bpy.types.Object) -> bpy.types.EditBone | None:
        """Gets the corresponding edit bone for the given data bone."""
        try:
            edit_bone = armature.data.edit_bones.get(data_bone.name)
            if not edit_bone:
                print(f"[AetherBlend] Edit bone '{data_bone.name}' not found in armature '{armature.name}'.")
                return None
            return edit_bone
        except Exception as e:
            print(f"[AetherBlend] Error getting edit bone for '{data_bone.name}': {e}")
            return None

class ABOperationStack:
    STACK_KEYS : ClassVar[tuple[str, ...]] = ('prePOSE', 'postPOSE', 'preEDIT', 'postEDIT')

    def __init__(self):
        self.stack: dict[str, dict[str, list[ABOperation]]] = {
            key: {} for key in self.STACK_KEYS
        }

    def add_operation(self, bone_name: str, operation: ABOperation):
        operationMode = operation.mode
        operationTime = operation.time

        key = f"{operationTime.lower()}{operationMode.upper()}"
        if bone_name not in self.stack[key]:
            self.stack[key][bone_name] = []
        self.stack[key][bone_name].append(operation)

    def merge(self, other_stack: 'ABOperationStack'):
        for key in self.stack.keys():
            for bone_name, operations in other_stack.stack[key].items():
                if bone_name not in self.stack[key]:
                    self.stack[key][bone_name] = []
                self.stack[key][bone_name].extend(operations)

    def applyPrePoseOperations(self, armature: bpy.types.Object):
        self._apply_operations(self.stack['prePOSE'], armature, "POSE")

    def applyPostPoseOperations(self, armature: bpy.types.Object):
        self._apply_operations(self.stack['postPOSE'], armature, "POSE")

    def applyPreEditOperations(self, armature: bpy.types.Object):
        self._apply_operations(self.stack['preEDIT'], armature, "EDIT")

    def applyPostEditOperations(self, armature: bpy.types.Object):
        self._apply_operations(self.stack['postEDIT'], armature, "EDIT")

    def _addPoseOperationStack(self, pose_ops_stack: PoseOperationsStack):
        for bone_name, operations in pose_ops_stack.stack.items():
            for operation in operations:
                if operation.rigify_settings:
                    rigify_op = RigifyTypeOperation(operation.rigify_settings)
                    self.add_operation(bone_name, rigify_op)
                
                if operation.constraints:
                    constraintList = operation.constraints
                    for constraint in constraintList:
                        constraint_op = ConstraintOperation(constraint)
                        self.add_operation(bone_name, constraint_op)
                
                if operation.b_collection:
                    collection_op = CollectionOperation(operation.b_collection)
                    self.add_operation(bone_name, collection_op)

    def _apply_operations(self, operations: dict[str, list[ABOperation]], armature: bpy.types.Object, mode: Mode):
        if not operations:
            return

        current_mode = bpy.context.mode.upper()
        if current_mode.startswith("EDIT"):
            current_mode = "EDIT"
        elif current_mode.startswith("POSE"):
            current_mode = "POSE"

        if current_mode != mode:
            try:
                bpy.ops.object.mode_set(mode=mode)
            except Exception as e:
                print(f"[AetherBlend] Error switching to {mode} mode: {e}")
                return

        for bone_name, ops in operations.items():
            data_bone = armature.data.bones.get(bone_name)
            if not data_bone:
                print(f"[AetherBlend] Bone '{bone_name}' not found in armature '{armature.name}'.")
                continue

            for operation in ops:
                operation.apply(data_bone, armature)

@dataclass(frozen=True)
class ConstraintOperation(ABOperation):
    mode: ClassVar[Mode] = "POSE"

    constraint: Constraint

    def apply(self, data_bone: bpy.types.Bone, armature: bpy.types.Object):
        """Applies the constraint operation to the given pose bone."""
        if not self._switch_mode():
            return
        poseBone = self._getPoseBone(data_bone, armature)
        if not poseBone:
            return
        try:
            self.constraint.apply(poseBone, armature)
        except Exception as e:
            print(f"[AetherBlend] Error applying ConstraintOperation for bone '{data_bone.name}': {e}")

@dataclass(frozen=True)
class RigifyTypeOperation(ABOperation):
    mode: ClassVar[Mode] = "POSE"

    rigify_type: rigify.types.rigify_type

    def apply(self, data_bone: bpy.types.Bone, armature: bpy.types.Object):
        """Applies the Rigify type operation to the given pose bone."""
        if not self._switch_mode():
            return
        poseBone = self._getPoseBone(data_bone, armature)
        if not poseBone:
            return
        try:
            self.rigify_type.apply(poseBone, armature)
        except Exception as e:
            print(f"[AetherBlend] Error applying RigifyTypeOperation for bone '{data_bone.name}': {e}")

@dataclass(frozen=True)
class CollectionOperation(ABOperation):
    mode: ClassVar[Mode] = "POSE"

    collection_name: str

    def apply(self, data_bone: bpy.types.Bone, armature: bpy.types.Object):
        """Applies the collection operation to the given pose bone."""
        if not self._switch_mode():
            return
        poseBone = self._getPoseBone(data_bone, armature)
        if not poseBone:
            return
        try:
            utils.armature.b_collection.assign_bones(armature, [poseBone.name], self.collection_name)
        except Exception as e:
            print(f"[AetherBlend] Error applying CollectionOperation for bone '{data_bone.name}': {e}")




    

