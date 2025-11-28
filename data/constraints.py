from . schemas import CopyLocationConstraint, CopyRotationConstraint, TrackToBone, Constraint, CopyScaleConstraint

CONSTRAINTS_TRACK_TO_AFTER_ORIGINAL: list[TrackToBone] = [
    #Eyes
    # Left Eye
    TrackToBone(origin_name="j_f_mabdn_03in_l", target_name="lid.B.L.001", custom_space="ORG-eye.L", parent_name="ORG-eye.L"),
    TrackToBone(origin_name="j_f_mabdn_01_l", target_name="lid.B.L.002", custom_space="ORG-eye.L", parent_name="ORG-eye.L"),
    TrackToBone(origin_name="j_f_mabdn_02out_l", target_name="lid.B.L.003", custom_space="ORG-eye.L", parent_name="ORG-eye.L"),

    TrackToBone(origin_name="j_f_mabup_03in_l", target_name="lid.T.L.003", custom_space="ORG-eye.L", parent_name="ORG-eye.L"),
    TrackToBone(origin_name="j_f_mabup_01_l", target_name="lid.T.L.002", custom_space="ORG-eye.L", parent_name="ORG-eye.L"),
    TrackToBone(origin_name="j_f_mabup_02out_l", target_name="lid.T.L.001", custom_space="ORG-eye.L", parent_name="ORG-eye.L"),

    # Right Eye
    TrackToBone(origin_name="j_f_mabdn_03in_r", target_name="lid.B.R.001", custom_space="ORG-eye.R", parent_name="ORG-eye.R"),
    TrackToBone(origin_name="j_f_mabdn_01_r", target_name="lid.B.R.002", custom_space="ORG-eye.R", parent_name="ORG-eye.R"),
    TrackToBone(origin_name="j_f_mabdn_02out_r", target_name="lid.B.R.003", custom_space="ORG-eye.R", parent_name="ORG-eye.R"),

    TrackToBone(origin_name="j_f_mabup_03in_r", target_name="lid.T.R.003", custom_space="ORG-eye.R", parent_name="ORG-eye.R"),
    TrackToBone(origin_name="j_f_mabup_01_r", target_name="lid.T.R.002", custom_space="ORG-eye.R", parent_name="ORG-eye.R"),
    TrackToBone(origin_name="j_f_mabup_02out_r", target_name="lid.T.R.001", custom_space="ORG-eye.R", parent_name="ORG-eye.R"),
]

CONSTRAINTS_COPY_ROT: dict[str, list[str]] = {
    }

CONSTRAINTS_CHILD_OF: dict[str, list[str]] = {
    # Root
    "n_root": ["root"],
}

CONSTRAINTS_COPY_LOC: dict[str, list[str]] = {
    }


