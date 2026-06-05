import bpy
from ...properties.tab_prop import get_active_tab
from ...utils.ui_visibility import visible_in_current_area

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

        row = layout.row(align=True)
        row.operator("aether.character_import", text="Import Character", icon = "IMPORT")


def menu_func_import(self, context):
    """Add the import operator to the File > Import menu"""
    self.layout.operator("aether.character_import", text="FFXIV Character (Meddle)")

def register():
    bpy.utils.register_class(AETHER_PT_ImportPanel)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)

def unregister():
    bpy.utils.unregister_class(AETHER_PT_ImportPanel)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import) 
 


            
            