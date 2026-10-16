"""Rig edit feature: convert and clean up a generated rig."""
from . import operators, panels

__all__ = ['operators', 'panels']

modules = (operators, panels)

def register():
    for mod in modules:
        mod.register()

def unregister():
    for mod in reversed(modules):
        mod.unregister()
