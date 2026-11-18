"""Shared UI: icons, tabs, info panel and Properties editor mirrors."""

from . import icons as icons
from . import info_panel, tabs

modules = (tabs, info_panel)


def register() -> None:
    """Register this module's classes."""
    for mod in modules:
        if hasattr(mod, "register"):
            mod.register()


def unregister() -> None:
    """Unregister this module's classes."""
    for mod in reversed(modules):
        if hasattr(mod, "unregister"):
            mod.unregister()
