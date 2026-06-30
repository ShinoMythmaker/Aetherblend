from .ffxiv_default import get_rig_module as _get_default_rig_module
from .ffxiv_ivcs import get_rig_module as _get_ivcs_rig_module
from .vrm_default import get_rig_module as _get_vrm_rig_module

ffxiv_default = _get_default_rig_module()
ffxiv_ivcs = _get_ivcs_rig_module()
vrm_default = _get_vrm_rig_module()

__all__ = ["ffxiv_default", "ffxiv_ivcs", "vrm_default"]
