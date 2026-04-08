from ......core.rigify.settings import UI_Collections, BoneCollection
from ......core.shared import RigModule


def get_rig_module() -> RigModule:
    rig_module = RigModule(
        name="Debug",
        type="UI-Addon",
        bone_groups=[],
        ui = UI_Collections([
                BoneCollection(name="FFXIV", ui=True, row_index=1, title="FFXIV", visible=False),
                BoneCollection(name="Linked", ui=True, color_set="Torso_Tweak", row_index=2, title="XIV", visible=False),
                BoneCollection(name="Unlinked", ui=True, color_set="IVCS", row_index=2, title="-EX", visible=False),
                BoneCollection(name="LINK", ui=True,color_set="Torso",row_index=3, title="LINK", visible=False),
                BoneCollection(name="MCH", ui=True,  row_index=3, title="MCH", visible=False),
                BoneCollection(name="DEF", ui=True,  row_index=3, title="DEF", visible=False),
                BoneCollection(name="ORG", ui=True,row_index=3, title="ORG", visible=False),
        ])
    )
    return rig_module