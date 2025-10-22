from dataclasses import dataclass
from typing import Dict

@dataclass(frozen=True)
class MetaRigCollectionInfo:
    name: str
    color_type: str
    row_index: int
    title: str

@dataclass(frozen=True)
class RigifySettings:
    rigify_type: str | None  = None
    fk_coll: str | None  = None
    tweak_coll: str | None  = None
    copy_rot_axes: Dict[str, bool] | None = None
    make_extra_ik_control: bool | None = False

@dataclass(frozen=True)
class BoneExtensionInfo:
    org_bone: str
    name: str
    extension_factors: float
    axis_type: str # e.g., "global", "local", "armature"
    axis: str # e.g., "X", "Y", "Z"
    start: str = "tail" # e.g., "head", "tail"
    is_connected: bool = False

@dataclass(frozen=True)
class BoneChainInfo:
    ffxiv_bones: list[str]
    gen_bones: dict[str, RigifySettings | None]
    parent_bone: str | None
    bone_extensions: BoneExtensionInfo | None = None
    roll: float | None = 0.0
    extend_last: bool = False
    extension_factor: float = 0.0

xiv_tail_bones = ["n_sippo_a", "n_sippo_b", "n_sippo_c", "n_sippo_d", "n_sippo_e"]
sb_tail_parent_bone = "j_kosi"
sb_tail_collection = "SB_Tail"

xiv_ear_bone_r = ["j_mimi_r"]
sb_ear_target_bone_r = ["n_ear_a_r"]
xiv_ear_bone_l = ["j_mimi_l"]
sb_ear_target_bone_l = ["n_ear_a_l"]
sb_ear_parent_bone = "j_kao"
sb_ears_collection = "SB_Ear"

xiv_breast_bone_r = ["j_mune_r"]
xiv_breast_bone_l = ["j_mune_l"]
sb_breast_parent_bone = "j_sebo_b"
sb_breast_collection = "SB_Breast"

spring_prefix = "sb_"
spring_bone_collection = "Spring Bones"


META_RIG_COLLECTIONS_INFO: list[MetaRigCollectionInfo] = [
    MetaRigCollectionInfo(name="Fingers", color_type="Extra", row_index=1, title="Fingers"),
    MetaRigCollectionInfo(name="Fingers (Details)", color_type="FK", row_index=2, title="(Details)"),

    MetaRigCollectionInfo(name="Arm.L (IK)", color_type="IK", row_index=4, title="IK.L"),
    MetaRigCollectionInfo(name="Arm.L (FK)", color_type="FK", row_index=5, title="FK.L"),
    MetaRigCollectionInfo(name="Arm.L (Tweak)", color_type="Tweak", row_index=6, title="Tweak.L"),
    MetaRigCollectionInfo(name="Arm.R (IK)", color_type="IK", row_index=4, title="IK.R"),
    MetaRigCollectionInfo(name="Arm.R (FK)", color_type="FK", row_index=5, title="FK.R"),
    MetaRigCollectionInfo(name="Arm.R (Tweak)", color_type="Tweak", row_index=6, title="Tweak.R"),

    MetaRigCollectionInfo(name="Leg.L (IK)", color_type="IK", row_index=8, title="IK.L"),
    MetaRigCollectionInfo(name="Leg.L (FK)", color_type="FK", row_index=9, title="FK.L"),
    MetaRigCollectionInfo(name="Leg.L (Tweak)", color_type="Tweak", row_index=10, title="Tweak.L"),
    MetaRigCollectionInfo(name="Leg.R (IK)", color_type="IK", row_index=8, title="IK.R"),
    MetaRigCollectionInfo(name="Leg.R (FK)", color_type="FK", row_index=9, title="FK.R"),
    MetaRigCollectionInfo(name="Leg.R (Tweak)", color_type="Tweak", row_index=10, title="Tweak.R"),

    MetaRigCollectionInfo(name="Tail", color_type="Special", row_index=12, title="Tail"),
    MetaRigCollectionInfo(name="Tail (Tweak)", color_type="Tweak", row_index=13, title="Tweaks"),
]

