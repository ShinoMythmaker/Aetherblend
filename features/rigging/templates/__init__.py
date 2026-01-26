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
        #Root
        WidgetOverride(
            bone="root",
            scale_factor=0.2,
        ),
        WidgetOverride(
            bone="Cheek.T.L",
            scale_factor=0.3,
        ),
        WidgetOverride(
            bone="Cheek.T.L.001",
            scale_factor=0.3,
        ),
        WidgetOverride(
            bone="Cheek.B.L.001",
            scale_factor=0.3,
        ),
        WidgetOverride(
            bone="Cheek.B.L",
            scale_factor=0.3,
        ),
        WidgetOverride(
            bone="Nose.L",
            scale_factor=0.3,
        ),
        WidgetOverride(
            bone="Nostril.L",
            scale_factor=0.2,
        ),
        WidgetOverride(
            bone="Nose",
            scale_factor=0.2,
        ),
        #Right Face
         WidgetOverride(
            bone="Cheek.T.R",
            scale_factor=0.3,
        ),
        WidgetOverride(
            bone="Cheek.T.R.001",
            scale_factor=0.3,
        ),
        WidgetOverride(
            bone="Cheek.B.R.001",
            scale_factor=0.3,
        ),
        WidgetOverride(
            bone="Cheek.B.R",
            scale_factor=0.3,
        ),
        WidgetOverride(
            bone="Nose.R",
            scale_factor=0.3,
        ),
        WidgetOverride(
            bone="Nostril.R",
            scale_factor=0.2,
        ),
        #Mouth
        WidgetOverride(
            bone="jaw_master_mouth",
            scale=[0.8, 1.0, 0.5]
        ),
        WidgetOverride(
            bone="Teeth.T",
            scale_factor=1.7,
            translation=[0.0, 0.003, 0.0],
            rotation=[0.0, 0.0, 3.1415],
        ),
        WidgetOverride(
            bone="Teeth.B",
            scale_factor=1.7,
            translation=[0.0, 0.003, 0.0],
            rotation=[0.0, 0.0, 3.1415],
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
            [RIGHT_EYE],
            [BROW],
        ]
)