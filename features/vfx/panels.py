import bpy
from ...properties.tab_prop import get_active_tab
from ...utils.ui_visibility import visible_in_current_area

class AETHER_PT_VFXExportPanel(bpy.types.Panel):
    bl_label = "VFX Export"
    bl_idname = "AETHER_PT_vfx_export_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'  
    bl_category = 'AetherBlend'
    bl_order = 4 
    
    @classmethod
    def poll(cls, context):
        return visible_in_current_area(context) and get_active_tab(context) == 'IMPORT_EXPORT'

    def draw(self, context):
        layout = self.layout
        
        row = layout.row(align=True)
        row.operator("aether.vfx_export_model", text="Model Export", icon = "EXPORT")
        row = layout.row(align=True)
        row.operator("aether.vfx_export_emitter", text="Emitter Export", icon = "EXPORT")

def menu_func_export(self, context):
    """Add the export operator to the File > Export menu"""
    self.layout.operator("aether.vfx_export_model", text="AB VFX Model")
    self.layout.operator("aether.vfx_export_emitter", text="AB VFX Emitter")

def register():
    bpy.utils.register_class(AETHER_PT_VFXExportPanel)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)

def unregister():
    bpy.utils.unregister_class(AETHER_PT_VFXExportPanel)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export) 