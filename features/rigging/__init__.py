from . import operators
from . import properties
from . import panels

modules = (properties, operators, panels)

def register():
    for mod in modules:
        mod.register()

def unregister():
    for mod in modules:
        mod.unregister()
