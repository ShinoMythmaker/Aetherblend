from . schemas import CopyLocationConstraint, CopyRotationConstraint, TrackToBone, Constraint, CopyScaleConstraint, CopyTransformsConstraint, AssignCollection, OffsetTransformConstraint, copyBone, connectBone, TrackToConstraint

LINK_EDIT_OPERATIONS = [
    copyBone(bone_name="MCH-n_root", src_bone_name="n_root", parent_bone_name="root"),
    # Spine
    copyBone(bone_name="MCH-j_kosi", src_bone_name="j_kosi", parent_bone_name="DEF-hips"),
    copyBone(bone_name="MCH-j_sebo_a", src_bone_name="j_sebo_a", parent_bone_name="DEF-spine.01"),
    copyBone(bone_name="MCH-j_sebo_b", src_bone_name="j_sebo_b", parent_bone_name="DEF-spine.02"),
    copyBone(bone_name="MCH-j_sebo_c", src_bone_name="j_sebo_c", parent_bone_name="DEF-spine.03"),
    copyBone(bone_name="MCH-j_sako_l", src_bone_name="j_sako_l", parent_bone_name="shoulder.L"),
    copyBone(bone_name="MCH-j_sako_r", src_bone_name="j_sako_r", parent_bone_name="shoulder.R"),
    
    # Chest
    copyBone(bone_name="MCH-j_mune_l", src_bone_name="j_mune_l", parent_bone_name="DEF-Chest.L"),
    copyBone(bone_name="MCH-j_mune_r", src_bone_name="j_mune_r", parent_bone_name="DEF-Chest.R"),
    copyBone(bone_name="MCH-n_hara", src_bone_name="n_hara", parent_bone_name="torso"),

    # Head
    copyBone(bone_name="MCH-j_kubi", src_bone_name="j_kubi", parent_bone_name="DEF-neck"),
    copyBone(bone_name="MCH-j_kao", src_bone_name="j_kao", parent_bone_name="DEF-head"),
    copyBone(bone_name="MCH-j_mimi_l", src_bone_name="j_mimi_l", parent_bone_name="DEF-ear.L"),
    copyBone(bone_name="MCH-j_mimi_r", src_bone_name="j_mimi_r", parent_bone_name="DEF-ear.R"),
    copyBone(bone_name="MCH-j_f_ago", src_bone_name="j_f_ago", parent_bone_name="DEF-jaw"),

    copyBone(bone_name="MCH-j_zera_a_l", src_bone_name="j_zera_a_l", parent_bone_name="DEF-v_ear.L"),
    copyBone(bone_name="MCH-j_zera_b_l", src_bone_name="j_zera_b_l", parent_bone_name="DEF-v_ear.L.001"),
    copyBone(bone_name="MCH-j_zera_a_r", src_bone_name="j_zera_a_r", parent_bone_name="DEF-v_ear.R"),
    copyBone(bone_name="MCH-j_zera_b_r", src_bone_name="j_zera_b_r", parent_bone_name="DEF-v_ear.R.001"),

    copyBone(bone_name="MCH-j_zerc_a_l", src_bone_name="j_zerc_a_l", parent_bone_name="DEF-v_ear.L"),
    copyBone(bone_name="MCH-j_zerc_b_l", src_bone_name="j_zerc_b_l", parent_bone_name="DEF-v_ear.L.001"),
    copyBone(bone_name="MCH-j_zerc_a_r", src_bone_name="j_zerc_a_r", parent_bone_name="DEF-v_ear.R"),
    copyBone(bone_name="MCH-j_zerc_b_r", src_bone_name="j_zerc_b_r", parent_bone_name="DEF-v_ear.R.001"),

    copyBone(bone_name="MCH-j_zerd_a_l", src_bone_name="j_zerd_a_l", parent_bone_name="DEF-v_ear.L"),
    copyBone(bone_name="MCH-j_zerd_b_l", src_bone_name="j_zerd_b_l", parent_bone_name="DEF-v_ear.L.001"),
    copyBone(bone_name="MCH-j_zerd_a_r", src_bone_name="j_zerd_a_r", parent_bone_name="DEF-v_ear.R"),
    copyBone(bone_name="MCH-j_zerd_b_r", src_bone_name="j_zerd_b_r", parent_bone_name="DEF-v_ear.R.001"),



    # Hands
    copyBone(bone_name="MCH-j_te_l", src_bone_name="j_te_l", parent_bone_name="DEF-hand.L"),
    copyBone(bone_name="MCH-j_te_r", src_bone_name="j_te_r", parent_bone_name="DEF-hand.R"),

    # Legs
    
    copyBone(bone_name="MCH-j_asi_d_l", src_bone_name="j_asi_d_l", parent_bone_name="DEF-foot.L"),
    copyBone(bone_name="MCH-j_asi_e_l", src_bone_name="j_asi_e_l", parent_bone_name="DEF-toe.L"),
    copyBone(bone_name="MCH-j_asi_d_r", src_bone_name="j_asi_d_r", parent_bone_name="DEF-foot.R"),
    copyBone(bone_name="MCH-j_asi_e_r", src_bone_name="j_asi_e_r", parent_bone_name="DEF-toe.R"),
    
    # Tail
    copyBone(bone_name="MCH-n_sippo_a", src_bone_name="n_sippo_a", parent_bone_name="DEF-tail.A"),
    copyBone(bone_name="MCH-n_sippo_b", src_bone_name="n_sippo_b", parent_bone_name="DEF-tail.B"),
    copyBone(bone_name="MCH-n_sippo_c", src_bone_name="n_sippo_c", parent_bone_name="DEF-tail.C"),
    copyBone(bone_name="MCH-n_sippo_d", src_bone_name="n_sippo_d", parent_bone_name="DEF-tail.D"),
    copyBone(bone_name="MCH-n_sippo_e", src_bone_name="n_sippo_e", parent_bone_name="DEF-tail.E"),
    
    # Skirt
    copyBone(bone_name="MCH-j_sk_f_a_l", src_bone_name="j_sk_f_a_l", parent_bone_name="DEF-skirt_front.L"),
    copyBone(bone_name="MCH-j_sk_s_a_l", src_bone_name="j_sk_s_a_l", parent_bone_name="DEF-skirt_out.L"),
    copyBone(bone_name="MCH-j_sk_b_a_l", src_bone_name="j_sk_b_a_l", parent_bone_name="DEF-skirt_back.L"),
    copyBone(bone_name="MCH-j_sk_f_a_r", src_bone_name="j_sk_f_a_r", parent_bone_name="DEF-skirt_front.R"),
    copyBone(bone_name="MCH-j_sk_s_a_r", src_bone_name="j_sk_s_a_r", parent_bone_name="DEF-skirt_out.R"),
    copyBone(bone_name="MCH-j_sk_b_a_r", src_bone_name="j_sk_b_a_r", parent_bone_name="DEF-skirt_back.R"),


    # Eyes 
    connectBone(bone_name="MCH-track_j_f_mabdn_03in_l", bone_a="j_f_mabdn_03in_l", bone_b="lid.B.L.001", parent_bone_name="ORG-eye.L"),
    connectBone(bone_name="MCH-track_j_f_mabdn_01_l", bone_a="j_f_mabdn_01_l", bone_b="lid.B.L.002", parent_bone_name="ORG-eye.L"),
    connectBone(bone_name="MCH-track_j_f_mabdn_02out_l", bone_a="j_f_mabdn_02out_l", bone_b="lid.B.L.003", parent_bone_name="ORG-eye.L"),
    connectBone(bone_name="MCH-track_j_f_mabup_03in_l", bone_a="j_f_mabup_03in_l", bone_b="lid.T.L.003", parent_bone_name="ORG-eye.L"),
    connectBone(bone_name="MCH-track_j_f_mabup_01_l", bone_a="j_f_mabup_01_l", bone_b="lid.T.L.002", parent_bone_name="ORG-eye.L"),
    connectBone(bone_name="MCH-track_j_f_mabup_02out_l", bone_a="j_f_mabup_02out_l", bone_b="lid.T.L.001", parent_bone_name="ORG-eye.L"),
    connectBone(bone_name="MCH-track_j_f_mabdn_03in_r", bone_a="j_f_mabdn_03in_r", bone_b="lid.B.R.001", parent_bone_name="ORG-eye.R"),
    connectBone(bone_name="MCH-track_j_f_mabdn_01_r", bone_a="j_f_mabdn_01_r", bone_b="lid.B.R.002", parent_bone_name="ORG-eye.R"),
    connectBone(bone_name="MCH-track_j_f_mabdn_02out_r", bone_a="j_f_mabdn_02out_r", bone_b="lid.B.R.003", parent_bone_name="ORG-eye.R"),
    connectBone(bone_name="MCH-track_j_f_mabup_03in_r", bone_a="j_f_mabup_03in_r", bone_b="lid.T.R.003", parent_bone_name="ORG-eye.R"),
    connectBone(bone_name="MCH-track_j_f_mabup_01_r", bone_a="j_f_mabup_01_r", bone_b="lid.T.R.002", parent_bone_name="ORG-eye.R"),
    connectBone(bone_name="MCH-track_j_f_mabup_02out_r", bone_a="j_f_mabup_02out_r", bone_b="lid.T.R.001", parent_bone_name="ORG-eye.R"),

    # Mouth
    copyBone(bone_name="MCH-j_f_dlip_01_l", src_bone_name="j_f_dlip_01_l", parent_bone_name="DEF-Lip.B.L"),
    copyBone(bone_name="MCH-j_f_dmlip_01_l", src_bone_name="j_f_dmlip_01_l", parent_bone_name="DEF-Lip.B.L.001"),
    copyBone(bone_name="MCH-j_f_dslip_l", src_bone_name="j_f_dslip_l", parent_bone_name="DEF-Lip.Master.B.L.001"),   

    copyBone(bone_name="MCH-j_f_ulip_01_l", src_bone_name="j_f_ulip_01_l", parent_bone_name="DEF-Lip.T.L"), 
    copyBone(bone_name="MCH-j_f_umlip_01_l", src_bone_name="j_f_umlip_01_l", parent_bone_name="DEF-Lip.T.L.001"),
    copyBone(bone_name="MCH-j_f_uslip_l", src_bone_name="j_f_uslip_l", parent_bone_name="DEF-Lip.Master.T.L.002"),

    copyBone(bone_name="MCH-j_f_dlip_01_r", src_bone_name="j_f_dlip_01_r", parent_bone_name="DEF-Lip.B.R"),
    copyBone(bone_name="MCH-j_f_dmlip_01_r", src_bone_name="j_f_dmlip_01_r", parent_bone_name="DEF-Lip.B.R.001"),
    copyBone(bone_name="MCH-j_f_dslip_r", src_bone_name="j_f_dslip_r", parent_bone_name="DEF-Lip.Master.B.R.001"),

    copyBone(bone_name="MCH-j_f_ulip_01_r", src_bone_name="j_f_ulip_01_r", parent_bone_name="DEF-Lip.T.R"),
    copyBone(bone_name="MCH-j_f_umlip_01_r", src_bone_name="j_f_umlip_01_r", parent_bone_name="DEF-Lip.T.R.001"),
    copyBone(bone_name="MCH-j_f_uslip_r", src_bone_name="j_f_uslip_r", parent_bone_name="DEF-Lip.Master.T.R.002"),

    # Tongue 
    copyBone(bone_name="MCH-j_f_bero_01", src_bone_name="j_f_bero_01", parent_bone_name="DEF-Tongue.002"),
    copyBone(bone_name="MCH-j_f_bero_02", src_bone_name="j_f_bero_02", parent_bone_name="DEF-Tongue.001"),
    copyBone(bone_name="MCH-j_f_bero_03", src_bone_name="j_f_bero_03", parent_bone_name="DEF-Tongue"),
]

