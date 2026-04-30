from .default import get_rig_module as _get_default_rig_module
from .manual import get_rig_module as _get_simple_rig_module

default = _get_default_rig_module()
manual = _get_simple_rig_module()

__all__ = ["default", "manual"]
