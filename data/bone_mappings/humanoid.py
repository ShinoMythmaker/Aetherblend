import mathutils

from .. schemas import GenerativeBone, ConnectBone, ExtensionBone, RigifySettings, CenterBone, SkinBone, BridgeBone


LEG_L: list[GenerativeBone] = [
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="thigh.L", bone_a="j_asi_a_l", bone_b="j_asi_c_l", parent="hips"),
        req_bones=["j_asi_a_l", "j_asi_c_l"],
        settings=RigifySettings(bone_name="thigh.L", rigify_type="limbs.leg", fk_coll="Leg.L (FK)", tweak_coll="Leg.L (Tweak)"),
        b_collection="Leg.L (IK)"
    ),
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="shin.L", bone_a="j_asi_c_l", bone_b="j_asi_d_l", parent="thigh.L", is_connected=True),
        req_bones=["j_asi_c_l", "j_asi_d_l"],
        b_collection="Leg.L (IK)",
    ),
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="foot.L", bone_a="j_asi_d_l", bone_b="j_asi_e_l", parent="shin.L", is_connected=True),
        req_bones=["j_asi_d_l", "j_asi_e_l"],
        b_collection="Leg.L (IK)",
    ),
    GenerativeBone(
        ref="tgt",
        data=ExtensionBone(name="toe.L", bone_a="foot.L", parent="foot.L", size_factor=(-0.5), axis_type="armature", is_connected=True),
        req_bones=["foot.L"],
        b_collection="Leg.L (IK)",
    ),
    GenerativeBone(
        ref="tgt",
        data=ExtensionBone(name="heel.L", bone_a="foot.L", parent="foot.L", size_factor=(0.9), axis_type="armature", is_connected=False),
        req_bones=["foot.L"],
        b_collection="Leg.L (IK)",
    ),
]

LEG_R: list[GenerativeBone] = [
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="thigh.R", bone_a="j_asi_a_r", bone_b="j_asi_c_r", parent="hips"),
        req_bones=["j_asi_a_r", "j_asi_c_r"],
        settings=RigifySettings(bone_name="thigh.R", rigify_type="limbs.leg", fk_coll="Leg.R (FK)", tweak_coll="Leg.R (Tweak)"),
        b_collection="Leg.R (IK)"
    ),
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="shin.R", bone_a="j_asi_c_r", bone_b="j_asi_d_r", parent="thigh.R", is_connected=True),
        req_bones=["j_asi_c_r", "j_asi_d_r"],
        b_collection="Leg.R (IK)",
    ),
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="foot.R", bone_a="j_asi_d_r", bone_b="j_asi_e_r", parent="shin.R", is_connected=True),
        req_bones=["j_asi_d_r", "j_asi_e_r"],
        b_collection="Leg.R (IK)",
    ),
    GenerativeBone(
        ref="tgt",
        data=ExtensionBone(name="toe.R", bone_a="foot.R", parent="foot.R", size_factor=(-0.5), axis_type="armature", is_connected=True),
        req_bones=["foot.R"],
        b_collection="Leg.R (IK)",
    ),
    GenerativeBone(
        ref="tgt",
        data=ExtensionBone(name="heel.R", bone_a="foot.R", parent="foot.R", size_factor=(0.9), axis_type="armature", is_connected=False),
        req_bones=["foot.R"],
        b_collection="Leg.R (IK)",
    ),
]

SPINE: list[GenerativeBone] = [
    #Spine bones
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="spine.01", bone_a="j_sebo_a", bone_b="j_sebo_b"),
        req_bones=["j_sebo_a", "j_sebo_b"],
        settings=RigifySettings(bone_name="spine.01", rigify_type="spines.basic_spine", fk_coll="Torso (Tweak)", tweak_coll="Torso (Tweak)", pivot_pos=1),
        b_collection="Torso"
    ),
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="spine.02", bone_a="j_sebo_b", bone_b="j_sebo_c", parent="spine.01", is_connected=True),
        req_bones=["j_sebo_b", "j_sebo_c"],
        b_collection="Torso",
    ),
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="spine.03", bone_a="j_sebo_c", bone_b="j_kubi", parent="spine.02", is_connected=True),
        req_bones=["j_sebo_c", "j_kubi"],
        b_collection="Torso",
    ),

    #Hips
    GenerativeBone(
        ref="tgt",
        data=ExtensionBone(name="hips", bone_a="spine.01", size_factor= (-1.2), start="head", parent="spine.01"),
        req_bones=["spine.01"],
        settings=RigifySettings(bone_name="hips", rigify_type="basic.super_copy", super_copy_widget_type="palm"),
        b_collection="Torso",
    ),

    #Shoulder Bones
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="shoulder.L", bone_a="j_sako_l", bone_b="j_ude_a_l", parent="spine.03"),
        req_bones=["j_sako_l", "j_ude_a_l"],
        settings=RigifySettings(bone_name="shoulder.L", rigify_type="basic.super_copy", super_copy_widget_type="shoulder"),
        b_collection="Torso",
    ),
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="shoulder.R", bone_a="j_sako_r", bone_b="j_ude_a_r", parent="spine.03"),
        req_bones=["j_sako_r", "j_ude_a_r"],
        settings=RigifySettings(bone_name="shoulder.R", rigify_type="basic.super_copy", super_copy_widget_type="shoulder"),
        b_collection="Torso",
    ),

]

CHEST: list[GenerativeBone] = [
    GenerativeBone(
        ref="src",
        data=ExtensionBone(name="Chest.L", bone_a="j_mune_l", axis_type="local", axis="X", start="head", parent="spine.03", is_connected=False, roll=47),
        req_bones=["j_mune_l"],
        b_collection="Torso",
        settings=RigifySettings(bone_name="Chest.L", rigify_type="basic.super_copy", super_copy_widget_type="circle"),
    ),

    GenerativeBone(
        ref="src",
        data=ExtensionBone(name="Chest.R", bone_a="j_mune_r", axis_type="local", axis="X", start="head", parent="spine.03", is_connected=False, roll=43),
        req_bones=["j_mune_r"],
        b_collection="Torso",
        settings=RigifySettings(bone_name="Chest.R", rigify_type="basic.super_copy", super_copy_widget_type="circle"),
    )
]

ARM_L:list[GenerativeBone] = [
    # Left Arm
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="upper_arm.L", bone_a="j_ude_a_l", bone_b="j_ude_b_l", parent="shoulder.L"),
        req_bones=["j_ude_a_l", "j_ude_b_l"],
        settings=RigifySettings(bone_name="upper_arm.L", rigify_type="limbs.arm", fk_coll="Arm.L (FK)", tweak_coll="Arm.L (Tweak)"),
        b_collection="Arm.L (IK)"
        ),
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="forearm.L", bone_a="j_ude_b_l", bone_b="j_te_l", parent="upper_arm.L", is_connected=True),
        req_bones=["j_ude_b_l", "j_te_l"],
        b_collection="Arm.L (IK)"
        ),
    GenerativeBone(
        ref="tgt",
        data=ExtensionBone(name="hand.L", bone_a="forearm.L", size_factor=0.6, axis_type="local", axis="Y", is_connected=True, parent="forearm.L"),
        req_bones=["forearm.L"],
        b_collection="Arm.L (IK)"
    ),
]

