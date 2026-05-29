from .....core.shared import PropOverride

PO_DEFAULT = {
        "ik_stretch_arm_l": PropOverride(bone="upper_arm_parent.L", property_name="IK_Stretch", value=0),
        "ik_stretch_arm_r": PropOverride(bone="upper_arm_parent.R", property_name="IK_Stretch", value=0),
        "ik_stretch_thigh_l": PropOverride(bone="thigh_parent.L", property_name="IK_Stretch", value=0),
        "ik_stretch_thigh_r": PropOverride(bone="thigh_parent.R", property_name="IK_Stretch", value=0),
        "head_follow": PropOverride(bone="head", property_name="head_follow", value=1),
    }