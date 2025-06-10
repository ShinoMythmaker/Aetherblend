import os
import requests
import zipfile
import shutil
import subprocess
import tempfile
import bpy
from ..preferences import get_preferences 

def confirm_action(message):
    """Display a confirmation dialog and return True if accepted."""
    return bpy.ops.wm.confirm_dialog('INVOKE_DEFAULT', message=message)

def download_branch(branch):
    """Download and extract the selected branch using preferences."""
    prefs = get_preferences()
    github_repo = prefs.github_repo  
    addon_path = prefs.addon_path    

    url = f"{github_repo}{branch}.zip"
    temp_dir = tempfile.mkdtemp()
    zip_path = os.path.join(temp_dir, f"{branch}.zip")

    try:
        response = requests.get(url, stream=True)
        if response.status_code != 200:
            print(f"[AetherBlend] Failed to download {branch} branch.")
            return False

        with open(zip_path, 'wb') as zip_file:
            zip_file.write(response.content)

        # Extract contents
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # Locate the correct subfolder (`aetherblend/`)
        extracted_folder = os.path.join(temp_dir, "aetherblend")
        if not os.path.exists(extracted_folder):
            print(f"[AetherBlend] Error: Extracted folder not found.")
            return False

        # Move files into addon directory
        for item in os.listdir(extracted_folder):
            shutil.move(os.path.join(extracted_folder, item), addon_path)

    except Exception as e:
        print(f"[AetherBlend] Branch switch error: {e}")
        return False

    return True

def restart_blender():
    """Launch a new Blender instance and close the current one."""
    blender_path = bpy.app.binary_path
    subprocess.Popen([blender_path])  # Start new instance
    bpy.ops.wm.quit_blender()  # Close current instance