FINGERS_INFO: Dict[[str, str], BoneChainInfo] = {
    ("Fingers", "Thumb.L"): BoneChainInfo(
        ffxiv_bones=["j_oya_a_l", "j_oya_b_l"],
        gen_bones= {
            "f_thumb.L01": RigifySettings(rigify_type="limbs.super_finger", tweak_coll="Fingers (Details)", make_extra_ik_control=True),
            "f_thumb.L02": None,
            "f_thumb.L03": None
        },
        parent_bone="hand.L",
        extend_last=True,
        extension_factor=0.6
        ),
    ("Fingers", "Pointer.L"): BoneChainInfo(
        ffxiv_bones=["j_hito_a_l", "j_hito_b_l", "iv_hito_c_l"],
        gen_bones= {
            "f_pointer.L01": RigifySettings(rigify_type="limbs.super_finger", tweak_coll="Fingers (Details)", make_extra_ik_control=True),
            "f_pointer.L02": None,
            "f_pointer.L03": None
        },
        roll=(-135.0),
        parent_bone="hand.L",
        extend_last=True,
        extension_factor=1
    ),
    ("Fingers", "Middle.L"): BoneChainInfo(
        ffxiv_bones=["j_naka_a_l", "j_naka_b_l", "iv_naka_c_l"],
        gen_bones= {
            "f_middle.L01": RigifySettings(rigify_type="limbs.super_finger", tweak_coll="Fingers (Details)", make_extra_ik_control=True),
            "f_middle.L02": None,
            "f_middle.L03": None
        },
        roll=(-135.0),
        parent_bone="hand.L",
        extend_last=True,
        extension_factor=1
    ),
    ("Fingers", "Ring.L"): BoneChainInfo(
        ffxiv_bones=["j_kusu_a_l", "j_kusu_b_l", "iv_kusu_c_l"],
        gen_bones= {
            "f_ring.L01": RigifySettings(rigify_type="limbs.super_finger", tweak_coll="Fingers (Details)", make_extra_ik_control=True),
            "f_ring.L02": None,
            "f_ring.L03": None
        },
        roll=(-135.0),
        parent_bone="hand.L",
        extend_last=True,
        extension_factor=1
    ),
    ("Fingers", "Pinky.L"): BoneChainInfo(
        ffxiv_bones=["j_ko_a_l", "j_ko_b_l", "iv_ko_c_l"],
        gen_bones= {
            "f_pinky.L01": RigifySettings(rigify_type="limbs.super_finger", tweak_coll="Fingers (Details)", make_extra_ik_control=True),
            "f_pinky.L02": None,
            "f_pinky.L03": None
        },
        roll=(-135.0),
        parent_bone="hand.L",
        extend_last=True,
        extension_factor=1
    ),
    ("Fingers", "Thumb.R"): BoneChainInfo(
        ffxiv_bones=["j_oya_a_r", "j_oya_b_r"],
        gen_bones= {
            "f_thumb.R01": RigifySettings(rigify_type="limbs.super_finger", tweak_coll="Fingers (Details)", make_extra_ik_control=True),
            "f_thumb.R02": None,
            "f_thumb.R03": None
        },
        parent_bone="hand.R",
        extend_last=True,
        extension_factor=0.6
        ),
    ("Fingers", "Pointer.R"): BoneChainInfo(
        ffxiv_bones=["j_hito_a_r", "j_hito_b_r", "iv_hito_c_r"],
        gen_bones= {
            "f_pointer.R01": RigifySettings(rigify_type="limbs.super_finger", tweak_coll="Fingers (Details)", make_extra_ik_control=True),
            "f_pointer.R02": None,
            "f_pointer.R03": None
        },
        roll=135.0,
        parent_bone="hand.R",
        extend_last=True,
        extension_factor=1
    ),
    ("Fingers", "Middle.R"): BoneChainInfo(
        ffxiv_bones=["j_naka_a_r", "j_naka_b_r", "iv_naka_c_r"],
        gen_bones= {
            "f_middle.R01": RigifySettings(rigify_type="limbs.super_finger", tweak_coll="Fingers (Details)", make_extra_ik_control=True),
            "f_middle.R02": None,
            "f_middle.R03": None
        },
        roll=135.0,
        parent_bone="hand.R",
        extend_last=True,
        extension_factor=1
    ),
    ("Fingers", "Ring.R"): BoneChainInfo(
        ffxiv_bones=["j_kusu_a_r", "j_kusu_b_r", "iv_kusu_c_r"],
        gen_bones= {
            "f_ring.R01": RigifySettings(rigify_type="limbs.super_finger", tweak_coll="Fingers (Details)", make_extra_ik_control=True),
            "f_ring.R02": None,
            "f_ring.R03": None
        },
        roll=135.0,
        parent_bone="hand.R",
        extend_last=True,
        extension_factor=1
    ),
    ("Fingers", "Pinky.R"): BoneChainInfo(
        ffxiv_bones=["j_ko_a_r", "j_ko_b_r", "iv_ko_c_r"],
        gen_bones= {
            "f_pinky.R01": RigifySettings(rigify_type="limbs.super_finger", tweak_coll="Fingers (Details)", make_extra_ik_control=True),
            "f_pinky.R02": None,
            "f_pinky.R03": None
        },
        roll=135.0,
        parent_bone="hand.R",
        extend_last=True,
        extension_factor=1
    )
}


