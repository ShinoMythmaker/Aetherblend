from . import ffxiv_character_ot
from . import panels
from . import vrm_ot

modules = (ffxiv_character_ot, vrm_ot, panels)

def register():
    for mod in modules:
        mod.register()

def unregister():
    for mod in modules:
        mod.unregister()
