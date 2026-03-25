from . import shared
from . import constraints
from . import generators
from . import rigify
from . import drivers

__all__ = ['shared', 'constraints', 'generators', 'rigify', 'drivers']

def register():
    """Register all core components."""
    drivers.register()

def unregister():
    """Unregister all core components."""
    drivers.unregister()
