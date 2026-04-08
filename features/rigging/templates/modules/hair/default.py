from ......core.generators import RegexBoneGroup
from ......core.shared import BoneGroup, RigModule
from ......core.rigify.settings import UI_Collections, BoneCollection

HAIR = BoneGroup(
    name="Hair",
    transform_link=[],
    bones=[
        RegexBoneGroup(
            name="Hair",
            pattern=r"^j_ex_h.*",
            parent="Head",
            extension_size_factor=10.0,
            is_connected=False,
            req_bones=[],
            b_collection="Hair",
        ),
        RegexBoneGroup(
            name="Kami",
            pattern=r"^j_kami.*",
            parent="Head",
            extension_size_factor=10.0,
            is_connected=False,
            req_bones=[],
            b_collection="Hair",
        ),
        RegexBoneGroup(
            name="Accessory",
            pattern=r"^j_ex_met.*",
            parent="Head",
            extension_size_factor=10.0,
            is_connected=False,
            req_bones=[],
            b_collection="Accessory",
        )
    ]
)

def get_rig_module() -> RigModule:
    rig_module = RigModule(
        name="Default",
        type="Generation",
        bone_groups=[HAIR],
        ui=UI_Collections([
            BoneCollection(name="Hair", ui=True, color_set="Head", row_index=1, title="Hair", visible=False),
            BoneCollection(name="Accessory", ui=True, color_set="Head", row_index=1, title="Accessory", visible=False),
        ])
    )
    return rig_module