from . import operators
from . import panels

modules = (operators, panels)

def register():
    for mod in modules:
        mod.register()

def unregister():
    for mod in modules:
        mod.unregister()
