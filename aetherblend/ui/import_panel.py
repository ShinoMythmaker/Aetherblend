import bpy

class AETHER_PT_ImportPanel(bpy.types.Panel):
    bl_label = "Import"
    bl_idname = "AETHER_PT_import_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'  
    bl_category = 'AetherBlend'
    bl_order = 1 
    
    def draw(self, context):
        layout = self.layout

        #check here if meddle operators are available otherwise display it. too lazye rn will do later
        row = layout.row(align=True)
        row.operator("aether.character_import", text="Import Character", icon = "IMPORT")

def register():
    bpy.utils.register_class(AETHER_PT_ImportPanel)

def unregister():
    bpy.utils.unregister_class(AETHER_PT_ImportPanel) 
 


            
            