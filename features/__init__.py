from . import model_import
from . import rigging
from . import cplus
from . import animation
from . import vfx
from . import shaders
from . import spring_bones

modules = (model_import, rigging, cplus, animation, vfx, shaders, spring_bones)

def register():
    for mod in modules:
        mod.register()

def unregister():
    for mod in modules:
        mod.unregister()
