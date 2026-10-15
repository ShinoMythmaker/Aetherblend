from .ffxiv_miqo import get_rig_module as _get_miqo_rig_module
from .ffxiv_viera_a import get_rig_module as _get_vieraa_rig_module
from .ffxiv_viera_b import get_rig_module as _get_vierab_rig_module
from .ffxiv_viera_c import get_rig_module as _get_vierac_rig_module
from .ffxiv_viera_d import get_rig_module as _get_vierad_rig_module

ffxiv_miqo = _get_miqo_rig_module()
ffxiv_viera_a = _get_vieraa_rig_module()
ffxiv_viera_b = _get_vierab_rig_module()
ffxiv_viera_c = _get_vierac_rig_module()
ffxiv_viera_d = _get_vierad_rig_module()

__all__ = ["ffxiv_miqo", "ffxiv_viera_a", "ffxiv_viera_b", "ffxiv_viera_c", "ffxiv_viera_d"]
