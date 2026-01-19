from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import math
import mathutils
import re

import bpy

@dataclass(frozen=True)
class MetaRigCollectionInfo:
    name: str
    color_type: str
    row_index: int
    title: str
    visible: bool = True

## Constraints
class Constraint(ABC):
    """Abstract base class for all bone constraints."""
    
    @abstractmethod
    def apply(self, bone: bpy.types.PoseBone, armature: bpy.types.Object) -> None:
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

    def apply(self, bone: bpy.types.PoseBone, armature: bpy.types.Object) -> None:
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

    def apply(self, bone: bpy.types.PoseBone, armature: bpy.types.Object) -> None:
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

    def apply(self, bone: bpy.types.PoseBone, armature: bpy.types.Object) -> None:
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
    target_space: str = "WORLD"
    owner_space: str = "WORLD"
    influence: float = 1.0
    name: str = "AetherBlend_CopyTransform"

    def apply(self, bone: bpy.types.PoseBone, armature: bpy.types.Object) -> None:
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
class AssignCollection(Constraint):
    """Pseudo-constraint that moves bones to a specified collection."""
    collection_name: str = "UnmappedBones"
    state: bool = False 

    def apply(self, bone: bpy.types.PoseBone, armature: bpy.types.Object) -> None:
        """Assigns Bones to specified collection."""
        if bpy.context.object.mode != 'POSE':
            bpy.ops.object.mode_set(mode='POSE')
        
        bone_collections = armature.data.collections
        collection = bone_collections.get(self.collection_name)
        
        if collection is None:
            collection = bone_collections.new(self.collection_name)
            collection.is_visible = self.state
        
        for other_collection in bone.bone.collections:
            other_collection.unassign(bone.bone)
        
        collection.assign(bone.bone)


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

    def apply(self, bone: bpy.types.PoseBone, armature: bpy.types.Object) -> None:
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

    def apply(self, bone: bpy.types.PoseBone, armature: bpy.types.Object, target_override: str | None = None) -> None:
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


@dataclass(frozen=True)
class RelinkConstraints(Constraint):
    "Set the rigify typ basic.raw_copy, set the relink_constraints to true and set the parent bone to the new bone"
    parent_bone: str | None = None

    def apply(self, pose_bone: bpy.types.PoseBone, armature: bpy.types.Object) -> None:
        """Relinks constraints from target bone to the given bone."""
        target_bone_name = self.target_bone
        if not target_bone_name:
            print(f"[AetherBlend] No target bone specified for RelinkConstraints on '{pose_bone.name}'")
            return
        
        pose_bone.rigify_type = 'basic.raw_copy'
            
        if hasattr(pose_bone, 'rigify_parameters'):
            try:
                pose_bone.rigify_parameters.relink_constraints = True
                pose_bone.rigify_parameters.parent_bone = self.parent_bone
            except:
                pass

## LINK Edit Operations 
class LinkEditOperation(ABC):
    """Abstract base class for all link edit operations."""
    
    @abstractmethod
    def execute(self, armature: bpy.types.Object) -> None:
        """Executes the link edit operation on the given armature."""
        pass

@dataclass(frozen=True)
class copyBone(LinkEditOperation):
    bone_name: str
    src_bone_name: str
    parent_bone_name: str | None = None

    def execute(self, armature: bpy.types.Object) -> None:
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
    def execute(self, armature: bpy.types.Object) -> None:
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