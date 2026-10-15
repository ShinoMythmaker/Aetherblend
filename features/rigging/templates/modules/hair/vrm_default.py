from ......core.bone_generators import RegexBoneGroup
from ......core.rigify.settings import BoneCollection, UI_Collections
from ......core.shared import BoneGroup, RigModule

HAIR = BoneGroup(
    name="Hair",
    transform_link=[],
    generators=[
        RegexBoneGroup(
            name="Hair",
            pattern=r"^J_Sec_Hair.*",
            parent=["Head", "j_kao"],
            extension_size_factor=10.0,
            is_connected=False,
            req_bones=[],
            b_collection="Hair",
        ),
    ]
)

def get_rig_module() -> RigModule:
    return RigModule(
        name="VRM-Default",
        type="Generation",
        bone_groups=[HAIR],
        ui_collections=UI_Collections([
            BoneCollection(name="Hair", ui=True, color_set="Head", row_index=1, title="Hair", visible=False),
        ])
    )
