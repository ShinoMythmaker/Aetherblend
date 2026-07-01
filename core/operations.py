import bpy
import math
import mathutils

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import ClassVar, Literal

from .drivers import Driver
from .custom_properties import CustomProperty

from .constraints import Constraint, CopyTransformsConstraint
from . import rigify
from .. import utils

Mode = Literal["POSE", "EDIT"]
Time = Literal["Pre", "Post"]

_WGTS = "WGTS"

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

    def remove_bones(self, bone_names: set[str]) -> None:
        """Removes queued pose operations for bones that were explicitly deleted."""
        if not bone_names:
            return

        for bone_name in bone_names:
            self.stack.pop(bone_name, None)

    def execute(self, armature: bpy.types.Object):
        """Executes all PoseOperations in the stack on the corresponding bones."""
        for bone_name, ops_list in self.stack.items():
            pose_bone = armature.pose.bones.get(bone_name)
            if pose_bone:
                for ops in ops_list:
                    ops.execute(pose_bone, armature)
            else:
                print(f"[AetherBlend] PoseOperationsStack: Bone '{bone_name}' not found in armature.")

@dataclass()
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
    generation_data: dict | None = None

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

    def remove_bones(self, bone_names: set[str]) -> None:
        """Removes queued operations that target bones that were explicitly deleted."""
        if not bone_names:
            return

        for key, operations in self.stack.items():
            self.stack[key] = [
                operation
                for operation in operations
                if not (hasattr(operation, "bone_name") and getattr(operation, "bone_name") in bone_names)
            ]

    def applyPrePoseOperations(self, armature: bpy.types.Object):
        self._apply_operations(self.stack['prePOSE'], armature,)

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
            operation.apply(armature, self.generation_data)

@dataclass()
class ConstraintOperation(ABOperation):
    mode: ClassVar[Mode] = "POSE"

    bone_name: str
    constraint: Constraint

    def apply(self, armature: bpy.types.Object, data_dict: dict | None = None):
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

@dataclass()
class RigifyTypeOperation(ABOperation):
    mode: ClassVar[Mode] = "POSE"

    bone_name: str
    rigify_type: rigify.types.rigify_type

    def apply(self, armature: bpy.types.Object, data_dict: dict | None = None):
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

@dataclass
class TransformLink:
    """Links a bone to a target for rigging purposes."""
    target: str
    bone: str
    retarget: str | None = None
    constraint: Constraint | None = None

    def mark_linked(self, armature: bpy.types.Object) -> None:
        """Marks the bone as linked in the armature's data."""
        bone = armature.data.bones.get(self.bone)
        if bone:
            bone["ab_linked"] = True

    def to_pose_operations(self) -> dict[str, list[PoseOperations]]:
        """Convert this TransformLink to PoseOperations."""
        pose_operations_dict: dict[str, list[PoseOperations]] = {}
        ff_bone = self.bone
        link_bone = f"LINK-{ff_bone}"
        constraint = self.constraint if self.constraint is not None else CopyTransformsConstraint(link_bone, name=f"AB-LINK@LINK-{ff_bone}", remove_target_shear=True)
        if ff_bone not in pose_operations_dict:
            pose_operations_dict[ff_bone] = []
        pose_operations_dict[ff_bone].append(
            PoseOperations(
                constraints=[constraint]
            )
        )

        if link_bone not in pose_operations_dict:
            pose_operations_dict[link_bone] = []
        pose_operations_dict[link_bone].append(
            PoseOperations(
                rigify_settings=rigify.types.basic_raw_copy(True, self.target)
            )
        )
        return pose_operations_dict
    
    def to_ABOperation(self) -> list[ABOperation]:
        """Convert this TransformLink to an ABOperation."""
        ops = []
        ff_bone = self.bone
        link_bone = f"LINK-{ff_bone}"

        constraint = self.constraint if self.constraint is not None else CopyTransformsConstraint(link_bone, name=f"AB-LINK@LINK-{ff_bone}", remove_target_shear=True)
        ops.append(ConstraintOperation(ff_bone, constraint=constraint))

        rigify_op = rigify.types.basic_raw_copy(True, self.target)
        ops.append(RigifyTypeOperation(link_bone, rigify_type=rigify_op))

        return ops

