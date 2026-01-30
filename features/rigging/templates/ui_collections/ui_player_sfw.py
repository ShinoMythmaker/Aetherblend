from .....core.rigify.settings import BoneCollection

UI_PLAYER_SFW = {
                "head": BoneCollection(name="Head", ui=True, color_set="Head", row_index=1, title="Head"),
                "face_primary": BoneCollection(name="Face (Primary)", ui=True, color_set="Face_Primary", row_index=2, title="Primary", visible=False),
                "face_secondary": BoneCollection(name="Face (Secondary)", ui=True, color_set="Face_Secondary", row_index=2, title="Secondary", visible=False),
                "mouth": BoneCollection(name="Mouth", ui=True, color_set="Torso", row_index=3, title="Mouth", visible=False),


                "hair": BoneCollection(name="Hair", ui=True, color_set="Head", row_index=4, title="Hair", visible=False),
                "accessory": BoneCollection(name="Accessory", ui=True, color_set="Head", row_index=4, title="Accessory", visible=False),

                "torso": BoneCollection(name="Torso", ui=True, color_set="Torso", row_index=6, title="Torso"),
                "torso_tweak": BoneCollection(name="Torso (Tweak)", ui=True, color_set="Torso_Tweak", row_index=7, title="Tweak", visible=False),
                "fingers_left": BoneCollection(name="Fingers.L", ui=True, color_set="Fingers_Left", row_index=8, title="Fingers.L"),
                "fingers_right": BoneCollection(name="Fingers.R", ui=True, color_set="Fingers_Right", row_index=8, title="Fingers.R"),
                # BoneCollection(name="Fingers (Details)", ui=True, color_set="FK", row_index=9, title="(Details)", visible=False),
                # "toes_left": BoneCollection(name="Toes.L", ui=True, color_set="Fingers_Left", row_index=9, title="Toes.L", visible=False),
                # "toes_right": BoneCollection(name="Toes.R", ui=True, color_set="Fingers_Right", row_index=9, title="Toes.R", visible=False),
                

                "arm_l_ik": BoneCollection(name="Arm.L (IK)", ui=True, color_set="IK_Left", row_index=11, title="Arm IK.L"),
                "arm_l_fk": BoneCollection(name="Arm.L (FK)", ui=True, color_set="FK_Left", row_index=12, title="FK.L", visible=False),
                "arm_l_tweak": BoneCollection(name="Arm.L (Tweak)", ui=True, color_set="Tweak_Left", row_index=13, title="Tweak.L", visible=False),
                "arm_r_ik": BoneCollection(name="Arm.R (IK)", ui=True, color_set="IK_Right", row_index=11, title="Arm IK.R"),
                "arm_r_fk": BoneCollection(name="Arm.R (FK)", ui=True, color_set="FK_Right", row_index=12, title="FK.R", visible=False),
                "arm_r_tweak": BoneCollection(name="Arm.R (Tweak)", ui=True, color_set="Tweak_Right", row_index=13, title="Tweak.R", visible=False),

                "leg_l_ik": BoneCollection(name="Leg.L (IK)", ui=True, color_set="IK_Left", row_index=15, title="Leg IK.L"),
                "leg_l_fk": BoneCollection(name="Leg.L (FK)", ui=True, color_set="FK_Left", row_index=16, title="FK.L", visible=False),
                "leg_l_tweak": BoneCollection(name="Leg.L (Tweak)", ui=True, color_set="Tweak_Left", row_index=17, title="Tweak.L", visible=False),
                "leg_r_ik": BoneCollection(name="Leg.R (IK)", ui=True, color_set="IK_Right", row_index=15, title="Leg IK.R"),
                "leg_r_fk": BoneCollection(name="Leg.R (FK)", ui=True, color_set="FK_Right", row_index=16, title="FK.R", visible=False),
                "leg_r_tweak": BoneCollection(name="Leg.R (Tweak)", ui=True, color_set="Tweak_Right", row_index=17, title="Tweak.R", visible=False),

                "tail": BoneCollection(name="Tail", ui=True, color_set="Torso_Tweak", row_index=19, title="Tail"),
                # "tail_tweak": BoneCollection(name="Tail (Tweak)", ui=True, color_set="Tweak", row_index=20, title="Tweaks", visible=False),

                "skirt": BoneCollection(name="Skirt", ui=True, color_set="Torso", row_index=22, title="Skirt", visible=False),
                "skirt_tweak": BoneCollection(name="Skirt (Tweak)", ui=True, color_set="Torso", row_index=23, title="Tweak", visible=False),
                # "ivcs": BoneCollection(name="IVCS", ui=True, color_set="IVCS", row_index=25, title="IVCS", visible=False)
                # BoneCollection(name="Genitals (Male)", ui=True, color_set="FK", row_index=25, title="Genitals (Male)", visible=False),
                # BoneCollection(name="Tweak (Male)", ui=True, color_set="Tweak", row_index=26, title="Tweak (Male)", visible=False),
                # BoneCollection(name="Genitals (Female)", ui=True, color_set="FK", row_index=25, title="Genitals (Female)", visible=False),
                # BoneCollection(name="Tweak (Female)", ui=True, color_set="Tweak", row_index=26, title="Tweak (Female)", visible=False),
        }

