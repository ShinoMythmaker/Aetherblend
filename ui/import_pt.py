import bpy
import addon_utils
from ..preferences import get_preferences

def check_for_meddle():
    """Check if Meddle Tools addon is installed and enabled"""
    addon_module = [m for m in addon_utils.modules() if m.bl_info.get('name') == "Meddle Tools"]
    if not addon_module:
        return False
    addon_enabled = addon_utils.check(addon_module[0].__name__)[0]
    return addon_enabled

class AETHER_PT_ImportPanel(bpy.types.Panel):
    bl_label = "Import"
    bl_idname = "AETHER_PT_import_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'  
    bl_category = 'AetherBlend'
    bl_order = 1 

    @classmethod
    def poll(cls, context):
        prefs = get_preferences()
        if prefs.import_panel:
            return prefs.import_panel == 'ON'
        return False
    
    def draw(self, context):
        layout = self.layout

        if not check_for_meddle():
            layout = self.layout
            box = layout.box()
            box.label(text="Missing Meddle Tools addon", icon='ERROR')
            return None


        row = layout.row(align=True)
        row.operator("aether.character_import", text="Import Character", icon = "IMPORT")


def menu_func_import(self, context):
    """Add the import operator to the File > Import menu"""
    if check_for_meddle():
        self.layout.operator("aether.character_import", text="FFXIV Character (Meddle)")

def register():
    bpy.utils.register_class(AETHER_PT_ImportPanel)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)

def unregister():
    bpy.utils.unregister_class(AETHER_PT_ImportPanel)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import) 
 


            
            