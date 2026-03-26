from .miqo import get_rig_module as _get_miqo_rig_module
from .viera import get_rig_module as _get_viera_rig_module

miqo = _get_miqo_rig_module()
viera = _get_viera_rig_module()

__all__ = ["miqo", "viera"]
