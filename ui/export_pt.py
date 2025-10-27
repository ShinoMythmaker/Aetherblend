import bpy

class AETHER_PT_ExportPanel(bpy.types.Panel):
    bl_label = "Export"
    bl_idname = "AETHER_PT_export_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'  
    bl_category = 'AetherBlend'
    bl_order = 3 
    
    def draw(self, context):
        layout = self.layout

        #check here if meddle operators are available otherwise display it. too lazy rn will do later
        row = layout.row(align=True)
        row.operator("aether.pose_export", text="Pose Export", icon = "EXPORT")

def register():
    bpy.utils.register_class(AETHER_PT_ExportPanel)

def unregister():
    bpy.utils.unregister_class(AETHER_PT_ExportPanel) 