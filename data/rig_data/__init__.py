
from .human import *
from ...generator import AetherRigGenerator
from ...rigify import *

HUMAN = AetherRigGenerator (
    name = "Human Rig",
    color_sets=[
        ColorSet(name="FK", normal="#00EDFF", select="#FFFFFF", active="#FFFF00"),
        ColorSet(name="IK", normal="#1BEFF7", select="#FFFFFF", active="#FFFF00"),
        ColorSet(name="Tweak", normal="#FFA500", select="#DA1E1E", active="#5D0BF7"),
        ColorSet(name="Special", normal="#00FF00", select="#FFFFFF", active="#FFFF00"),
        ColorSet(name="Extra", normal="#FF0000", select="#FFFFFF", active="#FFFF00"),   
    ],
    b_collections=[
                BoneCollection(name="Face", ui=True, color_set="FK", row_index=1, title="Face"),
                BoneCollection(name="Face (Primary)", ui=True, color_set="IK", row_index=2, title="(Primary)", visible=False),
                BoneCollection(name="Face (Secondary)", ui=True, color_set="Special", row_index=2, title="(Secondary)", visible=False),
                BoneCollection(name="Hair", ui=True, color_set="IK", row_index=3, title="Hair", visible=False),
                BoneCollection(name="Accessory", ui=True, color_set="Special", row_index=3, title="Accessory", visible=False),
                BoneCollection(name="Torso", ui=True, color_set="Special", row_index=5, title="Torso"),
                BoneCollection(name="Torso (Tweak)", ui=True, color_set="Tweak", row_index=6, title="(Tweak)", visible=False),

                BoneCollection(name="Fingers", ui=True, color_set="Extra", row_index=8, title="Fingers"),
                BoneCollection(name="Fingers (Details)", ui=True, color_set="FK", row_index=9, title="(Details)", visible=False),
                BoneCollection(name="Toes", ui=True, color_set="Extra", row_index=8, title="Toes"),
                BoneCollection(name="Toes (Details)", ui=True, color_set="FK", row_index=9, title="(Details)", visible=False),

                BoneCollection(name="Arm.L (IK)", ui=True, color_set="IK", row_index=11, title="Arm IK.L"),
                BoneCollection(name="Arm.L (FK)", ui=True, color_set="FK", row_index=12, title="FK.L", visible=False),
                BoneCollection(name="Arm.L (Tweak)", ui=True, color_set="Tweak", row_index=13, title="Tweak.L", visible=False),
                BoneCollection(name="Arm.R (IK)", ui=True, color_set="IK", row_index=11, title="Arm IK.R"),
                BoneCollection(name="Arm.R (FK)", ui=True, color_set="FK", row_index=12, title="FK.R", visible=False),
                BoneCollection(name="Arm.R (Tweak)", ui=True, color_set="Tweak", row_index=13, title="Tweak.R", visible=False),

                BoneCollection(name="Leg.L (IK)", ui=True, color_set="IK", row_index=15, title="Leg IK.L"),
                BoneCollection(name="Leg.L (FK)", ui=True, color_set="FK", row_index=16, title="FK.L", visible=False),
                # BoneCollection(name="Leg.L (Tweak)", ui=True, color_set="Tweak", row_index=17, title="Tweak.L", visible=False), Nothing in here right now - Oats
                BoneCollection(name="Leg.R (IK)", ui=True, color_set="IK", row_index=15, title="Leg IK.R"),
                BoneCollection(name="Leg.R (FK)", ui=True, color_set="FK", row_index=16, title="FK.R", visible=False),
                # BoneCollection(name="Leg.R (Tweak)", ui=True, color_set="Tweak", row_index=17, title="Tweak.R", visible=False),

                BoneCollection(name="Tail", ui=True, color_set="Special", row_index=19, title="Tail"),
                # BoneCollection(name="Tail (Tweak)", ui=True, color_set="Tweak", row_index=20, title="Tweaks", visible=False),

                BoneCollection(name="Skirt", ui=True, color_set="Special", row_index=22, title="Skirt", visible=False),
                BoneCollection(name="Skirt (Tweak)", ui=True, color_set="Tweak", row_index=23, title="Tweak", visible=False),

                # BoneCollection(name="Genitals (Male)", ui=True, color_set="FK", row_index=25, title="Genitals (Male)", visible=False),
                # BoneCollection(name="Tweak (Male)", ui=True, color_set="Tweak", row_index=26, title="Tweak (Male)", visible=False),
                # BoneCollection(name="Genitals (Female)", ui=True, color_set="FK", row_index=25, title="Genitals (Female)", visible=False),
                # BoneCollection(name="Tweak (Female)", ui=True, color_set="Tweak", row_index=26, title="Tweak (Female)", visible=False),
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
            [HEAD]
        ]
)