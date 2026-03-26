from ......core.generators import RegexBoneGroup
from ......core.shared import PoseOperations, BoneGroup, TransformLink, RigModule
from ......core import rigify

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
        type="hair",
        bone_groups=[HAIR]
    )
    return rig_module