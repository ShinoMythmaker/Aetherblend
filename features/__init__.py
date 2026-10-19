"""Add-on features. Each feature is a self-contained package that registers its own operators, panels and properties."""

from . import cplus, import_export, rig_edit, rig_generator, rig_ui, shaders, vfx

__all__ = ["cplus", "import_export", "rig_edit", "rig_generator", "rig_ui", "shaders", "vfx"]

modules = (import_export, cplus, rig_generator, rig_edit, rig_ui, shaders, vfx)


def register() -> None:
    for mod in modules:
        mod.register()


def unregister() -> None:
    for mod in reversed(modules):
        mod.unregister()
