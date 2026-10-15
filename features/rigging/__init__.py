from . import panels, properties, rig_edit_operators, rig_operators, template_manager, ui_operators

modules = (properties, template_manager, rig_operators, ui_operators, rig_edit_operators, panels)

def register():
    for mod in modules:
        mod.register()

def unregister():
    for mod in modules:
        mod.unregister()
