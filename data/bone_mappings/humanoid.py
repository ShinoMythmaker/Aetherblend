import mathutils

from .. schemas import GenerativeBone, ConnectBone, ExtensionBone, RigifySettings, EyeBone, SkinBone, BridgeBone


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
        settings=RigifySettings(bone_name="hips", rigify_type="basic.super_copy", super_copy_widget_type="pivot"),
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
        data=SkinBone(name="lid.T.L", bone_a="j_f_mabup_02out_l"),
        req_bones=["j_f_mabup_02out_l"],
        b_collection="Face (Secondary)",
        settings=RigifySettings(bone_name="lid.T.L", rigify_type="skin.stretchy_chain", skin_chain_pivot_pos=2,secondary_layer_extra="Face (Primary)" ,skin_control_orientation_bone="head", skin_chain_falloff_spherical=[False, True, False])
    ),
    GenerativeBone(
        ref="src",
        data=SkinBone(name="lid.T.L.002", bone_a="j_f_mabup_01_l"),
        req_bones=["j_f_mabup_01_l"],
        b_collection="Face (Secondary)"
    ),
    GenerativeBone(
        ref="src",
        data=SkinBone(name="lid.B.L", bone_a="j_f_mabdn_03in_l"),
        req_bones=["j_f_mabdn_03in_l"],
        b_collection="Face (Secondary)",
        settings=RigifySettings(bone_name="lid.B.L", rigify_type="skin.stretchy_chain", skin_chain_pivot_pos=2,secondary_layer_extra="Face (Primary)" ,skin_control_orientation_bone="head")
    ),
    GenerativeBone(
        ref="src",
        data=SkinBone(name="lid.B.L.002", bone_a="j_f_mabdn_01_l"),
        req_bones=["j_f_mabdn_01_l"],
        b_collection="Face (Secondary)"
    ),

    GenerativeBone(
        ref="tgt",
        data=EyeBone(name="eye.L", ref_bones=["lid.T.L", "lid.T.L.002", "lid.B.L", "lid.B.L.002"], parent="head"),
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
        data=SkinBone(name="lid.T.R", bone_a="j_f_mabup_02out_r"),
        req_bones=["j_f_mabup_02out_r"],
        b_collection="Face (Secondary)",
        settings=RigifySettings(bone_name="lid.T.R", rigify_type="skin.stretchy_chain", skin_chain_pivot_pos=2,secondary_layer_extra="Face (Primary)" ,skin_control_orientation_bone="head", skin_chain_falloff_spherical=[False, True, False])
    ),
    GenerativeBone(
        ref="src",
        data=SkinBone(name="lid.T.R.002", bone_a="j_f_mabup_01_r"),
        req_bones=["j_f_mabup_01_r"],
        b_collection="Face (Secondary)"
    ),
    GenerativeBone(
        ref="src",
        data=SkinBone(name="lid.B.R", bone_a="j_f_mabdn_03in_r"),
        req_bones=["j_f_mabdn_03in_r"],
        b_collection="Face (Secondary)",
        settings=RigifySettings(bone_name="lid.B.R", rigify_type="skin.stretchy_chain", skin_chain_pivot_pos=2,secondary_layer_extra="Face (Primary)" ,skin_control_orientation_bone="head")
    ),
    GenerativeBone(
        ref="src",
        data=SkinBone(name="lid.B.R.002", bone_a="j_f_mabdn_01_r"),
        req_bones=["j_f_mabdn_01_r"],
        b_collection="Face (Secondary)"
    ),

    GenerativeBone(
        ref="tgt",
        data=EyeBone(name="eye.R", ref_bones=["lid.T.R", "lid.T.R.002", "lid.B.R", "lid.B.R.002"], parent="head"),
        req_bones=["lid.T.R", "lid.T.R.002", "lid.B.R", "lid.B.R.002"],
        b_collection="Face",
        settings=RigifySettings(bone_name="eye.R", rigify_type="face.skin_eye")
    ),

    GenerativeBone(
        ref="tgt",
        data=BridgeBone(name="lid.T.R.001", bone_a="lid.T.R", bone_b="lid.T.R.002", offset_factor=mathutils.Vector((0.0, -0.001, 0.001)), is_connected=True, parent="eye.R"),
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
        data=BridgeBone(name="lid.B.R.001", bone_a="lid.B.R", bone_b="lid.B.R.002", offset_factor=mathutils.Vector((-0.002, 0.0, 0.001)), is_connected=True, parent="eye.R"),
        req_bones=["lid.B.R", "lid.B.R.002"],
        b_collection="Face (Secondary)",
    ),
    GenerativeBone(
        ref="tgt",
        data=BridgeBone(name="lid.B.R.003", bone_a="lid.B.R.002", bone_b="lid.T.R", offset_factor=mathutils.Vector((0.003, -0.001, -0.003)), is_connected=False),
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

JAW: list[GenerativeBone] = [
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="jaw", bone_a="j_f_ago", bone_b="j_f_hagukidn", parent="head", is_connected=False),
        req_bones=["j_f_ago", "j_f_hagukidn"],
        b_collection="Face",
        settings=RigifySettings(bone_name="jaw", rigify_type="basic.super_copy", super_copy_widget_type="jaw")
    )
]

EAR_L: list[GenerativeBone] = [
    GenerativeBone(
        ref="src",
        data=ExtensionBone(name="ear.L", bone_a="j_mimi_l", parent="head", is_connected=False, axis_type="local", axis="X", start="head"),
        req_bones=["j_mimi_l"],
        b_collection="Face",
        settings=RigifySettings(bone_name="ear.L", rigify_type="basic.super_copy", super_copy_widget_type="bone")
    )
]

EAR_R: list[GenerativeBone] = [
    GenerativeBone(
        ref="src",
        data=ExtensionBone(name="ear.R", bone_a="j_mimi_r", parent="head", is_connected=False, axis_type="local", axis="X", start="head"),
        req_bones=["j_mimi_r"],
        b_collection="Face",
        settings=RigifySettings(bone_name="ear.R", rigify_type="basic.super_copy", super_copy_widget_type="bone")
    )
]