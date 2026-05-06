from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Literal, ClassVar
import bpy

DriverType = Literal['AVERAGE', 'SUM', 'SCRIPTED', 'MIN', 'MAX']
VariableType = Literal['SINGLE_PROP', 'TRANSFORMS', 'ROTATION_DIFF', 'LOC_DIFF', 'CONTEXT_PROP']

TransformType = Literal['LOC_X', 'LOC_Y', 'LOC_Z', 'ROT_X', 'ROT_Y', 'ROT_Z', 'ROT_W', 'SCALE_X', 'SCALE_Y', 'SCALE_Z', 'SCALE_AVG']
RotationMode = Literal['AUTO', 'XYZ', 'XZY', 'YXZ', 'YZX', 'ZXY', 'ZYX', 'QUATERNION', 'SWING_TWIST_X', 'SWING_TWIST_Y', 'SWING_TWIST_Z']
SpaceType = Literal['WORLD_SPACE', 'TRANSFORM_SPACE', 'LOCAL_SPACE']
ContextProperty = Literal['ACTIVE_VIEW_LAYER', 'ACTIVE_SCENE']


class DriverVariable(ABC):
    """Abstract base class for driver variables."""
    name: str
    type: ClassVar[VariableType]

    @abstractmethod
    def add(self, driver: bpy.types.FCurve) -> bpy.types.FCurve:
        """Adds the variable to the given driver."""
        pass

@dataclass()
class Driver():
    """Universal Driver Class"""
    type: DriverType
    expression: str | None = None
    use_self: bool | None = None
    variables: list[DriverVariable]
    
    def apply(self, pose_bone: bpy.types.PoseBone, property: tuple[str, int], armature: bpy.types.Object) -> None:
        """Applies the driver to the given bone."""

        driver = pose_bone.driver_add(property[0], property[1])

        if self.expression is not None:
            driver.driver.expression = self.expression

        if self.use_self is not None:
            driver.driver.use_self = self.use_self

        for variable in self.variables:
            variable.add(driver, armature)

####################################################
# Driver Variables 
####################################################

@dataclass(frozen=True)
class TransfromChannelVariable(DriverVariable):
    """Driver variable for a transform channel."""
    type: ClassVar[VariableType] = 'TRANSFORMS'

    target_bone: str | None = None
    transform_type: TransformType | None = None
    rotation_mode: RotationMode | None = None
    transform_space: SpaceType | None = None
    context_property: ContextProperty | None = None
    use_fallback_value: bool | None = None
    fallback_value: float | None = None

    def add(self, driver: bpy.types.FCurve, armature: bpy.types.Object) -> bpy.types.FCurve:
        var = driver.driver.variables.new()
        var.name = self.name
        var.type = 'TRANSFORMS'

        d_target = var.targets[0]

        if armature is not None:
            d_target.id = armature
        else:
            print(f"[AetherBlend] Warning: Armature not found for driver variable '{self.name}'. Driver may not work as expected.")
            return driver
            
        if self.target_bone is not None:
            d_target.bone_target = self.target_bone
        if self.transform_type is not None:
            d_target.transform_type = self.transform_type
        if self.transform_space is not None:
            d_target.transform_space = self.transform_space
        if self.rotation_mode is not None:
            d_target.rotation_mode = self.rotation_mode
        if self.context_property is not None:
            d_target.context_property = self.context_property
        if self.use_fallback_value is not None:
            d_target.use_fallback_value = self.use_fallback_value
        if self.fallback_value is not None:
            d_target.fallback_value = self.fallback_value

        return driver

