from . import preferences
from . import features
from . import ui
from . import core
from .properties import tab_prop

def register():
    """Register all addon components."""
    preferences.register()
    core.register()
    tab_prop.register()
    features.register()
    ui.register()


def unregister():
    """Unregister all addon components."""
    ui.unregister()
    features.unregister()
    tab_prop.unregister()
    core.unregister()
    preferences.unregister()
