"""Active tab state for the add-on sidebar."""

import bpy
from bpy.props import EnumProperty

TAB_ITEMS = [
    ("IMPORT_EXPORT", "Import/Export", "Import and Export tools", "IMPORT", 0),
    ("GENERATE", "Generate", "Rig generation tools", "ARMATURE_DATA", 1),
    ("RIG_LAYERS", "Rig Layers", "Rig layers", "BONE_DATA", 2),
    ("RIG_UI", "Rig UI", "Rig UI and bake settings", "PROPERTIES", 3),
]


def get_active_tab_prop_name(context: bpy.types.Context) -> str:
    """Return the name of the scene property that stores the active tab."""
    area = getattr(context, "area", None)
    if area is not None and area.type == "PROPERTIES":
        return "active_tab_tool"
    return "active_tab"


def get_active_tab(context: bpy.types.Context) -> str:
    """Return the active tab identifier."""
    tabs = getattr(getattr(context, "scene", None), "aether_tabs", None)
    if tabs is None:
        return "IMPORT_EXPORT"
    return getattr(tabs, get_active_tab_prop_name(context), "IMPORT_EXPORT")


def set_active_tab(context: bpy.types.Context, value: str) -> None:
    """Set the active tab identifier."""
    tabs = getattr(getattr(context, "scene", None), "aether_tabs", None)
    if tabs is None:
        return
    setattr(tabs, get_active_tab_prop_name(context), value)


class AETHER_PG_ui_tabs(bpy.types.PropertyGroup):
    """Properties for AetherBlend tab management."""

    active_tab: EnumProperty(
        name="Active Tab",
        description="Currently active tab in AetherBlend panel",
        items=TAB_ITEMS,
        default="IMPORT_EXPORT",
    )  # type: ignore

    active_tab_tool: EnumProperty(
        name="Active Tool Tab",
        description="Currently active tab in AetherBlend tool panel",
        items=TAB_ITEMS,
        default="IMPORT_EXPORT",
    )  # type: ignore


def register() -> None:
    """Register this module's classes."""
    bpy.utils.register_class(AETHER_PG_ui_tabs)
    bpy.types.Scene.aether_tabs = bpy.props.PointerProperty(type=AETHER_PG_ui_tabs)


def unregister() -> None:
    """Unregister this module's classes."""
    del bpy.types.Scene.aether_tabs
    bpy.utils.unregister_class(AETHER_PG_ui_tabs)
