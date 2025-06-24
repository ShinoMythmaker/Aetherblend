import bpy
from ..status import AetherBlendStatus as status

class AETHER_PT_RigEditor(bpy.types.Panel):
    bl_label = "Rig Editor"
    bl_idname = "AETHER_PT_rig_editor"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'  
    bl_category = 'AetherBlend'
    bl_order = 2 

    def draw(self, context):
        if status.get_prompt_user():
            return
    
        layout = self.layout

        row = layout.row(align=True)
        if context.scene.sb_global_spring == False:
            row.operator("sb.spring_bone", text="Start - Interactive Mode", icon='PLAY')           
        if context.scene.sb_global_spring == True:
            row.operator("sb.spring_bone", text="Stop", icon='PAUSE') 
            
        row = layout.row(align=True)
        row.operator("aether.generate_spring_tail", text="Spring Tail", icon = "PIVOT_MEDIAN")


def register():
    bpy.utils.register_class(AETHER_PT_RigEditor)

def unregister():  
    bpy.utils.unregister_class(AETHER_PT_RigEditor)