from . schemas import TrackToBone

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
        # Eyes
        "j_f_eye_l": ["MCH-eye.L"],
        "j_f_mab_l": ["eye_master.L"],
        "j_f_eye_r": ["MCH-eye.R"],
        "j_f_mab_r": ["eye_master.R"],

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
        "n_sippo_a": ["ORG-tail.A"],
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
    "j_kosi": ["j_sebo_a"]
    }