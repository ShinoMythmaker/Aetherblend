"""Property definitions for the Customize+ feature."""

import bpy

from ...utils.axis_conversion import AXIS_ITEMS


class AETHER_PROP_CustomizePlus(bpy.types.PropertyGroup):
    """Store Customize+ data and backup settings on armatures."""

    code: bpy.props.StringProperty(name="C+ String", description="Paste your Customize+ string here")  # type: ignore
    applied: bpy.props.BoolProperty(name="C+ Applied", description="Tracks if C+ is currently applied to this armature", default=False)  # type: ignore
    backup_armature: bpy.props.PointerProperty(
        name="Backup Armature",
        type=bpy.types.Object,
        description="Reference to the backup armature for C+ reversion",
        poll=lambda self, obj: obj.type == "ARMATURE",
    )  # type: ignore

    cplus_primary_axis: bpy.props.EnumProperty(
        name="Primary Axis",
        description="Primary bone axis used when applying C+ transforms",
        items=AXIS_ITEMS,
        default="X",
    )  # type: ignore
    cplus_secondary_axis: bpy.props.EnumProperty(
        name="Secondary Axis",
        description="Secondary bone axis used when applying C+ transforms",
        items=AXIS_ITEMS,
        default="Y",
    )  # type: ignore


def register() -> None:
    """Register C+ settings on Blender objects."""
    bpy.utils.register_class(AETHER_PROP_CustomizePlus)
    bpy.types.Object.aether_cplus = bpy.props.PointerProperty(type=AETHER_PROP_CustomizePlus)


def unregister() -> None:
    """Remove C+ settings from Blender objects."""
    if hasattr(bpy.types.Object, "aether_cplus"):
        del bpy.types.Object.aether_cplus
    bpy.utils.unregister_class(AETHER_PROP_CustomizePlus)
