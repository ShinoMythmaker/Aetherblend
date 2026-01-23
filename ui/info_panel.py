import bpy

GITHUB_URL = "https://github.com/ShinoMythmaker/Aetherblend"

class AETHER_PT_InfoPanel(bpy.types.Panel):
    """Addon Info Panel"""
    bl_label = " "
    bl_idname = "AETHER_PT_info_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "AetherBlend"
    bl_order = 0 

    def draw_header(self, context):
        self.layout.label(text=f"AetherBlend")

    def draw(self, context):
        layout = self.layout
        
        layout.operator("wm.url_open", text="Support & Links", icon="HEART").url = "https://shinomythmaker.carrd.co/"
        
        row = layout.row()
        row.operator("wm.url_open", text="Wiki", icon="HELP").url = f"{GITHUB_URL}/wiki"
        row.operator("wm.url_open", text="Issues", icon="BOOKMARKS").url = f"{GITHUB_URL}/issues"
        
        # Tab selector
        layout.separator()
        tabs = context.scene.aether_tabs
        
        # Check if armature is selected
        armature = context.active_object
        has_armature = armature is not None and armature.type == 'ARMATURE'
        
        # Check if armature has rig_id (for Rig Layers tab)
        has_rig_id = False
        if has_armature:
            rig_id = armature.data.get("rig_id")
            has_rig_id = rig_id is not None
        
        split = layout.split(factor=0.2, align=True)
        split.prop_enum(tabs, "active_tab", 'IMPORT_EXPORT', icon='FILE', text="")
        split = split.split(factor=0.25, align=True)
        col = split.column(align=True)
        col.enabled = has_armature
        col.prop_enum(tabs, "active_tab", 'CPLUS', text="C+")
        split = split.split(factor=0.333, align=True)
        col = split.column(align=True)
        col.enabled = has_armature
        col.prop_enum(tabs, "active_tab", 'GENERATE', icon='POSE_HLT', text="")
        split = split.split(factor=0.5, align=True)
        col = split.column(align=True)
        col.enabled = has_rig_id
        col.prop_enum(tabs, "active_tab", 'RIG_LAYERS', icon='BONE_DATA', text="")
        col = split.column(align=True)
        col.enabled = has_rig_id
        col.prop_enum(tabs, "active_tab", 'RIG_UI', icon='PROPERTIES', text="")


def register():
    bpy.utils.register_class(AETHER_PT_InfoPanel)

def unregister():
    bpy.utils.unregister_class(AETHER_PT_InfoPanel)
        