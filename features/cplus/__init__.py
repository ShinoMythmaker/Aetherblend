"""Customize+ feature: parse, apply, and revert character bone transforms."""

from . import operators, panels, properties

__all__ = ["operators", "panels", "properties"]

modules = (properties, operators, panels)


def register() -> None:
    """Register the C+ feature."""
    for mod in modules:
        mod.register()


def unregister() -> None:
    """Unregister the C+ feature."""
    for mod in reversed(modules):
        mod.unregister()
