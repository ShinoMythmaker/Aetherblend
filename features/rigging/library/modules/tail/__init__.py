from .ffxiv_fk import get_rig_module as _get_fk_rig_module
from .ffxiv_spline import get_rig_module as _get_spline_rig_module

ffxiv_fk = _get_fk_rig_module()
ffxiv_spline = _get_spline_rig_module()

__all__ = ["ffxiv_fk", "ffxiv_spline"]
