import bpy
import os
from ..utils import system
from ..status import (
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

        if not status.restarted_check:
            row = layout.row()
            row.operator("aether.check_installs", text="Run Version Control", icon="FILE_REFRESH")
        else:
            row.operator("aether.check_installs", text="", icon="FILE_REFRESH")
        
        layout.separator()

        # --- VERSION CONTROL ---

        if status.get_status():
            if status.get_prompt_user_meddle() or status.get_prompt_user_aether():
                status_box = layout.box()
                status_col = status_box.column(align=False)
                status_col.label(text="Version Update Required")

                status_col.separator()

                if status.get_prompt_user_aether():
                    row = status_col.row()
                    row.label(text="AetherBlend", icon="ERROR")
                    row.operator("aether.restart_blender", text="Restart!", icon="FILE_REFRESH")
                if status.get_prompt_user_meddle():
                    row = status_col.row()
                    row.label(text="Meddle", icon="ERROR")
                    row.operator("aether.restart_blender", text="Restart!", icon="FILE_REFRESH")
            else:
                status_box = layout.box()
                status_col = status_box.column(align=False)
                status_col.label(text="Version Error")

                status_col.separator()

                # Check AetherBlend status
                if not status.is_branch:
                    row = status_col.row()
                    row.label(text="AetherBlend", icon="ERROR")
                    row.operator("aether.update", text="Update",  icon="IMPORT")
                elif not status.is_latest:
                    row = status_col.row()
                    row.label(text="AetherBlend", icon="ERROR")
                    row.operator("aether.update", text="Update",  icon="IMPORT")
                
                # Check Meddle status
                if not status.meddle_installed:
                    row = status_col.row()
                    row.label(text="Meddle", icon="CANCEL")
                    row.operator("wm.url_open", text="Github", icon="URL").url = f"https://github.com/{GITHUB_MEDDLE_USER}/{GITHUB_MEDDLE_REPO}/releases/latest"
                elif not status.meddle_is_latest:
                    row = status_col.row()
                    row.label(text="Meddle", icon="ERROR")
                    row.operator("aether.meddle_update", text="Update",  icon="IMPORT")
                elif not status.meddle_enabled:
                    row = status_col.row()
                    row.label(text="Meddle", icon="CHECKBOX_DEHLT")
                    row.operator("aether.enable_meddle", text="Enable", icon="CHECKBOX_HLT")


def register():
    bpy.utils.register_class(AETHER_PT_InfoPanel)

def unregister():
    bpy.utils.unregister_class(AETHER_PT_InfoPanel)
        