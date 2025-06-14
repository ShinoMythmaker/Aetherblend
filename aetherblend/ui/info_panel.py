import bpy
import os
from ..utils import system
from ..preferences import (
    AetherBlendStatus as status,
    GITHUB_USER, GITHUB_REPO,
    GITHUB_MEDDLE_USER, GITHUB_MEDDLE_REPO,
    AETHERBLEND_FOLDER
)

class AETHER_PT_InfoPanel(bpy.types.Panel):
    """Addon Info Panel"""
    bl_label = " "
    bl_idname = "AETHER_PT_info_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "AetherBlend"

    def draw_header(self, context):
        self.local_manifest_path = os.path.join(AETHERBLEND_FOLDER, "blender_manifest.toml")
        self.local_manifest_path = os.path.abspath(self.local_manifest_path)

        self.layout.label(text=f"AetherBlend {system.parse_key_from_manifest(self.local_manifest_path, 'version')} - {system.parse_key_from_manifest(self.local_manifest_path, 'branch')}")


    def draw(self, context):
        layout = self.layout
        
        layout.operator("wm.url_open", text="Support & Links", icon="HEART").url = "https://mektools.carrd.co/"
        
        row = layout.row()
        row.operator("wm.url_open", text="Wiki", icon="HELP").url = f"https://github.com/{GITHUB_USER}/{GITHUB_REPO}/wiki"
        row.operator("wm.url_open", text="Issues", icon="BOOKMARKS").url = f"https://github.com/{GITHUB_USER}/{GITHUB_REPO}/issues"
        row.operator("aether.check_installs", text="", icon="FILE_REFRESH")
        
        layout.separator()

        # --- VERSION CONTROL ---
        show_status = (
            not status.BRANCH_MATCH_RESULT or
            not status.VERSION_MATCH_RESULT or
            not status.MEDDLE_INSTALLED or
            not status.MEDDLE_VERSION_MATCH_RESULT
        )

        if show_status:
            status_box = layout.box()
            status_col = status_box.column(align=False)
            status_col.label(text="Version Error")

            status_col.separator()

            if not status.BRANCH_MATCH_RESULT:
                row = status_col.row()
                row.label(text="AetherBlend", icon="ERROR")
                row.operator("aether.update", text="Update",  icon="IMPORT")
            elif not status.VERSION_MATCH_RESULT:
                row = status_col.row()
                row.label(text="AetherBlend", icon="ERROR")
                row.operator("aether.update", text="Update",  icon="IMPORT")

            if not status.MEDDLE_INSTALLED:
                row = status_col.row()
                row.label(text="Meddle", icon="CANCEL")
                row.operator("wm.url_open", text="Github", icon="URL").url = f"https://github.com/{GITHUB_MEDDLE_USER}/{GITHUB_MEDDLE_REPO}/releases/latest"
            elif not status.MEDDLE_VERSION_MATCH_RESULT:
                row = status_col.row()
                row.label(text="Meddle", icon="ERROR")
                row.operator("aether.meddle_update", text="Update",  icon="IMPORT")

def register():
    bpy.utils.register_class(AETHER_PT_InfoPanel)

def unregister():
    bpy.utils.unregister_class(AETHER_PT_InfoPanel)
        