"""Backend template lookup and rig generator construction."""

import bpy

from .generator import AetherRigGenerator
from .library import CS_COLORSETS, DEFAULT_TEMPLATE_NAME, TEMPLATES, UI_LAYOUTS

DEFAULT_COLORSET_NAME = "AetherBlend"
DEFAULT_UI_LAYOUT_NAME = "Default"


def get_template_items(self: bpy.types.PropertyGroup, context: bpy.types.Context) -> list[tuple[str, str, str]]:
    """Dropdown items for the per-rig template property."""
    return [(name, name, "") for name in TEMPLATES]


def get_colorset_items(self: bpy.types.PropertyGroup, context: bpy.types.Context) -> list[tuple[str, str, str]]:
    """Dropdown items for the colorset override."""
    return [(key, key, "") for key in CS_COLORSETS]


def get_ui_layout_items(self: bpy.types.PropertyGroup, context: bpy.types.Context) -> list[tuple[str, str, str]]:
    """Dropdown items for the curated bone collection layout."""
    return [(name, name, "") for name in UI_LAYOUTS]


def get_rig_generator(aether_rig: bpy.types.PropertyGroup) -> AetherRigGenerator | None:
    """Build a generator using the selected template, colorset and UI layout."""
    template = TEMPLATES.get(getattr(aether_rig, "template", DEFAULT_TEMPLATE_NAME)) or TEMPLATES[DEFAULT_TEMPLATE_NAME]
    color_sets = CS_COLORSETS.get(getattr(aether_rig, "selected_colorset", DEFAULT_COLORSET_NAME))
    layout_name = getattr(aether_rig, "selected_ui_layout", DEFAULT_UI_LAYOUT_NAME)
    ui_layout = UI_LAYOUTS.get(layout_name)

    if not color_sets:
        print("[AetherBlend] Select an available colorset before generating the rig.")
        return None

    if ui_layout is None:
        print(f"[AetherBlend] UI layout '{layout_name}' is unavailable. Select an available UI layout.")
        return None

    return AetherRigGenerator(name=template.name, color_sets=color_sets, ui_layout=ui_layout, modules=template.modules)


def register() -> None:
    """Register this module's classes."""
    pass


def unregister() -> None:
    """Unregister this module's classes."""
    pass
