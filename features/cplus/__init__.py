from . import decoder, editor_panel, operators, panels, properties

modules = (properties, operators, panels)

def register():
    for mod in modules:
        mod.register()

def unregister():
    for mod in modules:
        mod.unregister()