NEW_CONSTRAINTS: dict[str, list[Constraint]] = {

    # Spine 
    "j_kosi": [CopyLocationConstraint(target_bone="j_sebo_a"), CopyRotationConstraint(target_bone="j_sebo_a"), CopyRotationConstraint(target_bone="hips.001")],

    "j_sebo_a": [CopyLocationConstraint(target_bone="DEF-spine.01"), CopyRotationConstraint(target_bone="DEF-spine.01")],
    "j_sebo_b": [CopyRotationConstraint(target_bone="DEF-spine.02")],
    "j_sebo_c": [CopyRotationConstraint(target_bone="DEF-spine.03")],

    "j_sako_l": [CopyRotationConstraint(target_bone="shoulder.L")],
    "j_sako_r": [CopyRotationConstraint(target_bone="shoulder.R")],

    # Left Arm
    "j_ude_a_l": [CopyLocationConstraint(target_bone="DEF-upper_arm.L"), CopyRotationConstraint(target_bone="ORG-upper_arm.L")],
    "j_ude_b_l": [CopyLocationConstraint(target_bone="DEF-forearm.L"), CopyRotationConstraint(target_bone="ORG-forearm.L")],
    "j_te_l": [CopyLocationConstraint(target_bone="DEF-hand.L"), CopyRotationConstraint(target_bone="ORG-hand.L")],

    # Right Arm
    "j_ude_a_r": [CopyLocationConstraint(target_bone="DEF-upper_arm.R"), CopyRotationConstraint(target_bone="ORG-upper_arm.R")],
    "j_ude_b_r": [CopyLocationConstraint(target_bone="DEF-forearm.R"), CopyRotationConstraint(target_bone="ORG-forearmm.R")],
    "j_te_r": [CopyLocationConstraint(target_bone="DEF-hand.R"), CopyRotationConstraint(target_bone="ORG-hand.R")],

    # Right Fingers
    "j_oya_a_r": [CopyRotationConstraint(target_bone="ORG-f_thumb.R01")],
    "j_oya_b_r": [CopyRotationConstraint(target_bone="ORG-f_thumb.R02")],
    "j_hito_a_r": [CopyRotationConstraint(target_bone="ORG-f_pointer.R01")],
    "j_hito_b_r": [CopyRotationConstraint(target_bone="ORG-f_pointer.R02")],
    "iv_hito_c_r": [CopyRotationConstraint(target_bone="ORG-f_pointer.R03")],
    "j_naka_a_r": [CopyRotationConstraint(target_bone="ORG-f_middle.R01")],
    "j_naka_b_r": [CopyRotationConstraint(target_bone="ORG-f_middle.R02")],
    "iv_naka_c_r": [CopyRotationConstraint(target_bone="ORG-f_middle.R03")],
    "j_kusu_a_r": [CopyRotationConstraint(target_bone="ORG-f_ring.R01")],
    "j_kusu_b_r": [CopyRotationConstraint(target_bone="ORG-f_ring.R02")],
    "iv_kusu_c_r": [CopyRotationConstraint(target_bone="ORG-f_ring.R03")],
    "j_ko_a_r": [CopyRotationConstraint(target_bone="ORG-f_pinky.R01")],
    "j_ko_b_r": [CopyRotationConstraint(target_bone="ORG-f_pinky.R02")],
    "iv_ko_c_r": [CopyRotationConstraint(target_bone="ORG-f_pinky.R03")],

    # Left Fingers 
    "j_oya_a_l": [CopyRotationConstraint(target_bone="ORG-f_thumb.L01")],
    "j_oya_b_l": [CopyRotationConstraint(target_bone="ORG-f_thumb.L02")],
    "j_hito_a_l": [CopyRotationConstraint(target_bone="ORG-f_pointer.L01")],
    "j_hito_b_l": [CopyRotationConstraint(target_bone="ORG-f_pointer.L02")],
    "iv_hito_c_l": [CopyRotationConstraint(target_bone="ORG-f_pointer.L03")],
    "j_naka_a_l": [CopyRotationConstraint(target_bone="ORG-f_middle.L01")],
    "j_naka_b_l": [CopyRotationConstraint(target_bone="ORG-f_middle.L02")],
    "iv_naka_c_l": [CopyRotationConstraint(target_bone="ORG-f_middle.L03")],
    "j_kusu_a_l": [CopyRotationConstraint(target_bone="ORG-f_ring.L01")],
    "j_kusu_b_l": [CopyRotationConstraint(target_bone="ORG-f_ring.L02")],
    "iv_kusu_c_l": [CopyRotationConstraint(target_bone="ORG-f_ring.L03")],
    "j_ko_a_l": [CopyRotationConstraint(target_bone="ORG-f_pinky.L01")],
    "j_ko_b_l": [CopyRotationConstraint(target_bone="ORG-f_pinky.L02")],
    "iv_ko_c_l": [CopyRotationConstraint(target_bone="ORG-f_pinky.L03")],

    #Brows

    "j_f_mayu_r": [CopyLocationConstraint(target_bone="DEF-brow.T.R"), CopyRotationConstraint(target_bone="brow.T.R")],
    "j_f_mmayu_r":[CopyLocationConstraint(target_bone="DEF-brow.T.R.001"), CopyRotationConstraint(target_bone="brow.T.R.001")],
    "j_f_miken_01_r":[CopyLocationConstraint(target_bone="DEF-brow.T.R.002"), CopyRotationConstraint(target_bone="brow.T.R.002")],
    "j_f_miken_01_r":[CopyLocationConstraint(target_bone="DEF-brow.T.R.003"), CopyRotationConstraint(target_bone="brow.T.R.003")],

    "j_f_mayu_l": [CopyLocationConstraint(target_bone="DEF-brow.T.L"), CopyRotationConstraint(target_bone="brow.T.L")],
    "j_f_mmayu_l": [CopyLocationConstraint(target_bone="DEF-brow.T.L.001"), CopyRotationConstraint(target_bone="brow.T.L.001")],
    "j_f_miken_01_l": [CopyLocationConstraint(target_bone="DEF-brow.T.L.002"), CopyRotationConstraint(target_bone="brow.T.L.002")],
    "j_f_miken_02_l": [CopyLocationConstraint(target_bone="DEF-brow.T.L.003"), CopyRotationConstraint(target_bone="brow.T.L.003")],


    #Eyes 
    "j_f_eyepuru_l": [CopyRotationConstraint(target_bone="MCH-eye.L", influence=0.5)],
    "j_f_mab_l": [CopyRotationConstraint(target_bone="eye_master.L")],
    "j_f_eyepuru_r": [CopyRotationConstraint(target_bone="MCH-eye.R", influence=0.5)],
    "j_f_mab_r": [CopyRotationConstraint(target_bone="eye_master.R")],

    # Left Mouth

    "j_f_ulip_01_l": [CopyLocationConstraint(target_bone="DEF-Lip.T.L")],
    "j_f_umlip_01_l": [CopyLocationConstraint(target_bone="DEF-Lip.T.L.001")],
    "j_f_uslip_l": [CopyLocationConstraint(target_bone="DEF-Lip.T.L.001", head_tail=1.0), CopyRotationConstraint(target_bone="Lip.Master.T.L.002")],
    "j_f_ulip_02_l":[CopyRotationConstraint(target_bone="Lip.T.L")],
    "j_f_umlip_02_l":[CopyRotationConstraint(target_bone="Lip.T.L.001")],



    "j_f_dlip_01_l": [CopyLocationConstraint(target_bone="DEF-Lip.B.L")],
    "j_f_dmlip_01_l": [CopyLocationConstraint(target_bone="DEF-Lip.B.L.001")],
    "j_f_dslip_l": [CopyLocationConstraint(target_bone="DEF-Lip.B.L.001", head_tail=1.0), CopyRotationConstraint(target_bone="Lip.Master.B.L.001")],
    "j_f_dlip_02_l":[CopyRotationConstraint(target_bone="Lip.B.L")],
    "j_f_dmlip_02_l":[CopyRotationConstraint(target_bone="Lip.B.L.001")],

    # Right Mouth

    "j_f_ulip_01_r": [CopyLocationConstraint(target_bone="DEF-Lip.T.R")],
    "j_f_umlip_01_r": [CopyLocationConstraint(target_bone="DEF-Lip.T.R.001")],
    "j_f_uslip_r": [CopyLocationConstraint(target_bone="DEF-Lip.T.R.001", head_tail=1.0), CopyRotationConstraint(target_bone="Lip.Master.T.R.002")],
    "j_f_ulip_02_r":[CopyRotationConstraint(target_bone="Lip.T.R")],
    "j_f_umlip_02_r":[CopyRotationConstraint(target_bone="Lip.T.R.001")],

    "j_f_dlip_01_r": [CopyLocationConstraint(target_bone="DEF-Lip.B.R")],
    "j_f_dmlip_01_r": [CopyLocationConstraint(target_bone="DEF-Lip.B.R.001")],
    "j_f_dslip_r": [CopyLocationConstraint(target_bone="DEF-Lip.B.R.001", head_tail=1.0), CopyRotationConstraint(target_bone="Lip.Master.B.R.001")],
    "j_f_dlip_02_r":[CopyRotationConstraint(target_bone="Lip.B.R")],
    "j_f_dmlip_02_r":[CopyRotationConstraint(target_bone="Lip.B.R.001")],

    # Tongue

    "j_f_bero_03": [CopyLocationConstraint(target_bone="ORG-Tongue"), CopyRotationConstraint(target_bone="ORG-Tongue")],
    "j_f_bero_02": [CopyLocationConstraint(target_bone="ORG-Tongue.001"), CopyRotationConstraint(target_bone="ORG-Tongue.001")],
    "j_f_bero_01": [CopyLocationConstraint(target_bone="ORG-Tongue.002"), CopyRotationConstraint(target_bone="ORG-Tongue.002")],
    
    # Jaw
    "j_f_ago": [CopyRotationConstraint(target_bone="jaw",)],
    "j_f_hagukiup": [CopyLocationConstraint(target_bone="ORG-Teeth.T"), CopyRotationConstraint(target_bone="ORG-Teeth.T")],
    "j_f_hagukidn": [CopyLocationConstraint(target_bone="ORG-Teeth.B"), CopyRotationConstraint(target_bone="ORG-Teeth.B")],

    #Head
    "j_kubi": [CopyRotationConstraint(target_bone="ORG-neck")],
    "j_kao": [CopyRotationConstraint(target_bone="ORG-head")],

    "j_mimi_l": [CopyRotationConstraint(target_bone="ORG-ear.L")],
    "j_mimi_r": [CopyRotationConstraint(target_bone="ORG-ear.R")],

    # Right Cheek

    "j_f_shoho_r": [CopyLocationConstraint(target_bone="DEF-Cheek.B.R")],
    "j_f_dhoho_r": [CopyLocationConstraint(target_bone="DEF-Cheek.B.R.001")],
    "j_f_hoho_r": [CopyLocationConstraint(target_bone="DEF-Cheek.B.R.001", head_tail=1.0)],
    "j_f_dmemoto_r": [CopyLocationConstraint(target_bone="DEF-Cheek.T.R.001")],

    # Left Cheek

    "j_f_shoho_l": [CopyLocationConstraint(target_bone="DEF-Cheek.B.L")],
    "j_f_dhoho_l": [CopyLocationConstraint(target_bone="DEF-Cheek.B.L.001")],
    "j_f_hoho_l": [CopyLocationConstraint(target_bone="DEF-Cheek.B.L.001", head_tail=1.0)],
    "j_f_dmemoto_l": [CopyLocationConstraint(target_bone="DEF-Cheek.T.L.001")],

    # Nose
    "j_f_dmiken_l": [CopyLocationConstraint(target_bone="ORG-Nose.L")],
    "j_f_dmiken_r": [CopyLocationConstraint(target_bone="ORG-Nose.R")],
    "j_f_uhana": [CopyLocationConstraint(target_bone="ORG-Nose")],
    "j_f_hana_l": [CopyLocationConstraint(target_bone="ORG-Nose.L.001")],
    "j_f_hana_r": [CopyLocationConstraint(target_bone="DEF-Nose.R.001")],

    # Left Leg
    # DEF-toe because the ORG bone here stays still in local space. 
    # This issue is a mystery to me because it works when manually merging the rigify rig with the ffxiv rig. 
    # So i assume this happens in the parent clean up step.
    "j_asi_a_l": [CopyRotationConstraint(target_bone="ORG-thigh.L")],
    "j_asi_c_l": [CopyRotationConstraint(target_bone="ORG-shin.L")],
    "j_asi_d_l": [CopyRotationConstraint(target_bone="ORG-foot.L")],
    "j_asi_e_l": [CopyRotationConstraint(target_bone="DEF-toe.L")],

    # Right Leg
    "j_asi_a_r": [CopyRotationConstraint(target_bone="ORG-thigh.R")],
    "j_asi_c_r": [CopyRotationConstraint(target_bone="ORG-shin.R")],
    "j_asi_d_r": [CopyRotationConstraint(target_bone="ORG-foot.R")],
    "j_asi_e_r": [CopyRotationConstraint(target_bone="DEF-toe.R")],

    # Tail
    "n_sippo_a": [CopyRotationConstraint(target_bone="ORG-tail.A")],
    "n_sippo_b": [CopyRotationConstraint(target_bone="tail.B")],
    "n_sippo_c": [CopyRotationConstraint(target_bone="tail.C")],
    "n_sippo_d": [CopyRotationConstraint(target_bone="tail.D")],
    "n_sippo_e": [CopyRotationConstraint(target_bone="Tail.A_master")],

    # Skirt

    "j_sk_f_a_l": [CopyRotationConstraint(target_bone="DEF-skirt_front.L")],
    "j_sk_f_b_l": [CopyRotationConstraint(target_bone="DEF-skirt_front.L.001")],
    "j_sk_f_c_l": [CopyRotationConstraint(target_bone="DEF-skirt_front.L.002")],

    "j_sk_s_a_l": [CopyRotationConstraint(target_bone="DEF-skirt_out.L")],
    "j_sk_s_b_l": [CopyRotationConstraint(target_bone="DEF-skirt_out.L.001")],
    "j_sk_s_c_l": [CopyRotationConstraint(target_bone="DEF-skirt_out.L.002")],

    "j_sk_b_a_l": [CopyRotationConstraint(target_bone="DEF-skirt_back.L")],
    "j_sk_b_b_l": [CopyRotationConstraint(target_bone="DEF-skirt_back.L.001")],
    "j_sk_b_c_l": [CopyRotationConstraint(target_bone="DEF-skirt_back.L.002")],

    "j_sk_f_a_r": [CopyRotationConstraint(target_bone="DEF-skirt_front.R")],
    "j_sk_f_b_r": [CopyRotationConstraint(target_bone="DEF-skirt_front.R.001")],
    "j_sk_f_c_r": [CopyRotationConstraint(target_bone="DEF-skirt_front.R.002")],

    "j_sk_s_a_r": [CopyRotationConstraint(target_bone="DEF-skirt_out.R")],
    "j_sk_s_b_r": [CopyRotationConstraint(target_bone="DEF-skirt_out.R.001")],
    "j_sk_s_c_r": [CopyRotationConstraint(target_bone="DEF-skirt_out.R.002")],

    "j_sk_b_a_r": [CopyRotationConstraint(target_bone="DEF-skirt_back.R")],
    "j_sk_b_b_r": [CopyRotationConstraint(target_bone="DEF-skirt_back.R.001")],
    "j_sk_b_c_r": [CopyRotationConstraint(target_bone="DEF-skirt_back.R.002")],


    # Simple Face Bones 
}