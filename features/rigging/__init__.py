from . import operators
from . import properties
from . import panels
from . import module_manager

modules = (properties, module_manager, operators, panels)

def register():
    for mod in modules:
        mod.register()

def unregister():
    for mod in modules:
        mod.unregister()
