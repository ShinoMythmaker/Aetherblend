"""Shaders feature: apply shaders to imported models."""
from . import operators, panels

__all__ = ['operators', 'panels']

modules = (operators, panels)

def register():
    for mod in modules:
        mod.register()

def unregister():
    for mod in modules:
        mod.unregister()
