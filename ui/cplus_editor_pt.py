import bpy

class AETHER_PT_CPlusEditor(bpy.types.Panel):
    bl_label = "C+ Editor"
    bl_idname = "AETHER_PT_cplus_editor"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'  
    bl_category = 'AetherBlend'
    bl_order = 3 
    
    @classmethod
    def poll(cls, context):
        return context.scene.aether_tabs.active_tab == 'CPLUS'
    
    def draw(self, context):
        layout = self.layout
        
        box = layout.box()
        col = box.column(align=True)
        col.label(text="Work In Progress", icon='INFO')
        col.separator()
        # col.label(text="This feature will provide an interactive")
        # col.label(text="character creator experience similar to")
        # col.label(text="the in-game customization interface.")
        col.separator()
        col.label(text="Currently in development.", icon='MODIFIER')

def register():
    bpy.utils.register_class(AETHER_PT_CPlusEditor)

def unregister():
    bpy.utils.unregister_class(AETHER_PT_CPlusEditor)
