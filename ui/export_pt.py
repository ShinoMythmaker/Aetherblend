import bpy
from ..preferences import get_preferences

class AETHER_PT_ExportPanel(bpy.types.Panel):
    bl_label = "Export"
    bl_idname = "AETHER_PT_export_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'  
    bl_category = 'AetherBlend'
    bl_order = 3 
    
    @classmethod
    def poll(cls, context):
        return context.scene.aether_tabs.active_tab == 'IMPORT_EXPORT'

    def draw(self, context):
        layout = self.layout

        #check here if meddle operators are available otherwise display it. too lazy rn will do later
        row = layout.row(align=True)
        row.operator("aether.pose_export", text="Pose Export", icon = "EXPORT")
        row.operator("aether.anim_export", text="Anim Export", icon = "EXPORT")
        
        row = layout.row(align=True)
        row.operator("aether.vfx_export", text="VFX Model Export", icon = "EXPORT")

def menu_func_export(self, context):
    """Add the export operator to the File > Export menu"""
    self.layout.operator("aether.pose_export", text="FFXIV Pose (.pose)")
    self.layout.operator("aether.anim_export", text="FFXIV Animation (.glb)")
    self.layout.operator("aether.vfx_export", text="FFXIV VFX Model (.glb)")

def register():
    bpy.utils.register_class(AETHER_PT_ExportPanel)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)

def unregister():
    bpy.utils.unregister_class(AETHER_PT_ExportPanel)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export) 