from . import decoder
from . import operators
from . import properties
from . import panels
from . import editor_panel

modules = (properties, operators, panels, editor_panel)

def register():
    for mod in modules:
        mod.register()

def unregister():
    for mod in modules:
        mod.unregister()
