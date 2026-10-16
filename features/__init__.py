"""Add-on features. Each feature is a self-contained package that registers its own operators, panels and properties."""

from . import import_export, rig_edit, rig_generator, rig_ui, shaders

__all__ = ["import_export", "rig_edit", "rig_generator", "rig_ui", "shaders"]

modules = (import_export, rig_generator, rig_edit, rig_ui, shaders)


def register() -> None:
    for mod in modules:
        mod.register()


def unregister() -> None:
    for mod in reversed(modules):
        mod.unregister()
