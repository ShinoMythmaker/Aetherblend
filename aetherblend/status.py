from .utils import system
import bpy
import os

# Aetherblend GitHub repository information
GITHUB_USER = "ShinoMythmaker"
GITHUB_REPO = "Aetherblend"

# Meddle Github repository information
GITHUB_MEDDLE_USER = "PassiveModding"
GITHUB_MEDDLE_REPO = "MeddleTools"

# Extension and manifest paths
EXTENSIONS_PATH = bpy.utils.user_resource('EXTENSIONS', path="user_default")
AETHERBLEND_FOLDER = os.path.join(EXTENSIONS_PATH, "aetherblend")
MEDDLE_FOLDER = os.path.join(EXTENSIONS_PATH, "meddle_tools")

class AetherBlendStatus:
    """Class to hold the status of AetherBlend and Meddle installations."""
    startup_check = False
    is_branch = False
    is_latest = False
    meddle_installed = False
    meddle_enabled = False
    meddle_is_latest = False
    
    @staticmethod
    def get_prompt_user_aether():
        """Returns whether the user has been prompted to restart Blender for AetherBlend."""
        return bpy.app.driver_namespace.get("aetherblend_prompt_user", False)

    @staticmethod
    def set_prompt_user_aether(value: bool):
        """Sets whether the user has been prompted to restart Blender for AetherBlend."""
        bpy.app.driver_namespace["aetherblend_prompt_user"] = value

    @staticmethod
    def get_prompt_user_meddle():
        """Returns whether the user has been prompted to restart Blender for Meddle."""
        return bpy.app.driver_namespace.get("meddle_prompt_user", False)

    @staticmethod
    def set_prompt_user_meddle(value: bool):
        """Sets whether the user has been prompted to restart Blender for Meddle."""
        bpy.app.driver_namespace["meddle_prompt_user"] = value

    @staticmethod
    def get_meddle_status():
        """Reads if Meddle is installed and up-to-date."""
        return (AetherBlendStatus.meddle_installed and AetherBlendStatus.meddle_is_latest and AetherBlendStatus.meddle_enabled and AetherBlendStatus.startup_check)

    @staticmethod
    def get_aetherblend_status():
        """Reads if AetherBlend is installed and up-to-date."""
        return (AetherBlendStatus.is_branch and AetherBlendStatus.is_latest and AetherBlendStatus.startup_check)
    
    @staticmethod
    def get_status():
        """Returns the overall status of AetherBlend and Meddle installations."""
        return (AetherBlendStatus.get_aetherblend_status() and AetherBlendStatus.get_meddle_status())


    @staticmethod
    def check_installs(branch="main"):
        """Check if AetherBlend and Meddle are installed and up-to-date."""
        print("[AetherBlend] Checking installations...")

        AetherBlendStatus.check_aetherblend_status(branch)
        AetherBlendStatus.check_meddle_status()
        AetherBlendStatus.startup_check = True
        system.update_window()

        print("[AetherBlend] All checks completed successfully.")

        return {'FINISHED'}
    

    @staticmethod
    def check_aetherblend_status(remote_branch="main"):
        """Check if AetherBlend is installed and up-to-date."""
        info = system.get_addon_info("AetherBlend")

        installed = info["installed"]
        enabled = info["enabled"]
        version = info["version"]
        local_branch = info["branch"]

        AetherBlendStatus.is_branch = False
        AetherBlendStatus.is_latest = False

        if not installed:
            print("[AetherBlend] AetherBlend is NOT installed.")
            return {'CANCELLED'}

        if local_branch is None:
            print("[AetherBlend] Could not determine installed branch.")
            return {'CANCELLED'}
        elif local_branch == remote_branch:
            print(f"[AetherBlend] Branch match: {local_branch}")
            AetherBlendStatus.is_branch = True
        else:
            print(f"[AetherBlend] Branch mismatch: Installed '{local_branch}', Selected '{remote_branch}'")
            return {'CANCELLED'}

        if version is None:
            print("[AetherBlend] Could not determine installed version.")
            return {'CANCELLED'}

        remote_manifest_url = system.get_github_url(
            GITHUB_USER, GITHUB_REPO, branch=remote_branch, path="aetherblend/blender_manifest.toml"
        )
        remote_version = system.parse_key_from_remote_manifest(remote_manifest_url, "version")
        if remote_version is None:
            print("[AetherBlend] Could not fetch remote version.")
            return {'CANCELLED'}

        if version == remote_version:
            print(f"[AetherBlend] Version up-to-date: {version}")
            AetherBlendStatus.is_latest = True
        else:
            print(f"[AetherBlend] Version mismatch: Installed '{version}', Remote '{remote_version}'")
        
        return {'FINISHED'}

    @staticmethod
    def check_meddle_status(): 
        """Check if Meddle Tools is installed and up-to-date."""    
        info = system.get_addon_info("Meddle Tools")

        installed = info["installed"]
        enabled = info["enabled"]
        version = info["version"]
        branch = "main"

        AetherBlendStatus.meddle_installed = installed
        AetherBlendStatus.meddle_enabled = enabled
        AetherBlendStatus.meddle_is_latest = False

        if info is None or not installed:
            print("[AetherBlend] Meddle is NOT installed.") 
            return {'CANCELLED'}

        print("[AetherBlend] Meddle is installed.")

        if version is None:
            print("[AetherBlend] Meddle could not determine installed version.")
            return {'CANCELLED'}

        remote_manifest_url = system.get_github_url(
            GITHUB_MEDDLE_USER, GITHUB_MEDDLE_REPO, branch=branch, path="MeddleTools/blender_manifest.toml"
        )
        remote_version = system.parse_key_from_remote_manifest(remote_manifest_url, "version")
        if remote_version is None:
            print("[AetherBlend] Meddle could not fetch remote version.")
            return {'CANCELLED'}

        if version == remote_version:
            print(f"[AetherBlend] Meddle version up-to-date: {version}")
            AetherBlendStatus.meddle_is_latest = True
        else:
            print(f"[AetherBlend] Meddle version mismatch: Installed '{version}', Remote '{remote_version}'")
            return {'CANCELLED'}

        if enabled:
            print("[AetherBlend] Meddle is enabled.")
        else:
            print("[AetherBlend] Meddle is installed but NOT enabled.")

        return {'FINISHED'}