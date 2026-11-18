"""Visibility rules for the add-on panels."""

import bpy

from ..preferences import get_preferences


def visible_in_current_area(context: bpy.types.Context) -> bool:
    """Return whether panels are allowed in the current editor area."""
    prefs = get_preferences()
    area = context.area
    if area is None:
        return True
    if area.type == "VIEW_3D":
        return prefs.show_n_panel == "ON"
    if area.type == "PROPERTIES":
        return prefs.show_properties_tool_tab == "ON"
    return True
