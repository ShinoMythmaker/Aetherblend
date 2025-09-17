import bpy
from ..status import AetherBlendStatus as status


class AETHER_PT_MetaRigPanel(bpy.types.Panel):
    bl_label = "Meta Rig"
    bl_idname = "AETHER_PT_meta_rig_panel"
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
            and not status.get_prompt_user()
            and status.startup_check
            and getattr(armature, 'aether_is_ffxiv_rig', False)  # FFXIV rig check
        )

    def draw(self, context):
        layout = self.layout
        armature = context.active_object

        # Workflow buttons at the top
        col = layout.column(align=True)
        
        # Create a row with the three workflow buttons
        row = col.row(align=True)
        
        # Meta Rig button (always enabled) - use scale to make it fill space
        meta_col = row.column(align=True)
        meta_col.scale_x = 2.0
        if armature.aether_meta_rig:
            meta_col.operator("aether.generate_meta_rig", text="Meta", icon="FILE_REFRESH")
        else:
            meta_col.operator("aether.generate_meta_rig", text="Meta", icon="ARMATURE_DATA")
        
        # Arrow - smaller scale
        arrow_col = row.column(align=True)
        arrow_col.scale_x = 0.3
        arrow_col.label(text="→")
        
        # Control Rig button (enabled only if meta rig exists)
        control_col = row.column(align=True)
        control_col.scale_x = 2.0
        control_col.enabled = bool(armature.aether_meta_rig)
        if armature.aether_control_rig:
            control_col.operator("aether.generate_control_rig", text="Control", icon="FILE_REFRESH")
        else:
            control_col.operator("aether.generate_control_rig", text="Control", icon="OUTLINER_OB_ARMATURE")
        
        # Arrow - smaller scale
        arrow_col2 = row.column(align=True)
        arrow_col2.scale_x = 0.3
        arrow_col2.label(text="→")
        
        # Link button (enabled only if control rig exists)
        link_col = row.column(align=True)
        link_col.scale_x = 2.0
        link_col.enabled = bool(armature.aether_control_rig)
        if getattr(armature, 'aether_control_linked', False):
            link_col.operator("aether.unlink_control_rig", text="Unlink", icon="UNLINKED")
        else:
            link_col.operator("aether.link_control_rig", text="Link", icon="LINKED")

        layout.separator()

        # Pointer fields section
        col = layout.column(align=True)
        col.label(text="Rig References:")
        
        # Meta Rig pointer field - adjust label width
        row = col.row(align=True)
        label_col = row.column(align=True)
        label_col.scale_x = 0.8
        label_col.label(text="Meta Rig")
        
        field_col = row.column(align=True)
        field_col.scale_x = 1.2
        field_col.prop(armature, "aether_meta_rig", text="")

        # Control Rig pointer field - adjust label width
        row = col.row(align=True)
        label_col = row.column(align=True)
        label_col.scale_x = 0.8
        label_col.label(text="Control Rig")
        
        field_col = row.column(align=True)
        field_col.scale_x = 1.2
        field_col.prop(armature, "aether_control_rig", text="")


def register():
    # Add custom properties to armature objects
    bpy.types.Object.aether_meta_rig = bpy.props.PointerProperty(
        name="Meta Rig",
        type=bpy.types.Object,
        description="Reference to the meta rig for this armature",
        poll=lambda self, obj: obj.type == 'ARMATURE'
    )
    
    bpy.types.Object.aether_control_rig = bpy.props.PointerProperty(
        name="Control Rig",
        type=bpy.types.Object,
        description="Reference to the control rig for this armature",
        poll=lambda self, obj: obj.type == 'ARMATURE'
    )
    
    bpy.types.Object.aether_control_linked = bpy.props.BoolProperty(
        name="Control Linked",
        description="Whether the control rig is linked to this armature",
        default=False
    )
    
    bpy.utils.register_class(AETHER_PT_MetaRigPanel)

def unregister():
    bpy.utils.unregister_class(AETHER_PT_MetaRigPanel)
    if hasattr(bpy.types.Object, 'aether_meta_rig'):
        del bpy.types.Object.aether_meta_rig
    if hasattr(bpy.types.Object, 'aether_control_rig'):
        del bpy.types.Object.aether_control_rig
    if hasattr(bpy.types.Object, 'aether_control_linked'):
        del bpy.types.Object.aether_control_linked