ARM_R:list[GenerativeBone] = [
    # Right Arm
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="upper_arm.R", bone_a="j_ude_a_r", bone_b="j_ude_b_r", parent="shoulder.R"),
        req_bones=["j_ude_a_r", "j_ude_b_r"],
        settings=RigifySettings(bone_name="upper_arm.R", rigify_type="limbs.arm", fk_coll="Arm.R (FK)", tweak_coll="Arm.R (Tweak)"),
        b_collection="Arm.R (IK)"
        ),
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="forearm.R", bone_a="j_ude_b_r", bone_b="j_te_r", parent="upper_arm.R", is_connected=True),
        req_bones=["j_ude_b_r", "j_te_r"],
        b_collection="Arm.R (IK)"
        ),
    GenerativeBone(
        ref="tgt",
        data=ExtensionBone(name="hand.R", bone_a="forearm.R", size_factor=0.6, axis_type="local", axis="Y", is_connected=True, parent="forearm.R"),
        req_bones=["forearm.R"],
        b_collection="Arm.R (IK)"
    ),
] 

TAIL: list[GenerativeBone] = [
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="tail.A", bone_a="n_sippo_a", bone_b="n_sippo_b", parent="hips"),
        req_bones=["n_sippo_a", "n_sippo_b"],
        settings=RigifySettings(bone_name="tail.A", rigify_type="spines.basic_tail", copy_rot_axes={"use_x": True, "use_y": True, "use_z": True}, tweak_coll="Tail (Tweak)"),
        b_collection="Tail"
    ),
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="tail.B", bone_a="n_sippo_b", bone_b="n_sippo_c", parent="tail.A", is_connected=True),
        req_bones=["n_sippo_b", "n_sippo_c"],
        b_collection="Tail"
    ),
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="tail.C", bone_a="n_sippo_c", bone_b="n_sippo_d", parent="tail.B", is_connected=True),
        req_bones=["n_sippo_c", "n_sippo_d"],   
        b_collection="Tail" 
    ),
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="tail.D", bone_a="n_sippo_d", bone_b="n_sippo_e", parent="tail.C", is_connected=True),
        req_bones=["n_sippo_d", "n_sippo_e"],
        b_collection="Tail",
    ),
]

EYE_L: list[GenerativeBone] = [
    GenerativeBone(
        ref="src",
        data=SkinBone(name="lid.T.L", bone_a="j_f_mabup_02out_l", mesh_restriction="eye_occlusion"),
        req_bones=["j_f_mabup_02out_l"],
        b_collection="Face (Secondary)",
        settings=RigifySettings(bone_name="lid.T.L", rigify_type="skin.stretchy_chain", skin_chain_pivot_pos=2,secondary_layer_extra="Face (Primary)" ,skin_control_orientation_bone="head", skin_chain_falloff_spherical=[False, True, False], skin_chain_falloff=[0.0, -2.0, 0.0], skin_chain_falloff_length=True)
    ),
    GenerativeBone(
        ref="src",
        data=SkinBone(name="lid.T.L.002", bone_a="j_f_mabup_01_l", mesh_restriction="eye_occlusion"),
        req_bones=["j_f_mabup_01_l"],
        b_collection="Face (Secondary)"
    ),
    GenerativeBone(
        ref="src",
        data=SkinBone(name="lid.B.L", bone_a="j_f_mabdn_03in_l", mesh_restriction="eye_occlusion"),
        req_bones=["j_f_mabdn_03in_l"],
        b_collection="Face (Secondary)",
        settings=RigifySettings(bone_name="lid.B.L", rigify_type="skin.stretchy_chain", skin_chain_pivot_pos=2,secondary_layer_extra="Face (Primary)" ,skin_control_orientation_bone="head")
    ),
    GenerativeBone(
        ref="src",
        data=SkinBone(name="lid.B.L.002", bone_a="j_f_mabdn_01_l", mesh_restriction="eye_occlusion"),
        req_bones=["j_f_mabdn_01_l"],
        b_collection="Face (Secondary)"
    ),

    GenerativeBone(
        ref="tgt",
        data=CenterBone(name="eye.L", ref_bones=["lid.T.L", "lid.T.L.002", "lid.B.L", "lid.B.L.002"], parent="head", axis="Y", inverted=True),
        req_bones=["lid.T.L", "lid.T.L.002", "lid.B.L", "lid.B.L.002"],
        b_collection="Face",
        settings=RigifySettings(bone_name="eye.L", rigify_type="face.skin_eye")
    ),

    GenerativeBone(
        ref="tgt",
        data=BridgeBone(name="lid.T.L.001", bone_a="lid.T.L", bone_b="lid.T.L.002", offset_factor=mathutils.Vector((0.0, -0.001, 0.001)), is_connected=True, parent="eye.L"),
        req_bones=["lid.T.L", "lid.T.L.002"],
        b_collection="Face (Secondary)",
        
    ),
    GenerativeBone(
        ref="tgt",
        data=BridgeBone(name="lid.T.L.003", bone_a="lid.T.L.002", bone_b="lid.B.L", offset_factor=mathutils.Vector((0.0, 0.0, 0.003)), is_connected=False),
        req_bones=["lid.T.L.002", "lid.B.L"],
        b_collection="Face (Secondary)"
    ),
    GenerativeBone(
        ref="tgt",
        data=BridgeBone(name="lid.B.L.001", bone_a="lid.B.L", bone_b="lid.B.L.002", offset_factor=mathutils.Vector((-0.002, 0.0, 0.001)), is_connected=True, parent="eye.L"),
        req_bones=["lid.B.L", "lid.B.L.002"],
        b_collection="Face (Secondary)",
    ),
    GenerativeBone(
        ref="tgt",
        data=BridgeBone(name="lid.B.L.003", bone_a="lid.B.L.002", bone_b="lid.T.L", offset_factor=mathutils.Vector((0.003, -0.001, -0.003)), is_connected=False),
        req_bones=["lid.B.L.002", "lid.T.L"],
        b_collection="Face (Secondary)"
    ),
]

EYE_R: list[GenerativeBone] = [
    GenerativeBone(
        ref="src",
        data=SkinBone(name="lid.T.R", bone_a="j_f_mabup_02out_r", mesh_restriction="eye_occlusion"),
        req_bones=["j_f_mabup_02out_r"],
        b_collection="Face (Secondary)",
        settings=RigifySettings(bone_name="lid.T.R", rigify_type="skin.stretchy_chain", skin_chain_pivot_pos=2,secondary_layer_extra="Face (Primary)" ,skin_control_orientation_bone="head", skin_chain_falloff_spherical=[False, True, False], skin_chain_falloff=[0.0, -2.0, 0.0], skin_chain_falloff_length=True)
    ),
    GenerativeBone(
        ref="src",
        data=SkinBone(name="lid.T.R.002", bone_a="j_f_mabup_01_r", mesh_restriction="eye_occlusion"),
        req_bones=["j_f_mabup_01_r"],
        b_collection="Face (Secondary)"
    ),
    GenerativeBone(
        ref="src",
        data=SkinBone(name="lid.B.R", bone_a="j_f_mabdn_03in_r", mesh_restriction="eye_occlusion"),
        req_bones=["j_f_mabdn_03in_r"],
        b_collection="Face (Secondary)",
        settings=RigifySettings(bone_name="lid.B.R", rigify_type="skin.stretchy_chain", skin_chain_pivot_pos=2,secondary_layer_extra="Face (Primary)" ,skin_control_orientation_bone="head")
    ),
    GenerativeBone(
        ref="src",
        data=SkinBone(name="lid.B.R.002", bone_a="j_f_mabdn_01_r", mesh_restriction="eye_occlusion"),
        req_bones=["j_f_mabdn_01_r"],
        b_collection="Face (Secondary)"
    ),

    GenerativeBone(
        ref="tgt",
        data=CenterBone(name="eye.R", ref_bones=["lid.T.R", "lid.T.R.002", "lid.B.R", "lid.B.R.002"], parent="head", axis="Y", inverted=True),
        req_bones=["lid.T.R", "lid.T.R.002", "lid.B.R", "lid.B.R.002"],
        b_collection="Face",
        settings=RigifySettings(bone_name="eye.R", rigify_type="face.skin_eye")
    ),

    GenerativeBone(
        ref="tgt",
        data=BridgeBone(name="lid.T.R.001", bone_a="lid.T.R", bone_b="lid.T.R.002", offset_factor=mathutils.Vector((0.0, 0.001, 0.001)), is_connected=True, parent="eye.R"),
        req_bones=["lid.T.R", "lid.T.R.002"],
        b_collection="Face (Secondary)",
        
    ),
    GenerativeBone(
        ref="tgt",
        data=BridgeBone(name="lid.T.R.003", bone_a="lid.T.R.002", bone_b="lid.B.R", offset_factor=mathutils.Vector((0.0, 0.0, 0.003)), is_connected=False),
        req_bones=["lid.T.R.002", "lid.B.R"],
        b_collection="Face (Secondary)"
    ),
    GenerativeBone(
        ref="tgt",
        data=BridgeBone(name="lid.B.R.001", bone_a="lid.B.R", bone_b="lid.B.R.002", offset_factor=mathutils.Vector((0.002, 0.0, 0.001)), is_connected=True, parent="eye.R"),
        req_bones=["lid.B.R", "lid.B.R.002"],
        b_collection="Face (Secondary)",
    ),
    GenerativeBone(
        ref="tgt",
        data=BridgeBone(name="lid.B.R.003", bone_a="lid.B.R.002", bone_b="lid.T.R", offset_factor=mathutils.Vector((-0.003, -0.001, -0.003)), is_connected=False),
        req_bones=["lid.B.R.002", "lid.T.R"],
        b_collection="Face (Secondary)"
    ),
]

