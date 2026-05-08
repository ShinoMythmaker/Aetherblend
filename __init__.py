import sys
import site
# Make user site-packages available when running from source (dev only).
for _path in site.getusersitepackages() if isinstance(site.getusersitepackages(), list) else [site.getusersitepackages()]:
    if _path not in sys.path:
        sys.path.append(_path)

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

