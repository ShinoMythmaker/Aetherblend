"""Add-on features. Each feature is a self-contained package that registers its own operators, panels and properties."""
from . import animation, model_import, rig_edit, rig_generator, rig_ui, shaders

__all__ = ['animation', 'model_import', 'rig_edit', 'rig_generator', 'rig_ui', 'shaders']

modules = (model_import, rig_generator, rig_edit, rig_ui, animation, shaders)

def register():
    for mod in modules:
        mod.register()

def unregister():
    for mod in modules:
        mod.unregister()
