from .miqo import get_rig_module as _get_miqo_rig_module
from .viera_a import get_rig_module as _get_viera_rig_module

miqo = _get_miqo_rig_module()
viera_a = _get_viera_rig_module()

__all__ = ["miqo", "viera_a"]
