import bpy
from ..status import AetherBlendStatus as status

class AETHER_PT_ImportPanel(bpy.types.Panel):
    bl_label = "Import"
    bl_idname = "AETHER_PT_import_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'  
    bl_category = 'AetherBlend'
    bl_order = 1 

    @classmethod
    def poll(cls, context):
        return not status.get_prompt_user()
    
    def draw(self, context):
        layout = self.layout

        if status.meddle_installed and status.meddle_enabled:
            row = layout.row(align=True)
            row.operator("aether.character_import", text="Import Character", icon = "IMPORT")

def register():
    bpy.utils.register_class(AETHER_PT_ImportPanel)

def unregister():
    bpy.utils.unregister_class(AETHER_PT_ImportPanel) 
 


            
            