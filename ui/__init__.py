from . import info_panel
from . import aetherbridge_pt
from . import spring_bone_pt
from . import properties_bridge

modules = (info_panel, properties_bridge)

def register():
    for mod in modules:
        if hasattr(mod, 'register'):
            mod.register()

def unregister():
    for mod in reversed(modules):
        if hasattr(mod, 'unregister'):
            mod.unregister()
