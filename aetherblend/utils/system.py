import os
import requests
import zipfile
import shutil
import subprocess
import tempfile
import bpy
import addon_utils

def download_addon(url: str, name: str = "download") -> str:
    """Download the selected branch from GitHub and return the ZIP path."""
    temp_dir = tempfile.mkdtemp()
    zip_path = os.path.join(temp_dir, f"{name}.zip")

    try:
        response = requests.get(url, stream=True)
        if response.status_code != 200:
            print(f"[AetherBlend] Failed to download {url}.")
            return None

        with open(zip_path, 'wb') as zip_file:
            zip_file.write(response.content)

    except Exception as e:
        print(f"[AetherBlend] Download error: {e}")
        return None

    return zip_path  # Return path

def install_addon(zip_path: str, path: str, name: str = "download") -> bool:
    """Extract and install the downloaded branch."""
    if not zip_path:
        print("[AetherBlend] Installation failed: No valid ZIP file.")
        return False

    temp_dir = tempfile.mkdtemp()

    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            extracted_folder = os.path.join(temp_dir, f"{name}_extracted")
            zip_ref.extractall(extracted_folder)

            # Locate the main repo folder (e.g., "AetherBlend-main")
            extracted_main_folder = os.path.join(extracted_folder, os.listdir(extracted_folder)[0])

            # Locate the actual addon folder (`aetherblend/`) inside the repo
            extracted_addon_folder = os.path.join(extracted_main_folder, name)

            # Ensure the target folder exists
            if not os.path.exists(path):
                os.makedirs(path)

            # Remove old version safely
            shutil.rmtree(path, ignore_errors=True)

            # Move the extracted addon folder to the correct location
            shutil.move(extracted_addon_folder, path)

    except Exception as e:
        print(f"[AetherBlend] Installation failed: {e}")
        return False

    return True

def restart_blender():
    """Launch a new Blender instance and close the current one."""
    blender_path = bpy.app.binary_path
    subprocess.Popen([blender_path])  # Start new instance
    bpy.ops.wm.quit_blender()  # Close current instance


def parse_simple_manifest(path_or_text):
    """Parse a simple key=value manifest file and return a dict."""
    data = {}
    if isinstance(path_or_text, str) and os.path.exists(path_or_text):
        with open(path_or_text, "r") as f:
            lines = f.readlines()
    else:
        # Assume it's the text content
        lines = path_or_text.splitlines()
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def get_installed_version(path):
    """Read the version from the manifest file."""
    if not os.path.exists(path):
        return None
    data = parse_simple_manifest(path)
    return data.get("version")

def get_installed_branch(path):
    """Read the branch from the manifest file."""
    if not os.path.exists(path):
        return None
    data = parse_simple_manifest(path)
    return data.get("branch")

def get_remote_version(url):
    """Fetch the latest version from the remote branch."""
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"[AetherBlend] Failed to fetch version from {url}")
            return None
        data = parse_simple_manifest(response.text)
        return data.get("version")
    except Exception as e:
        print(f"[AetherBlend] Error fetching remote version: {e}")
        return None
    

def get_github_url(username: str, repo: str, branch: str = "main", path: str = "") -> str:
    """Construct the GitHub URL for the specified repository and branch."""
    return f"https://raw.githubusercontent.com/{username}/{repo}/refs/heads/{branch}/{path}"

def get_github_download_url(username: str, repo: str, branch: str = "main") -> str:
    """Construct the GitHub download URL for the specified repository and branch."""
    return f"https://github.com/{username}/{repo}/archive/refs/heads/{branch}.zip"

def is_addon_installed(addon_name):
    for mod in addon_utils.modules():
        if mod.bl_info['name'] == addon_name:  
            return True
    return False




