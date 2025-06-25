import bpy
from ..status import AetherBlendStatus as status
from ..utils import rig as rig_utils
from ..data.constants import sb_tail_collection

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
        row.label(text="Spring Bones", icon='CONSTRAINT_BONE')
        if context.scene.ab_sb_global_spring_frame == False:          
            row.operator("aether.spring_bone_frame", text="Start", icon='PLAY')
        if context.scene.ab_sb_global_spring_frame == True:           
            row.operator("aether.spring_bone_frame", text="Stop", icon='PAUSE')
        

        row = layout.row(align=True)
        row.label(text="Tail Bones", icon='BONE_DATA')
        if rig_utils.bone.get_collectiion(context.active_object, sb_tail_collection):
            if context.scene.ab_sb_global_spring_frame == True:           
                row.operator("aether.bake_spring_tail", text="Bake", icon= "LIGHT_SUN")
            row.operator("aether.delete_spring_tail", text="Delete", icon = "TRASH")
        else:
            row.operator("aether.generate_spring_tail", text="Generate", icon = "PIVOT_MEDIAN")


def register():
    bpy.utils.register_class(AETHER_PT_RigEditor)

def unregister():  
    bpy.utils.unregister_class(AETHER_PT_RigEditor)