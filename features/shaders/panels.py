import bpy

from ...properties.tab_prop import get_active_tab
from ...preferences import is_set_enabled
from ...utils import addon_dependencies
from ...utils.ui_visibility import visible_in_current_area


def shader_panel_poll(context):
    if not visible_in_current_area(context):
        return False
    if get_active_tab(context) != 'GENERATE':
        return False

    armature = context.active_object
    return bool(armature and armature.type == 'ARMATURE')


def draw_action_row(layout, label: str, operator_id: str, *, enabled: bool):
    row = layout.row(align=True)
    # Keep enough width for operator text; very high factors collapse labels to icon-only.
    split = row.split(factor=0.6, align=True)

    left = split.row(align=True)
    left.alignment = 'RIGHT'
    if enabled:
        left.label(text=label)
    else:
        left.label(text=label, icon='ERROR')

    right = split.row(align=True)
    right.ui_units_x = 7.0
    right.enabled = enabled
    right.operator(operator_id, text="Apply", icon='TRIA_DOWN_BAR')

def draw_toggle_row(layout, label: str, operator_id: str, *, enabled: bool):
    row = layout.row(align=True)
    # Keep enough width for operator text; very high factors collapse labels to icon-only.
    split = row.split(factor=0.6, align=True)

    left = split.row(align=True)
    left.alignment = 'RIGHT'
    if enabled:
        left.label(text=label)
    else:
        left.label(text=label, icon='ERROR')

    right = split.row(align=True)
    right.ui_units_x = 7.0
    right.enabled = enabled
    right.operator(operator_id, text="Toggle", icon='NODE_MATERIAL')



class AETHER_PT_shaders(bpy.types.Panel):
    bl_label = "Shaders"
    bl_idname = "AETHER_PT_shaders"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AetherBlend'
    bl_order = 6
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return shader_panel_poll(context)

    def draw(self, context):
        pass


class AETHER_PT_VRM_Shaders(bpy.types.Panel):
    bl_label = "VRM Shaders"
    bl_idname = "AETHER_PT_vrm_shaders"
    bl_parent_id = "AETHER_PT_shaders"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AetherBlend'

    @classmethod
    def poll(cls, context):
        return shader_panel_poll(context) and is_set_enabled('VRM')

    def draw(self, context):
        layout = self.layout

        draw_toggle_row(layout, "Toon Outline", "aether.vrm_toggle_outline", enabled=True)


class AETHER_PT_shaders_materials(bpy.types.Panel):
    bl_label = "Materials"
    bl_idname = "AETHER_PT_shaders_materials"
    bl_parent_id = "AETHER_PT_shaders"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AetherBlend'

    @classmethod
    def poll(cls, context):
        return shader_panel_poll(context)

    def draw(self, context):
        layout = self.layout

        has_meddle = addon_dependencies.is_addon_enabled(module_name="meddle", display_name="Meddle Tools")
        has_ffgear = addon_dependencies.is_addon_enabled(module_name="ffgear", display_name="FFGear")

        draw_action_row(layout, "Meddle Shader", "aether.shader_meddle", enabled=has_meddle)
        draw_action_row(layout, "FFGear Shader", "aether.shader_ffgear", enabled=has_ffgear)


class AETHER_PT_shaders_node_trees(bpy.types.Panel):
    bl_label = "Node Trees"
    bl_idname = "AETHER_PT_shaders_node_trees"
    bl_parent_id = "AETHER_PT_shaders"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AetherBlend'

    @classmethod
    def poll(cls, context):
        return shader_panel_poll(context)

    def draw(self, context):
        layout = self.layout
        has_meddle = addon_dependencies.is_addon_enabled(module_name="meddle", display_name="Meddle Tools")

        # AB Iris/Limbal rely on Meddle-import shader context.
        draw_action_row(layout, "AB Iris Shader", "aether.shader_iris", enabled=has_meddle)
        draw_action_row(layout, "AB Limbal Shader", "aether.shader_limbal", enabled=has_meddle)


def register():
    bpy.utils.register_class(AETHER_PT_shaders)
    bpy.utils.register_class(AETHER_PT_VRM_Shaders)
    bpy.utils.register_class(AETHER_PT_shaders_materials)
    bpy.utils.register_class(AETHER_PT_shaders_node_trees)

def unregister():
    bpy.utils.unregister_class(AETHER_PT_shaders_node_trees)
    bpy.utils.unregister_class(AETHER_PT_shaders_materials)
    bpy.utils.unregister_class(AETHER_PT_VRM_Shaders)
    bpy.utils.unregister_class(AETHER_PT_shaders)
        