"""AetherBlend: Blender add-on for posing and animating FFXIV characters."""
# import sys
# import site
# Make user site-packages available when running from source (dev only).
# for _path in site.getusersitepackages() if isinstance(site.getusersitepackages(), list) else [site.getusersitepackages()]:  # noqa: E501
#     if _path not in sys.path:
#         sys.path.append(_path)
# Should not be needed anymore i would much rather have developers install dependancies via the script to ensure using the same artifacts as users.  # noqa: E501

from . import features, preferences, ui
from .utils import addon_dependencies


def register() -> None:
    """Register all addon components."""
    addon_dependencies.print_missing_required_addons()
    preferences.register()
    features.register()
    ui.register()


def unregister() -> None:
    """Unregister all addon components."""
    ui.unregister()
    features.unregister()
    preferences.unregister()
