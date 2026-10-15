from ......core.bone_generators import RegexBoneGroup
from ......core.rigify.settings import BoneCollection, UI_Collections
from ......core.shared import BoneGroup, RigModule

OPT = BoneGroup(
        name="Optional",
        transform_link=[],
        generators=[
            # Miscellaneous
            RegexBoneGroup(
                name="Misc",
                pattern=r"^J_Opt.*",
                original_parent=True,
                b_collection="Misc",
                prefix="OPT"
            ),
        ]
)


def get_rig_module() -> RigModule:
    return RigModule(
        name="VRM-Default",
        type="Generation",
        bone_groups=[OPT],
        ui_collections = UI_Collections([
            BoneCollection(name="Misc", ui=True, color_set="Head", row_index=1, title="Misc", visible=False),
        ],
        ),
    )
