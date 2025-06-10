import bpy
from ..preferences import get_preferences

class AETHER_PT_InfoPanel(bpy.types.Panel):
    """Addon Info Panel"""
    bl_label = "AetherBlend Info"
    bl_idname = "aether.info_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "AetherBlend"

    def draw(self, context):
        layout = self.layout
        prefs = get_preferences()

        layout.label(text="Active Branch:")
        layout.label(text=f"dev")

def register():
    bpy.utils.register_class(AETHER_PT_InfoPanel)

def unregister():
    bpy.utils.unregister_class(AETHER_PT_InfoPanel)
        