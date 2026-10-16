"""Driver instruction: drive a property of a bone with an expression."""
from collections.abc import Mapping
from typing import NamedTuple

import bpy

from .... import utils


class TransformVariable(NamedTuple):
    """A driver variable that reads one transform channel of a bone, by default of the rig itself."""

    bone: str
    channel: str  # e.g. "ROT_X", "LOC_Y", "SCALE_Z"
    rotation_mode: str = "QUATERNION"
    space: str = "LOCAL_SPACE"
    source: bpy.types.Object | None = None  # another armature to read from instead of the rig


class PropertyVariable(NamedTuple):
    """A driver variable that reads a custom property of the armature data (see armature_prop)."""

    property_name: str


def driver(
    rig: bpy.types.Object,
    bone: str,
    property_path: str,
    *,
    index: int = -1,
    constraint: str | None = None,
    expression: str,
    variables: Mapping[str, TransformVariable | PropertyVariable],
) -> None:
    """Drive a property of a bone (for example "rotation_quaternion" with an index) by a scripted expression.

    With `constraint`, the property belongs to that constraint of the bone (for example "influence").
    """
    pose_bone = utils.armature.get_pose_bone(rig, bone)
    if not pose_bone:
        return

    owner = pose_bone
    if constraint:
        owner = pose_bone.constraints.get(constraint)
        if not owner:
            print(f"[AetherBlend] Cannot drive: constraint '{constraint}' not found on '{bone}'.")
            return

    _apply_driver(rig, owner, property_path, index, expression, variables)


def object_driver(
    rig: bpy.types.Object,
    target: bpy.types.Object,
    property_path: str,
    *,
    index: int = -1,
    expression: str,
    variables: Mapping[str, TransformVariable | PropertyVariable],
) -> None:
    """Drive a property of another object, for example a custom property of a mesh that a shader reads."""
    _apply_driver(rig, target, property_path, index, expression, variables)


def _apply_driver(
    rig: bpy.types.Object,
    owner,
    property_path: str,
    index: int,
    expression: str,
    variables: Mapping[str, TransformVariable | PropertyVariable],
) -> None:
    fcurve = owner.driver_add(property_path, index)
    fcurve.driver.type = "SCRIPTED"
    fcurve.driver.expression = expression
    while fcurve.driver.variables:
        fcurve.driver.variables.remove(fcurve.driver.variables[0])

    for variable_name, variable in variables.items():
        driver_variable = fcurve.driver.variables.new()
        driver_variable.name = variable_name
        if isinstance(variable, PropertyVariable):
            driver_variable.type = "SINGLE_PROP"
            target = driver_variable.targets[0]
            target.id_type = "ARMATURE"
            target.id = rig.data
            target.data_path = variable.property_name
            continue

        driver_variable.type = "TRANSFORMS"
        target = driver_variable.targets[0]
        target.id = variable.source or rig
        target.bone_target = variable.bone
        target.transform_type = variable.channel
        target.rotation_mode = variable.rotation_mode
        target.transform_space = variable.space
