import bpy
import os
import subprocess
from ..utils import system
from ..preferences import (
    get_preferences, AetherBlendStatus as status,
    GITHUB_USER, GITHUB_REPO,
    GITHUB_MEDDLE_USER, GITHUB_MEDDLE_REPO,
    EXTENSIONS_PATH, AETHERBLEND_FOLDER, MEDDLE_FOLDER
)

    
def check_branch_match(self, context):
    """Check if the installed branch matches the selected branch in preferences"""
    prefs = get_preferences()
    selected_branch = prefs.branch

    # Local manifest path
    local_manifest_path = os.path.join(AETHERBLEND_FOLDER, "blender_manifest.toml")
    local_manifest_path = os.path.abspath(local_manifest_path)

    # Get installed branch
    installed_branch = system.parse_key_from_manifest(local_manifest_path, "branch")
    if installed_branch is None:
        self.report({'WARNING'}, "[AetherBlend] Could not determine installed branch.")
        status.set(BRANCH_MATCH_RESULT=False)
        return {'CANCELLED'}

    # Compare branches
    if installed_branch == selected_branch:
        self.report({'INFO'}, f"[AetherBlend] Branch match: {installed_branch}")
        status.set(BRANCH_MATCH_RESULT=True)
    else:
        self.report({'WARNING'}, f"[AetherBlend] Branch mismatch: Installed '{installed_branch}', Selected '{selected_branch}'")
        status.set(BRANCH_MATCH_RESULT=False)

    return {'FINISHED'}
    
def check_version_match(self, context):
    """Check if the installed version matches the remote version on GitHub"""
    prefs = get_preferences()
    selected_branch = prefs.branch

    # Local manifest path
    local_manifest_path = os.path.join(AETHERBLEND_FOLDER, "blender_manifest.toml")
    local_manifest_path = os.path.abspath(local_manifest_path)

    # Get installed version
    installed_version = system.parse_key_from_manifest(local_manifest_path, "version")
    if installed_version is None:
        self.report({'WARNING'}, "[AetherBlend] Could not determine installed version.")
        status.set(VERSION_MATCH_RESULT=False)
        return {'CANCELLED'}

    # Get remote manifest URL and version
    remote_manifest_url = system.get_github_url(
        GITHUB_USER, GITHUB_REPO, branch=selected_branch, path="aetherblend/blender_manifest.toml"
    )
    remote_version = system.parse_key_from_remote_manifest(remote_manifest_url, "version")
    if remote_version is None:
        self.report({'WARNING'}, "[AetherBlend] Could not fetch remote version.")
        status.set(VERSION_MATCH_RESULT=False)
        return {'CANCELLED'}

    # Compare versions
    if installed_version == remote_version:
        self.report({'INFO'}, f"[AetherBlend] Version up-to-date: {installed_version}")
        status.set(VERSION_MATCH_RESULT=True)
    else:
        self.report({'WARNING'}, f"[AetherBlend] Version mismatch: Installed '{installed_version}', Remote '{remote_version}'")
        status.set(VERSION_MATCH_RESULT=False)

    return {'FINISHED'}
    
def check_meddle_installed(self, context):
    """Check if Meddle Tools is installed"""
    if system.is_addon_installed("Meddle Tools"):
        self.report({'INFO'}, "[AetherBlend][Meddle] Meddle is installed.")
        status.set(MEDDLE_INSTALLED=True)
        return {'FINISHED'}
    else:
        self.report({'ERROR'}, "[AetherBlend][Meddle] Meddle is NOT installed.")
        status.set(MEDDLE_INSTALLED=False)
        return {'CANCELLED'}
    
def check_meddle_version_match(self, context):
    """Check if the installed Meddle version matches the remote version on GitHub"""
    selected_branch = "main"

    # Local manifest path
    local_manifest_path = os.path.join(MEDDLE_FOLDER, "blender_manifest.toml")
    local_manifest_path = os.path.abspath(local_manifest_path)

    # Get installed version
    installed_version = system.parse_key_from_manifest(local_manifest_path, "version")
    if installed_version is None:
        self.report({'WARNING'}, "[AetherBlend][Meddle] Could not determine installed version.")
        status.set(MEDDLE_VERSION_MATCH_RESULT=False)
        return {'CANCELLED'}

    # Get remote manifest URL and version
    remote_manifest_url = system.get_github_url(
        GITHUB_MEDDLE_USER, GITHUB_MEDDLE_REPO, branch=selected_branch, path="MeddleTools/blender_manifest.toml"
    )
    remote_version = system.parse_key_from_remote_manifest(remote_manifest_url, "version")
    if remote_version is None:
        self.report({'WARNING'}, "[AetherBlend][Meddle] Could not fetch remote version.")
        status.set(MEDDLE_VERSION_MATCH_RESULT=False)
        return {'CANCELLED'}

    # Compare versions
    if installed_version == remote_version:
        self.report({'INFO'}, f"[AetherBlend][Meddle] Version up-to-date: {installed_version}")
        status.set(MEDDLE_VERSION_MATCH_RESULT=True)
    else:
        self.report({'WARNING'}, f"[AetherBlend][Meddle] Version mismatch: Installed '{installed_version}', Remote '{remote_version}'")
        status.set(MEDDLE_VERSION_MATCH_RESULT=False)

    return {'FINISHED'}
    
