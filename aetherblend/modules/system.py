import os
import requests # type: ignore
import zipfile
import shutil
import subprocess
import tempfile
import bpy
from ..preferences import get_preferences

def confirm_action(message):
    """Show a confirmation popup and return True if accepted."""
    return bpy.ops.aether.confirm_dialog('INVOKE_DEFAULT', message=message)

class AETHER_OT_ConfirmDialog(bpy.types.Operator):
    """Confirmation Dialog"""
    bl_idname = "aether.confirm_dialog"
    bl_label = "Confirm Action"

    message: bpy.props.StringProperty(name="Message")

    def execute(self, context):
        self.report({'INFO'}, f"[AetherBlend] Confirmed: {self.message}")
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

def download_branch(branch):
    """Download the selected branch from GitHub and return the ZIP path."""
    prefs = get_preferences()
    github_repo = prefs.github_repo
    url = f"{github_repo}{branch}.zip"
    temp_dir = tempfile.mkdtemp()
    zip_path = os.path.join(temp_dir, f"{branch}.zip")

    try:
        response = requests.get(url, stream=True)
        if response.status_code != 200:
            print(f"[AetherBlend] Failed to download {branch} branch.")
            return None

        with open(zip_path, 'wb') as zip_file:
            zip_file.write(response.content)

    except Exception as e:
        print(f"[AetherBlend] Download error: {e}")
        return None

    return zip_path  # Return path for separate installation step

def install_branch(zip_path):
    """Extract and install the downloaded branch."""
    if not zip_path:
        print("[AetherBlend] Installation failed: No valid ZIP file.")
        return False

    temp_dir = tempfile.mkdtemp()

    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            extracted_folder = os.path.join(temp_dir, "aetherblend_extracted")
            zip_ref.extractall(extracted_folder)

            # Locate the main repo folder (e.g., "AetherBlend-main")
            extracted_main_folder = os.path.join(extracted_folder, os.listdir(extracted_folder)[0])

            # Locate the actual addon folder (`aetherblend/`) inside the repo
            extracted_addon_folder = os.path.join(extracted_main_folder, "aetherblend")

            prefs = get_preferences()
            addon_path = prefs.addon_path

            # Ensure the target folder exists
            if not os.path.exists(addon_path):
                os.makedirs(addon_path)

            # Remove old version safely
            shutil.rmtree(addon_path, ignore_errors=True)

            # Move the extracted addon folder to the correct location
            shutil.move(extracted_addon_folder, addon_path)

    except Exception as e:
        print(f"[AetherBlend] Installation failed: {e}")
        return False

    return True

def restart_blender():
    """Launch a new Blender instance and close the current one."""
    blender_path = bpy.app.binary_path
    subprocess.Popen([blender_path])  # Start new instance
    bpy.ops.wm.quit_blender()  # Close current instance