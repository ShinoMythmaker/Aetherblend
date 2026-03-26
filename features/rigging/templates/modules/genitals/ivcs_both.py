from ......core.shared import RigModule

from .ivcs_female import get_rig_module as get_female_rig_module
from .ivcs_male import get_rig_module as get_male_rig_module

def get_rig_module() -> RigModule:
    female_module = get_female_rig_module()
    male_module = get_male_rig_module()

    rig_module = RigModule(
        name="IVCS Both",
        type="genitals",
        bone_groups=[*female_module.bone_groups, *male_module.bone_groups]
    )
    return rig_module