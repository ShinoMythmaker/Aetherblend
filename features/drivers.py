import bpy
from abc import ABC
from dataclasses import dataclass, field

@dataclass
class DriverVariable(ABC):
    """Abstract base class for all driver variables."""
    variable_name: str

    def add(self, var, armature):
        """Adds the driver variable to the given driver."""
        pass

@dataclass
class Driver(ABC):
    """Abstract base class for all drivers."""
    driver_variables: list[DriverVariable] #stores a list of all classes that are of type DriverVariable, eg. TransformVariable
    driver_name: str 
    filter_pattern: str | None = None #used to identify the bones that should receive a driver, this is kinda dumb but I don't know a better solution that isn't hardcoded - Oats
    

    def apply_driver(self, pose_bone: bpy.types.PoseBone, armature: bpy.types.Object):
        """Applies the driver to the given bone."""
        pass

    def add_variables(self, f_curve, armature):
        """Adds the driver variables to the given driver."""
        for variable in self.driver_variables:
            var = f_curve.driver.variables.new()
            variable.add(var, armature)

@dataclass
class TransformVariable(DriverVariable):
    variable_target: str | None = None
    transform_type: str = "LOC_X" # Accepted values: LOC_X, LOC_Y, LOC_Z, ROT_X, ROT_Y, ROT_Z, SCALE_X, SCALE_Y, SCALE_Z
    rotation_mode: str | None = None # Refer to rig to decide which mode is appropriate. Accepted values: 'QUATERNION', 'XYZ', 'XZY', 'YXZ', 'YZX', 'ZXY', 'ZYX' — probably
    transform_space: str = "LOCAL SPACE"

    def add(self, var, armature):
            
        var.name = self.variable_name
        var.type = "TRANSFORMS"
        var.targets[0].id = armature
        var.targets[0].bone_target = self.variable_target
        var.targets[0].transform_type = self.transform_type
        var.targets[0].transform_space = self.transform_space
        if self.rotation_mode:
            var.targets[0].rotation_mode = self.rotation_mode
        else:
            return {"FINISHED"}
        return {"FINISHED"}

@dataclass
class TransformDriver(Driver):
    """Contains steps for driver creation."""

    channel_target: str = "location"
    channel_target_index: int = -1  # index correlates to given channel's axis, where -1 defaults to all axes. 0 = X, 1 = Y, 2 = Z except for quaternion rotation, where 0 =  W.
    driver_expression: str = "var + 0.0" # Standard expression. Expression can use basic math operators and in-line conditionals.

    def apply_driver(self, pose_bone: bpy.types.PoseBone, armature: bpy.types.Object):

        bones = armature.pose.bones
        driver_bones = [bone for bone in bones if self.filter_pattern in bone.name] #filter out bones

        for pose_bone in driver_bones:
            f_curve = pose_bone.driver_add(self.channel_target, self.channel_target_index)
            f_curve.driver.expression = self.driver_expression
            self.add_variables(f_curve, armature)

@dataclass
class SkirtDriver(TransformDriver):
    """Driver for skirt bones that uses a custom expression and variable setup."""
    driver_name: str = "Skirt Driver"
    channel_target: str = "rotation_quaternion"
    channel_target_index: int = 1  # Y-axis
    driver_expression: str = "var * 0.5" # Example expression that halves the variable's value
    filter_pattern: str = "j_sk"  # Pattern to identify skirt bones

class AETHER_OT_SetDrivers(bpy.types.Operator):
    """Apply drivers based on filter patterns."""
    bl_idname = "aether.set_drivers"
    bl_label = "Set Drivers"
    bl_description = "Applies all drivers to the bones in the armature based on their filter patterns."
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "Select an armature")
            return {'CANCELLED'}
        
        driver = SkirtDriver(driver_name="Skirt", 
                             channel_target="rotation_quaternion",
                             channel_target_index=1,
                             driver_expression="var * 0.5",
                                filter_pattern="j_sk",
                                driver_variables=[TransformVariable(variable_name="var", variable_target="j_hip", transform_type="LOC_Y", transform_space="LOCAL_SPACE")],
                            )


        driver.apply_driver(self, armature)  # Apply the driver to the armature
        return {'FINISHED'}

def register():
    bpy.utils.register_class(AETHER_OT_SetDrivers)

def unregister():
    bpy.utils.unregister_class(AETHER_OT_SetDrivers)