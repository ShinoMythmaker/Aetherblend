import bpy

class AETHER_PT_RigPanel(bpy.types.Panel):
    bl_label = "Rig Panel"
    bl_idname = "AETHER_PT_rig_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AetherBlend'
    bl_order = 3

    @classmethod
    def poll(cls, context):
        armature = context.active_object
        return (
            armature is not None 
            and armature.type == 'ARMATURE' 
            and getattr(armature, 'aether_rig', None)
        )

    def draw(self, context):
        layout = self.layout
        armature = context.active_object
        aether_rig = getattr(armature, 'aether_rig', None)

        col = layout.column(align=True)
        
        row = col.row(align=True)
        
        meta_col = row.column(align=True)
        meta_col.scale_x = 2.0
        if aether_rig.meta_rig:
            meta_col.operator("aether.generate_meta_rig", text="Meta", icon="FILE_REFRESH")
        else:
            meta_col.operator("aether.generate_meta_rig", text="Meta", icon="ARMATURE_DATA")
        
        arrow_col = row.column(align=True)
        arrow_col.scale_x = 0.3
        arrow_col.label(text="→")

        control_col = row.column(align=True)
        control_col.scale_x = 2.0
        control_col.enabled = bool(aether_rig.meta_rig)
        if aether_rig.meta_rig:
            control_col.operator("aether.generate_rigify_rig", text="Control", icon="FILE_REFRESH")
        else:
            control_col.operator("aether.generate_rigify_rig", text="Control", icon="OUTLINER_OB_ARMATURE")

        arrow_col2 = row.column(align=True)
        arrow_col2.scale_x = 0.3
        arrow_col2.label(text="→")
        
        link_col = row.column(align=True)
        link_col.scale_x = 2.0
        link_col.enabled = bool(aether_rig.rigify_rig)
        if aether_rig.rigify_linked:
            link_col.operator("aether.unlink_rigify_rig", text="Unlink", icon="UNLINKED")
        else:
            link_col.operator("aether.link_rigify_rig", text="Link", icon="LINKED")

        layout.separator()

        col = layout.column(align=True)
        col.label(text="Rig References:")
        
        row = col.row(align=True)
        label_col = row.column(align=True)
        label_col.scale_x = 0.8
        label_col.label(text="Meta Rig")
        
        field_col = row.column(align=True)
        field_col.scale_x = 1.2
        field_col.prop_search(aether_rig, "meta_rig", bpy.context.scene, "objects", text="")

        row = col.row(align=True)
        label_col = row.column(align=True)
        label_col.scale_x = 0.8
        label_col.label(text="Rigify Rig")
        
        field_col = row.column(align=True)
        field_col.scale_x = 1.2
        field_col.prop_search(aether_rig, "rigify_rig", bpy.context.scene, "objects", text="")


def register():
    bpy.utils.register_class(AETHER_PT_RigPanel)

def unregister():
    bpy.utils.unregister_class(AETHER_PT_RigPanel)