LINK_POSE_OPERATIONS: dict[str, list[Constraint]] = {
    "n_root": [CopyTransformsConstraint(target_bone="MCH-n_root", target_space="WORLD", owner_space="WORLD")],

    # Spine 
    "j_kosi": [CopyTransformsConstraint(target_bone="MCH-j_kosi", target_space="WORLD", owner_space="WORLD")],

    "n_hara": [CopyTransformsConstraint(target_bone="MCH-n_hara", target_space="WORLD", owner_space="WORLD")],

    "j_sebo_a": [CopyTransformsConstraint(target_bone="MCH-j_sebo_a", target_space="WORLD", owner_space="WORLD")],
    "j_sebo_b": [CopyTransformsConstraint(target_bone="MCH-j_sebo_b", target_space="WORLD", owner_space="WORLD")],
    "j_sebo_c": [CopyTransformsConstraint(target_bone="MCH-j_sebo_c", target_space="WORLD", owner_space="WORLD")],

    "j_sako_l": [CopyTransformsConstraint(target_bone="MCH-j_sako_l", target_space="WORLD", owner_space="WORLD")],
    "j_sako_r": [CopyTransformsConstraint(target_bone="MCH-j_sako_r", target_space="WORLD", owner_space="WORLD")],

    # Chest
    "j_mune_l": [CopyTransformsConstraint(target_bone="MCH-j_mune_l", target_space="WORLD", owner_space="WORLD")],
    "j_mune_r": [CopyTransformsConstraint(target_bone="MCH-j_mune_r", target_space="WORLD", owner_space="WORLD")],


    # Left Arm
    "j_ude_a_l": [CopyRotationConstraint(target_bone="ORG-upper_arm.L"), CopyLocationConstraint(target_bone="ORG-upper_arm.L")],
    "j_ude_b_l": [CopyRotationConstraint(target_bone="ORG-forearm.L"), CopyLocationConstraint(target_bone="ORG-forearm.L")],
    "j_te_l": [CopyTransformsConstraint(target_bone="MCH-j_te_l", target_space="WORLD", owner_space="WORLD")],

    # Right Arm
    "j_ude_a_r": [CopyRotationConstraint(target_bone="ORG-upper_arm.R"), CopyLocationConstraint(target_bone="ORG-upper_arm.R")],
    "j_ude_b_r": [CopyRotationConstraint(target_bone="ORG-forearm.R"), CopyLocationConstraint(target_bone="ORG-forearm.R")],
    "j_te_r": [CopyTransformsConstraint(target_bone="MCH-j_te_r", target_space="WORLD", owner_space="WORLD")],

    # Twist
    "n_hte_r": [CopyLocationConstraint(target_bone="DEF-wrist.R"), CopyRotationConstraint(target_bone="DEF-hand.R", axis=[True, False, False]), CopyRotationConstraint(target_bone="wrist.R", axis=[True, False, False])],
    "n_hte_l": [CopyLocationConstraint(target_bone="DEF-wrist.L"), CopyRotationConstraint(target_bone="DEF-hand.L", axis=[True, False, False]), CopyRotationConstraint(target_bone="wrist.L", axis=[True, False, False])],
    "n_hhiji_r": [CopyRotationConstraint(target_bone="elbow.R"), CopyLocationConstraint(target_bone="DEF-elbow.R")],
    "n_hhiji_l": [CopyRotationConstraint(target_bone="elbow.L"), CopyLocationConstraint(target_bone="DEF-elbow.L")],
    "n_hkata_l": [CopyRotationConstraint(target_bone="shoulder_tweak.L"), CopyLocationConstraint(target_bone="DEF-shoulder_tweak.L")],
    "n_hkata_r": [CopyRotationConstraint(target_bone="shoulder_tweak.R"), CopyLocationConstraint(target_bone="DEF-shoulder_tweak.R")],

    # Right Fingers
    "j_oya_a_r": [CopyRotationConstraint(target_bone="ORG-f_thumb.R.001")],
    "j_oya_b_r": [CopyRotationConstraint(target_bone="ORG-f_thumb.R.002")],
    "j_hito_a_r": [CopyRotationConstraint(target_bone="ORG-f_pointer.R.001")],
    "j_hito_b_r": [CopyRotationConstraint(target_bone="ORG-f_pointer.R.002")],
    "iv_hito_c_r": [CopyRotationConstraint(target_bone="ORG-f_pointer.R.003")],
    "j_naka_a_r": [CopyRotationConstraint(target_bone="ORG-f_middle.R.001")],
    "j_naka_b_r": [CopyRotationConstraint(target_bone="ORG-f_middle.R.002")],
    "iv_naka_c_r": [CopyRotationConstraint(target_bone="ORG-f_middle.R.003")],
    "j_kusu_a_r": [CopyRotationConstraint(target_bone="ORG-f_ring.R.001")],
    "j_kusu_b_r": [CopyRotationConstraint(target_bone="ORG-f_ring.R.002")],
    "iv_kusu_c_r": [CopyRotationConstraint(target_bone="ORG-f_ring.R.003")],
    "j_ko_a_r": [CopyRotationConstraint(target_bone="ORG-f_pinky.R.001")],
    "j_ko_b_r": [CopyRotationConstraint(target_bone="ORG-f_pinky.R.002")],
    "iv_ko_c_r": [CopyRotationConstraint(target_bone="ORG-f_pinky.R.003")],

    # Left Fingers 
    "j_oya_a_l": [CopyRotationConstraint(target_bone="ORG-f_thumb.L.001")],
    "j_oya_b_l": [CopyRotationConstraint(target_bone="ORG-f_thumb.L.002")],
    "j_hito_a_l": [CopyRotationConstraint(target_bone="ORG-f_pointer.L.001")],
    "j_hito_b_l": [CopyRotationConstraint(target_bone="ORG-f_pointer.L.002")],
    "iv_hito_c_l": [CopyRotationConstraint(target_bone="ORG-f_pointer.L.003")],
    "j_naka_a_l": [CopyRotationConstraint(target_bone="ORG-f_middle.L.001")],
    "j_naka_b_l": [CopyRotationConstraint(target_bone="ORG-f_middle.L.002")],
    "iv_naka_c_l": [CopyRotationConstraint(target_bone="ORG-f_middle.L.003")],
    "j_kusu_a_l": [CopyRotationConstraint(target_bone="ORG-f_ring.L.001")],
    "j_kusu_b_l": [CopyRotationConstraint(target_bone="ORG-f_ring.L.002")],
    "iv_kusu_c_l": [CopyRotationConstraint(target_bone="ORG-f_ring.L.003")],
    "j_ko_a_l": [CopyRotationConstraint(target_bone="ORG-f_pinky.L.001")],
    "j_ko_b_l": [CopyRotationConstraint(target_bone="ORG-f_pinky.L.002")],
    "iv_ko_c_l": [CopyRotationConstraint(target_bone="ORG-f_pinky.L.003")],

    # Left Toes

    "iv_asi_oya_a_l": [CopyRotationConstraint(target_bone="ORG-Hallux.L")],
    "iv_asi_oya_b_l": [CopyRotationConstraint(target_bone="ORG-Hallux.L.001")],
    "iv_asi_hito_a_l": [CopyRotationConstraint(target_bone="ORG-Index.L")],
    "iv_asi_hito_b_l": [CopyRotationConstraint(target_bone="ORG-Index.L.001")],
    "iv_asi_naka_a_l": [CopyRotationConstraint(target_bone="ORG-Middle.L")],
    "iv_asi_naka_b_l": [CopyRotationConstraint(target_bone="ORG-Middle.L.001")],
    "iv_asi_kusu_a_l": [CopyRotationConstraint(target_bone="ORG-Ring.L")],
    "iv_asi_kusu_b_l": [CopyRotationConstraint(target_bone="ORG-Ring.L.001")],
    "iv_asi_ko_a_l": [CopyRotationConstraint(target_bone="ORG-Pinky.L")],
    "iv_asi_ko_b_l": [CopyRotationConstraint(target_bone="ORG-Pinky.L.001")],

    # Right Toes

    "iv_asi_oya_a_r": [CopyRotationConstraint(target_bone="ORG-Hallux.R")],
    "iv_asi_oya_b_r": [CopyRotationConstraint(target_bone="ORG-Hallux.R.001")],
    "iv_asi_hito_a_r": [CopyRotationConstraint(target_bone="ORG-Index.R")],
    "iv_asi_hito_b_r": [CopyRotationConstraint(target_bone="ORG-Index.R.001")],
    "iv_asi_naka_a_r": [CopyRotationConstraint(target_bone="ORG-Middle.R")],
    "iv_asi_naka_b_r": [CopyRotationConstraint(target_bone="ORG-Middle.R.001")],
    "iv_asi_kusu_a_r": [CopyRotationConstraint(target_bone="ORG-Ring.R")],
    "iv_asi_kusu_b_r": [CopyRotationConstraint(target_bone="ORG-Ring.R.001")],
    "iv_asi_ko_a_r": [CopyRotationConstraint(target_bone="ORG-Pinky.R")],
    "iv_asi_ko_b_r": [CopyRotationConstraint(target_bone="ORG-Pinky.R.001")],

    #Brows

    "j_f_mayu_r": [CopyLocationConstraint(target_bone="DEF-brow.T.R"), CopyRotationConstraint(target_bone="brow.T.R")],
    "j_f_mmayu_r":[CopyLocationConstraint(target_bone="DEF-brow.T.R.001"), CopyRotationConstraint(target_bone="brow.T.R.001")],
    "j_f_miken_01_r":[CopyLocationConstraint(target_bone="DEF-brow.T.R.002"), CopyRotationConstraint(target_bone="brow.T.R.002")],
    "j_f_miken_02_r":[CopyLocationConstraint(target_bone="DEF-brow.T.R.003"), CopyRotationConstraint(target_bone="brow.T.R.003")],

    "j_f_mayu_l": [CopyLocationConstraint(target_bone="DEF-brow.T.L"), CopyRotationConstraint(target_bone="brow.T.L")],
    "j_f_mmayu_l": [CopyLocationConstraint(target_bone="DEF-brow.T.L.001"), CopyRotationConstraint(target_bone="brow.T.L.001")],
    "j_f_miken_01_l": [CopyLocationConstraint(target_bone="DEF-brow.T.L.002"), CopyRotationConstraint(target_bone="brow.T.L.002")],
    "j_f_miken_02_l": [CopyLocationConstraint(target_bone="DEF-brow.T.L.003"), CopyRotationConstraint(target_bone="brow.T.L.003")],


    #Eyes 
    "j_f_eyepuru_l": [CopyRotationConstraint(target_bone="MCH-eye.L", influence=0.5)],
    "j_f_mab_l": [CopyRotationConstraint(target_bone="eye_master.L")],
    "j_f_eyepuru_r": [CopyRotationConstraint(target_bone="MCH-eye.R", influence=0.5)],
    "j_f_mab_r": [CopyRotationConstraint(target_bone="eye_master.R")],

    "j_f_mabdn_03in_l": [CopyRotationConstraint(target_bone="MCH-track_j_f_mabdn_03in_l")],
    "j_f_mabdn_01_l": [CopyRotationConstraint(target_bone="MCH-track_j_f_mabdn_01_l")],
    "j_f_mabdn_02out_l": [CopyRotationConstraint(target_bone="MCH-track_j_f_mabdn_02out_l")],
    "j_f_mabup_03in_l": [CopyRotationConstraint(target_bone="MCH-track_j_f_mabup_03in_l")],
    "j_f_mabup_01_l": [CopyRotationConstraint(target_bone="MCH-track_j_f_mabup_01_l")],
    "j_f_mabup_02out_l": [CopyRotationConstraint(target_bone="MCH-track_j_f_mabup_02out_l")],
    "j_f_mabdn_03in_r": [CopyRotationConstraint(target_bone="MCH-track_j_f_mabdn_03in_r")],
    "j_f_mabdn_01_r": [CopyRotationConstraint(target_bone="MCH-track_j_f_mabdn_01_r")],
    "j_f_mabdn_02out_r": [CopyRotationConstraint(target_bone="MCH-track_j_f_mabdn_02out_r")],
    "j_f_mabup_03in_r": [CopyRotationConstraint(target_bone="MCH-track_j_f_mabup_03in_r")],
    "j_f_mabup_01_r": [CopyRotationConstraint(target_bone="MCH-track_j_f_mabup_01_r")],
    "j_f_mabup_02out_r": [CopyRotationConstraint(target_bone="MCH-track_j_f_mabup_02out_r")],



    "MCH-track_j_f_mabdn_03in_l": [TrackToConstraint(target_bone="lid.B.L.001", space_subtarget="ORG-eye.L", target_space="CUSTOM", owner_space="CUSTOM"), AssignCollection(collection_name="MCH")],
    "MCH-track_j_f_mabdn_01_l": [TrackToConstraint(target_bone="lid.B.L.002", space_subtarget="ORG-eye.L", target_space="CUSTOM", owner_space="CUSTOM"), AssignCollection(collection_name="MCH")],
    "MCH-track_j_f_mabdn_02out_l": [TrackToConstraint(target_bone="lid.B.L.003", space_subtarget="ORG-eye.L", target_space="CUSTOM", owner_space="CUSTOM"), AssignCollection(collection_name="MCH")],
    "MCH-track_j_f_mabup_03in_l": [TrackToConstraint(target_bone="lid.T.L.003", space_subtarget="ORG-eye.L", target_space="CUSTOM", owner_space="CUSTOM"), AssignCollection(collection_name="MCH")],
    "MCH-track_j_f_mabup_01_l": [TrackToConstraint(target_bone="lid.T.L.002", space_subtarget="ORG-eye.L", target_space="CUSTOM", owner_space="CUSTOM"), AssignCollection(collection_name="MCH")],
    "MCH-track_j_f_mabup_02out_l": [TrackToConstraint(target_bone="lid.T.L.001", space_subtarget="ORG-eye.L", target_space="CUSTOM", owner_space="CUSTOM"), AssignCollection(collection_name="MCH")],
    "MCH-track_j_f_mabdn_03in_r": [TrackToConstraint(target_bone="lid.B.R.001", space_subtarget="ORG-eye.R", target_space="CUSTOM", owner_space="CUSTOM"), AssignCollection(collection_name="MCH")],
    "MCH-track_j_f_mabdn_01_r": [TrackToConstraint(target_bone="lid.B.R.002", space_subtarget="ORG-eye.R", target_space="CUSTOM", owner_space="CUSTOM"), AssignCollection(collection_name="MCH")],
    "MCH-track_j_f_mabdn_02out_r": [TrackToConstraint(target_bone="lid.B.R.003", space_subtarget="ORG-eye.R", target_space="CUSTOM", owner_space="CUSTOM"), AssignCollection(collection_name="MCH")],
    "MCH-track_j_f_mabup_03in_r": [TrackToConstraint(target_bone="lid.T.R.003", space_subtarget="ORG-eye.R", target_space="CUSTOM", owner_space="CUSTOM"), AssignCollection(collection_name="MCH")],
    "MCH-track_j_f_mabup_01_r": [TrackToConstraint(target_bone="lid.T.R.002", space_subtarget="ORG-eye.R", target_space="CUSTOM", owner_space="CUSTOM"), AssignCollection(collection_name="MCH")],
    "MCH-track_j_f_mabup_02out_r": [TrackToConstraint(target_bone="lid.T.R.001", space_subtarget="ORG-eye.R", target_space="CUSTOM", owner_space="CUSTOM"), AssignCollection(collection_name="MCH")],


    # Left Mouth

    "j_f_ulip_01_l": [CopyLocationConstraint(target_bone="MCH-j_f_ulip_01_l"), CopyRotationConstraint(target_bone="MCH-j_f_ulip_01_l", mix_mode="REPLACE", owner_space="WORLD", target_space="WORLD")],
    "j_f_umlip_01_l": [CopyLocationConstraint(target_bone="MCH-j_f_umlip_01_l"), CopyRotationConstraint(target_bone="MCH-j_f_umlip_01_l", mix_mode="REPLACE", owner_space="WORLD", target_space="WORLD")],
    "j_f_uslip_l": [CopyLocationConstraint(target_bone="MCH-j_f_uslip_l"), CopyRotationConstraint(target_bone="MCH-j_f_uslip_l", mix_mode="REPLACE", owner_space="WORLD", target_space="WORLD"), CopyRotationConstraint(target_bone="Lip.Master.T.L.002"), CopyScaleConstraint(target_bone="Lip.Master.T.L.002")],
    "j_f_ulip_02_l":[CopyRotationConstraint(target_bone="Lip.T.L"), CopyScaleConstraint(target_bone="Lip.T.L")],
    "j_f_umlip_02_l":[CopyRotationConstraint(target_bone="Lip.T.L.001"), CopyScaleConstraint(target_bone="Lip.T.L.001")],



    "j_f_dlip_01_l": [CopyLocationConstraint(target_bone="MCH-j_f_dlip_01_l"), CopyRotationConstraint(target_bone="MCH-j_f_dlip_01_l", mix_mode="REPLACE", owner_space="WORLD", target_space="WORLD")],
    "j_f_dmlip_01_l": [CopyLocationConstraint(target_bone="MCH-j_f_dmlip_01_l"), CopyRotationConstraint(target_bone="MCH-j_f_dmlip_01_l", mix_mode="REPLACE", owner_space="WORLD", target_space="WORLD")],
    "j_f_dslip_l": [CopyLocationConstraint(target_bone="MCH-j_f_dslip_l"), CopyRotationConstraint(target_bone="MCH-j_f_dslip_l", mix_mode="REPLACE", owner_space="WORLD", target_space="WORLD"),CopyRotationConstraint(target_bone="Lip.Master.B.L.001"), CopyScaleConstraint(target_bone="Lip.Master.B.L.001")],
    "j_f_dlip_02_l":[CopyRotationConstraint(target_bone="Lip.B.L"), CopyScaleConstraint(target_bone="Lip.B.L")],
    "j_f_dmlip_02_l":[CopyRotationConstraint(target_bone="Lip.B.L.001"), CopyScaleConstraint(target_bone="Lip.B.L.001")],

    # Right Mouth

    "j_f_ulip_01_r": [CopyLocationConstraint(target_bone="MCH-j_f_ulip_01_r"), CopyRotationConstraint(target_bone="MCH-j_f_ulip_01_r", mix_mode="REPLACE", owner_space="WORLD", target_space="WORLD")],
    "j_f_umlip_01_r": [CopyLocationConstraint(target_bone="MCH-j_f_umlip_01_r"), CopyRotationConstraint(target_bone="MCH-j_f_umlip_01_r", mix_mode="REPLACE", owner_space="WORLD", target_space="WORLD")],
    "j_f_uslip_r": [CopyLocationConstraint(target_bone="MCH-j_f_uslip_r"), CopyRotationConstraint(target_bone="MCH-j_f_uslip_r", mix_mode="REPLACE", owner_space="WORLD", target_space="WORLD"), CopyRotationConstraint(target_bone="Lip.Master.T.R.002"), CopyScaleConstraint(target_bone="Lip.Master.T.R.002")],
    "j_f_ulip_02_r":[CopyRotationConstraint(target_bone="Lip.T.R"), CopyScaleConstraint(target_bone="Lip.T.R")],
    "j_f_umlip_02_r":[CopyRotationConstraint(target_bone="Lip.T.R.001"), CopyScaleConstraint(target_bone="Lip.T.R.001")],

    "j_f_dlip_01_r": [CopyLocationConstraint(target_bone="MCH-j_f_dlip_01_r"), CopyRotationConstraint(target_bone="MCH-j_f_dlip_01_r", mix_mode="REPLACE", owner_space="WORLD", target_space="WORLD")],
    "j_f_dmlip_01_r": [CopyLocationConstraint(target_bone="MCH-j_f_dmlip_01_r"), CopyRotationConstraint(target_bone="MCH-j_f_dmlip_01_r", mix_mode="REPLACE", owner_space="WORLD", target_space="WORLD")],
    "j_f_dslip_r": [CopyLocationConstraint(target_bone="MCH-j_f_dslip_r"), CopyRotationConstraint(target_bone="MCH-j_f_dslip_r", mix_mode="REPLACE", owner_space="WORLD", target_space="WORLD"), CopyRotationConstraint(target_bone="Lip.Master.B.R.001"), CopyScaleConstraint(target_bone="Lip.Master.B.R.001")],
    "j_f_dlip_02_r":[CopyRotationConstraint(target_bone="Lip.B.R"), CopyScaleConstraint(target_bone="Lip.B.R")],
    "j_f_dmlip_02_r":[CopyRotationConstraint(target_bone="Lip.B.R.001"), CopyScaleConstraint(target_bone="Lip.B.R.001")],

    # Tongue

    "j_f_bero_03": [CopyTransformsConstraint(target_bone="MCH-j_f_bero_03", target_space="WORLD", owner_space="WORLD")],
    "j_f_bero_02": [CopyTransformsConstraint(target_bone="MCH-j_f_bero_02", target_space="WORLD", owner_space="WORLD")],
    "j_f_bero_01": [CopyTransformsConstraint(target_bone="MCH-j_f_bero_01", target_space="WORLD", owner_space="WORLD")],
    
    # Jaw
    "j_f_ago": [CopyTransformsConstraint(target_bone="MCH-j_f_ago", target_space="WORLD", owner_space="WORLD")],
    "j_f_hagukiup": [CopyLocationConstraint(target_bone="ORG-Teeth.T"), CopyRotationConstraint(target_bone="ORG-Teeth.T")],
    "j_f_hagukidn": [CopyLocationConstraint(target_bone="ORG-Teeth.B"), CopyRotationConstraint(target_bone="ORG-Teeth.B")],

    #Head
    "j_kubi": [CopyTransformsConstraint(target_bone="MCH-j_kubi", target_space="WORLD", owner_space="WORLD")],
    "j_kao": [CopyTransformsConstraint(target_bone="MCH-j_kao", target_space="WORLD", owner_space="WORLD")],

    "j_mimi_l": [CopyTransformsConstraint(target_bone="MCH-j_mimi_l", target_space="WORLD", owner_space="WORLD")],
    "j_mimi_r": [CopyTransformsConstraint(target_bone="MCH-j_mimi_r", target_space="WORLD", owner_space="WORLD")],
    "j_zerd_a_l": [CopyTransformsConstraint(target_bone="MCH-j_zerd_a_l", target_space="WORLD", owner_space="WORLD")],
    "j_zerd_b_l": [CopyTransformsConstraint(target_bone="MCH-j_zerd_b_l", target_space="WORLD", owner_space="WORLD")],
    "j_zerd_a_r": [CopyTransformsConstraint(target_bone="MCH-j_zerd_a_r", target_space="WORLD", owner_space="WORLD")],
    "j_zerd_b_r": [CopyTransformsConstraint(target_bone="MCH-j_zerd_b_r", target_space="WORLD", owner_space="WORLD")],
    "j_zerc_a_l": [CopyTransformsConstraint(target_bone="MCH-j_zerc_a_l", target_space="WORLD", owner_space="WORLD")],
    "j_zerc_b_l": [CopyTransformsConstraint(target_bone="MCH-j_zerc_b_l", target_space="WORLD", owner_space="WORLD")],
    "j_zerc_a_r": [CopyTransformsConstraint(target_bone="MCH-j_zerc_a_r", target_space="WORLD", owner_space="WORLD")],
    "j_zerc_b_r": [CopyTransformsConstraint(target_bone="MCH-j_zerc_b_r", target_space="WORLD", owner_space="WORLD")],
    "j_zera_a_l": [CopyTransformsConstraint(target_bone="MCH-j_zera_a_l", target_space="WORLD", owner_space="WORLD")],
    "j_zera_b_l": [CopyTransformsConstraint(target_bone="MCH-j_zera_b_l", target_space="WORLD", owner_space="WORLD")],
    "j_zera_a_r": [CopyTransformsConstraint(target_bone="MCH-j_zera_a_r", target_space="WORLD", owner_space="WORLD")],
    "j_zera_b_r": [CopyTransformsConstraint(target_bone="MCH-j_zera_b_r", target_space="WORLD", owner_space="WORLD")],

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
    "j_asi_a_l": [CopyRotationConstraint(target_bone="ORG-thigh.L"), CopyLocationConstraint(target_bone="ORG-thigh.L")],
    "j_asi_c_l": [CopyRotationConstraint(target_bone="ORG-shin.L"), CopyLocationConstraint(target_bone="ORG-shin.L")],
    "j_asi_d_l": [CopyTransformsConstraint(target_bone="MCH-j_asi_d_l", target_space="WORLD", owner_space="WORLD")],
    "j_asi_e_l": [CopyTransformsConstraint(target_bone="MCH-j_asi_e_l", target_space="WORLD", owner_space="WORLD")],

    # Right Leg
    "j_asi_a_r": [CopyRotationConstraint(target_bone="ORG-thigh.R"), CopyLocationConstraint(target_bone="ORG-thigh.R")],
    "j_asi_c_r": [CopyRotationConstraint(target_bone="ORG-shin.R"), CopyLocationConstraint(target_bone="ORG-shin.R")],
    "j_asi_d_r": [CopyTransformsConstraint(target_bone="MCH-j_asi_d_r", target_space="WORLD", owner_space="WORLD")],
    "j_asi_e_r": [CopyTransformsConstraint(target_bone="MCH-j_asi_e_r", target_space="WORLD", owner_space="WORLD")],

    # Tail
    "n_sippo_a": [CopyTransformsConstraint(target_bone="MCH-n_sippo_a", target_space="WORLD", owner_space="WORLD")],
    "n_sippo_b": [CopyTransformsConstraint(target_bone="MCH-n_sippo_b", target_space="WORLD", owner_space="WORLD")],
    "n_sippo_c": [CopyTransformsConstraint(target_bone="MCH-n_sippo_c", target_space="WORLD", owner_space="WORLD")],
    "n_sippo_d": [CopyTransformsConstraint(target_bone="MCH-n_sippo_d", target_space="WORLD", owner_space="WORLD")],
    "n_sippo_e": [CopyTransformsConstraint(target_bone="MCH-n_sippo_e", target_space="WORLD", owner_space="WORLD")],

    # Skirt

    "j_sk_f_a_l": [CopyTransformsConstraint(target_bone="MCH-j_sk_f_a_l", target_space="WORLD", owner_space="WORLD")],
    "j_sk_f_b_l": [CopyRotationConstraint(target_bone="DEF-skirt_front.L.001")],
    "j_sk_f_c_l": [CopyRotationConstraint(target_bone="DEF-skirt_front.L.002")],

    "j_sk_s_a_l": [CopyTransformsConstraint(target_bone="MCH-j_sk_s_a_l", target_space="WORLD", owner_space="WORLD")],
    "j_sk_s_b_l": [CopyRotationConstraint(target_bone="DEF-skirt_out.L.001")],
    "j_sk_s_c_l": [CopyRotationConstraint(target_bone="DEF-skirt_out.L.002")],

    "j_sk_b_a_l": [CopyTransformsConstraint(target_bone="MCH-j_sk_b_a_l", target_space="WORLD", owner_space="WORLD")],
    "j_sk_b_b_l": [CopyRotationConstraint(target_bone="DEF-skirt_back.L.001")],
    "j_sk_b_c_l": [CopyRotationConstraint(target_bone="DEF-skirt_back.L.002")],

    "j_sk_f_a_r": [CopyTransformsConstraint(target_bone="MCH-j_sk_f_a_r", target_space="WORLD", owner_space="WORLD")],
    "j_sk_f_b_r": [CopyRotationConstraint(target_bone="DEF-skirt_front.R.001")],
    "j_sk_f_c_r": [CopyRotationConstraint(target_bone="DEF-skirt_front.R.002")],

    "j_sk_s_a_r": [CopyTransformsConstraint(target_bone="MCH-j_sk_s_a_r", target_space="WORLD", owner_space="WORLD")],
    "j_sk_s_b_r": [CopyRotationConstraint(target_bone="DEF-skirt_out.R.001")],
    "j_sk_s_c_r": [CopyRotationConstraint(target_bone="DEF-skirt_out.R.002")],

    "j_sk_b_a_r": [CopyTransformsConstraint(target_bone="MCH-j_sk_b_a_r", target_space="WORLD", owner_space="WORLD")],
    "j_sk_b_b_r": [CopyRotationConstraint(target_bone="DEF-skirt_back.R.001")],
    "j_sk_b_c_r": [CopyRotationConstraint(target_bone="DEF-skirt_back.R.002")],

    # Genitals

    "iv_ochinko_f": [CopyRotationConstraint(target_bone="DEF-shaft"), CopyLocationConstraint(target_bone="DEF-shaft")],
    "iv_ochinko_e": [CopyRotationConstraint(target_bone="DEF-shaft.001"), CopyLocationConstraint(target_bone="DEF-shaft.001")],
    "iv_ochinko_d": [CopyRotationConstraint(target_bone="DEF-shaft.002"), CopyLocationConstraint(target_bone="DEF-shaft.002")],
    "iv_ochinko_c": [CopyRotationConstraint(target_bone="DEF-shaft.003"), CopyLocationConstraint(target_bone="DEF-shaft.003")],
    "iv_ochinko_b": [CopyRotationConstraint(target_bone="DEF-shaft.004"), CopyLocationConstraint(target_bone="DEF-shaft.004")],

    "iv_kougan_l": [CopyRotationConstraint(target_bone="ORG-testicle.L")],
    "iv_kougan_r": [CopyRotationConstraint(target_bone="ORG-testicle.R")],

    "iv_kuritto": [CopyLocationConstraint(target_bone="clitoris.control"), CopyRotationConstraint(target_bone="clitoris.control")],
    "iv_inshin_l": [CopyRotationConstraint(target_bone="labia.L"), CopyLocationConstraint(target_bone="DEF-labia.L")],
    "iv_inshin_r": [CopyRotationConstraint(target_bone="labia.R"), CopyLocationConstraint(target_bone="DEF-labia.R")],
    "iv_koumon": [CopyLocationConstraint(target_bone="fourchette.control")],

    # Rigify Bones 
    ## Arms
    "forearm_tweak.L.001": [AssignCollection()],
    "forearm_tweak.R.001": [AssignCollection()],
    "forearm_tweak.L": [AssignCollection()],
    "forearm_tweak.R": [AssignCollection()],
    "upper_arm_tweak.L.001": [AssignCollection()],
    "upper_arm_tweak.R.001": [AssignCollection()],
    "upper_arm_tweak.L": [AssignCollection()],
    "upper_arm_tweak.R": [AssignCollection()],
    "upper_arm_parent.L": [AssignCollection()],
    "upper_arm_parent.R": [AssignCollection()],

    "hand_tweak.R": [AssignCollection()],
    "hand_tweak.L": [AssignCollection()],

    ## Legs
    "foot_tweak.L": [AssignCollection()],
    "foot_tweak.R": [AssignCollection()],
    "shin_tweak.L.001": [AssignCollection()],
    "shin_tweak.R.001": [AssignCollection()],
    "shin_tweak.L": [AssignCollection()],
    "shin_tweak.R": [AssignCollection()],
    "thigh_tweak.L.001": [AssignCollection()],
    "thigh_tweak.R.001": [AssignCollection()],
    "thigh_tweak.L": [AssignCollection()],
    "thigh_tweak.R": [AssignCollection()],
    "thigh_parent.L": [AssignCollection()],
    "thigh_parent.R": [AssignCollection()],

    ## Skirt
    "skirt_support.B.L.002": [AssignCollection()],
    "skirt_support.B.R.002": [AssignCollection()],
    "skirt_out.L": [AssignCollection()],
    "skirt_out.R": [AssignCollection()],
    "skirt_front.L": [AssignCollection()],
    "skirt_front.R": [AssignCollection()],
    "skirt_back.L": [AssignCollection()],
    "skirt_back.R": [AssignCollection()],

    ## Spine
    "tweak_spine.004": [AssignCollection()],
    "spine_fk.01": [AssignCollection()],
    "tweak_spine.03": [AssignCollection()],
    "tweak_spine.02": [AssignCollection()],
    "tweak_spine.01": [AssignCollection()],
    "tweak_neck": [AssignCollection()],

    ## Tail
    "tweak_base_tail.A": [AssignCollection()],
    "tweak_tail.A": [AssignCollection()],
    "tweak_tail.B": [AssignCollection()],
    "tweak_tail.C": [AssignCollection()],
    "tweak_tail.D": [AssignCollection()],

    ## Face
    "Lip.Master.T.L.002": [CopyRotationConstraint(target_bone="Lip.Master_end.B.L.001"), CopyScaleConstraint(target_bone="Lip.Master_end.B.L.001", offset=True, additive=True, uniform_scale=True)],
    "Lip.Master.B.L.001": [CopyRotationConstraint(target_bone="Lip.Master_end.B.L.001"), CopyScaleConstraint(target_bone="Lip.Master_end.B.L.001", offset=True, additive=True, uniform_scale=True)],
    "Lip.Master.T.R.002": [CopyRotationConstraint(target_bone="Lip.Master_end.B.R.001"), CopyScaleConstraint(target_bone="Lip.Master_end.B.R.001", offset=True, additive=True, uniform_scale=True)],
    "Lip.Master.B.R.001": [CopyRotationConstraint(target_bone="Lip.Master_end.B.R.001"), CopyScaleConstraint(target_bone="Lip.Master_end.B.R.001", offset=True, additive=True, uniform_scale=True)],
    "Lip.T.R": [CopyRotationConstraint(target_bone="Lip.Master.T"), CopyScaleConstraint(target_bone="Lip.Master.T", offset=True, additive=True, uniform_scale=True)],
    "Lip.T.L": [CopyRotationConstraint(target_bone="Lip.Master.T"), CopyScaleConstraint(target_bone="Lip.Master.T", offset=True, additive=True, uniform_scale=True)],
    "Lip.B.L": [CopyRotationConstraint(target_bone="Lip.Master.B"), CopyScaleConstraint(target_bone="Lip.Master.B", offset=True, additive=True, uniform_scale=True)],
    "Lip.B.R": [CopyRotationConstraint(target_bone="Lip.Master.B"), CopyScaleConstraint(target_bone="Lip.Master.B", offset=True, additive=True, uniform_scale=True)],

    "eye_master.L": [AssignCollection()],
    "eye_master.R": [AssignCollection()],

    "jaw_mouth": [AssignCollection()],

    "lid.T.L.002": [CopyLocationConstraint(target_bone="lid.B.L.002", name="eye_lid_close.L", influence=0)],
    "lid.T.R.002": [CopyLocationConstraint(target_bone="lid.B.R.002", name="eye_lid_close.R", influence=0)],

    "v_ear.L": [AssignCollection()],
    "v_ear.R": [AssignCollection()],

    ## MCH Bones 

    "MCH-n_root": [AssignCollection(collection_name="MCH")],
    # Spine
    "MCH-j_kosi": [AssignCollection(collection_name="MCH")],
    "MCH-j_sebo_a": [AssignCollection(collection_name="MCH")],
    "MCH-j_sebo_b": [AssignCollection(collection_name="MCH")],
    "MCH-j_sebo_c": [AssignCollection(collection_name="MCH")],
    "MCH-j_sako_l": [AssignCollection(collection_name="MCH")],
    "MCH-j_sako_r": [AssignCollection(collection_name="MCH")],
    "MCH-n_hara": [AssignCollection(collection_name="MCH")],
    
    # Chest
    "MCH-j_mune_l": [AssignCollection(collection_name="MCH")],
    "MCH-j_mune_r": [AssignCollection(collection_name="MCH")],
    
    # Twist
    "MCH-n_hhiji_r": [AssignCollection(collection_name="MCH")],
    "MCH-n_hhiji_l": [AssignCollection(collection_name="MCH")],

    "MCH-j_zera_a_l": [AssignCollection(collection_name="MCH")],
    "MCH-j_zera_b_l": [AssignCollection(collection_name="MCH")],
    "MCH-j_zerc_a_l": [AssignCollection(collection_name="MCH")],
    "MCH-j_zerc_b_l": [AssignCollection(collection_name="MCH")],
    "MCH-j_zerd_a_l": [AssignCollection(collection_name="MCH")],
    "MCH-j_zerd_b_l": [AssignCollection(collection_name="MCH")],

    "MCH-j_zera_a_r": [AssignCollection(collection_name="MCH")],
    "MCH-j_zera_b_r": [AssignCollection(collection_name="MCH")],
    "MCH-j_zerc_a_r": [AssignCollection(collection_name="MCH")],
    "MCH-j_zerc_b_r": [AssignCollection(collection_name="MCH")],
    "MCH-j_zerd_a_r": [AssignCollection(collection_name="MCH")],
    "MCH-j_zerd_b_r": [AssignCollection(collection_name="MCH")],
    
    # Head
    "MCH-j_kubi": [AssignCollection(collection_name="MCH")],
    "MCH-j_kao": [AssignCollection(collection_name="MCH")],
    "MCH-j_mimi_l": [AssignCollection(collection_name="MCH")],
    "MCH-j_mimi_r": [AssignCollection(collection_name="MCH")],
    "MCH-j_f_ago": [AssignCollection(collection_name="MCH")],

    # Tongue 

    "tweak_Tongue": [AssignCollection(collection_name="Face (Secondary)")],
    "MCH-j_f_bero_01": [AssignCollection(collection_name="MCH")],
    "MCH-j_f_bero_02": [AssignCollection(collection_name="MCH")],
    "MCH-j_f_bero_03": [AssignCollection(collection_name="MCH")],

    # Mouth
    "MCH-j_f_dlip_01_l": [AssignCollection(collection_name="MCH")],
    "MCH-j_f_dmlip_01_l": [AssignCollection(collection_name="MCH")],
    "MCH-j_f_dslip_l": [AssignCollection(collection_name="MCH")],

    "MCH-j_f_dlip_01_r": [AssignCollection(collection_name="MCH")],
    "MCH-j_f_dmlip_01_r": [AssignCollection(collection_name="MCH")],
    "MCH-j_f_dslip_r": [AssignCollection(collection_name="MCH")],

    "MCH-j_f_ulip_01_l": [AssignCollection(collection_name="MCH")],
    "MCH-j_f_umlip_01_l": [AssignCollection(collection_name="MCH")],
    "MCH-j_f_uslip_l": [AssignCollection(collection_name="MCH")],

    "MCH-j_f_ulip_01_r": [AssignCollection(collection_name="MCH")],
    "MCH-j_f_umlip_01_r": [AssignCollection(collection_name="MCH")],
    "MCH-j_f_uslip_r": [AssignCollection(collection_name="MCH")],

    # Arms
    "MCH-j_te_l": [AssignCollection(collection_name="MCH")],
    "MCH-j_te_r": [AssignCollection(collection_name="MCH")],

    # Legs
    "MCH-j_asi_d_l": [AssignCollection(collection_name="MCH")],
    "MCH-j_asi_e_l": [AssignCollection(collection_name="MCH")],
    "MCH-j_asi_d_r": [AssignCollection(collection_name="MCH")],
    "MCH-j_asi_e_r": [AssignCollection(collection_name="MCH")],
    
    # Tail
    "MCH-n_sippo_a": [AssignCollection(collection_name="MCH")],
    "MCH-n_sippo_b": [AssignCollection(collection_name="MCH")],
    "MCH-n_sippo_c": [AssignCollection(collection_name="MCH")],
    "MCH-n_sippo_d": [AssignCollection(collection_name="MCH")],
    "MCH-n_sippo_e": [AssignCollection(collection_name="MCH")],
    
    # Skirt
    "MCH-j_sk_f_a_l": [AssignCollection(collection_name="MCH")],
    "MCH-j_sk_s_a_l": [AssignCollection(collection_name="MCH")],
    "MCH-j_sk_b_a_l": [AssignCollection(collection_name="MCH")],
    "MCH-j_sk_f_a_r": [AssignCollection(collection_name="MCH")],
    "MCH-j_sk_s_a_r": [AssignCollection(collection_name="MCH")],
    "MCH-j_sk_b_a_r": [AssignCollection(collection_name="MCH")],

}

REGEX_CONSTRAINTS: dict[str, list[Constraint]] = {
    "^DEF-HAIR_(.+)$": [OffsetTransformConstraint(name="AetherBlend_OffsetTransform_Hair")],
    "^DEF-ACCESSORY_(.+)$": [OffsetTransformConstraint(name="AetherBlend_OffsetTransform_Accessory")],
}