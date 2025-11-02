from dataclasses import dataclass
import mathutils

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
    copy_rot_axes: dict[str, bool] | None = None
    make_extra_ik_control: bool | None = None
    super_copy_widget_type: str | None = None
    pivot_pos: int | None = None
    secondary_layer_extra: str | None  = None
    skin_chain_pivot_pos: int | None  = None
    skin_chain_falloff_spherical: list[bool] | None  = None
    skin_control_orientation_bone: str | None  = None

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
class SkinBone:
    org_bone: str
    name: str
    size_factor: float = 1.0
    lead_bone: bool = False

@dataclass(frozen=True)
class BridgeBone:
    bone_a: str
    bone_b: str
    segments: int = 1
    offset_factor: mathutils.Vector = mathutils.Vector((0.0, 0.0, 0.0))
    connected: bool = True

@dataclass(frozen=True)
class BoneChainInfo:
    ffxiv_bones: list[str] | None = None
    gen_bones: dict[str, RigifySettings | None] | None = None
    parent_bone: str | None = None
    bone_extensions: BoneExtensionInfo | None = None
    roll: float | None = 0.0
    extend_last: bool = False
    extension_factor: float = 0.0
    skin_bones: list[SkinBone] | None = None
    bridge_bones: list[BridgeBone] | None = None


@dataclass(frozen=True)
class EyeBone:
    outer_bones: list[SkinBone]
    bridges: list[BridgeBone]
    eye_name: str
    eye_collection: str
    parent_bone: str | None = None
    bone_settings: dict[str, RigifySettings | None] | None = None

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
    MetaRigCollectionInfo(name="Face", color_type="FK", row_index=1, title="Face"),
    MetaRigCollectionInfo(name="Face (Primary)", color_type="IK", row_index=2, title="(Primary)"),
    MetaRigCollectionInfo(name="Face (Secondary)", color_type="Special", row_index=2, title="(Secondary)"),

    MetaRigCollectionInfo(name="Torso", color_type="Special", row_index=4, title="Torso"),
    MetaRigCollectionInfo(name="Torso (Tweak)", color_type="Tweak", row_index=5, title="(Tweak)"),

    MetaRigCollectionInfo(name="Fingers", color_type="Extra", row_index=7, title="Fingers"),
    MetaRigCollectionInfo(name="Fingers (Details)", color_type="FK", row_index=8, title="(Details)"),

    MetaRigCollectionInfo(name="Arm.L (IK)", color_type="IK", row_index=10, title="IK.L"),
    MetaRigCollectionInfo(name="Arm.L (FK)", color_type="FK", row_index=11, title="FK.L"),
    MetaRigCollectionInfo(name="Arm.L (Tweak)", color_type="Tweak", row_index=12, title="Tweak.L"),
    MetaRigCollectionInfo(name="Arm.R (IK)", color_type="IK", row_index=10, title="IK.R"),
    MetaRigCollectionInfo(name="Arm.R (FK)", color_type="FK", row_index=11, title="FK.R"),
    MetaRigCollectionInfo(name="Arm.R (Tweak)", color_type="Tweak", row_index=12, title="Tweak.R"),

    MetaRigCollectionInfo(name="Leg.L (IK)", color_type="IK", row_index=14, title="IK.L"),
    MetaRigCollectionInfo(name="Leg.L (FK)", color_type="FK", row_index=15, title="FK.L"),
    MetaRigCollectionInfo(name="Leg.L (Tweak)", color_type="Tweak", row_index=16, title="Tweak.L"),
    MetaRigCollectionInfo(name="Leg.R (IK)", color_type="IK", row_index=14, title="IK.R"),
    MetaRigCollectionInfo(name="Leg.R (FK)", color_type="FK", row_index=15, title="FK.R"),
    MetaRigCollectionInfo(name="Leg.R (Tweak)", color_type="Tweak", row_index=16, title="Tweak.R"),

    MetaRigCollectionInfo(name="Tail", color_type="Special", row_index=18, title="Tail"),
    MetaRigCollectionInfo(name="Tail (Tweak)", color_type="Tweak", row_index=19, title="Tweaks"),
]