UI_PLAYER_SFW_IV = {
                "head": BoneCollection(name="Head", ui=True, color_set="Head", row_index=1, title="Head"),
                "face_primary": BoneCollection(name="Face (Primary)", ui=True, color_set="Face_Primary", row_index=2, title="Primary", visible=False),
                "face_secondary": BoneCollection(name="Face (Secondary)", ui=True, color_set="Face_Secondary", row_index=2, title="Secondary", visible=False),
                "mouth": BoneCollection(name="Mouth", ui=True, color_set="Torso", row_index=3, title="Mouth", visible=False),


                "hair": BoneCollection(name="Hair", ui=True, color_set="Head", row_index=4, title="Hair", visible=False),
                "accessory": BoneCollection(name="Accessory", ui=True, color_set="Head", row_index=4, title="Accessory", visible=False),

                "torso": BoneCollection(name="Torso", ui=True, color_set="Torso", row_index=6, title="Torso"),
                "torso_tweak": BoneCollection(name="Torso (Tweak)", ui=True, color_set="Torso_Tweak", row_index=7, title="Tweak", visible=False),
                "fingers_left": BoneCollection(name="Fingers.L", ui=True, color_set="Fingers_Left", row_index=8, title="Fingers.L"),
                "fingers_right": BoneCollection(name="Fingers.R", ui=True, color_set="Fingers_Right", row_index=8, title="Fingers.R"),
                # BoneCollection(name="Fingers (Details)", ui=True, color_set="FK", row_index=9, title="(Details)", visible=False),
                # "toes_left": BoneCollection(name="Toes.L", ui=True, color_set="Fingers_Left", row_index=9, title="Toes.L", visible=False),
                # "toes_right": BoneCollection(name="Toes.R", ui=True, color_set="Fingers_Right", row_index=9, title="Toes.R", visible=False),
                

                "arm_l_ik": BoneCollection(name="Arm.L (IK)", ui=True, color_set="IK_Left", row_index=11, title="Arm IK.L"),
                "arm_l_fk": BoneCollection(name="Arm.L (FK)", ui=True, color_set="FK_Left", row_index=12, title="FK.L", visible=False),
                "arm_l_tweak": BoneCollection(name="Arm.L (Tweak)", ui=True, color_set="Tweak_Left", row_index=13, title="Tweak.L", visible=False),
                "arm_r_ik": BoneCollection(name="Arm.R (IK)", ui=True, color_set="IK_Right", row_index=11, title="Arm IK.R"),
                "arm_r_fk": BoneCollection(name="Arm.R (FK)", ui=True, color_set="FK_Right", row_index=12, title="FK.R", visible=False),
                "arm_r_tweak": BoneCollection(name="Arm.R (Tweak)", ui=True, color_set="Tweak_Right", row_index=13, title="Tweak.R", visible=False),

                "leg_l_ik": BoneCollection(name="Leg.L (IK)", ui=True, color_set="IK_Left", row_index=15, title="Leg IK.L"),
                "leg_l_fk": BoneCollection(name="Leg.L (FK)", ui=True, color_set="FK_Left", row_index=16, title="FK.L", visible=False),
                "leg_l_tweak": BoneCollection(name="Leg.L (Tweak)", ui=True, color_set="Tweak_Left", row_index=17, title="Tweak.L", visible=False),
                "leg_r_ik": BoneCollection(name="Leg.R (IK)", ui=True, color_set="IK_Right", row_index=15, title="Leg IK.R"),
                "leg_r_fk": BoneCollection(name="Leg.R (FK)", ui=True, color_set="FK_Right", row_index=16, title="FK.R", visible=False),
                "leg_r_tweak": BoneCollection(name="Leg.R (Tweak)", ui=True, color_set="Tweak_Right", row_index=17, title="Tweak.R", visible=False),

                "tail": BoneCollection(name="Tail", ui=True, color_set="Torso_Tweak", row_index=19, title="Tail"),
                # "tail_tweak": BoneCollection(name="Tail (Tweak)", ui=True, color_set="Tweak", row_index=20, title="Tweaks", visible=False),

                "skirt": BoneCollection(name="Skirt", ui=True, color_set="Torso", row_index=22, title="Skirt", visible=False),
                "skirt_tweak": BoneCollection(name="Skirt (Tweak)", ui=True, color_set="Torso", row_index=23, title="Tweak", visible=False),
                "ivcs": BoneCollection(name="IVCS", ui=True, color_set="IVCS", row_index=25, title="IVCS", visible=False)
                # BoneCollection(name="Genitals (Male)", ui=True, color_set="FK", row_index=25, title="Genitals (Male)", visible=False),
                # BoneCollection(name="Tweak (Male)", ui=True, color_set="Tweak", row_index=26, title="Tweak (Male)", visible=False),
                # BoneCollection(name="Genitals (Female)", ui=True, color_set="FK", row_index=25, title="Genitals (Female)", visible=False),
                # BoneCollection(name="Tweak (Female)", ui=True, color_set="Tweak", row_index=26, title="Tweak (Female)", visible=False),
        }

