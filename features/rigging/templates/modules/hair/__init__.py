from .ffxiv_default import get_rig_module as _get_default_rig_module
from .vrm_hair import get_rig_module as _get_vrm_rig_module

ffxiv_default = _get_default_rig_module()
vrm_hair = _get_vrm_rig_module()

__all__ = ["ffxiv_default", "vrm_hair"]
