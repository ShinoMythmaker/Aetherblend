from . import (
    aether_rig_generator,
    constraints,
    drivers,
    instructions,
    module,
    panels,
    properties,
    rig_edit_operators,
    rig_operators,
    rigify,
    template_manager,
    ui_operators,
)

__all__ = ['constraints', 'drivers', 'instructions', 'module', 'aether_rig_generator', 'rigify']

modules = (properties, template_manager, rig_operators, ui_operators, rig_edit_operators, panels)

def register():
    for mod in modules:
        mod.register()

def unregister():
    for mod in reversed(modules):
        mod.unregister()
