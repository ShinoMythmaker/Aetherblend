import bpy
import addon_utils
import importlib.util

class AETHER_PT_ImportPanel(bpy.types.Panel):
    bl_label = "Import"
    bl_idname = "AETHER_PT_import_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'  
    bl_category = 'AetherBlend'
    bl_order = 1 
    
    def draw(self, context):
        layout = self.layout
        addon_module = [m for m in addon_utils.modules() if m.bl_info.get('name') == "Meddle Tools"]
        if not addon_module:
            layout = self.layout
            box = layout.box()
            box.label(text="Meddle Tools addon is not installed", icon='ERROR')
            return None
        
        addon_enabled = addon_utils.check(addon_module[0].__name__)[0]
        if not addon_enabled:
            layout = self.layout
            box = layout.box()
            box.label(text="Meddle Tools addon is not enabled", icon='ERROR')
            return None


        row = layout.row(align=True)
        row.operator("aether.character_import", text="Import Character", icon = "IMPORT")

def register():
    bpy.utils.register_class(AETHER_PT_ImportPanel)

def unregister():
    bpy.utils.unregister_class(AETHER_PT_ImportPanel) 
 


            
            