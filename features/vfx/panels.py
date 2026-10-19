"""Panels and File menu entries for VFX exports."""

import bpy

from ...ui.tabs import get_active_tab
from ...ui.visibility import visible_in_current_area


class AETHER_PT_VFXExportPanel(bpy.types.Panel):
    """Expose VFX exporters in the Import/Export tab."""

    bl_label = "VFX Export"
    bl_idname = "AETHER_PT_vfx_export_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "AetherBlend"
    bl_order = 4

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        """Show this panel when the Import/Export tab is active."""
        return visible_in_current_area(context) and get_active_tab(context) == "IMPORT_EXPORT"

    def draw(self, context: bpy.types.Context) -> None:
        """Draw the VFX model and emitter export buttons."""
        layout = self.layout
        layout.operator("aether.vfx_export_model", text="Model Export", icon="EXPORT")
        layout.operator("aether.vfx_export_emitter", text="Emitter Export", icon="EXPORT")


def menu_func_export(self: bpy.types.Menu, context: bpy.types.Context) -> None:
    """Add VFX export operators to the File > Export menu."""
    self.layout.operator("aether.vfx_export_model", text="AB VFX Model")
    self.layout.operator("aether.vfx_export_emitter", text="AB VFX Emitter")


def register() -> None:
    """Register the VFX panel and File menu entries."""
    bpy.utils.register_class(AETHER_PT_VFXExportPanel)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister() -> None:
    """Unregister the VFX panel and File menu entries."""
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    bpy.utils.unregister_class(AETHER_PT_VFXExportPanel)
