from .ffxiv_detailed import get_rig_module as _get_detailed_rig_module
from .vrm_default import get_rig_module as _get_vrm_rig_module

ffxiv_detailed = _get_detailed_rig_module()
vrm_default = _get_vrm_rig_module()

__all__ = ["ffxiv_detailed"]