SPINE_INFO: dict[list[str, str], BoneChainInfo] = {
    ("Torso", "Spine"): BoneChainInfo(
        ffxiv_bones=["j_sebo_a", "j_sebo_b", "j_sebo_c", "j_kubi"],
        gen_bones= {
            "spine.01": RigifySettings(rigify_type="spines.basic_spine", fk_coll="Torso (Tweak)", tweak_coll="Torso (Tweak)", pivot_pos=1),
            "spine.02": None,
            "spine.03": None,
            "hips": RigifySettings(rigify_type="basic.super_copy", super_copy_widget_type="pivot")
        },
        bone_extensions= [
        BoneExtensionInfo(
            org_bone="spine.01",
            name="hips",
            extension_factors= (-0.15),
            axis_type="local",
            axis="Y", 
            start="head",
            is_connected=False
        )]
    ),
    ("Torso", "Shoulder L"): BoneChainInfo(
        ffxiv_bones=["j_sako_l", "j_ude_a_l"],
        gen_bones= {
            "shoulder.L": RigifySettings(rigify_type="basic.super_copy", super_copy_widget_type="shoulder")
        },
        parent_bone="spine.03",
    ),
    ("Torso", "Shoulder R"): BoneChainInfo(
        ffxiv_bones=["j_sako_r", "j_ude_a_r"],
        gen_bones= {
            "shoulder.R": RigifySettings(rigify_type="basic.super_copy", super_copy_widget_type="shoulder")
        },
        parent_bone="spine.03",
    ),
    ("Torso", "Neck"): BoneChainInfo(
        ffxiv_bones=["j_kubi", "j_kao"],
        gen_bones= {
            "neck": RigifySettings(rigify_type="basic.super_copy", super_copy_widget_type="circle")
        },
        parent_bone="spine.03",
    ),
}

ARMS_INFO: dict[str, BoneChainInfo] = {
    "Arm.L (IK)": BoneChainInfo(
        ffxiv_bones=["j_ude_a_l", "j_ude_b_l", "j_te_l"],
        gen_bones= {
            "upper_arm.L": RigifySettings(rigify_type="limbs.arm", fk_coll="Arm.L (FK)", tweak_coll="Arm.L (Tweak)"),
            "forearm.L": None,
            "hand.L": None
        },
        parent_bone="shoulder.L",
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
        parent_bone="shoulder.R",
        extend_last=True,
        extension_factor=0.6
    )
}

