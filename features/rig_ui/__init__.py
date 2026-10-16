"""Rig UI feature: bone collection layers, rig UI links and eyelid editing on a generated rig."""
from . import operators, panels

__all__ = ['operators', 'panels']

modules = (operators, panels)


def register():
    for mod in modules:
        mod.register()


def unregister():
    for mod in reversed(modules):
        mod.unregister()
