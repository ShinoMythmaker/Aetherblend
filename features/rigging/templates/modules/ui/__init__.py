from .debug import get_rig_module as _get_base_rig_module

debug = _get_base_rig_module()

__all__ = ["debug"]