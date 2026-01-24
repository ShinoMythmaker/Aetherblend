"""Animation export properties."""

import bpy
from bpy.props import EnumProperty, BoolProperty


class AetherAnimationExportProperties(bpy.types.PropertyGroup):
    """Properties for animation export settings."""
    
    # Pose Export Axis Orientation
    pose_primary_axis: EnumProperty(
        name="Primary Pose Axis",
        description="Primary axis for pose export orientation. For FFXIV characters from Meddle, use -Z",
        items=(
            ('X', "X Axis", ""),
            ('Y', "Y Axis", ""),
            ('Z', "Z Axis", ""),
            ('-X', "-X Axis", ""),
            ('-Y', "-Y Axis", ""),
            ('-Z', "-Z Axis", ""),
        ),
        default='Y',
    )  # type: ignore
    
    pose_secondary_axis: EnumProperty(
        name="Secondary Pose Axis",
        description="Secondary axis for pose export orientation. For FFXIV characters from Meddle, use Y",
        items=(
            ('X', "X Axis", ""),
            ('Y', "Y Axis", ""),
            ('Z', "Z Axis", ""),
            ('-X', "-X Axis", ""),
            ('-Y', "-Y Axis", ""),
            ('-Z', "-Z Axis", ""),
        ),
        default='X',
    )  # type: ignore
    
    use_pose_axis_conversion: BoolProperty(
        name="Use Pose Axis Conversion",
        description="Apply pose axis conversion to match character import settings",
        default=True
    )  # type: ignore


def register():
    bpy.utils.register_class(AetherAnimationExportProperties)
    bpy.types.Scene.aether_animation_export = bpy.props.PointerProperty(type=AetherAnimationExportProperties)


def unregister():
    del bpy.types.Scene.aether_animation_export
    bpy.utils.unregister_class(AetherAnimationExportProperties)
