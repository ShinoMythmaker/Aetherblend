from . import animation, model_import, rigging, shaders

modules = (model_import, rigging, animation, shaders)

def register():
    for mod in modules:
        mod.register()

def unregister():
    for mod in modules:
        mod.unregister()