HEAD: list[GenerativeBone] = [
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="neck", bone_a="j_kubi", bone_b="j_kao", parent="spine.03", is_connected=False),
        req_bones=["j_kubi", "j_kao"],
        settings=RigifySettings(bone_name="neck", rigify_type="spines.super_head", tweak_coll="Torso (Tweak)"),
        b_collection="Torso",
    ),

    GenerativeBone(
        ref="tgt",
        data=ExtensionBone(name="head", bone_a="neck", parent="neck", is_connected=True, axis_type="armature", axis="Z"),
        req_bones=["neck"],
        b_collection="Torso",
    ),
]

MOUTH_MASTER: list[GenerativeBone] = [
    #Middle
    GenerativeBone(
        ref="src",
        data=CenterBone(name="MCH_mouth_master_middle_upper", ref_bones=["j_f_ulip_01_l", "j_f_ulip_01_r"], parent="head", axis="Y"),
        req_bones=["j_f_ulip_01_l", "j_f_ulip_01_r"],
        b_collection="MCH",
    ),
    GenerativeBone(
        ref="src",
        data=ExtensionBone(name="MCH_mouth_master_middle_support_l", bone_a="j_f_ulip_01_l", parent="MCH_mouth_master_middle_upper", is_connected=False, axis_type="local", axis="Y", start="head", size_factor=0.5),
        req_bones=["j_f_ulip_01_l"],
        b_collection="MCH",
    ),
    GenerativeBone(
        ref="src",
        data=ExtensionBone(name="MCH_mouth_master_middle_support_r", bone_a="j_f_ulip_01_r", parent="MCH_mouth_master_middle_upper", is_connected=False, axis_type="local", axis="Y", start="head", size_factor=0.5),
        req_bones=["j_f_ulip_01_r"],
        b_collection="MCH",
    ),
    GenerativeBone(
        ref="src",
        data=CenterBone(name="MCH_mouth_master_middle_lower", ref_bones=["j_f_dlip_01_l", "j_f_dlip_01_r"], parent="head", axis="Y"),
        req_bones=["j_f_dlip_01_l", "j_f_dlip_01_r"],
        b_collection="MCH",
    ),
    GenerativeBone(
        ref="src",
        data=ExtensionBone(name="MCH_mouth_master_middle_support_lower_l", bone_a="j_f_dlip_01_l", parent="MCH_mouth_master_middle_lower", is_connected=False, axis_type="local", axis="Y", start="head", size_factor=0.5),
        req_bones=["j_f_dlip_01_l"],
        b_collection="MCH",
    ),
    GenerativeBone(
        ref="src",
        data=ExtensionBone(name="MCH_mouth_master_middle_support_lower_r", bone_a="j_f_dlip_01_r", parent="MCH_mouth_master_middle_lower", is_connected=False, axis_type="local", axis="Y", start="head", size_factor=0.5),
        req_bones=["j_f_dlip_01_r"],
        b_collection="MCH",
    ),
    #Corners
    GenerativeBone(
        ref="src",
        data=CenterBone(name="MCH_mouth_master_corner_left", ref_bones=["j_f_uslip_l", "j_f_dslip_l"], parent="head", axis="X", inverted=True, size_factor=0.5,),
        req_bones=["j_f_uslip_l", "j_f_dslip_l"],
        b_collection="MCH",
    ),
    GenerativeBone(
        ref="src",
        data=CenterBone(name="MCH_mouth_master_corner_right", ref_bones=["j_f_uslip_r", "j_f_dslip_r"], parent="head", axis="X", inverted=True, size_factor=-0.5),
        req_bones=["j_f_uslip_r", "j_f_dslip_r"],
        b_collection="MCH",
    )    
]

JAW_MASTER: list[GenerativeBone] = [
    GenerativeBone(
        ref="src",
        data=ExtensionBone("MCH_jaw_support", bone_a="j_f_dago", axis_type="local", axis="Y", parent="head", is_connected=False),
        req_bones=["j_f_dago"],
        b_collection="MCH",
    ),
    
    GenerativeBone(
        ref="tgt",
        data=ConnectBone("jaw", bone_a="MCH_jaw_support", bone_b="MCH_mouth_master_middle_lower", parent="head", is_connected=False),
        req_bones=["MCH_jaw_support", "MCH_mouth_master_middle_lower"],
        b_collection="Face",
        settings=RigifySettings("jaw", rigify_type="face.skin_jaw", jaw_mouth_influence=1.0),
    )
]

