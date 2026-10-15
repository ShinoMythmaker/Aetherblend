from . import aetherbridge_pt, info_panel, properties_bridge, spring_bone_pt

modules = (info_panel, properties_bridge)

def register():
    for mod in modules:
        if hasattr(mod, 'register'):
            mod.register()

def unregister():
    for mod in reversed(modules):
        if hasattr(mod, 'unregister'):
            mod.unregister()