@dataclass()
class CollectionOperation(ABOperation):
    mode: ClassVar[Mode] = "POSE"

    bone_name: str
    collection_name: str

    def apply(self, armature: bpy.types.Object, data_dict: dict | None = None):
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

@dataclass()
class ParentBoneOperation(ABOperation):
    bone_name: str
    parent: tuple[str, ...]
    is_connected: bool = False
    
    mode: ClassVar[Mode] = "EDIT"

    def apply(self, armature: bpy.types.Object, data_dict: dict | None = None):
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
            editBone.use_connect = self.is_connected
            editBone.parent = parent_bone
        except Exception as e:
            print(f"[AetherBlend] Error applying ParentBoneOperation for bone '{self.bone_name}': {e}")

@dataclass()
class DriverOperation(ABOperation):
    mode: ClassVar[Mode] = "POSE"
    bone_name: str = field(default=None, kw_only=True)
    constraint_name: str = field(default=None, kw_only=True)
    driver_name: str
    property: tuple[str, int] | str
    driver: Driver
    data: str | None = None ## Optional for referencing data blocks

    def apply(self, armature: bpy.types.Object, data_dict: dict | None = None):
        """Applies the driver operation to the given pose bone."""
        if not self._switch_mode():
            return
        target = armature
        if self.data is None and self.bone_name is not None:          
            poseBone = self._getPoseBone(self.bone_name, armature)
            target = poseBone
            if self.constraint_name is not None:
                constraint = poseBone.constraints.get(self.constraint_name)
                if constraint:
                    target = constraint
        elif self.data is not None:
            data_block = data_dict.get(self.data) if data_dict else None
            if data_block is None:
                return
            target = data_block
        try:
            self.driver.apply(target, self.property, armature)
        except Exception as e:
            print(f"[AetherBlend] Error applying DriverOperation for target '{target.name if hasattr(target, 'name') else target}': {e}")

@dataclass()
class CustomPropertyOperation(ABOperation):
    mode: ClassVar[Mode] = "POSE"

    property: CustomProperty
    bone_name: str | None = None

    def apply(self, armature: bpy.types.Object, data_dict: dict | None = None):
        """Creates a custom property for a given bone or armature"""
        if not self._switch_mode():
            return
        
        try:
            target = armature.data
            if self.bone_name:
                poseBone = self._getPoseBone(self.bone_name, armature)
                if not poseBone:
                    return
                target = poseBone

            self.property.apply(target=target)

        except Exception as e:
            print(f"[AetherBlend] Error applying CustomPropertyOperation for armature. : {e}")