MOUTH: list[GenerativeBone] = [
    #Left
    GenerativeBone(
        ref="tgt",
        data=ConnectBone(name="Lip.Master.T.L", bone_a="MCH_mouth_master_middle_upper", bone_b="MCH_mouth_master_middle_support_l", parent="jaw", is_connected=False),
        req_bones=["MCH_mouth_master_middle_upper", "MCH_mouth_master_middle_support_l"],
        b_collection="Face (Secondary)",
        settings=RigifySettings(bone_name="Lip.Master.T.L", rigify_type="skin.stretchy_chain", skin_control_orientation_bone="head", skin_chain_pivot_pos=0, primary_layer_extra="Face (Primary)", skin_chain_falloff_length=True, skin_chain_falloff=[0.0, 1.0, 0.0]),
    ),

    GenerativeBone(
        ref="src",
        data=ConnectBone(name="Lip.T.L", bone_a="j_f_ulip_01_l", bone_b="j_f_umlip_01_l", parent="Lip.Master.T.L", is_connected=True),
        req_bones=["j_f_ulip_01_l", "j_f_umlip_01_l"],
        b_collection="Face (Primary)",
    ),

    GenerativeBone(
        ref="src",
        data=ConnectBone(name="Lip.T.L.001", bone_a="j_f_umlip_01_l", bone_b="j_f_uslip_l", parent="Lip.T.L", is_connected=True),
        req_bones=["j_f_umlip_01_l", "j_f_uslip_l"],
        b_collection="Face (Secondary)",
    ),

    GenerativeBone(
        ref="tgt",
        data=ConnectBone(name="Lip.Master.T.L.002", bone_a="Lip.T.L.001", bone_b="MCH_mouth_master_corner_left", parent="Lip.T.L.001", is_connected=True),
        req_bones=["Lip.T.L.001", "MCH_mouth_master_corner_left"],
        b_collection="Face (Secondary)",
    ),

    GenerativeBone(
        ref="tgt",
        data=ConnectBone(name="Lip.Master.B.L", bone_a="MCH_mouth_master_middle_lower", bone_b="MCH_mouth_master_middle_support_lower_l", parent="jaw", is_connected=False),
        req_bones=["MCH_mouth_master_middle_lower", "MCH_mouth_master_middle_support_lower_l"],
        b_collection="Face (Secondary)",
        settings=RigifySettings(bone_name="Lip.Master.B.L", rigify_type="skin.stretchy_chain", skin_control_orientation_bone="head", skin_chain_pivot_pos=0, primary_layer_extra="Face (Primary)", skin_chain_falloff_length=True, skin_chain_falloff=[0.0, 1.0, 0.0]),
    ),

     GenerativeBone(
         ref="src",
         data=ConnectBone(name="Lip.B.L", bone_a="j_f_dlip_01_l", bone_b="j_f_dmlip_01_l", parent="Lip.Master.B.L", is_connected=True),
         req_bones=["j_f_dlip_01_l", "j_f_dmlip_01_l"],
         b_collection="Face (Secondary)",
     ),

        GenerativeBone(
        ref="src",
        data=ConnectBone(name="Lip.B.L.001", bone_a="j_f_dmlip_01_l", bone_b="j_f_dslip_l", parent="Lip.B.L", is_connected=True),
        req_bones=["j_f_dmlip_01_l", "j_f_dslip_l"],
        b_collection="Face (Secondary)",
    ),

    GenerativeBone(
        ref="tgt",
        data=ConnectBone(name="Lip.Master.B.L.001", bone_a="Lip.B.L.001", bone_b="MCH_mouth_master_corner_left", parent="Lip.B.L.001", is_connected=True),
        req_bones=["Lip.B.L.001", "MCH_mouth_master_corner_left"],
        b_collection="Face (Secondary)",
    ),

    #Right
    GenerativeBone(
        ref="tgt",
        data=ConnectBone(name="Lip.Master.T.R", bone_a="MCH_mouth_master_middle_upper", bone_b="MCH_mouth_master_middle_support_r", parent="jaw", is_connected=False),
        req_bones=["MCH_mouth_master_middle_upper", "MCH_mouth_master_middle_support_r"],
        b_collection="Face (Secondary)",
        settings=RigifySettings(bone_name="Lip.Master.T.R", rigify_type="skin.stretchy_chain", skin_control_orientation_bone="head", skin_chain_pivot_pos=0, primary_layer_extra="Face (Primary)", skin_chain_falloff_length=True, skin_chain_falloff=[0.0, 1.0, 0.0]),
    ),

    GenerativeBone(
        ref="src",
        data=ConnectBone(name="Lip.T.R", bone_a="j_f_ulip_01_r", bone_b="j_f_umlip_01_r", parent="Lip.Master.T.R", is_connected=True),
        req_bones=["j_f_ulip_01_r", "j_f_umlip_01_r"],
        b_collection="Face (Primary)",
    ),

    GenerativeBone(
        ref="src",
        data=ConnectBone(name="Lip.T.R.001", bone_a="j_f_umlip_01_r", bone_b="j_f_uslip_r", parent="Lip.T.R", is_connected=True),
        req_bones=["j_f_umlip_01_r", "j_f_uslip_r"],
        b_collection="Face (Secondary)",
    ),

    GenerativeBone(
        ref="tgt",
        data=ConnectBone(name="Lip.Master.T.R.002", bone_a="Lip.T.R.001", bone_b="MCH_mouth_master_corner_right", parent="Lip.T.R.001", is_connected=True),
        req_bones=["Lip.T.R.001", "MCH_mouth_master_corner_right"],
        b_collection="Face (Secondary)",
    ),

    
    GenerativeBone(
        ref="tgt",
        data=ConnectBone(name="Lip.Master.B.R", bone_a="MCH_mouth_master_middle_lower", bone_b="MCH_mouth_master_middle_support_lower_r", parent="jaw", is_connected=False),
        req_bones=["MCH_mouth_master_middle_lower", "MCH_mouth_master_middle_support_lower_r"],
        b_collection="Face (Secondary)",
        settings=RigifySettings(bone_name="Lip.Master.B.R", rigify_type="skin.stretchy_chain", skin_control_orientation_bone="head", skin_chain_pivot_pos=0, primary_layer_extra="Face (Primary)", skin_chain_falloff_length=True, skin_chain_falloff=[0.0, 1.0, 0.0]),
    ),

    GenerativeBone(
        ref="src",
        data=ConnectBone(name="Lip.B.R", bone_a="j_f_dlip_01_r", bone_b="j_f_dmlip_01_r", parent="Lip.Master.B.R", is_connected=True),
        req_bones=["j_f_dlip_01_r", "j_f_dmlip_01_r"],
        b_collection="Face (Secondary)",
    ),

    GenerativeBone(
        ref="src",
        data=ConnectBone(name="Lip.B.R.001", bone_a="j_f_dmlip_01_r", bone_b="j_f_dslip_r", parent="Lip.B.R", is_connected=True),
        req_bones=["j_f_dmlip_01_r", "j_f_dslip_r"],
        b_collection="Face (Secondary)",
    ),

    GenerativeBone(
        ref="tgt",
        data=ConnectBone(name="Lip.Master.B.R.001", bone_a="Lip.B.R.001", bone_b="MCH_mouth_master_corner_right", parent="Lip.B.R.001", is_connected=True),
        req_bones=["Lip.B.R.001", "MCH_mouth_master_corner_right"],
        b_collection="Face (Secondary)",
    ),

    # Teeth

    GenerativeBone(
        ref="src",
        data=ExtensionBone(name="Teeth.T", bone_a="j_f_hagukiup", axis_type="local", axis="X", parent="head", is_connected=False, start="head", size_factor=-2.5),
        req_bones=["j_f_hagukiup"],
        b_collection="Face",
        settings=RigifySettings(bone_name="Teeth.T", rigify_type="basic.super_copy", super_copy_widget_type="teeth"),
    ),

    GenerativeBone(
        ref="src",
        data=ExtensionBone(name="Teeth.B", bone_a="j_f_hagukidn", axis_type="local", axis="X", parent="jaw", is_connected=False, start="head", size_factor=-2.5),
        req_bones=["j_f_hagukidn"],
        b_collection="Face",
        settings=RigifySettings(bone_name="Teeth.B", rigify_type="basic.super_copy", super_copy_widget_type="teeth"),
    ),

    # Tongue
    # I'm going back to front to closer match Rigify's standard
    # Unfortunately due to the bone placement in FF's rig I am unable to to generate the start of the tongue any closer to the mouth than it is, but it's not particularly pressing
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="Tongue", bone_a="j_f_bero_03", bone_b="j_f_bero_02", parent="jaw", is_connected=False),
        req_bones=["j_f_bero_03", "j_f_bero_02"],
        b_collection="Face",
        settings=RigifySettings(bone_name="Tongue", rigify_type="face.basic_tongue", tweak_coll="Face (Secondary)"),
    ),

    GenerativeBone(
        ref="src",
        data=ConnectBone(name="Tongue.001", bone_a="j_f_bero_02", bone_b="j_f_bero_01", parent="Tongue", is_connected=True),
        req_bones=["j_f_bero_02", "j_f_bero_01"],
        b_collection="Face (Secondary)",
    ),

    GenerativeBone(
        ref="tgt",
        data=ExtensionBone(name="Tongue.002", bone_a="Tongue.001", parent="Tongue.001", is_connected=True, axis_type="local", axis="Y", size_factor=1),
        req_bones=["Tongue.001"],
        b_collection="Face (Secondary)",
    ),

    #Cheek Glue

    GenerativeBone(
        ref="tgt",
        data=ConnectBone(name="Cheek.B.L.glue", bone_a="Cheek.B.L", bone_b="MCH_mouth_master_corner_left", parent="head", is_connected=False),
        req_bones=["Cheek.B.L", "MCH_mouth_master_corner_left"],
        b_collection="Face (Secondary)",
        settings=RigifySettings(bone_name="Cheek.B.L.glue", rigify_type="skin.glue", relink_constraints=True, skin_glue_use_tail=True, skin_glue_tail_reparent=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.3),
    ),

    GenerativeBone(
        ref="tgt",
        data=ConnectBone(name="Cheek.B.R.glue", bone_a="Cheek.B.R", bone_b="MCH_mouth_master_corner_right", parent="head", is_connected=False),
        req_bones=["Cheek.B.R", "MCH_mouth_master_corner_right"],
        b_collection="Face (Secondary)",
        settings=RigifySettings(bone_name="Cheek.B.R.glue", rigify_type="skin.glue", relink_constraints=True, skin_glue_use_tail=True, skin_glue_tail_reparent=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.3),
    ),
]

