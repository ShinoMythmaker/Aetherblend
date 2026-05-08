from . import rig_operators
from . import ui_operators
from . import rig_edit_operators
from . import properties
from . import panels
from . import template_manager

modules = (properties, template_manager, rig_operators, ui_operators, rig_edit_operators, panels)

def register():
    for mod in modules:
        mod.register()

def unregister():
    for mod in modules:
        mod.unregister()
