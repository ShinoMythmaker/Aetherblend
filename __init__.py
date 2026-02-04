from . import preferences
from . import features
from . import ui
from .properties import tab_prop

def register():
    """Register all addon components."""
    preferences.register()
    tab_prop.register()
    features.register()
    ui.register()


def unregister():
    """Unregister all addon components."""
    ui.unregister()
    features.unregister()
    tab_prop.unregister()
    preferences.unregister()