class AETHER_OT_Meddle_Update(bpy.types.Operator):
    """Installs the latest Meddle Tools from GitHub"""
    bl_idname = "aether.meddle_update"
    bl_label = "Installs latest Meddle Tools"
    bl_options = {'REGISTER'}

    def execute(self, context): 
        bpy.context.window.cursor_set('WAIT')  
        branch = "main"

        url = system.get_github_download_url(GITHUB_MEDDLE_USER, GITHUB_MEDDLE_REPO, branch)

        zip = system.download_zip(url, GITHUB_MEDDLE_REPO)
        
        try:
            bpy.ops.extensions.package_install_files(directory=EXTENSIONS_PATH, filepath=zip, repo='user_default', url=url)
            self.report({'INFO'}, f"[AetherBlend] Installed {GITHUB_MEDDLE_REPO}.")
            bpy.ops.aether.check_installs('EXEC_DEFAULT')
        except Exception as e:
            self.report({'ERROR'}, f"[AetherBlend] Failed to install {GITHUB_MEDDLE_REPO}. Error: {e}")
            return {'CANCELLED'}
        
        bpy.context.window.cursor_set('DEFAULT')  
        
        return {'FINISHED'}

class AETHER_OT_Update(bpy.types.Operator):
    """Installs the latest version of AetherBlend from GitHub"""
    bl_idname = "aether.update"
    bl_label = "Updates to newest Version"
    bl_options = {'REGISTER'}

    def execute(self, context): 
        bpy.context.window.cursor_set('WAIT')  
        prefs = get_preferences()
        branch = prefs.branch

        url = system.get_github_download_url(GITHUB_USER, GITHUB_REPO, branch=branch)
        zip = system.download_zip(url, GITHUB_REPO)
    
        try:
            bpy.ops.extensions.package_install_files(directory=EXTENSIONS_PATH, filepath=zip, repo='user_default', url=url)
            self.report({'INFO'}, f"[AetherBlend] Installed {GITHUB_REPO} on branch {branch}.")
            bpy.ops.aether.check_installs('EXEC_DEFAULT')
        except Exception as e:
            self.report({'ERROR'}, f"[AetherBlend] Failed to install {GITHUB_REPO} on branch {branch}")
            return {'CANCELLED'}
    
        bpy.context.window.cursor_set('DEFAULT')  

        return {'FINISHED'}
     
class AETHER_OT_RestartBlender(bpy.types.Operator):
    """Prompt user to save and restart Blender"""
    bl_idname = "aether.restart_blender"
    bl_label = "Restart Blender"
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
            message="Are you sure you want to restart Blender? Unsaved work will be lost."
        )
    
class AETHER_OT_CheckInstalls(bpy.types.Operator):
    """Check if AetherBlend and Meddle are installed and up-to-date"""
    bl_idname = "aether.check_installs"
    bl_label = "Check Installations"
    bl_options = {'REGISTER'}

    def execute(self, context):
        bpy.context.window.cursor_set('WAIT')

        check_branch_match(self, context)
        check_version_match(self, context)
        check_meddle_installed(self, context)
        check_meddle_version_match(self, context)

        bpy.context.window.cursor_set('DEFAULT')

        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas:
                if area.type == 'VIEW_3D': 
                    area.tag_redraw()

        return {'FINISHED'}

def register():
    bpy.utils.register_class(AETHER_OT_Update)
    bpy.utils.register_class(AETHER_OT_Meddle_Update)
    bpy.utils.register_class(AETHER_OT_RestartBlender)
    bpy.utils.register_class(AETHER_OT_CheckInstalls)

def unregister():
    bpy.utils.unregister_class(AETHER_OT_Update)
    bpy.utils.unregister_class(AETHER_OT_Meddle_Update)
    bpy.utils.unregister_class(AETHER_OT_RestartBlender)
    bpy.utils.unregister_class(AETHER_OT_CheckInstalls)