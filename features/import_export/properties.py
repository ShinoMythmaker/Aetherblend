"""Animation export properties."""

import bpy
from bpy.props import BoolProperty, EnumProperty


class AETHER_PG_import_export_export(bpy.types.PropertyGroup):
    """Properties for animation export settings."""

    # Pose Export Axis Orientation
    pose_primary_axis: EnumProperty(
        name="Primary Pose Axis",
        description="Primary axis for pose export orientation.",
        items=(
            ("X", "X Axis", ""),
            ("Y", "Y Axis", ""),
            ("Z", "Z Axis", ""),
            ("-X", "-X Axis", ""),
            ("-Y", "-Y Axis", ""),
            ("-Z", "-Z Axis", ""),
        ),
        default="Y",
    )  # type: ignore

    pose_secondary_axis: EnumProperty(
        name="Secondary Pose Axis",
        description="Secondary axis for pose export orientation.",
        items=(
            ("X", "X Axis", ""),
            ("Y", "Y Axis", ""),
            ("Z", "Z Axis", ""),
            ("-X", "-X Axis", ""),
            ("-Y", "-Y Axis", ""),
            ("-Z", "-Z Axis", ""),
        ),
        default="X",
    )  # type: ignore

    use_pose_axis_conversion: BoolProperty(
        name="Use Pose Axis Conversion",
        description="Apply pose axis conversion to match character import settings",
        default=True,
    )  # type: ignore


def register() -> None:
    """Register this module's classes."""
    bpy.utils.register_class(AETHER_PG_import_export_export)
    bpy.types.Scene.aether_animation_export = bpy.props.PointerProperty(type=AETHER_PG_import_export_export)


def unregister() -> None:
    """Unregister this module's classes."""
    del bpy.types.Scene.aether_animation_export
    bpy.utils.unregister_class(AETHER_PG_import_export_export)