@dataclass()
class WidgetOperation(ABOperation):
    """Overrides the widget of a bone."""
    mode: ClassVar[Mode] = "POSE"
    time : Time = field(default="Post", kw_only=True)

    bone_name: str
    color_set: str | None = None
    custom_color_normal: tuple[float, float, float] | None = None
    custom_color_select: tuple[float, float, float] | None = None
    custom_color_active: tuple[float, float, float] | None = None
    custom_object: str | None = None
    translation: tuple[float, float, float] = (0.0, 0.0, 0.0)
    rotation: tuple[float, float, float] = (0.0, 0.0, 0.0)
    scale: tuple[float, float, float] = (1.0, 1.0, 1.0)
    scale_factor: float = 1.0
    override_transform: str | None = None  # Bone Name
    affect_gizmo: bool = False
    use_as_pivot: bool = False
    scale_to_bone_length: bool = True
    wireframe: bool = False
    wire_width: float = 1.0


    def apply(self, armature: bpy.types.Object, data_dict: dict | None = None) -> None:
        """Applies the widget override to the given pose bone."""
        pose_bone = armature.pose.bones.get(self.bone_name)
        if not pose_bone:
            print(f"[AetherBlend] WidgetOperation bone '{self.bone_name}' not found in armature.")
            return
        
        
        
        scale = (self.scale[0] * self.scale_factor, self.scale[1] * self.scale_factor, self.scale[2] * self.scale_factor)

        degree = [math.radians(self.rotation[0]), math.radians(self.rotation[1]), math.radians(self.rotation[2])] 

        try:
            if self.color_set:
                pose_bone.color.palette = self.color_set
                if self.color_set == "CUSTOM":
                    if self.custom_color_normal:
                        pose_bone.color.custom.normal =  mathutils.Color(self.custom_color_normal)
                    if self.custom_color_select:
                        pose_bone.color.custom.select = mathutils.Color(self.custom_color_select)
                    if self.custom_color_active:
                        pose_bone.color.custom.active = mathutils.Color(self.custom_color_active)
            if self.custom_object:
                custom_object_name = self._searchWGTS(armature, self.custom_object)
                custom_shape_obj = bpy.data.objects.get(custom_object_name) if custom_object_name else None

                # Always reassign the custom shape when a custom object is requested.
                pose_bone.custom_shape = custom_shape_obj
                if not custom_shape_obj:
                    print(f"[AetherBlend] WidgetOperation custom object '{self.custom_object}' not found in WGTS collection of armature '{armature.name}'.")
            pose_bone.custom_shape_translation = self.translation
            pose_bone.custom_shape_rotation_euler = degree
            pose_bone.custom_shape_scale_xyz = scale
            pose_bone.custom_shape_transform = self.override_transform
            pose_bone.use_transform_at_custom_shape = self.affect_gizmo      ## 5.0
            pose_bone.use_transform_around_custom_shape = self.use_as_pivot  ## 5.0
            pose_bone.use_custom_shape_bone_size = self.scale_to_bone_length
            ##pose_bone.show_wire = self.wireframe  ## 5.0
            pose_bone.custom_shape_wire_width = self.wire_width
        except Exception as e:
            print(f"[AetherBlend] Error applying WidgetOperation for bone '{pose_bone.name}': {e}")

    @staticmethod
    def _searchWGTS(armature, name: str) -> str | None:
        """Searches for a widget object in the WGTS collection of the armature."""
        search_name = name.strip()
        if not search_name:
            return None

        expected_widget_name = search_name if search_name.startswith("AB_WGT_") else f"AB_WGT_{search_name}"

        local_collections: list[bpy.types.Collection] = []
        for armature_collection in armature.users_collection:
            local_collections.extend(utils.collection.collection_tree(armature_collection))

        matcher = lambda object_name: object_name == expected_widget_name

        found_name = utils.collection.find_object_name_in_prefixed_collections(
            local_collections,
            _WGTS,
            matcher,
        )
        if found_name:
            return found_name

        # Fallback: search all WGTS collections in the blend file.
        global_collections = [collection for collection in bpy.data.collections if collection.name.upper().startswith("WGTS")]
        found_name = utils.collection.find_object_name_in_prefixed_collections(
            global_collections,
            _WGTS,
            matcher,
        )
        if found_name:
            return found_name

        print(f"[AetherBlend] WidgetOperation: No matching WGTS widget '{expected_widget_name}' found for armature '{armature.name}'.")
        return None

    @staticmethod
    def _normalizeWidgetName(name: str) -> str:
        normalized_name = name.strip().lower()
        for separator in (".", "_", "-", " "):
            normalized_name = normalized_name.replace(separator, "")
        return normalized_name
    

