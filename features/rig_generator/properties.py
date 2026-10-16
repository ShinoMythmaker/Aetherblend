"""Rig generator property groups."""

import bpy

from . import template_manager


class AETHER_PG_rig_generator_string_item(bpy.types.PropertyGroup):
    value: bpy.props.StringProperty(name="Value", default="", options={"HIDDEN"})  # type: ignore


class AETHER_PG_rig_generator_rig(bpy.types.PropertyGroup):
    meta_rig: bpy.props.PointerProperty(
        name="Meta Rig",
        type=bpy.types.Object,
        description="Reference to the Meta-Rig for this armature",
        poll=lambda self, obj: obj.type == "ARMATURE",
    )  # type: ignore

    rigified: bpy.props.BoolProperty(
        name="Rigified", description="Whether the armature went through generation process or not", default=False
    )  # type: ignore

    converted: bpy.props.BoolProperty(
        name="Converted",
        description="Whether the armature has been converted to Blender-friendly form",
        default=False,
        options={"HIDDEN"},
    )  # type: ignore

    template: bpy.props.EnumProperty(
        name="Template",
        description="Rig template used when generating this armature",
        items=template_manager.get_template_items,
    )  # type: ignore

    selected_colorset: bpy.props.EnumProperty(
        name="Colorset",
        description="Select a colorset (replaces template default)",
        items=template_manager.get_colorset_items,
        default=0,
    )  # type: ignore

    link_inherit_scale: bpy.props.EnumProperty(
        name="LINK Inherit Scale",
        description="Inherit scale setting for LINK collection bones",
        items=[
            ("FULL", "Full", "Full inherit scale"),
            ("FIX_SHEAR", "Aligned", "Inherit scale with shear fixed"),
            ("AVERAGE", "Average", "Average scale inheritance"),
            ("NONE", "None", "No scale inheritance"),
            ("NONE_LEGACY", "None (Legacy)", "No scale inheritance (legacy)"),
        ],
        default="FULL",
    )  # type: ignore

    ui_flags: bpy.props.CollectionProperty(
        name="UI Flags",
        description="Resolved UI flags from the modules used during generation",
        type=AETHER_PG_rig_generator_string_item,
        options={"HIDDEN"},
    )  # type: ignore

    eye_lid_edit_mode: bpy.props.BoolProperty(
        name="Eye Lid Edit Mode", description="Whether the armature is in eye lid edit mode or not", default=False
    )  # type: ignore


def register() -> None:
    """Register this module's classes."""
    bpy.utils.register_class(AETHER_PG_rig_generator_string_item)
    bpy.utils.register_class(AETHER_PG_rig_generator_rig)
    bpy.types.Object.aether_rig = bpy.props.PointerProperty(type=AETHER_PG_rig_generator_rig)


def unregister() -> None:
    """Unregister this module's classes."""
    if hasattr(bpy.types.Object, "aether_rig"):
        del bpy.types.Object.aether_rig
    bpy.utils.unregister_class(AETHER_PG_rig_generator_rig)
    bpy.utils.unregister_class(AETHER_PG_rig_generator_string_item)