ARMS_INFO: Dict[str, BoneChainInfo] = {
    "Arm.L (IK)": BoneChainInfo(
        ffxiv_bones=["j_ude_a_l", "j_ude_b_l", "j_te_l"],
        gen_bones= {
            "upper_arm.L": RigifySettings(rigify_type="limbs.arm", fk_coll="Arm.L (FK)", tweak_coll="Arm.L (Tweak)"),
            "forearm.L": None,
            "hand.L": None
        },
        parent_bone="j_sako_l",
        extend_last=True,
        extension_factor=0.6
    ),
    "Arm.R (IK)": BoneChainInfo(
        ffxiv_bones=["j_ude_a_r", "j_ude_b_r", "j_te_r"],
        gen_bones= {
            "upper_arm.R": RigifySettings(rigify_type="limbs.arm", fk_coll="Arm.R (FK)", tweak_coll="Arm.R (Tweak)"),
            "forearm.R": None,
            "hand.R": None
        },
        parent_bone="j_sako_r",
        extend_last=True,
        extension_factor=0.6
    )
}

LEGS_INFO: Dict[str, BoneChainInfo] = {
    "Leg.L (IK)": BoneChainInfo(
        ffxiv_bones=["j_asi_a_l", "j_asi_c_l", "j_asi_d_l", "j_asi_e_l"],
        gen_bones= {
            "thigh.L": RigifySettings(rigify_type="limbs.leg", fk_coll="Leg.L (FK)", tweak_coll="Leg.L (Tweak)"),
            "shin.L": None,
            "foot.L": None,
            "toe.L": None
        },
        parent_bone="j_kosi",
        bone_extensions= [
        BoneExtensionInfo(
            org_bone="foot.L",
            name="toe.L",
            extension_factors= (-0.05),
            axis_type="armature",
            axis="Y", 
            start="tail",
            is_connected=True
        ),
        BoneExtensionInfo(
            org_bone="foot.L",
            name="heel.L",
            extension_factors=0.1,
            axis_type="armature",
            axis="Y", 
            start="tail",
            is_connected=False
        ), 
        ],
        extend_last=False,
        extension_factor=0.3
    ),
    "Leg.R (IK)": BoneChainInfo(
        ffxiv_bones=["j_asi_a_r","j_asi_c_r", "j_asi_d_r", "j_asi_e_r"],
        gen_bones= {
            "thigh.R": RigifySettings(rigify_type="limbs.leg", fk_coll="Leg.R (FK)", tweak_coll="Leg.R (Tweak)"),
            "shin.R": None,
            "foot.R": None,
            "toe.R": None
        },
        parent_bone="j_kosi",
        bone_extensions= [
        BoneExtensionInfo(
            org_bone="foot.R",
            name="toe.R",
            extension_factors= (-0.05),
            axis_type="armature",
            axis="Y", 
            start="tail",
            is_connected=True
        ),
        BoneExtensionInfo(
            org_bone="foot.R",
            name="heel.R",
            extension_factors=0.1,
            axis_type="armature",
            axis="Y",
            start="tail",
            is_connected=False
        ),
        ],
        extend_last=False,
        extension_factor=0.3
    ),
}

