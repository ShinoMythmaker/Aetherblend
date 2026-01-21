from dataclasses import dataclass, field
from abc import ABC, abstractmethod

import bpy

class Constraint(ABC):
    """Abstract base class for all bone constraints."""
    
    @abstractmethod
    def apply(self, pose_bone: bpy.types.PoseBone, armature: bpy.types.Object) -> None:
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

