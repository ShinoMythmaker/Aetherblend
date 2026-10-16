from . import animation, model_import, rig_generator, shaders

modules = (model_import, rig_generator, animation, shaders)

def register():
    for mod in modules:
        mod.register()

def unregister():
    for mod in modules:
        mod.unregister()
