import importlib
import os
from . import preferences
from .status import AetherBlendStatus as status

MODULE_FOLDERS = ["operators", "ui"]

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

    prefs = preferences.get_preferences()
    if prefs and getattr(prefs, "run_check_on_startup", False):
        status.check_installs(prefs.branch)
                
def unregister():
    """Automatically unregisters all operators and UI panels."""
    package = __package__

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

    
