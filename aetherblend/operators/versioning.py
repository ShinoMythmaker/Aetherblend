import bpy
import os
from ..utils import system
from ..preferences import get_preferences, set_branch_match_result, set_version_match_result, set_meddle_installed, set_meddle_version_match_result


#Aetherblend GitHub repository information
GITHUB_USER = "ShinoMythmaker"
GITHUB_REPO = "Aetherblend"

#Meddle Github repository information
GITHUB_MEDDLE_USER = "PassiveModding"
GITHUB_MEDDLE_REPO = "MeddleTools"

# Local manifest path
EXTENSIONS_PATH = bpy.utils.user_resource('EXTENSIONS', path="user_default")
AETHERBLEND_FOLDER = os.path.join(EXTENSIONS_PATH, "aetherblend")
MEDDLE_FOLDER = os.path.join(EXTENSIONS_PATH, "meddle_tools")

class AETHER_OT_Update(bpy.types.Operator):
    """Installs the latest version of AetherBlend from GitHub"""
    bl_idname = "aether.update"
    bl_label = "Updates to newsest Version"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context): 
        prefs = get_preferences()
        branch = prefs.branch

        url = system.get_github_download_url(GITHUB_USER, GITHUB_REPO, branch=branch)
        zip = system.download_addon(url, GITHUB_REPO)
        
        try:
            bpy.ops.extensions.package_install_files(directory=EXTENSIONS_PATH, filepath=zip, repo='user_default', url=url)
            self.report({'INFO'}, f"[AetherBlend] Installed {GITHUB_REPO} on branch {branch}.")
            bpy.ops.aether.check_installs('INVOKE_DEFAULT')
        except Exception as e:
            self.report({'ERROR'}, f"[AetherBlend] Failed to install {GITHUB_REPO} on branch {branch}")
            return {'CANCELLED'}
        
        return {'FINISHED'}
    
class AETHER_OT_CheckBranchMatch(bpy.types.Operator):
    """Check if installed branch matches the selected branch in preferences"""
    bl_idname = "aether.check_branch_match"
    bl_label = "Check Branch Match"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        prefs = get_preferences()
        selected_branch = prefs.branch

        path = os.path.join(AETHERBLEND_FOLDER, "blender_manifest.toml")
        path = os.path.abspath(path)

        installed_branch = system.get_installed_branch(path)
        if installed_branch is None:
            self.report({'ERROR'}, "[AetherBlend] Could not determine installed branch.")
            set_branch_match_result(False)
            return {'CANCELLED'}

        if installed_branch == selected_branch:
            self.report({'INFO'}, f"[AetherBlend] Branch matches: {installed_branch}")
            set_branch_match_result(True)
        else:
            self.report({'WARNING'}, f"[AetherBlend] Branch mismatch: Installed '{installed_branch}', Selected '{selected_branch}'")
            set_branch_match_result(False)

        return {'FINISHED'}
    

class AETHER_OT_CheckVersionMatch(bpy.types.Operator):
    """Check if installed version matches the remote version for the selected branch"""
    bl_idname = "aether.check_version_match"
    bl_label = "Check Version Match"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        prefs = get_preferences()
        selected_branch = prefs.branch

        # Local manifest path
        local_manifest_path = os.path.join(AETHERBLEND_FOLDER, "blender_manifest.toml")
        local_manifest_path = os.path.abspath(local_manifest_path)

        # Get installed version
        installed_version = system.get_installed_version(local_manifest_path)
        if installed_version is None:
            self.report({'ERROR'}, "[AetherBlend] Could not determine installed version.")
            set_version_match_result(False)
            return {'CANCELLED'}

        # Get remote manifest URL and version
        remote_manifest_url = system.get_github_url(
            GITHUB_USER, GITHUB_REPO, branch=selected_branch, path="aetherblend/blender_manifest.toml"
        )
        remote_version = system.get_remote_version(remote_manifest_url)
        if remote_version is None:
            self.report({'ERROR'}, "[AetherBlend] Could not fetch remote version.")
            set_version_match_result(False)
            return {'CANCELLED'}

        # Compare versions
        if installed_version == remote_version:
            self.report({'INFO'}, f"[AetherBlend] Version up-to-date: {installed_version}")
            set_version_match_result(True)
        else:
            self.report({'WARNING'}, f"[AetherBlend] Version mismatch: Installed '{installed_version}', Remote '{remote_version}'")
            set_version_match_result(False)

        return {'FINISHED'}
    
class AETHER_OT_CheckMeddleInstalled(bpy.types.Operator):
    """Check if Meddle add-on is installed"""
    bl_idname = "aether.check_meddle_installed"
    bl_label = "Check Meddle Installed"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, _):
        if system.is_addon_installed("Meddle Tools"):
            self.report({'INFO'}, "[AetherBlend] Meddle is installed.")
            set_meddle_installed(True)
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "[AetherBlend] Meddle is NOT installed.")
            set_meddle_installed(False)
            return {'CANCELLED'}
    
