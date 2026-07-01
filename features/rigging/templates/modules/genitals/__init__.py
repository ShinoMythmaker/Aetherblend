from .ffxiv_ivcs_female import get_rig_module as _get_ivcs_female_rig_module
from .ffxiv_ivcs_male import get_rig_module as _get_ivcs_male_rig_module
from .ffxiv_ivcs_both import get_rig_module as _get_ivcs_both_rig_module

ffxiv_ivcs_female = _get_ivcs_female_rig_module()
ffxiv_ivcs_male = _get_ivcs_male_rig_module()
ffxiv_ivcs_both = _get_ivcs_both_rig_module()

__all__ = ["ffxiv_ivcs_female", "ffxiv_ivcs_male", "ffxiv_ivcs_both"]