CHEEKS: list[GenerativeBone] = [
    #Left Cheek
     GenerativeBone(
        ref="src",
        data=ConnectBone(name="Cheek.B.L", bone_a="j_f_shoho_l", bone_b= "j_f_dhoho_l", parent="head", is_connected=False),
        req_bones=["j_f_shoho_l", "j_f_dhoho_l"],
        b_collection="Face (Primary)",
        settings=RigifySettings(bone_name="Cheek.B.L", rigify_type="skin.basic_chain"),
    ),

    GenerativeBone(
        ref="src",
        data=ConnectBone(name="Cheek.B.L.001", bone_a="j_f_dhoho_l", bone_b="j_f_hoho_l", parent="Cheek.B.L", is_connected=True),
        req_bones=["j_f_dhoho_l", "j_f_hoho_l"],
        b_collection="Face (Secondary)",
    ),

    GenerativeBone(
        ref="src",
        data=ConnectBone(name="Cheek.T.L", bone_a="j_f_hoho_l", bone_b="j_f_dmemoto_l", parent="head", is_connected=False),
        req_bones=["j_f_hoho_l", "j_f_dmemoto_l"],
        b_collection="Face (Secondary)",
        settings=RigifySettings(bone_name="Cheek.T.L", rigify_type="skin.basic_chain"),
    ),

    GenerativeBone(
        ref="src",
        data=ConnectBone(name="Cheek.T.L.001", bone_a="j_f_dmemoto_l", bone_b="j_f_dmiken_l", parent="Cheek.T.L", is_connected=True),
        req_bones=["j_f_dmemoto_l", "j_f_dmiken_l"],
        b_collection="Face (Secondary)",
    ),

    #Right Cheek
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="Cheek.B.R", bone_a="j_f_shoho_r", bone_b= "j_f_dhoho_r", parent="head", is_connected=False),
        req_bones=["j_f_shoho_r", "j_f_dhoho_r"],
        b_collection="Face (Primary)",
        settings=RigifySettings(bone_name="Cheek.B.R", rigify_type="skin.basic_chain"),
    ),

    GenerativeBone(
        ref="src",
        data=ConnectBone(name="Cheek.B.R.001", bone_a="j_f_dhoho_r", bone_b="j_f_hoho_r", parent="Cheek.B.R", is_connected=True),
        req_bones=["j_f_dhoho_r", "j_f_hoho_r"],
        b_collection="Face (Secondary)",
    ),

    GenerativeBone(
        ref="src",
        data=ConnectBone(name="Cheek.T.R", bone_a="j_f_hoho_r", bone_b="j_f_dmemoto_r", parent="head", is_connected=False),
        req_bones=["j_f_hoho_r", "j_f_dmemoto_r"],
        b_collection="Face (Secondary)",
        settings=RigifySettings(bone_name="Cheek.T.R", rigify_type="skin.basic_chain"),
    ),

    GenerativeBone(
        ref="src",
        data=ConnectBone(name="Cheek.T.R.001", bone_a="j_f_dmemoto_r", bone_b="j_f_dmiken_r", parent="Cheek.T.R", is_connected=True),
        req_bones=["j_f_dmemoto_r", "j_f_dmiken_r"],
        b_collection="Face (Secondary)",
    ),

     # Lower Lid Glue

    GenerativeBone(
        ref="tgt",
        data=ConnectBone(name="Lid.Cheek.R.glue", bone_a="lid.B.R.002", bone_b="Cheek.T.R", parent="head", is_connected=False),
        req_bones=["lid.B.R.002", "Cheek.T.R"],
        b_collection="Face (Secondary)",
        settings=RigifySettings(bone_name="Lid.Cheek.R.glue", rigify_type="skin.glue", relink_constraints=True, skin_glue_use_tail=True, skin_glue_tail_reparent=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.1),
    ),

    GenerativeBone(
        ref="tgt",
        data=ConnectBone(name="Lid.Cheek.L.glue", bone_a="lid.B.L.002", bone_b="Cheek.T.L", parent="head", is_connected=False),
        req_bones=["lid.B.L.002", "Cheek.T.L"],
        b_collection="Face (Secondary)",
        settings=RigifySettings(bone_name="Lid.Cheek.L.glue", rigify_type="skin.glue", relink_constraints=True, skin_glue_use_tail=True, skin_glue_tail_reparent=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.1),
    ),
]

BROW_L: list[GenerativeBone] = [
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="brow.T.L", bone_a="j_f_mayu_l", bone_b= "j_f_mmayu_l", parent="head", is_connected=False),
        req_bones=["j_f_mayu_l", "j_f_mmayu_l"],
        b_collection="Face (Secondary)",
        settings=RigifySettings(bone_name="brow.T.L", rigify_type="skin.stretchy_chain", skin_control_orientation_bone="head", secondary_layer_extra="Face (Primary)", skin_chain_pivot_pos=2, skin_chain_falloff_length=True, skin_chain_falloff=[0.0, 0.0, 0.0]),
    ),

    GenerativeBone(
        ref="src",
        data=ConnectBone(name="brow.T.L.001", bone_a="j_f_mmayu_l", bone_b= "j_f_miken_01_l", parent="brow.T.L", is_connected=True),
        req_bones=["j_f_mmayu_l", "j_f_miken_01_l", "brow.T.L"],
        b_collection="Face (Secondary)",
    ),

    GenerativeBone(
        ref="src",
        data=ConnectBone(name="brow.T.L.002", bone_a="j_f_miken_01_l", bone_b= "j_f_miken_02_l", parent="brow.T.L.001", is_connected=True),
        req_bones=["j_f_miken_01_l", "j_f_miken_02_l", "brow.T.L.001"],
        b_collection="Face (Secondary)",
    ),

    GenerativeBone(
        ref="tgt",
        data=ExtensionBone(name="brow.T.L.003", bone_a="brow.T.L.002", parent="brow.T.L.002", is_connected=True, axis_type="local", axis="Y", start="tail", size_factor=0.6),
        req_bones=["brow.T.L.002"],
        b_collection="Face (Secondary)",
    ),

    GenerativeBone(
        ref="tgt",
        data=ConnectBone(name="brow.T.L.002.glue", bone_a="lid.T.L.002", bone_b="brow.T.L.002", parent="head", is_connected=False),
        req_bones=["brow.T.L.002", "lid.T.L.002"],
        b_collection="Face (Secondary)",
        settings=RigifySettings(bone_name="brow.T.L.002.glue", rigify_type="skin.glue", relink_constraints=True, skin_glue_use_tail=True, skin_glue_tail_reparent=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.1),
    )
]

