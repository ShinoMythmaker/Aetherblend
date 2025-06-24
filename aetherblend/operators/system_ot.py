import bpy
from ..utils import system
import subprocess
import addon_utils
from ..preferences import get_preferences
from ..status import AetherBlendStatus as status, GITHUB_USER, GITHUB_REPO, GITHUB_MEDDLE_USER, GITHUB_MEDDLE_REPO, EXTENSIONS_PATH 


class AETHER_OT_Meddle_Update(bpy.types.Operator):
    """Installs the latest Meddle Tools from GitHub"""
    bl_idname = "aether.meddle_update"
    bl_label = "Installs latest Meddle Tools"
    bl_options = {'REGISTER'}

    def execute(self, context): 
        bpy.context.window.cursor_set('WAIT')  
        branch = "main"

        if status.prompt_user_meddle:
            self.report({'ERROR'}, "[AetherBlend] Previous update is not fully initialized, please restart Blender first.")
            return {'CANCELLED'}
        
        url = system.get_github_download_url(GITHUB_MEDDLE_USER, GITHUB_MEDDLE_REPO, branch)
        zip = system.download_zip(url, GITHUB_MEDDLE_REPO)

        if zip is None:
            self.report({'ERROR'}, "[AetherBlend] Failed to download Meddle Tools.")
            return {'CANCELLED'}
        
        try:
            bpy.ops.extensions.package_install_files(directory=EXTENSIONS_PATH, filepath=zip, repo='user_default', url=url)
            status.set_prompt_user_meddle(True)
            self.report({'INFO'}, f"[AetherBlend] New Meddle Version installed.")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Failed to install: {e}")
            return {'CANCELLED'}

class AETHER_OT_Update(bpy.types.Operator):
    """Installs the latest version of AetherBlend from GitHub"""
    bl_idname = "aether.update"
    bl_label = "Updates to newest Version"
    bl_options = {'REGISTER'}

    def execute(self, context): 
        prefs = get_preferences()
        branch = prefs.branch

        if status.prompt_user_aether:
            self.report({'ERROR'}, "[AetherBlend] Previous update is not fully initialized, please restart Blender first.")
            return {'CANCELLED'}

        url = system.get_github_download_url(GITHUB_USER, GITHUB_REPO, branch=branch)
        zip = system.download_zip(url, GITHUB_REPO)

        if zip is None:
            self.report({'ERROR'}, "[AetherBlend] Failed to download Meddle Tools.")
            return {'CANCELLED'}
    
        try:
            bpy.ops.extensions.package_install_files(directory=EXTENSIONS_PATH, filepath=zip, repo='user_default', url=url)
            status.set_prompt_user_aether(True)
            self.report({'INFO'}, f"[AetherBlend] New Version Installed")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Failed to install: {e}")
            return {'CANCELLED'}
    
class AETHER_OT_CheckInstalls(bpy.types.Operator):
    """Check if AetherBlend and Meddle are installed and up-to-date"""
    bl_idname = "aether.check_installs"
    bl_label = "Check Installations"
    bl_options = {'REGISTER'}

    def execute(self, context):
        prefs = get_preferences()
        status.check_installs(prefs.branch)
        self.report({'INFO'}, "[AetherBlend] Check complete.")

        return {'FINISHED'}

class AETHER_OT_EnableMeddle(bpy.types.Operator):
    """Enable the Meddle add-on/extension if installed"""
    bl_idname = "aether.enable_meddle"
    bl_label = "Enable Meddle"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        info = system.get_addon_info("Meddle Tools")

        if not info["installed"]:
            self.report({'ERROR'}, "Meddle is not installed.")
            return {'CANCELLED'}
        try:
            addon_utils.enable(info["name"], default_set=True, persistent=True)
            self.report({'INFO'}, "Meddle enabled.")
        except Exception as e:
            self.report({'ERROR'}, f"Failed to enable Meddle: {e}")
            return {'CANCELLED'}
        
        status.check_meddle_status()
        system.update_window()

        return {'FINISHED'}
    
class AETHER_OT_RestartBlender(bpy.types.Operator):
    """Prompt user to save and restart Blender"""
    bl_idname = "aether.restart_blender"
    bl_label = "Restart Required"
    bl_options = {'REGISTER'}

    def execute(self, context):
        # Restart Blender
        blender_path = bpy.app.binary_path
        subprocess.Popen([blender_path])  # Start new instance
        bpy.ops.wm.quit_blender()  # Close current instance
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(
            self, event,
            message="Restart now? Unsaved work will be lost."
        )


def register():
    bpy.utils.register_class(AETHER_OT_Update)
    bpy.utils.register_class(AETHER_OT_Meddle_Update)
    bpy.utils.register_class(AETHER_OT_CheckInstalls)
    bpy.utils.register_class(AETHER_OT_EnableMeddle)
    bpy.utils.register_class(AETHER_OT_RestartBlender)

def unregister():
    bpy.utils.unregister_class(AETHER_OT_EnableMeddle)
    bpy.utils.unregister_class(AETHER_OT_CheckInstalls)
    bpy.utils.unregister_class(AETHER_OT_Update)
    bpy.utils.unregister_class(AETHER_OT_Meddle_Update)
    bpy.utils.unregister_class(AETHER_OT_RestartBlender)