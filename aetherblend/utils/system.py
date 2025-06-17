import os
import requests
import tempfile
import addon_utils
import bpy

def download_zip(url: str, name: str = "download") -> str:
    """Download a ZIP file from a URL and return the path to the downloaded file."""
    temp_dir = tempfile.mkdtemp()
    zip_path = os.path.join(temp_dir, f"{name}.zip")

    try:
        response = requests.get(url, stream=True)
        if response.status_code != 200:
            print(f"[AetherBlend] Failed to download {url}")
            return None

        with open(zip_path, 'wb') as zip_file:
            zip_file.write(response.content)

    except Exception as e:
        print(f"[AetherBlend] Download error: {e}")
        return None

    return zip_path  # Return path

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

def parse_key_from_manifest(path, key):
    """Parse a key from a local manifest file."""
    if not os.path.exists(path):
        return None
    data = parse_simple_manifest(path)
    return data.get(key)

def parse_key_from_remote_manifest(url, key):
    """Parse a key from a remote manifest file."""
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

def get_addon_info(addon_name, manifest_path=None):
    """Get information about a Blender addon."""
    for mod in addon_utils.modules():
        if mod.bl_info.get("name") == addon_name:
            version = mod.bl_info.get("version")
            branch = mod.bl_info.get("branch")
            module_name = mod.__name__
            # Try to find manifest_path dynamically if not provided
            if not manifest_path and hasattr(mod, "__file__"):
                possible_manifest = os.path.join(os.path.dirname(mod.__file__), "blender_manifest.toml")
                if os.path.exists(possible_manifest):
                    manifest_path = possible_manifest
            if not branch:
                branch = parse_key_from_manifest(manifest_path, "branch")
            version_str = ".".join(str(v) for v in version) if version else None
            loaded_default, loaded_state = addon_utils.check(module_name)
            return {
                "installed": True,
                "enabled": loaded_state,
                "version": version_str,
                "branch": branch,
                "name": module_name
            }
    return {
        "installed": False,
        "enabled": False,
        "version": None,
        "branch": None,
        "name": None
    }

def update_window(areaType: str = "VIEW_3D"):
    """Update the specified area type in Blender."""
    for window in bpy.context.window_manager.windows:
            for area in window.screen.areas:
                if area.type == 'VIEW_3D': 
                    area.tag_redraw()




