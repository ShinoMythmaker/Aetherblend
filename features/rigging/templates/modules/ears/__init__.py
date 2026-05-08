from .miqo import get_rig_module as _get_miqo_rig_module
from .viera_a import get_rig_module as _get_vieraa_rig_module
from .viera_b import get_rig_module as _get_vierab_rig_module
from .viera_c import get_rig_module as _get_vierac_rig_module
from .viera_d import get_rig_module as _get_vierad_rig_module

miqo = _get_miqo_rig_module()
viera_a = _get_vieraa_rig_module()
viera_b = _get_vierab_rig_module()
viera_c = _get_vierac_rig_module()
viera_d = _get_vierad_rig_module()

__all__ = ["miqo", "viera_a", "viera_b", "viera_c", "viera_d"]