BROW_R: list[GenerativeBone] = [
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="brow.T.R", bone_a="j_f_mayu_r", bone_b= "j_f_mmayu_r", parent="head", is_connected=False),
        req_bones=["j_f_mayu_r", "j_f_mmayu_r"],
        b_collection="Face (Secondary)",
        settings=RigifySettings(bone_name="brow.T.R", rigify_type="skin.stretchy_chain", skin_control_orientation_bone="head", secondary_layer_extra="Face (Primary)", skin_chain_pivot_pos=2, skin_chain_falloff_length=True, skin_chain_falloff=[0.0, 0.0, 0.0]),
    ),

    GenerativeBone(
        ref="src",
        data=ConnectBone(name="brow.T.R.001", bone_a="j_f_mmayu_r", bone_b= "j_f_miken_01_r", parent="brow.T.R", is_connected=True),
        req_bones=["j_f_mmayu_r", "j_f_miken_01_r", "brow.T.R"],
        b_collection="Face (Secondary)",
    ),

    GenerativeBone(
        ref="src",
        data=ConnectBone(name="brow.T.R.002", bone_a="j_f_miken_01_r", bone_b= "j_f_miken_02_r", parent="brow.T.R.001", is_connected=True),
        req_bones=["j_f_miken_01_r", "j_f_miken_02_r", "brow.T.R.001"],
        b_collection="Face (Secondary)",
    ),

    GenerativeBone(
        ref="tgt",
        data=ExtensionBone(name="brow.T.R.003", bone_a="brow.T.R.002", parent="brow.T.R.002", is_connected=True, axis_type="local", axis="Y", start="tail", size_factor=0.6),
        req_bones=["brow.T.R.002"],
        b_collection="Face (Secondary)",
    ),

    GenerativeBone(
        ref="tgt",
        data=ConnectBone(name="brow.T.R.002.glue", bone_a="lid.T.R.002", bone_b="brow.T.R.002", parent="head", is_connected=False),
        req_bones=["brow.T.R.002", "lid.T.R.002"],
        b_collection="Face (Secondary)",
        settings=RigifySettings(bone_name="brow.T.R.002.glue", rigify_type="skin.glue", relink_constraints=True, skin_glue_use_tail=True, skin_glue_tail_reparent=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.1),
    )
]

NOSE: list[GenerativeBone] = [
    GenerativeBone(
        ref="src",
        data=ExtensionBone(name="Nose", bone_a="j_f_uhana", parent="head", is_connected=False, axis_type="local", axis="Y", size_factor=-1.2, start="head"),
        req_bones=["j_f_uhana"],
        b_collection="Face (Primary)",
        settings=RigifySettings(bone_name="Nose", rigify_type="skin.basic_chain", skin_chain_priority=2),
    ),

    GenerativeBone(
        ref="src",
        data=ConnectBone(name="Nose.L", bone_a="j_f_dmiken_l", bone_b="j_f_uhana", parent="head", is_connected=False),
        req_bones=["j_f_dmiken_l", "j_f_uhana"],
        b_collection="Face (Secondary)",
        settings=RigifySettings(bone_name="Nose.L", rigify_type="skin.basic_chain", skin_chain_priority=1),
    ),
    
    #because I need a tgt armature bone to connect with Nose
    GenerativeBone(
        ref="src",
        data=ExtensionBone(name="Nose.L.001.support", bone_a="j_f_hana_l", parent="head", is_connected=False, axis_type="local", axis="Y", size_factor=0.2, start="head"),
        req_bones=["j_f_hana_l"],
        b_collection="Face (Secondary)",
    ),

    GenerativeBone(
        ref="tgt",
        data=ConnectBone(name="Nose.L.001", bone_a="Nose.L.001.support", bone_b="Nose", parent="head", is_connected=False, end="tail"),
        req_bones=["Nose.L.001.support", "Nose"],
        b_collection="Face (Secondary)",
        settings=RigifySettings(bone_name="Nose.L.001", rigify_type="skin.basic_chain", skin_chain_priority=1),
    ),

    GenerativeBone(
        ref="tgt",
        data=ConnectBone(name="Nose.Tip.glue", bone_a="Nose.L.001", bone_b="Nose", parent="head", is_connected=False, start="tail"),
        req_bones=["Nose.L.001", "Nose"],
        b_collection="Face (Secondary)",
        settings=RigifySettings(bone_name="Nose.Tip.glue", rigify_type="skin.glue", relink_constraints=True, skin_glue_use_tail=True, skin_glue_tail_reparent=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.2),
    ),

    GenerativeBone(
        ref="tgt",
        data=ConnectBone(name="Nose.L.002.glue", bone_a="Nose.L.001.support", bone_b="Nose", parent="head", is_connected=False, end="tail"),
        req_bones=["Nose.L.001.support", "Nose"],
        b_collection="Face (Secondary)",
        settings=RigifySettings(bone_name="Nose.L.002.glue", rigify_type="skin.glue", relink_constraints=True, skin_glue_use_tail=True, skin_glue_tail_reparent=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.2),
    ),

    GenerativeBone(
        ref="src",
        data=ConnectBone(name="Nose.R", bone_a="j_f_dmiken_r", bone_b="j_f_uhana", parent="head", is_connected=False),
        req_bones=["j_f_dmiken_r", "j_f_uhana"],
        b_collection="Face (Secondary)",
        settings=RigifySettings(bone_name="Nose.R", rigify_type="skin.basic_chain", skin_chain_priority=1),
    ),

    #because I need a tgt armature bone to connect with Nose
    GenerativeBone(
        ref="src",
        data=ExtensionBone(name="Nose.R.001.support", bone_a="j_f_hana_r", parent="head", is_connected=False, axis_type="local", axis="Y", size_factor=0.2, start="head"),
        req_bones=["j_f_hana_r"],
        b_collection="Face (Secondary)",
    ),

    GenerativeBone(
        ref="tgt",
        data=ConnectBone(name="Nose.R.001", bone_a="Nose.R.001.support", bone_b="Nose", parent="head", is_connected=False, end="tail"),
        req_bones=["Nose.R.001.support", "Nose"],
        b_collection="Face (Secondary)",
        settings=RigifySettings(bone_name="Nose.R.001", rigify_type="skin.basic_chain", skin_chain_priority=1),
    ),

    GenerativeBone(
        ref="tgt",
        data=ConnectBone(name="Nose.R.002.glue", bone_a="Nose.R.001.support", bone_b="Nose", parent="head", is_connected=False, end="tail"),
        req_bones=["Nose.R.001.support", "Nose"],
        b_collection="Face (Secondary)",
        settings=RigifySettings(bone_name="Nose.R.002.glue", rigify_type="skin.glue", relink_constraints=True, skin_glue_use_tail=True, skin_glue_tail_reparent=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.2),
    ),

    GenerativeBone(
        ref="src",
        data=ConnectBone(name="Nose.L.glue", bone_a="j_f_dmiken_l", bone_b="j_f_uhana", parent="head", is_connected=False),
        req_bones=["j_f_dmiken_l", "j_f_uhana"],
        b_collection="Face (Secondary)",
        settings=RigifySettings(bone_name="Nose.L.glue", rigify_type="skin.glue", relink_constraints=True, skin_glue_use_tail=True, skin_glue_tail_reparent=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.2),
    ),

    GenerativeBone(
        ref="src",
        data=ConnectBone(name="Nose.R.glue", bone_a="j_f_dmiken_r", bone_b="j_f_uhana", parent="head", is_connected=False),
        req_bones=["j_f_dmiken_r", "j_f_uhana"],
        b_collection="Face (Secondary)",
        settings=RigifySettings(bone_name="Nose.R.glue", rigify_type="skin.glue", relink_constraints=True, skin_glue_use_tail=True, skin_glue_tail_reparent=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.2),
    ),

    GenerativeBone(
        ref="src",
        data=ConnectBone(name="Nose.L.glue.001", bone_a="j_f_dmiken_l", bone_b="j_f_miken_02_l", parent="head", is_connected=False),
        req_bones=["j_f_dmiken_l", "j_f_uhana"],
        b_collection="Face (Secondary)",
        settings=RigifySettings(bone_name="Nose.L.glue.001", rigify_type="skin.glue", relink_constraints=True, skin_glue_use_tail=True, skin_glue_tail_reparent=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5),
    ),

    GenerativeBone(
        ref="src",
        data=ConnectBone(name="Nose.R.glue.001", bone_a="j_f_dmiken_r", bone_b="j_f_miken_02_r", parent="head", is_connected=False),
        req_bones=["j_f_dmiken_r", "j_f_uhana"],
        b_collection="Face (Secondary)",
        settings=RigifySettings(bone_name="Nose.R.glue.001", rigify_type="skin.glue", relink_constraints=True, skin_glue_use_tail=True, skin_glue_tail_reparent=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5),
    ),
]

