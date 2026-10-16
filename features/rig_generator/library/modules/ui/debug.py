"""Adds the buttons that show the helper bone collections of the rig."""
from ....definitions import RigModule
from ....rigify.settings import BoneCollection, UI_Collections


class Module(RigModule):
    name = "Debug"
    ui_collections = UI_Collections([
        BoneCollection(name="Original", ui=True, row_index=1, title="Original", visible=False),
        BoneCollection(name="Linked", ui=True, color_set="Torso_Tweak", row_index=2, title="Linked", visible=False),
        BoneCollection(name="Unlinked", ui=True, color_set="IVCS", row_index=2, title="Unlinked", visible=False),
        BoneCollection(name="LINK", ui=True, color_set="Torso", row_index=3, title="LINK", visible=False),
        BoneCollection(name="MCH", ui=True, row_index=3, title="MCH", visible=False),
        BoneCollection(name="DEF", ui=True, row_index=3, title="DEF", visible=False),
        BoneCollection(name="ORG", ui=True, row_index=3, title="ORG", visible=False),
    ])
