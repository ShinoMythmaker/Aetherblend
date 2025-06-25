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

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == 'ARMATURE' and not status.get_prompt_user() and status.startup_check
    
    def draw(self, context):
        layout = self.layout

        row = layout.row(align=True)
        row.label(text="Spring Bones", icon='CONSTRAINT_BONE')

        box = layout.box()
        row = box.row(align=True)

        spring_active = getattr(context.scene, "ab_sb_global_spring", False)
        spring_frame_active = getattr(context.scene, "ab_sb_global_spring_frame", False)

        # Spring Frame button (disabled if spring modal is active)
        col1 = row.column(align=True)
        col1.enabled = not spring_active
        col1.operator("aether.spring_bone_frame", text="Frame", icon='PLAY' if not spring_frame_active else 'PAUSE')
        

        # Spring Modal button (disabled if spring frame is active)
        col2= row.column(align=True)
        col2.enabled = not spring_frame_active
        col2.operator("aether.spring_bone", text="Active", icon='PLAY' if not spring_active else 'PAUSE')
        

        row = box.row(align=True)
        col = row.column(align=True)
        split = col.split(factor=0.5)
        col_label = split.column(align=True)
        col_ops = split.column(align=True)
        col_ops_row = col_ops.row(align=False)

        col_label.label(text="Tail Bones", icon='BONE_DATA')
        if rig_utils.bone.get_collectiion(context.active_object, sb_tail_collection):
            delete_string = "Delete"
            if context.scene.ab_sb_global_spring_frame == True:           
                col_ops_row.operator("aether.bake_spring_tail", text="Bake", icon="LIGHT_SUN")
                delete_string = ""
            col_ops_row.operator("aether.delete_spring_tail", text=delete_string, icon="TRASH")
            
        else:
            col_ops_row.operator("aether.generate_spring_tail", text="Generate", icon="PIVOT_MEDIAN")


def register():
    bpy.utils.register_class(AETHER_PT_RigEditor)

def unregister():  
    bpy.utils.unregister_class(AETHER_PT_RigEditor)