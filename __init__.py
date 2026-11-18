"""AetherBlend: Blender add-on for posing and animating FFXIV characters."""

from . import features, preferences, ui
from .utils import addon_dependencies


def register() -> None:
    """Register all addon components."""
    addon_dependencies.print_missing_required_addons()
    ui.icons.register()
    preferences.register()
    features.register()
    ui.register()


def unregister() -> None:
    """Unregister all addon components."""
    ui.unregister()
    features.unregister()
    preferences.unregister()
    ui.icons.unregister()