TAILS_INFO: Dict[str, BoneChainInfo] = {
    "Tail": BoneChainInfo(
        ffxiv_bones=["n_sippo_a", "n_sippo_b", "n_sippo_c", "n_sippo_d", "n_sippo_e"],
        gen_bones= {
            "tail.A": RigifySettings(rigify_type="spines.basic_tail", copy_rot_axes={"use_x": True, "use_y": True, "use_z": True}, tweak_coll="Tail (Tweak)"),
            "tail.B": None,
            "tail.C": None,
            "tail.D": None,
        },
        parent_bone="j_kosi",
        extend_last=False,
        extension_factor=0.4
    )
}


CONSTRAINT_BONE_MAP: Dict[str, str] = {
        # Left Fingers 
        "j_oya_a_l": "ORG-f_thumb.L01",
        "j_oya_b_l": "ORG-f_thumb.L02",
        "j_hito_a_l": "ORG-f_pointer.L01",
        "j_hito_b_l": "ORG-f_pointer.L02",
        "iv_hito_c_l": "ORG-f_pointer.L03",
        "j_naka_a_l": "ORG-f_middle.L01",
        "j_naka_b_l": "ORG-f_middle.L02",
        "iv_naka_c_l": "ORG-f_middle.L03",
        "j_kusu_a_l": "ORG-f_ring.L01",
        "j_kusu_b_l": "ORG-f_ring.L02",
        "iv_kusu_c_l": "ORG-f_ring.L03",
        "j_ko_a_l": "ORG-f_pinky.L01",
        "j_ko_b_l": "ORG-f_pinky.L02",
        "iv_ko_c_l": "ORG-f_pinky.L03",

        # Right Fingers
        "j_oya_a_r": "ORG-f_thumb.R01",
        "j_oya_b_r": "ORG-f_thumb.R02",
        "j_hito_a_r": "ORG-f_pointer.R01",
        "j_hito_b_r": "ORG-f_pointer.R02",
        "iv_hito_c_r": "ORG-f_pointer.R03",
        "j_naka_a_r": "ORG-f_middle.R01",
        "j_naka_b_r": "ORG-f_middle.R02",
        "iv_naka_c_r": "ORG-f_middle.R03",
        "j_kusu_a_r": "ORG-f_ring.R01",
        "j_kusu_b_r": "ORG-f_ring.R02",
        "iv_kusu_c_r": "ORG-f_ring.R03",
        "j_ko_a_r": "ORG-f_pinky.R01",
        "j_ko_b_r": "ORG-f_pinky.R02",
        "iv_ko_c_r": "ORG-f_pinky.R03",


        # Left Arm
        "j_ude_a_l": "ORG-upper_arm.L",
        "j_ude_b_l": "ORG-forearm.L", 
        "j_te_l": "ORG-hand.L",
        
        # Right Arm  
        "j_ude_a_r": "ORG-upper_arm.R",
        "j_ude_b_r": "ORG-forearm.R",
        "j_te_r": "ORG-hand.R",

        # DEF-toe because the ORG bone here stays still in local space. 
        # This issue is a mystery to me because it works when manually merging the rigify rig with the ffxiv rig. 
        # So i assume this happens in the parent clean up step.
        # Left Leg
        "j_asi_a_l": "ORG-thigh.L",
        "j_asi_c_l": "ORG-shin.L",
        "j_asi_d_l": "ORG-foot.L",
        "j_asi_e_l": "DEF-toe.L",

        # Right Leg
        "j_asi_a_r": "ORG-thigh.R",
        "j_asi_c_r": "ORG-shin.R",
        "j_asi_d_r": "ORG-foot.R",
        "j_asi_e_r": "DEF-toe.R", 

        # Tail 
        "n_sippo_a": "tail.A",
        "n_sippo_b": "tail.B",
        "n_sippo_c": "tail.C",
        "n_sippo_d": "tail.D",
        "n_sippo_e": "Tail.A_master"
    }