from .human import *
from ....core.shared import AetherRigGenerator
from ....core.rigify import *

HUMAN = AetherRigGenerator (
    name = "Human Rig",
    color_sets=[
        ColorSet(name="IK_Right", normal="#4CFF88", select="#FFFFFF", active="#FFFF70"),
        ColorSet(name="IK_Left", normal="#4C9AFF", select="#FFFFFF", active="#FFFF70"),
        ColorSet(name="FK_Right", normal="#4CFF88", select="#FFFFFF", active="#FFFF70"),
        ColorSet(name="FK_Left", normal="#4C9AFF", select="#FFFFFF", active="#FFFF70"),
        ColorSet(name="Tweak_Right", normal="#4CFF88", select="#FFFFFF", active="#FFFF70"),
        ColorSet(name="Tweak_Left", normal="#4C9AFF", select="#FFFFFF", active="#FFFF70"),
        ColorSet(name="Fingers_Right", normal="#4CFF88", select="#FFFFFF", active="#FFFF70"),
        ColorSet(name="Fingers_Left", normal="#4C9AFF", select="#FFFFFF", active="#FFFF70"),
        ColorSet(name="Torso", normal="#FF547F", select="#FFFFFF", active="#FFFF70"),
        ColorSet(name="Torso_Tweak", normal="#BC58FF", select="#FFFFFF", active="#FFFF70"), 
        ColorSet(name="Head", normal="#64FFEA", select="#FFFFFF", active="#FFFF70"),  
    ],
    b_collections=[
                BoneCollection(name="Face", ui=True, color_set="Head", row_index=1, title="Face"),
                BoneCollection(name="Face (Primary)", ui=True, color_set="Head", row_index=2, title="(Primary)", visible=False),
                BoneCollection(name="Face (Secondary)", ui=True, color_set="Head", row_index=2, title="(Secondary)", visible=False),
                BoneCollection(name="Hair", ui=True, color_set="Head", row_index=3, title="Hair", visible=False),
                BoneCollection(name="Accessory", ui=True, color_set="Head", row_index=3, title="Accessory", visible=False),
                BoneCollection(name="Torso", ui=True, color_set="Torso", row_index=5, title="Torso"),
                BoneCollection(name="Torso (Tweak)", ui=True, color_set="Torso_Tweak", row_index=6, title="(Tweak)", visible=False),

                BoneCollection(name="Fingers.L", ui=True, color_set="Fingers_Left", row_index=8, title="Fingers.L"),
                BoneCollection(name="Fingers.R", ui=True, color_set="Fingers_Right", row_index=8, title="Fingers.R"),
                # BoneCollection(name="Fingers (Details)", ui=True, color_set="FK", row_index=9, title="(Details)", visible=False),
                # BoneCollection(name="Toes", ui=True, color_set="Extra", row_index=8, title="Toes"),
                # BoneCollection(name="Toes (Details)", ui=True, color_set="FK", row_index=9, title="(Details)", visible=False),

                BoneCollection(name="Arm.L (IK)", ui=True, color_set="IK_Left", row_index=11, title="Arm IK.L"),
                BoneCollection(name="Arm.L (FK)", ui=True, color_set="FK_Left", row_index=12, title="FK.L", visible=False),
                BoneCollection(name="Arm.L (Tweak)", ui=True, color_set="Tweak_Left", row_index=13, title="Tweak.L", visible=False),
                BoneCollection(name="Arm.R (IK)", ui=True, color_set="IK_Right", row_index=11, title="Arm IK.R"),
                BoneCollection(name="Arm.R (FK)", ui=True, color_set="FK_Right", row_index=12, title="FK.R", visible=False),
                BoneCollection(name="Arm.R (Tweak)", ui=True, color_set="Tweak_Right", row_index=13, title="Tweak.R", visible=False),

                BoneCollection(name="Leg.L (IK)", ui=True, color_set="IK_Left", row_index=15, title="Leg IK.L"),
                BoneCollection(name="Leg.L (FK)", ui=True, color_set="FK_Left", row_index=16, title="FK.L", visible=False),
                BoneCollection(name="Leg.L (Tweak)", ui=True, color_set="Tweak_Left", row_index=17, title="Tweak.L", visible=False),
                BoneCollection(name="Leg.R (IK)", ui=True, color_set="IK_Right", row_index=15, title="Leg IK.R"),
                BoneCollection(name="Leg.R (FK)", ui=True, color_set="FK_Right", row_index=16, title="FK.R", visible=False),
                BoneCollection(name="Leg.R (Tweak)", ui=True, color_set="Tweak_Right", row_index=17, title="Tweak.R", visible=False),

                BoneCollection(name="Tail", ui=True, color_set="Special", row_index=19, title="Tail"),
                BoneCollection(name="Tail (Tweak)", ui=True, color_set="Tweak", row_index=20, title="Tweaks", visible=False),

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
            [HEAD],
            [LEFT_EYE],
            [RIGHT_EYE]
        ]
)