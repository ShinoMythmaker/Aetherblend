"""VFX model-creation and export tools."""

from . import operators, panels

__all__ = ["operators", "panels"]

modules = (operators, panels)


def register() -> None:
    """Register the VFX feature."""
    for mod in modules:
        mod.register()


def unregister() -> None:
    """Unregister the VFX feature."""
    for mod in reversed(modules):
        mod.unregister()
