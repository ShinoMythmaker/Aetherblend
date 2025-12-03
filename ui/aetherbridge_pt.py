import bpy

class AETHER_PT_AetherBridge(bpy.types.Panel):
    bl_label = "AetherBridge"
    bl_idname = "AETHER_PT_aetherbridge"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'  
    bl_category = 'AetherBlend'
    bl_order = 4 
    
    @classmethod
    def poll(cls, context):
        return context.scene.aether_tabs.active_tab == 'IMPORT_EXPORT'
    
    def draw(self, context):
        layout = self.layout
        
        box = layout.box()
        col = box.column(align=True)
        col.label(text="Work In Progress", icon='INFO')
        col.separator()
        # col.label(text="This feature will enable direct integration")
        # col.label(text="with the Brio API for importing and")
        # col.label(text="exporting character data.")
        col.separator()
        col.label(text="Currently waiting on Brio API release.", icon='SORTTIME')

def register():
    bpy.utils.register_class(AETHER_PT_AetherBridge)

def unregister():
    bpy.utils.unregister_class(AETHER_PT_AetherBridge)
