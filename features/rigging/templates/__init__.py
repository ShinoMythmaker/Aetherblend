from ....core.shared import AetherRigGenerator
from ....core.rigify import *

from .ui_collections import *
from .colorsets import *
from .human import *


HUMAN = AetherRigGenerator (
    name = "Human Rig",
    color_sets=AETHER_BLEND,
    ui_collections=HUMAN_SFW,  
    widget_overrides=[
        WidgetOverride(
            bone="Cheek.T.L",
            scale_factor=0.5,
            )
    ],
    bone_groups = [
            [SPINE],
            [ARM_R],
            [ARM_L],
            [LEG_R],
            [LEG_L],
            [SKIRT_R],
            [SKIRT_R_MCH],
            [SKIRT_L],
            [SKIRT_L_MCH],
            [HAND_R],
            [HAND_L],
            [TAIL],
            [HEAD],
            [LEFT_EYE],
            [RIGHT_EYE]
        ]
)