VIERA_EAR_L: list[GenerativeBone] = [
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="v_ear.L", bone_a="j_zerd_a_l", bone_b="j_zerd_b_l", parent="head", is_connected=False),
        req_bones=["j_zerd_a_l", "j_zerd_b_l"],
        b_collection="Face",
        settings=RigifySettings(bone_name="v_ear.L", rigify_type="skin.basic_chain"),
        # is_optional=True,
    ),

    GenerativeBone(
        ref="tgt",
        data=ExtensionBone(name="v_ear.L.001", bone_a="v_ear.L", parent="v_ear.L", is_connected=True, axis_type="local", axis="Y"),
        req_bones=["v_ear.L"],
        b_collection="Face",
        # is_optional=True,
    ),


]

VIERA_EAR_R: list[GenerativeBone] = [
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="v_ear.R", bone_a="j_zerd_a_r", bone_b="j_zerd_b_r", parent="head", is_connected=False),
        req_bones=["j_zerd_a_r", "j_zerd_b_r"],
        b_collection="Face",
        settings=RigifySettings(bone_name="v_ear.R", rigify_type="skin.basic_chain"),
        # is_optional=True,
    ),

    GenerativeBone(
        ref="tgt",
        data=ExtensionBone(name="v_ear.R.001", bone_a="v_ear.R", parent="v_ear.R", is_connected=True, axis_type="local", axis="Y"),
        req_bones=["v_ear.R"],
        b_collection="Face",
        # is_optional=True,
    ),
]

EAR_L: list[GenerativeBone] = [
    GenerativeBone(
        ref="src",
        data=ExtensionBone(name="ear.L", bone_a="j_mimi_l", parent="head", is_connected=False, axis_type="local", axis="X", start="head"),
        req_bones=["j_mimi_l"],
        b_collection="Face",
        settings=RigifySettings(bone_name="ear.L", rigify_type="basic.super_copy", super_copy_widget_type="bone")
    ),
]

EAR_R: list[GenerativeBone] = [
    GenerativeBone(
        ref="src",
        data=ExtensionBone(name="ear.R", bone_a="j_mimi_r", parent="head", is_connected=False, axis_type="local", axis="X", start="head"),
        req_bones=["j_mimi_r"],
        b_collection="Face",
        settings=RigifySettings(bone_name="ear.R", rigify_type="basic.super_copy", super_copy_widget_type="bone")
    ),
]

SIMPLE_FACE_BONES: list[GenerativeBone] = [
    #I wish so much misfortune on whoever made the pre-DT vanilla face armature for FF
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="simple.jaw", bone_a="j_ago", bone_b="j_f_dlip_b", parent="head", is_connected=False),
        req_bones=["j_ago", "j_f_dlip_b"],
        b_collection="Face",
        settings=RigifySettings(bone_name="simple.jaw", rigify_type="basic.super_copy", super_copy_widget_type="jaw")
    ),

    GenerativeBone(
        ref="src",
        data=ExtensionBone(name="simple.lip.B", bone_a="j_f_dlip_b", parent="simple.jaw", is_connected=False, axis_type="local", axis="X", start="head", size_factor=0.1),
        req_bones=["j_f_dlip_b"],
        b_collection="Face (Primary)",
        settings=RigifySettings(bone_name="simple.lip.B", rigify_type="basic.super_copy", super_copy_widget_type="circle")
    ),

    GenerativeBone(
        ref="src",
        data=ExtensionBone(name="simple.lip.T", bone_a="j_f_ulip_b", parent="head", is_connected=False, axis_type="local", axis="X", start="head", size_factor=0.1),
        req_bones=["j_f_ulip_b"],
        b_collection="Face (Primary)",
        settings=RigifySettings(bone_name="simple.lip.T", rigify_type="basic.super_copy", super_copy_widget_type="circle")
    )
]

