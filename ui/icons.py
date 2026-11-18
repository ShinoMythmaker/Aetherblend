"""Shared custom icon previews loaded from the add-on's assets."""

from pathlib import Path

import bpy.utils.previews

_ICON_DIR = Path(__file__).resolve().parents[1] / "assets" / "icons"
_ICON_FILES = {"ffxiv_logo": "ffxiv_logo.svg"}
_previews: bpy.utils.previews.ImagePreviewCollection | None = None


def get_icon_id(name: str) -> int:
    """Return a registered custom icon's Blender ID."""
    if _previews is None:
        raise RuntimeError("AetherBlend icons have not been registered")
    return _previews[name].icon_id


def register() -> None:
    """Load the shared previews before registering their UI consumers."""
    global _previews
    if _previews is not None:
        raise RuntimeError("AetherBlend icons are already registered")
    previews = bpy.utils.previews.new()
    try:
        for name, filename in _ICON_FILES.items():
            previews.load(name, str(_ICON_DIR / filename), "IMAGE")
    except (RuntimeError, KeyError, OSError):
        bpy.utils.previews.remove(previews)
        raise
    _previews = previews


def unregister() -> None:
    """Release shared previews after unregistering their UI consumers."""
    global _previews
    if _previews is not None:
        bpy.utils.previews.remove(_previews)
        _previews = None
