from . import operators, panels

def register():
    operators.register()
    panels.register()

def unregister():
    panels.unregister()
    operators.unregister()