FINGERS_INFO: dict[list[str, str], BoneChainInfo] = {
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

LEGS_INFO: dict[str, BoneChainInfo] = {
    "Leg.L (IK)": BoneChainInfo(
        ffxiv_bones=["j_asi_a_l", "j_asi_c_l", "j_asi_d_l", "j_asi_e_l"],
        gen_bones= {
            "thigh.L": RigifySettings(rigify_type="limbs.leg", fk_coll="Leg.L (FK)", tweak_coll="Leg.L (Tweak)"),
            "shin.L": None,
            "foot.L": None,
            "toe.L": None
        },
        parent_bone="hips",
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
        parent_bone="hips",
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

TAILS_INFO: dict[str, BoneChainInfo] = {
    "Tail": BoneChainInfo(
        ffxiv_bones=["n_sippo_a", "n_sippo_b", "n_sippo_c", "n_sippo_d", "n_sippo_e"],
        gen_bones= {
            "tail.A": RigifySettings(rigify_type="spines.basic_tail", copy_rot_axes={"use_x": True, "use_y": True, "use_z": True}, tweak_coll="Tail (Tweak)"),
            "tail.B": None,
            "tail.C": None,
            "tail.D": None,
        },
        parent_bone="hips",
        extend_last=False,
        extension_factor=0.4
    )
}

EYES_GEN_INFO: dict[list[str, str], EyeBone] = {
    ("Face (Secondary)", "Eye.L"): EyeBone(
        outer_bones=[
            SkinBone(org_bone="j_f_mabup_02out_l", name="lid.T.L"),
            SkinBone(org_bone="j_f_mabup_01_l", name="lid.T.L.002"),
            SkinBone(org_bone="j_f_mabdn_03in_l", name="lid.B.L"),
            SkinBone(org_bone="j_f_mabdn_01_l", name="lid.B.L.002"),
        ],
        bridges=[
            BridgeBone(bone_a="lid.T.L", bone_b="lid.T.L.002", segments=1, offset_factor=mathutils.Vector((0.0, -0.001, 0.001)), connected=True),
            BridgeBone(bone_a="lid.T.L.002", bone_b="lid.B.L", segments=1, offset_factor=mathutils.Vector((0.0, 0.0, 0.003)), connected=False),
            BridgeBone(bone_a="lid.B.L", bone_b="lid.B.L.002", segments=1, offset_factor=mathutils.Vector((-0.002, 0.0, 0.001)), connected=True),
            BridgeBone(bone_a="lid.B.L.002", bone_b="lid.T.L", segments=1, offset_factor=mathutils.Vector((0.003, -0.001, -0.003)), connected=False),
        ],
        eye_name="eye.L",
        eye_collection="Face",
        parent_bone="neck",
        bone_settings={
            "eye.L": RigifySettings(rigify_type="face.skin_eye"),
            "lid.B.L": RigifySettings(rigify_type="skin.stretchy_chain", skin_chain_pivot_pos=2,secondary_layer_extra="Face (Primary)" ,skin_control_orientation_bone="neck"),
            "lid.T.L": RigifySettings(rigify_type="skin.stretchy_chain", skin_chain_pivot_pos=2,secondary_layer_extra="Face (Primary)" ,skin_control_orientation_bone="neck", skin_chain_falloff_spherical=[False, True, False]),
        },
    ),
    ("Face (Secondary)", "Eye.R"): EyeBone(
        outer_bones=[
            SkinBone(org_bone="j_f_mabup_02out_r", name="lid.T.R"),
            SkinBone(org_bone="j_f_mabup_01_r", name="lid.T.R.002"),
            SkinBone(org_bone="j_f_mabdn_03in_r", name="lid.B.R"),
            SkinBone(org_bone="j_f_mabdn_01_r", name="lid.B.R.002"),
        ],
        bridges=[
            BridgeBone(bone_a="lid.T.R", bone_b="lid.T.R.002", segments=1, offset_factor=mathutils.Vector((0.0, -0.001, 0.001)), connected=True),
            BridgeBone(bone_a="lid.T.R.002", bone_b="lid.B.R", segments=1, offset_factor=mathutils.Vector((0.0, 0.0, 0.003)), connected=False),
            BridgeBone(bone_a="lid.B.R", bone_b="lid.B.R.002", segments=1, offset_factor=mathutils.Vector((0.002, 0.0, 0.001)), connected=True),
            BridgeBone(bone_a="lid.B.R.002", bone_b="lid.T.R", segments=1, offset_factor=mathutils.Vector((-0.003, -0.001, -0.003)), connected=False),
        ],
        eye_name="eye.R",
        eye_collection="Face",
        parent_bone="neck",
        bone_settings={
            "eye.R": RigifySettings(rigify_type="face.skin_eye"),
            "lid.B.R": RigifySettings(rigify_type="skin.stretchy_chain", skin_chain_pivot_pos=2,secondary_layer_extra="Face (Primary)" ,skin_control_orientation_bone="neck"),
            "lid.T.R": RigifySettings(rigify_type="skin.stretchy_chain", skin_chain_pivot_pos=2,secondary_layer_extra="Face (Primary)" ,skin_control_orientation_bone="neck", skin_chain_falloff_spherical=[False, True, False]),
        },
    ),
}



CONSTRAINTS_TRACK_TO_AFTER_ORIGINAL: dict[str, str] = {
    #Eyes 
    # Left Eye  
    "j_f_mabdn_03in_l": "lid.B.L.001",
    "j_f_mabdn_01_l": "lid.B.L.002",
    "j_f_mabdn_02out_l": "lid.B.L.003",

    "j_f_mabup_03in_l": "lid.T.L.003",
    "j_f_mabup_01_l": "lid.T.L.002",
    "j_f_mabup_02out_l": "lid.T.L.001",

    # Right Eye
    "j_f_mabdn_03in_r": "lid.B.R.001",
    "j_f_mabdn_01_r": "lid.B.R.002",
    "j_f_mabdn_02out_r": "lid.B.R.003",

    "j_f_mabup_03in_r": "lid.T.R.003",
    "j_f_mabup_01_r": "lid.T.R.002",
    "j_f_mabup_02out_r": "lid.T.R.001",
}


CONSTRAINTS_COPY_ROT: dict[str, list[str]] = {
        # Eyes
        "j_f_eye_l": ["MCH-eye.L"],
        "j_f_eye_r": ["MCH-eye.R"],

        # Spine 
        "j_kosi": ["j_sebo_a", "hips.001"],

        "j_sebo_a": ["DEF-spine.01"],
        "j_sebo_b": ["DEF-spine.02"],
        "j_sebo_c": ["DEF-spine.03"],

        "j_sako_l": ["shoulder.L"],
        "j_sako_r": ["shoulder.R"],
        "j_kubi": ["neck"],


        # Left Fingers 
        "j_oya_a_l": ["ORG-f_thumb.L01"],
        "j_oya_b_l": ["ORG-f_thumb.L02"],
        "j_hito_a_l": ["ORG-f_pointer.L01"],
        "j_hito_b_l": ["ORG-f_pointer.L02"],
        "iv_hito_c_l": ["ORG-f_pointer.L03"],
        "j_naka_a_l": ["ORG-f_middle.L01"],
        "j_naka_b_l": ["ORG-f_middle.L02"],
        "iv_naka_c_l": ["ORG-f_middle.L03"],
        "j_kusu_a_l": ["ORG-f_ring.L01"],
        "j_kusu_b_l": ["ORG-f_ring.L02"],
        "iv_kusu_c_l": ["ORG-f_ring.L03"],
        "j_ko_a_l": ["ORG-f_pinky.L01"],
        "j_ko_b_l": ["ORG-f_pinky.L02"],
        "iv_ko_c_l": ["ORG-f_pinky.L03"],

        # Right Fingers
        "j_oya_a_r": ["ORG-f_thumb.R01"],
        "j_oya_b_r": ["ORG-f_thumb.R02"],
        "j_hito_a_r": ["ORG-f_pointer.R01"],
        "j_hito_b_r": ["ORG-f_pointer.R02"],
        "iv_hito_c_r": ["ORG-f_pointer.R03"],
        "j_naka_a_r": ["ORG-f_middle.R01"],
        "j_naka_b_r": ["ORG-f_middle.R02"],
        "iv_naka_c_r": ["ORG-f_middle.R03"],
        "j_kusu_a_r": ["ORG-f_ring.R01"],
        "j_kusu_b_r": ["ORG-f_ring.R02"],
        "iv_kusu_c_r": ["ORG-f_ring.R03"],
        "j_ko_a_r": ["ORG-f_pinky.R01"],
        "j_ko_b_r": ["ORG-f_pinky.R02"],
        "iv_ko_c_r": ["ORG-f_pinky.R03"],


        # Left Arm
        "j_ude_a_l": ["ORG-upper_arm.L"],
        "j_ude_b_l": ["ORG-forearm.L"],
        "j_te_l": ["ORG-hand.L"],

        # Right Arm
        "j_ude_a_r": ["ORG-upper_arm.R"],
        "j_ude_b_r": ["ORG-forearm.R"],
        "j_te_r": ["ORG-hand.R"],

        # DEF-toe because the ORG bone here stays still in local space. 
        # This issue is a mystery to me because it works when manually merging the rigify rig with the ffxiv rig. 
        # So i assume this happens in the parent clean up step.
        # Left Leg
        "j_asi_a_l": ["ORG-thigh.L"],
        "j_asi_c_l": ["ORG-shin.L"],
        "j_asi_d_l": ["ORG-foot.L"],
        "j_asi_e_l": ["DEF-toe.L"],

        # Right Leg
        "j_asi_a_r": ["ORG-thigh.R"],
        "j_asi_c_r": ["ORG-shin.R"],
        "j_asi_d_r": ["ORG-foot.R"],
        "j_asi_e_r": ["DEF-toe.R"],

        # Tail
        "n_sippo_a": ["tail.A"],
        "n_sippo_b": ["tail.B"],
        "n_sippo_c": ["tail.C"],
        "n_sippo_d": ["tail.D"],
        "n_sippo_e": ["Tail.A_master"]
    }

CONSTRAINTS_CHILD_OF: dict[str, list[str]] = {
    # Root
    "n_root": ["root"],
}

CONSTRAINTS_COPY_LOC: dict[str, list[str]] = {
    # Spine
    "j_sebo_a": ["DEF-spine.01"],
    "j_kosi": ["j_sebo_a"],
}