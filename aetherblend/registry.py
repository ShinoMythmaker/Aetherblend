import importlib
import os
import bpy
from . import preferences
from bpy.app.handlers import persistent

MODULE_FOLDERS = ["operators", "ui"]


@persistent
def aether_check_installs_on_startup(dummy):
    """Check installations on Blender startup."""
    prefs = preferences.get_preferences()
    if getattr(prefs, "run_check_on_startup", True):
        bpy.ops.aether.check_installs('EXEC_DEFAULT')

def run_check_installs_later():
    """Run the check installs operator after a short delay."""
    try:
        bpy.ops.aether.check_installs('EXEC_DEFAULT')
    except Exception as e:
        print(f"[AetherBlend] Could not run check_installs after enable: {e}")
    return None  # Only run once

def register():
    """Automatically registers all operators and UI panels."""
    package = __package__
    
    preferences.register()

    for folder in MODULE_FOLDERS:
        path = os.path.join(os.path.dirname(__file__), folder)

        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith(".py") and not file.startswith("__"):
                    # Convert file path into an importable module path
                    relative_path = os.path.relpath(root, path).replace(os.sep, ".")
                    
                    # Remove unnecessary dots
                    module_path = relative_path.strip(".")
                    
                    # Ensure proper module formatting
                    full_module_name = f"{package}.{folder}"
                    if module_path:
                        full_module_name += f".{module_path}"
                    full_module_name += f".{file[:-3]}"  # Add filename without `.py`

                    try:
                        mod = importlib.import_module(full_module_name)
                        if hasattr(mod, "register"):
                            mod.register()
                    except Exception as e:
                        print(f"[AetherBlend] Failed to register {full_module_name}: {e}")
    
    #bpy.app.handlers.load_post.append(aether_check_installs_on_startup)
    bpy.app.timers.register(run_check_installs_later, first_interval=0.5)

def unregister():
    """Automatically unregisters all operators and UI panels."""
    package = __package__

    if aether_check_installs_on_startup in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(aether_check_installs_on_startup)

    for folder in MODULE_FOLDERS:
        path = os.path.join(os.path.dirname(__file__), folder)

        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith(".py") and not file.startswith("__"):
                    relative_path = os.path.relpath(root, path).replace(os.sep, ".")
                    module_path = relative_path.strip(".")
                    
                    full_module_name = f"{package}.{folder}"
                    if module_path:
                        full_module_name += f".{module_path}"
                    full_module_name += f".{file[:-3]}"

                    try:
                        mod = importlib.import_module(full_module_name)
                        if hasattr(mod, "unregister"):
                            mod.unregister()
                    except Exception as e:
                        print(f"[AetherBlend] Failed to unregister {full_module_name}: {e}")
    
    preferences.unregister()