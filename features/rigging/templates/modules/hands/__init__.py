from .default import get_rig_module as _get_default_rig_module
from .ivcs import get_rig_module as _get_ivcs_rig_module

default = _get_default_rig_module()
ivcs = _get_ivcs_rig_module()

__all__ = ["default", "ivcs"]
