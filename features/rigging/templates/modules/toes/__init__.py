from .ivcs import get_rig_module as _get_ivcs_rig_module

ivcs = _get_ivcs_rig_module()

__all__ = ["ivcs"]
