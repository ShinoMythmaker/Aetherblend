from .vrm_default import get_rig_module as _get_vrm_rig_module

vrm_default = _get_vrm_rig_module()

__all__ = ["vrm_default"]