@dataclass()
class BoneRestrictionOperation(ABOperation):
    mode: ClassVar[Mode] = "POSE"

    bone_name: str
    hide_select: bool | None = None
    hide: bool | None = None
    lock_location: tuple[bool, bool, bool] | bool | None = None
    lock_rotation: tuple[bool, bool, bool] | bool | None = None
    lock_scale: tuple[bool, bool, bool] | bool | None = None
    inherit_location: bool | None = None
    inherit_rotation: bool | None = None
    inherit_scale: Literal["FULL", "FIX_SHEAR", "ALIGNED", "AVERAGE", "NONE", "NONE_LEGACY"] | None = None

    def apply(self, armature: bpy.types.Object, data_dict: dict | None = None):
        """Applies the bone restriction to the given pose bone."""
        if not self._switch_mode():
            return
        poseBone = self._getPoseBone(self.bone_name, armature)
        dataBone = armature.data.bones.get(self.bone_name)
        if not poseBone or not dataBone:
            return
        if self.hide_select is not None:
            dataBone.hide_select = self.hide_select
        if self.hide is not None:
            poseBone.hide = self.hide
            dataBone.hide = self.hide
        if isinstance(self.lock_location, bool):
            lock_location = (self.lock_location, self.lock_location, self.lock_location)
        else:            
            lock_location = self.lock_location

        if isinstance(self.lock_rotation, bool):
            lock_rotation = (self.lock_rotation, self.lock_rotation, self.lock_rotation)
        else:            
            lock_rotation = self.lock_rotation

        if isinstance(self.lock_scale, bool):
            lock_scale = (self.lock_scale, self.lock_scale, self.lock_scale)
        else:            
            lock_scale = self.lock_scale

        try:
            if self.lock_location is not None:
                poseBone.lock_location = lock_location
            if self.lock_rotation is not None:
                poseBone.lock_rotation = lock_rotation
            if self.lock_scale is not None:
                poseBone.lock_scale = lock_scale
            if self.inherit_location is not None:
                dataBone.use_local_location = self.inherit_location
            if self.inherit_rotation is not None:
                dataBone.use_inherit_rotation = self.inherit_rotation
            if self.inherit_scale is not None:
                dataBone.inherit_scale = self.inherit_scale
            # Add more restriction types as needed
        except Exception as e:
            print(f"[AetherBlend] Error applying BoneRestrictionOperation for bone '{self.bone_name}': {e}")

@dataclass()
class PoseBoneOperation(ABOperation):
    """Poses a bone by setting its location, rotation, and scale."""
    mode: ClassVar[Mode] = "POSE"
    time : Time = field(default="Post", kw_only=True)

    bone_name: str
    location: tuple[float, float, float] | None = None
    rotation: tuple[float, float, float] | None = None
    scale: tuple[float, float, float] | None = None

    def apply(self, armature: bpy.types.Object, data_dict: dict | None = None):
        """Poses a bone by setting its location, rotation, and scale."""
        if not self._switch_mode():
            return
        poseBone = self._getPoseBone(self.bone_name, armature)
        if not poseBone:
            return
        if self.location:
            poseBone.location = self.location
        if self.rotation:
            poseBone.rotation_euler = [math.radians(angle) for angle in self.rotation]
        if self.scale:
            poseBone.scale = self.scale


@dataclass
class PropOverrideOperation(ABOperation):
    """Overrides a custom property of a bone."""
    mode: ClassVar[Mode] = "POSE"
    time : Time = field(default="Post", kw_only=True)

    bone_name: str
    property_name: str
    value: float | int | str | bool

    def apply(self, armature: bpy.types.Object, data_dict: dict | None = None) -> None:
        """Applies the property override to the given pose bone."""
        if not self._switch_mode():
            return
        poseBone = self._getPoseBone(self.bone_name, armature)
        if not poseBone:
            return
        ## Alternatively in the futuire we could use data dict in here to target properties from speicifc objects
        ## however im too lazye to implement that rn, an example is in the driver opoperation - Shino
        if not poseBone:
            print(f"[AetherBlend] PropOverride bone '{self.bone_name}' not found in armature.")
            return
        
        try:
            poseBone[self.property_name] = self.value
        except Exception as e:
            print(f"[AetherBlend] Error applying PropOverride for bone '{poseBone.name}': {e}")

    

