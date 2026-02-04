from . import rig_operators
from . import ui_operators
from . import properties
from . import panels
from . import module_manager

modules = (properties, module_manager, rig_operators, ui_operators, panels)

def register():
    for mod in modules:
        mod.register()

def unregister():
    for mod in modules:
        mod.unregister()
