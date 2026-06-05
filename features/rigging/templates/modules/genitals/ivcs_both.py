from ......core.shared import RigModule
from ......core.rigify.settings import UI_Collections, BoneCollection

from .ivcs_female import get_rig_module as get_female_rig_module
from .ivcs_male import get_rig_module as get_male_rig_module

def get_rig_module() -> RigModule:
    female_module = get_female_rig_module()
    male_module = get_male_rig_module()

    rig_module = RigModule(
        name="IVCS Both",
        type="Generation",
        bone_groups=[*female_module.bone_groups, *male_module.bone_groups],
        ui_collections = UI_Collections([
            BoneCollection(name="Genitals (Male)", ui=True, color_set="IVCS", row_index=1, title="Genitals (Male)", visible=False),
            BoneCollection(name="Genitals (Female)", ui=True, color_set="IVCS", row_index=1, title="Genitals (Female)", visible=False),
        ]),
        operations=[
            *female_module.operations,
            *male_module.operations
        ]
    )
    return rig_module