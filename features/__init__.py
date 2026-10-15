from . import animation, cplus, model_import, rigging, shaders, spring_bones, vfx

modules = (model_import, rigging, cplus, animation, vfx, shaders, spring_bones)

def register():
    for mod in modules:
        mod.register()

def unregister():
    for mod in modules:
        mod.unregister()
