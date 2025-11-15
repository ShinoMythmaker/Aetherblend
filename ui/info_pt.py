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


def register():
    bpy.utils.register_class(AETHER_PT_InfoPanel)

def unregister():
    bpy.utils.unregister_class(AETHER_PT_InfoPanel)
        