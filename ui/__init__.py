from . import info_panel
from . import aetherbridge_pt
from . import spring_bone_pt

modules = (info_panel, aetherbridge_pt, spring_bone_pt)

def register():
    for mod in modules:
        if hasattr(mod, 'register'):
            mod.register()

def unregister():
    for mod in modules:
        if hasattr(mod, 'unregister'):
            mod.unregister()