SKIRT: list[GenerativeBone] = [
    # Left Side
    # Outside
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="skirt_out.L", bone_a="j_sk_s_a_l", bone_b="j_sk_s_b_l", parent="hips", is_connected=False),
        req_bones=["j_sk_s_a_l", "j_sk_s_b_l"],
        b_collection="Skirt (Tweak)",
        settings=RigifySettings(bone_name="skirt_out.L", rigify_type="skin.stretchy_chain", primary_layer_extra="Skirt", skin_chain_falloff=[0.0, 0.0, -0.3], skin_chain_falloff_length=True, skin_chain_falloff_spherical=[True, True, True])
    ),
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="skirt_out.L.001", bone_a="j_sk_s_b_l", bone_b="j_sk_s_c_l", parent="skirt_out.L", is_connected=True),
        req_bones=["j_sk_s_b_l", "j_sk_s_c_l"],
        b_collection="Skirt (Tweak)",
    ),
    GenerativeBone(
        ref="tgt",
        data=ExtensionBone(name="skirt_out.L.002", bone_a="skirt_out.L.001", is_connected=True, axis_type="local", axis="Y", start="tail", size_factor=0.8, parent="skirt_out.L.001"),
        req_bones=["skirt_out.L.001"],
        b_collection="Skirt (Tweak)",
    ),

    # Front
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="skirt_front.L", bone_a="j_sk_f_a_l", bone_b="j_sk_f_b_l", parent="hips", is_connected=False),
        req_bones=["j_sk_f_a_l", "j_sk_f_b_l"],
        b_collection="Skirt (Tweak)",
        settings=RigifySettings(bone_name="skirt_front.L", rigify_type="skin.stretchy_chain", primary_layer_extra="Skirt", skin_chain_falloff=[0.0, 0.0, 0.2], skin_chain_falloff_length=True, skin_chain_falloff_spherical=[True, True, True]),
    ),
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="skirt_front.L.001", bone_a="j_sk_f_b_l", bone_b="j_sk_f_c_l", parent="skirt_front.L", is_connected=True),
        req_bones=["j_sk_f_b_l", "j_sk_f_c_l", "skirt_front.L"],
        b_collection="Skirt (Tweak)",
    ),
    GenerativeBone(
        ref="tgt",
        data=ExtensionBone(name="skirt_front.L.002", bone_a="skirt_front.L.001", parent="skirt_front.L.001", is_connected=True, axis_type="local", axis="Y", start="tail", size_factor=0.8),
        req_bones=["skirt_front.L.001"],
        b_collection="Skirt (Tweak)",
    ),

    # Back
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="skirt_back.L", bone_a="j_sk_b_a_l", bone_b="j_sk_b_b_l", parent="hips", is_connected=False),
        req_bones=["j_sk_b_a_l", "j_sk_b_b_l"],
        b_collection="Skirt (Tweak)",
        settings=RigifySettings(bone_name="skirt_back.L", rigify_type="skin.stretchy_chain", primary_layer_extra="Skirt", skin_chain_falloff=[0.0, 0.0, -0.3], skin_chain_falloff_length=True, skin_chain_falloff_spherical=[True, True, True])
    ),
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="skirt_back.L.001", bone_a="j_sk_b_b_l", bone_b="j_sk_b_c_l", parent="skirt_back.L", is_connected=True),
        req_bones=["j_sk_b_b_l", "j_sk_b_c_l", "skirt_back.L"],
        b_collection="Skirt (Tweak)",
    ),
    GenerativeBone(
        ref="tgt",
        data=ExtensionBone(name="skirt_back.L.002", bone_a="skirt_back.L.001", parent="skirt_back.L.001", is_connected=True, axis_type="local", axis="Y", start="tail", size_factor=0.8),
        req_bones=["skirt_back.L.001"],
        b_collection="Skirt (Tweak)",
    ),

    # Right Side
    # Outside
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="skirt_out.R", bone_a="j_sk_s_a_r",bone_b="j_sk_s_b_r", parent="hips", is_connected=False),
        req_bones=["j_sk_s_a_r", "j_sk_s_b_r"],
        b_collection="Skirt (Tweak)",
        settings=RigifySettings(bone_name="skirt_out.R", rigify_type="skin.stretchy_chain", primary_layer_extra="Skirt", skin_chain_falloff=[0.0, 0.0, -0.3], skin_chain_falloff_length= True, skin_chain_falloff_spherical=[True, True, True])
    ),
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="skirt_out.R.001", bone_a="j_sk_s_b_r", bone_b="j_sk_s_c_r", parent="skirt_out.R", is_connected=True),
        req_bones=["j_sk_s_b_r", "j_sk_s_c_r", "skirt_out.R"],
        b_collection="Skirt (Tweak)",
    ),
    GenerativeBone(
        ref="tgt",
        data=ExtensionBone(name="skirt_out.R.002", bone_a="skirt_out.R.001", parent="skirt_out.R.001", is_connected=True, axis_type="local", axis="Y", start="tail", size_factor=0.8),
        req_bones=["skirt_out.R.001"],
        b_collection="Skirt (Tweak)",
    ),

    # Front
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="skirt_front.R", bone_a="j_sk_f_a_r",bone_b="j_sk_f_b_r", parent="hips", is_connected=False),
        req_bones=["j_sk_f_a_r", "j_sk_f_b_r"],
        b_collection="Skirt (Tweak)",
        settings=RigifySettings(bone_name="skirt_front.R", rigify_type="skin.stretchy_chain", primary_layer_extra="Skirt", skin_chain_falloff=[0.0, 0.0, 0.2], skin_chain_falloff_length=True, skin_chain_falloff_spherical=[True, True, True])
    ),
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="skirt_front.R.001", bone_a="j_sk_f_b_r", bone_b="j_sk_f_c_r", parent="skirt_front.R", is_connected=True),
        req_bones=["j_sk_f_b_r", "j_sk_f_c_r", "skirt_front.R"],
        b_collection="Skirt (Tweak)",
    ),
    GenerativeBone(
        ref="tgt",
        data=ExtensionBone(name="skirt_front.R.002", bone_a="skirt_front.R.001", parent="skirt_front.R.001", is_connected=True, axis_type="local", axis="Y", start="tail", size_factor=0.8),
        req_bones=["skirt_front.R.001"],
        b_collection="Skirt (Tweak)",
    ),

    # Back
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="skirt_back.R", bone_a="j_sk_b_a_r", bone_b="j_sk_b_b_r", parent="hips", is_connected=False),
        req_bones=["j_sk_b_a_r", "j_sk_b_b_r"],
        b_collection="Skirt (Tweak)",
        settings=RigifySettings(bone_name="skirt_back.R", rigify_type="skin.stretchy_chain", primary_layer_extra="Skirt", skin_chain_falloff=[0.0, 0.0, -0.3], skin_chain_falloff_length=True, skin_chain_falloff_spherical=[True, True, True])
    ),
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="skirt_back.R.001", bone_a="j_sk_b_b_r", bone_b="j_sk_b_c_r", parent="skirt_back.R", is_connected=True),
        req_bones=["j_sk_b_b_r", "j_sk_b_c_r", "skirt_back.R"],
        b_collection="Skirt (Tweak)",
    ),
    GenerativeBone(
        ref="tgt",
        data=ExtensionBone(name="skirt_back.R.002", bone_a="skirt_back.R.001", parent="skirt_back.R.001", is_connected=True, axis_type="local", axis="Y", start="tail", size_factor=0.8),
        req_bones=["skirt_back.R.001"],
        b_collection="Skirt (Tweak)",
    ),

    # Support Bones Front.L


    GenerativeBone(
        ref="tgt",
        data=ConnectBone(name="skirt_support.F.L.002", bone_a="shin.L", bone_b="skirt_front.L.002", parent="shin.L", is_connected=False, start="head", end="tail", roll=0),
        req_bones=["shin.L", "skirt_front.L.002"],
        b_collection="Skirt",
        settings=RigifySettings(bone_name="skirt_support.F.L.002", rigify_type="skin.basic_chain", skin_chain_priority=1),
    ),

    # Support Bones Side.L
    
    GenerativeBone(
        ref="tgt",
        data=ConnectBone(name="skirt_support.S.L.002", bone_a="shin.L", bone_b="skirt_out.L.002", parent="shin.L", is_connected=False, start="head", end="tail", roll=0.0),
        req_bones=["shin.L", "skirt_out.L.002"],
        b_collection="Skirt",
        settings=RigifySettings(bone_name="skirt_support.S.L.002", rigify_type="skin.basic_chain", skin_chain_priority=1),
    ),

    # Support Bones Back.L
    # For some reason the controller names are taken from these and not the main skirt bones. This isn't an issue with the other support bones so I dunno
    
    GenerativeBone(
        ref="tgt",
        data=ConnectBone(name="skirt_support.B.L.002", bone_a="shin.L", bone_b="skirt_back.L.002", parent="shin.L", is_connected=False, start="head", end="tail", roll=0.0),
        req_bones=["shin.L", "skirt_back.L"],
        b_collection="Skirt",
        settings=RigifySettings(bone_name="skirt_support.B.L.002", rigify_type="skin.basic_chain", skin_chain_priority=1),
    ),

    # Support Bones Front.R
    

    GenerativeBone(
        ref="tgt",
        data=ConnectBone(name="skirt_support.F.R.002", bone_a="shin.R", bone_b="skirt_front.R.002", parent="shin.R", is_connected=False, start="head", end="tail", roll=0),
        req_bones=["shin.R", "skirt_front.R.002"],
        b_collection="Skirt",
        settings=RigifySettings(bone_name="skirt_support.F.R.002", rigify_type="skin.basic_chain", skin_chain_priority=1),
    ),

    # Support Bones Side.R

    
    
    GenerativeBone(
        ref="tgt",
        data=ConnectBone(name="skirt_support.S.R.002", bone_a="shin.R", bone_b="skirt_out.R.002", parent="shin.R", is_connected=False, start="head", end="tail", roll=0.0),
        req_bones=["shin.R", "skirt_out.R.002"],
        b_collection="Skirt",
        settings=RigifySettings(bone_name="skirt_support.S.R.002", rigify_type="skin.basic_chain", skin_chain_priority=1),
    ),

    # Support Bones Back.R

    
    GenerativeBone(
        ref="tgt",
        data=ConnectBone(name="skirt_support.B.R.002", bone_a="shin.R", bone_b="skirt_back.R.002", parent="shin.R", is_connected=False, start="head", end="tail", roll=0.0),
        req_bones=["shin.R", "skirt_back.R.002"],
        b_collection="Skirt",
        settings=RigifySettings(bone_name="skirt_support.B.R.002", rigify_type="skin.basic_chain", skin_chain_priority=1),
    ),
]