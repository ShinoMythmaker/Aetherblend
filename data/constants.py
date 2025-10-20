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

@dataclass(frozen=True)
class BoneChainInfo:
    ffxiv_bones: list[str]
    gen_bones: dict[str, RigifySettings | None]
    parent_bone: str | None
    extend_last: bool
    extension_factor: float

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
    MetaRigCollectionInfo(name="Arm.L (IK)", color_type="IK", row_index=1, title="IK.L"),
    MetaRigCollectionInfo(name="Arm.L (FK)", color_type="FK", row_index=2, title="FK.L"),
    MetaRigCollectionInfo(name="Arm.L (Tweak)", color_type="Tweak", row_index=3, title="Tweak.L"),
    MetaRigCollectionInfo(name="Arm.R (IK)", color_type="IK", row_index=1, title="IK.R"),
    MetaRigCollectionInfo(name="Arm.R (FK)", color_type="FK", row_index=2, title="FK.R"),
    MetaRigCollectionInfo(name="Arm.R (Tweak)", color_type="Tweak", row_index=3, title="Tweak.R"),

    MetaRigCollectionInfo(name="Leg.L (IK)", color_type="IK", row_index=5, title="IK.L"),
    MetaRigCollectionInfo(name="Leg.L (FK)", color_type="FK", row_index=6, title="FK.L"),
    MetaRigCollectionInfo(name="Leg.L (Tweak)", color_type="Tweak", row_index=7, title="Tweak.L"),
    MetaRigCollectionInfo(name="Leg.R (IK)", color_type="IK", row_index=5, title="IK.R"),
    MetaRigCollectionInfo(name="Leg.R (FK)", color_type="FK", row_index=6, title="FK.R"),
    MetaRigCollectionInfo(name="Leg.R (Tweak)", color_type="Tweak", row_index=7, title="Tweak.R"),

    MetaRigCollectionInfo(name="Tail", color_type="Special", row_index=9, title="Tail"),
    MetaRigCollectionInfo(name="Tail (Tweak)", color_type="Tweak", row_index=9, title="Tweaks"),
]

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
    # "Leg.L (IK)": BoneChainInfo(
    #     ffxiv_bones=["j_asi_a_l", "j_asi_c_l", "j_asi_d_l", "j_asi_e_l"],
    #     gen_bones= {
    #         "thigh.L": RigifySettings(rigify_type="limbs.leg", fk_coll="Leg.L (FK)", tweak_coll="Leg.L (Tweak)"),
    #         "shin.L": None,
    #         "foot.L": None,
    #         "toe.L": None
    #     },
    #     parent_bone="j_kosi",
    #     extend_last=True,
    #     extension_factor=0.2
    # ),
    # "Leg.R (IK)": BoneChainInfo(
    #     ffxiv_bones=["j_asi_a_r","j_asi_c_r", "j_asi_d_r", "j_asi_e_r"],
    #     gen_bones= {
    #         "thigh.R": RigifySettings(rigify_type="limbs.leg", fk_coll="Leg.R (FK)", tweak_coll="Leg.R (Tweak)"),
    #         "shin.R": None,
    #         "foot.R": None,
    #         "toe.R": None
    #     },
    #     parent_bone="j_kosi",
    #     extend_last=True,
    #     extension_factor=0.2
    # ),
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
        # Left Arm
        "j_ude_a_l": "ORG-upper_arm.L",
        "j_ude_b_l": "ORG-forearm.L", 
        "j_te_l": "ORG-hand.L",
        
        # Right Arm  
        "j_ude_a_r": "ORG-upper_arm.R",
        "j_ude_b_r": "ORG-forearm.R",
        "j_te_r": "ORG-hand.R",

        # Tail 
        "n_sippo_a": "tail.A",
        "n_sippo_b": "tail.B",
        "n_sippo_c": "tail.C",
        "n_sippo_d": "tail.D",
        "n_sippo_e": "Tail.A_master"
    }