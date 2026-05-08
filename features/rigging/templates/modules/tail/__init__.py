from .forward_kinematics import get_rig_module as _get_fk_rig_module
from .spline import get_rig_module as _get_spline_rig_module

forward_kinematics = _get_fk_rig_module()
spline = _get_spline_rig_module()

__all__ = ["forward_kinematics", "spline"]
