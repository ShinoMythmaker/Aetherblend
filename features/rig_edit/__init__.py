"""Rig edit feature: convert and clean up a generated rig."""

from . import operators, panels

__all__ = ["operators", "panels"]

modules = (operators, panels)


def register() -> None:
    for mod in modules:
        mod.register()


def unregister() -> None:
    for mod in reversed(modules):
        mod.unregister()
