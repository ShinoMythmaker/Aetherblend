from . import info_panel
from . import aetherbridge_pt
from . import spring_bone_pt

modules = (info_panel,)

def register():
    for mod in modules:
        if hasattr(mod, 'register'):
            mod.register()

def unregister():
    for mod in modules:
        if hasattr(mod, 'unregister'):
            mod.unregister()
