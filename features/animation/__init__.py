from . import animation_import, export_anim, export_pose, panels, properties

modules = (properties, export_anim, export_pose, panels, animation_import)

def register():
    for mod in modules:
        mod.register()

def unregister():
    for mod in modules:
        mod.unregister()
