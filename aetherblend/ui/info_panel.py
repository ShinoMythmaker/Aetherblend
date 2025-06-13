import bpy
from ..preferences import get_branch_match_result

class AETHER_PT_InfoPanel(bpy.types.Panel):
    """Addon Info Panel"""
    bl_label = "AetherBlend Info"
    bl_idname = "AETHER_PT_info_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "AetherBlend"

    def draw(self, context):
        layout = self.layout
        branch = get_branch_match_result()

        layout.label(text="Active Branch:")
        layout.label(text=f"dev")

        # Show branch match result
        if branch is True:
            layout.label(text="Branch Match: Yes", icon='CHECKMARK')
        elif branch is False:
            layout.label(text="Branch Match: No", icon='ERROR')
        else:
            layout.label(text="Branch Match: Unknown", icon='QUESTION')

        # Button to execute the version mismatch operator
        layout.operator("aether.check_branch_match", text="Check Branch Match", icon='FILE_REFRESH')
        layout.operator("aether.check_version_match", text="Check Version Match", icon='FILE_REFRESH')
        layout.operator("aether.check_meddle_installed", text="Check Meddle Install", icon='FILE_REFRESH')
        layout.operator("aether.check_meddle_version_match", text="Check Meddle Version", icon='FILE_REFRESH')

def register():
    bpy.utils.register_class(AETHER_PT_InfoPanel)

def unregister():
    bpy.utils.unregister_class(AETHER_PT_InfoPanel)
        