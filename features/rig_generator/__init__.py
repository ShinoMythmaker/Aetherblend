"""Rig generator feature: build a rig from a template of rig modules."""
from . import (
    definitions,
    generator,
    instructions,
    library,
    operators,
    panels,
    properties,
    rigify,
    template_manager,
)

__all__ = ['definitions', 'generator', 'instructions', 'library', 'rigify']

modules = (properties, template_manager, operators, panels)

def register():
    for mod in modules:
        mod.register()

def unregister():
    for mod in reversed(modules):
        mod.unregister()
