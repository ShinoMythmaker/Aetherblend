"""Import and export panels and File menu entries."""
import bpy

from ...preferences import is_set_enabled
from ...ui.tabs import get_active_tab
from ...ui.visibility import visible_in_current_area


class AETHER_PT_ImportPanel(bpy.types.Panel):
    bl_label = "Import"
    bl_idname = "AETHER_PT_import_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AetherBlend'
    bl_order = 1

    @classmethod
    def poll(cls, context):
        return visible_in_current_area(context) and get_active_tab(context) == 'IMPORT_EXPORT'

    def draw(self, context):
        layout = self.layout

        if is_set_enabled('FFXIV'):
            row = layout.row(align=True)
            row.operator("aether.import_export_import_character", text="FFXIV Character", icon = "IMPORT")

def menu_func_import(self, context):
    """Add the import operator to the File > Import menu"""
    self.layout.operator("aether.import_export_import_character", text="FFXIV Character (Meddle)")


class AETHER_PT_ExportPanel(bpy.types.Panel):
    bl_label = "Export"
    bl_idname = "AETHER_PT_export_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AetherBlend'
    bl_order = 3

    @classmethod
    def poll(cls, context):
        return visible_in_current_area(context) and get_active_tab(context) == 'IMPORT_EXPORT'

    def draw(self, context):
        layout = self.layout

        # Export Operators
        row = layout.row(align=True)
        row.operator("aether.animation_export_pose", text="Pose Export", icon = "EXPORT")
        row = layout.row(align=True)
        row.operator("aether.animation_export_anim", text="Anim Export", icon = "EXPORT")


def menu_func_export(self, context):
    """Add the export operator to the File > Export menu"""
    self.layout.operator("aether.animation_export_pose", text="AB Pose")
    self.layout.operator("aether.animation_export_anim", text="AB Animation")


def register():
    bpy.utils.register_class(AETHER_PT_ImportPanel)
    bpy.utils.register_class(AETHER_PT_ExportPanel)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    bpy.utils.unregister_class(AETHER_PT_ExportPanel)
    bpy.utils.unregister_class(AETHER_PT_ImportPanel)
