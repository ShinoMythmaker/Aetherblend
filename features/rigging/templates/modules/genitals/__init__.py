from .ivcs_female import get_rig_module as _get_ivcs_female_rig_module
from .ivcs_male import get_rig_module as _get_ivcs_male_rig_module
from .ivcs_both import get_rig_module as _get_ivcs_both_rig_module

ivcs_female = _get_ivcs_female_rig_module()
ivcs_male = _get_ivcs_male_rig_module()
ivcs_both = _get_ivcs_both_rig_module()

__all__ = ["ivcs_female", "ivcs_male", "ivcs_both"]
