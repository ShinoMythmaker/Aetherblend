"""Shader panels."""

import bpy

from ...ui.tabs import get_active_tab
from ...ui.visibility import visible_in_current_area
from ...utils import addon_dependencies


def shader_panel_poll(context: bpy.types.Context) -> bool:
    """Return whether the shader panels should be shown."""
    if not visible_in_current_area(context):
        return False
    if get_active_tab(context) != "GENERATE":
        return False

    armature = context.active_object
    return bool(armature and armature.type == "ARMATURE")


def draw_action_row(layout: bpy.types.UILayout, label: str, operator_id: str, *, enabled: bool) -> None:
    """Draw a labelled operator button row."""
    row = layout.row(align=True)
    # Keep enough width for operator text; very high factors collapse labels to icon-only.
    split = row.split(factor=0.6, align=True)

    left = split.row(align=True)
    left.alignment = "RIGHT"
    if enabled:
        left.label(text=label)
    else:
        left.label(text=label, icon="ERROR")

    right = split.row(align=True)
    right.ui_units_x = 7.0
    right.enabled = enabled
    right.operator(operator_id, text="Apply", icon="TRIA_DOWN_BAR")


class AETHER_PT_shaders_main(bpy.types.Panel):
    bl_label = "Shaders"
    bl_idname = "AETHER_PT_shaders_main"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "AetherBlend"
    bl_order = 6
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        return shader_panel_poll(context)

    def draw(self, context: bpy.types.Context) -> None:
        pass


class AETHER_PT_shaders_materials(bpy.types.Panel):
    bl_label = "Materials"
    bl_idname = "AETHER_PT_shaders_materials"
    bl_parent_id = "AETHER_PT_shaders_main"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "AetherBlend"

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        return shader_panel_poll(context)

    def draw(self, context: bpy.types.Context) -> None:
        layout = self.layout

        has_meddle = addon_dependencies.is_addon_enabled(module_name="meddle", display_name="Meddle Tools")
        has_ffgear = addon_dependencies.is_addon_enabled(module_name="ffgear", display_name="FFGear")

        draw_action_row(layout, "Meddle Shader", "aether.shaders_meddle", enabled=has_meddle)
        draw_action_row(layout, "FFGear Shader", "aether.shaders_ffgear", enabled=has_ffgear)


class AETHER_PT_shaders_node_trees(bpy.types.Panel):
    bl_label = "Node Trees"
    bl_idname = "AETHER_PT_shaders_node_trees"
    bl_parent_id = "AETHER_PT_shaders_main"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "AetherBlend"

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        return shader_panel_poll(context)

    def draw(self, context: bpy.types.Context) -> None:
        layout = self.layout
        has_meddle = addon_dependencies.is_addon_enabled(module_name="meddle", display_name="Meddle Tools")

        # AB Iris/Limbal rely on Meddle-import shader context.
        draw_action_row(layout, "AB Iris Shader", "aether.shaders_iris", enabled=has_meddle)
        draw_action_row(layout, "AB Limbal Shader", "aether.shaders_limbal", enabled=has_meddle)


def register() -> None:
    """Register this module's classes."""
    bpy.utils.register_class(AETHER_PT_shaders_main)
    bpy.utils.register_class(AETHER_PT_shaders_materials)
    bpy.utils.register_class(AETHER_PT_shaders_node_trees)


def unregister() -> None:
    """Unregister this module's classes."""
    bpy.utils.unregister_class(AETHER_PT_shaders_node_trees)
    bpy.utils.unregister_class(AETHER_PT_shaders_materials)
    bpy.utils.unregister_class(AETHER_PT_shaders_main)
