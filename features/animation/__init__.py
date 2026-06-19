from . import export_anim
from . import export_pose
from . import panels
from . import properties
from . import animation_import

modules = (properties, export_anim, export_pose, panels, animation_import)

def register():
    for mod in modules:
        mod.register()

def unregister():
    for mod in modules:
        mod.unregister()
