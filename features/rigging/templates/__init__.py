from ....core.shared import AetherRigGenerator
from ....core.rigify import *

from .ui_collections import *
from .colorsets import *
from .human import *


HUMAN = AetherRigGenerator (
    name = "Human Rig",
    color_sets=AETHER_BLEND,
    b_collections=HUMAN_SFW,  
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