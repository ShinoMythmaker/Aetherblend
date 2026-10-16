"""Adds the buttons that show the helper bone collections of the rig."""

from .... import definitions
from ....rigify import settings


class Module(definitions.RigModule):
    name = "Debug"
    ui_collections = settings.UI_Collections(
        [
            settings.BoneCollection(name="Original", ui=True, row_index=1, title="Original", visible=False),
            settings.BoneCollection(
                name="Linked", ui=True, color_set="Torso_Tweak", row_index=2, title="Linked", visible=False
            ),
            settings.BoneCollection(
                name="Unlinked", ui=True, color_set="IVCS", row_index=2, title="Unlinked", visible=False
            ),
            settings.BoneCollection(name="LINK", ui=True, color_set="Torso", row_index=3, title="LINK", visible=False),
            settings.BoneCollection(name="MCH", ui=True, row_index=3, title="MCH", visible=False),
            settings.BoneCollection(name="DEF", ui=True, row_index=3, title="DEF", visible=False),
            settings.BoneCollection(name="ORG", ui=True, row_index=3, title="ORG", visible=False),
        ]
    )
