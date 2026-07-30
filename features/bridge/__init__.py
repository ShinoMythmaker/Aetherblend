from . import panel
from . import stream

modules = (panel, stream)

def register():
    for mod in modules:
        mod.register()

def unregister():
    for mod in modules:
        mod.unregister()