UI_PLAYER_NSFW_IV = {
                "head": BoneCollection(name="Head", ui=True, color_set="Head", row_index=1, title="Head"),
                "face_primary": BoneCollection(name="Face (Primary)", ui=True, color_set="Face_Primary", row_index=2, title="Primary", visible=False),
                "face_secondary": BoneCollection(name="Face (Secondary)", ui=True, color_set="Face_Secondary", row_index=2, title="Secondary", visible=False),
                "mouth": BoneCollection(name="Mouth", ui=True, color_set="Torso", row_index=3, title="Mouth", visible=False),


                "hair": BoneCollection(name="Hair", ui=True, color_set="Head", row_index=4, title="Hair", visible=False),
                "accessory": BoneCollection(name="Accessory", ui=True, color_set="Head", row_index=4, title="Accessory", visible=False),

                "torso": BoneCollection(name="Torso", ui=True, color_set="Torso", row_index=6, title="Torso"),
                "torso_tweak": BoneCollection(name="Torso (Tweak)", ui=True, color_set="Torso_Tweak", row_index=7, title="Tweak", visible=False),
                "fingers_left": BoneCollection(name="Fingers.L", ui=True, color_set="Fingers_Left", row_index=8, title="Fingers.L"),
                "fingers_right": BoneCollection(name="Fingers.R", ui=True, color_set="Fingers_Right", row_index=8, title="Fingers.R"),
                # BoneCollection(name="Fingers (Details)", ui=True, color_set="FK", row_index=9, title="(Details)", visible=False),
                # "toes_left": BoneCollection(name="Toes.L", ui=True, color_set="Fingers_Left", row_index=9, title="Toes.L", visible=False),
                # "toes_right": BoneCollection(name="Toes.R", ui=True, color_set="Fingers_Right", row_index=9, title="Toes.R", visible=False),
                

                "arm_l_ik": BoneCollection(name="Arm.L (IK)", ui=True, color_set="IK_Left", row_index=11, title="Arm IK.L"),
                "arm_l_fk": BoneCollection(name="Arm.L (FK)", ui=True, color_set="FK_Left", row_index=12, title="FK.L", visible=False),
                "arm_l_tweak": BoneCollection(name="Arm.L (Tweak)", ui=True, color_set="Tweak_Left", row_index=13, title="Tweak.L", visible=False),
                "arm_r_ik": BoneCollection(name="Arm.R (IK)", ui=True, color_set="IK_Right", row_index=11, title="Arm IK.R"),
                "arm_r_fk": BoneCollection(name="Arm.R (FK)", ui=True, color_set="FK_Right", row_index=12, title="FK.R", visible=False),
                "arm_r_tweak": BoneCollection(name="Arm.R (Tweak)", ui=True, color_set="Tweak_Right", row_index=13, title="Tweak.R", visible=False),

                "leg_l_ik": BoneCollection(name="Leg.L (IK)", ui=True, color_set="IK_Left", row_index=15, title="Leg IK.L"),
                "leg_l_fk": BoneCollection(name="Leg.L (FK)", ui=True, color_set="FK_Left", row_index=16, title="FK.L", visible=False),
                "leg_l_tweak": BoneCollection(name="Leg.L (Tweak)", ui=True, color_set="Tweak_Left", row_index=17, title="Tweak.L", visible=False),
                "leg_r_ik": BoneCollection(name="Leg.R (IK)", ui=True, color_set="IK_Right", row_index=15, title="Leg IK.R"),
                "leg_r_fk": BoneCollection(name="Leg.R (FK)", ui=True, color_set="FK_Right", row_index=16, title="FK.R", visible=False),
                "leg_r_tweak": BoneCollection(name="Leg.R (Tweak)", ui=True, color_set="Tweak_Right", row_index=17, title="Tweak.R", visible=False),

                "tail": BoneCollection(name="Tail", ui=True, color_set="Torso_Tweak", row_index=19, title="Tail"),
                # "tail_tweak": BoneCollection(name="Tail (Tweak)", ui=True, color_set="Tweak", row_index=20, title="Tweaks", visible=False),

                "skirt": BoneCollection(name="Skirt", ui=True, color_set="Torso", row_index=22, title="Skirt", visible=False),
                "skirt_tweak": BoneCollection(name="Skirt (Tweak)", ui=True, color_set="Torso", row_index=23, title="Tweak", visible=False),
                "ivcs": BoneCollection(name="IVCS", ui=True, color_set="IVCS", row_index=25, title="IVCS", visible=False),
                "genitals_m": BoneCollection(name="Genitals (Male)", ui=True, color_set="IVCS", row_index=26, title="Genitals (Male)", visible=False),
                # BoneCollection(name="Tweak (Male)", ui=True, color_set="Tweak", row_index=26, title="Tweak (Male)", visible=False),
                "genitals_f": BoneCollection(name="Genitals (Female)", ui=True, color_set="IVCS", row_index=26, title="Genitals (Female)", visible=False),
                # BoneCollection(name="Tweak (Female)", ui=True, color_set="Tweak", row_index=26, title="Tweak (Female)", visible=False),
        }