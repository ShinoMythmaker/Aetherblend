import bpy
from ..data.constants import sb_tail_collection, sb_ears_collection, sb_breast_collection

class AETHER_PT_SpringBones(bpy.types.Panel):
    bl_label = "Spring Bones"
    bl_idname = "AETHER_PT_spring_bones"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'  
    bl_category = 'AetherBlend'
    bl_order = 4 

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == 'ARMATURE' and False
    
    def draw(self, context):
        armature = context.active_object
        layout = self.layout

        box = layout.box()
        row = box.row(align=True)

        spring_active = getattr(context.scene, "ab_sb_global_spring", False)
        spring_frame_active = getattr(context.scene, "ab_sb_global_spring_frame", False)

        # Spring Frame button (disabled if spring modal is active)
        col1 = row.column(align=True)
        col1.enabled = not spring_active
        col1.operator("aether.spring_bone_frame", text="Frame", icon='PLAY' if not spring_frame_active else 'PAUSE')
        

        # Spring Modal button (disabled if spring frame is active)
        if spring_frame_active:
            col2 = row.column(align=False)
            col2.operator("aether.bake_all_spring_bones", text="Bake All", icon='LIGHT_SUN')
        else:
            col2= row.column(align=True)
            col2.enabled = not spring_frame_active
            col2.operator("aether.spring_bone", text="Active", icon='PLAY' if not spring_active else 'PAUSE')
        

        row = box.row(align=True)
        col = row.column(align=True)
        split = col.split(factor=0.5)
        col_label = split.column(align=True)
        col_ops = split.column(align=True)
        
        col_ops_row = col_ops.row(align=False)
        col_label_row = col_label.row(align=True)
        col_label_row.label(text="Tail", icon='BONE_DATA')
        if armature.data.collections.get(sb_tail_collection):
            if context.scene.ab_sb_global_spring_frame == True:           
                col_ops_row.operator("aether.bake_spring_tail", text="Bake", icon="LIGHT_SUN")
                delete_string = ""
            col_ops_row.operator("aether.delete_spring_tail", text="Delete", icon="TRASH")
            
        else:
            col_ops_row.operator("aether.generate_spring_tail", text="Generate", icon="PIVOT_MEDIAN")

        col_ops_row = col_ops.row(align=False)
        col_label_row = col_label.row(align=True)
        col_label_row.label(text="Ears", icon='BONE_DATA')
        if armature.data.collections.get(sb_ears_collection):
            if context.scene.ab_sb_global_spring_frame == True:           
                col_ops_row.operator("aether.bake_spring_ears", text="Bake", icon="LIGHT_SUN")
                delete_string = ""
            col_ops_row.operator("aether.delete_spring_ears", text="Delete", icon="TRASH")
            
        else:
            col_ops_row.operator("aether.generate_spring_ears", text="Generate", icon="PIVOT_MEDIAN")

        col_ops_row = col_ops.row(align=False)
        col_label_row = col_label.row(align=True)
        col_label_row.label(text="Breasts", icon='BONE_DATA')
        if armature.data.collections.get(sb_breast_collection):
            if context.scene.ab_sb_global_spring_frame == True:           
                col_ops_row.operator("aether.bake_spring_breasts", text="Bake", icon="LIGHT_SUN")
            col_ops_row.operator("aether.delete_spring_breasts", text="Delete", icon="TRASH")
            
        else:
            col_ops_row.operator("aether.generate_spring_breasts", text="Generate", icon="PIVOT_MEDIAN")
        


def register():
    bpy.utils.register_class(AETHER_PT_SpringBones)

def unregister():  
    bpy.utils.unregister_class(AETHER_PT_SpringBones)