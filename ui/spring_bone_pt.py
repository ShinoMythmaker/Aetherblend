import bpy

class AETHER_PT_SpringBone(bpy.types.Panel):
    bl_label = "Spring Bones"
    bl_idname = "AETHER_PT_spring_bone"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'  
    bl_category = 'AetherBlend'
    bl_order = 5 
    
    @classmethod
    def poll(cls, context):
        return context.scene.aether_tabs.active_tab == 'GENERATE'
    
    def draw(self, context):
        layout = self.layout
        
        box = layout.box()
        col = box.column(align=True)
        col.label(text="Work In Progress", icon='INFO')
        col.separator()
        # col.label(text="This feature will enable physics-based")
        # col.label(text="spring bones for hair, tails, ears, and")
        # col.label(text="other dynamic elements.")
        col.separator()
        col.label(text="Temporarily removed - under redesign.", icon='PHYSICS')

def register():
    bpy.utils.register_class(AETHER_PT_SpringBone)

def unregister():
    bpy.utils.unregister_class(AETHER_PT_SpringBone)
