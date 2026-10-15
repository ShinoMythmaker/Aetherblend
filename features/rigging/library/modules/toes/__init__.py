from .ffxiv_ivcs import get_rig_module as _get_ivcs_rig_module

ffxiv_ivcs = _get_ivcs_rig_module()

__all__ = ["ffxiv_ivcs"]
