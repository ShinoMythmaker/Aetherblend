from . import character
from . import rigging
from . import cplus
from . import animation
from . import vfx
from . import shaders

modules = (character, rigging, cplus, animation, vfx, shaders)

def register():
    for mod in modules:
        mod.register()

def unregister():
    for mod in modules:
        mod.unregister()