class AETHER_OT_CheckMeddleVersionMatch(bpy.types.Operator):
    """Check if installed Meddle version matches the remote version for the main branch"""
    bl_idname = "aether.check_meddle_version_match"
    bl_label = "Check Version Match"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected_branch = "main"

        # Local manifest path
        local_manifest_path = os.path.join(MEDDLE_FOLDER, "blender_manifest.toml")
        local_manifest_path = os.path.abspath(local_manifest_path)

        # Get installed version
        installed_version = system.get_installed_version(local_manifest_path)
        if installed_version is None:
            self.report({'ERROR'}, "[AetherBlend] Could not determine installed version.")
            set_meddle_version_match_result(False)
            return {'CANCELLED'}

        # Get remote manifest URL and version
        remote_manifest_url = system.get_github_url(
            GITHUB_MEDDLE_USER, GITHUB_MEDDLE_REPO, branch=selected_branch, path="MeddleTools/blender_manifest.toml"
        )
        remote_version = system.get_remote_version(remote_manifest_url)
        if remote_version is None:
            self.report({'ERROR'}, "[AetherBlend] Could not fetch remote version.")
            set_meddle_version_match_result(False)
            return {'CANCELLED'}

        # Compare versions
        if installed_version == remote_version:
            self.report({'INFO'}, f"[AetherBlend] Version up-to-date: {installed_version}")
            set_meddle_version_match_result(True)
        else:
            self.report({'WARNING'}, f"[AetherBlend] Version mismatch: Installed '{installed_version}', Remote '{remote_version}'")
            set_meddle_version_match_result(False)

        return {'FINISHED'}
    
class AETHER_OT_Meddle_Update(bpy.types.Operator):
    """Installs the latest Meddle Tools from GitHub"""
    bl_idname = "aether.meddle_update"
    bl_label = "Installs latest Meddle Tools"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context): 
        branch = "main"

        url = system.get_github_download_url(GITHUB_MEDDLE_USER, GITHUB_MEDDLE_REPO, branch)

        zip = system.download_addon(url, GITHUB_MEDDLE_REPO)
        
        try:
            bpy.ops.extensions.package_install_files(directory=EXTENSIONS_PATH, filepath=zip, repo='user_default', url=url)
            self.report({'INFO'}, f"[AetherBlend] Installed {GITHUB_MEDDLE_REPO}.")
            bpy.ops.aether.check_installs('INVOKE_DEFAULT')
        except Exception as e:
            self.report({'ERROR'}, f"[AetherBlend] Failed to install {GITHUB_MEDDLE_REPO}. Error: {e}")
            return {'CANCELLED'}
        
        return {'FINISHED'}
    
class AETHER_OT_RestartBlender(bpy.types.Operator):
    """Prompt user to save and restart Blender"""
    bl_idname = "aether.restart_blender"
    bl_label = "Restart Blender"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Restart Blender
        system.restart_blender()
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
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Check AetherBlend installation
        try:
            bpy.ops.aether.check_branch_match()
        except Exception as e:
            self.report({'ERROR'}, f"{e}")
            return {'CANCELLED'}
        
        try:
            bpy.ops.aether.check_version_match()
        except Exception as e:
            self.report({'ERROR'}, f"{e}")
            return {'CANCELLED'}

        # Check Meddle installation
        try:
            bpy.ops.aether.check_meddle_installed()
        except Exception as e:
            self.report({'ERROR'}, f"{e}")
            return {'CANCELLED'}
        try:
            bpy.ops.aether.check_meddle_version_match()
        except Exception as e:
            self.report({'ERROR'}, f"{e}")
            return {'CANCELLED'}

        return {'FINISHED'}



def register():
    bpy.utils.register_class(AETHER_OT_Update)
    bpy.utils.register_class(AETHER_OT_CheckBranchMatch)
    bpy.utils.register_class(AETHER_OT_CheckVersionMatch)
    bpy.utils.register_class(AETHER_OT_CheckMeddleInstalled)
    bpy.utils.register_class(AETHER_OT_CheckMeddleVersionMatch)
    bpy.utils.register_class(AETHER_OT_Meddle_Update)
    bpy.utils.register_class(AETHER_OT_RestartBlender)
    bpy.utils.register_class(AETHER_OT_CheckInstalls)

def unregister():
    bpy.utils.unregister_class(AETHER_OT_Update)
    bpy.utils.unregister_class(AETHER_OT_CheckBranchMatch)
    bpy.utils.unregister_class(AETHER_OT_CheckVersionMatch)
    bpy.utils.unregister_class(AETHER_OT_CheckMeddleInstalled)
    bpy.utils.unregister_class(AETHER_OT_CheckMeddleVersionMatch)
    bpy.utils.unregister_class(AETHER_OT_Meddle_Update)
    bpy.utils.unregister_class(AETHER_OT_RestartBlender)
    bpy.utils.unregister_class(AETHER_OT_CheckInstalls)