from .ffxiv_default import get_rig_module as _get_default_rig_module
from .ffxiv_manual import get_rig_module as _get_simple_rig_module

ffxiv_default = _get_default_rig_module()
ffxiv_manual = _get_simple_rig_module()

__all__ = ["ffxiv_default", "ffxiv_manual"]
