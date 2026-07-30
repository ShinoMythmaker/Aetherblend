from . import info_panel

modules = (info_panel,)

def register():
    for mod in modules:
        if hasattr(mod, 'register'):
            mod.register()

def unregister():
    for mod in reversed(modules):
        if hasattr(mod, 'unregister'):
            mod.unregister()
