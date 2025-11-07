import mathutils

from .. schemas import GenerativeBone, ConnectBone, ExtensionBone, RigifySettings, EyeBone, SkinBone, BridgeBone

LEFT_HAND: list[GenerativeBone] = [
    #Thumb L
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="f_thumb.L01", bone_a="j_oya_a_l", bone_b="j_oya_b_l", parent="hand.L"),
        req_bones=["j_oya_a_l", "j_oya_b_l"],
        settings=RigifySettings(bone_name="f_thumb.L01", rigify_type="limbs.super_finger", tweak_coll="Fingers (Details)", make_extra_ik_control=True),
        b_collection="Fingers"
    ),
    GenerativeBone(
        ref="tgt",
        data=ExtensionBone(name="f_thumb.L02", bone_a="f_thumb.L01", parent="f_thumb.L01", is_connected=True),
        req_bones=["f_thumb.L01"],
        b_collection="Fingers"
    ),

    #Pointer L
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="f_pointer.L01", bone_a="j_hito_a_l", bone_b="j_hito_b_l", parent="hand.L", roll=(-135.0)),
        req_bones=["j_hito_a_l", "j_hito_b_l"],
        settings=RigifySettings(bone_name="f_pointer.L01", rigify_type="limbs.super_finger", tweak_coll="Fingers (Details)", make_extra_ik_control=True),
        b_collection="Fingers"
    ),
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="f_pointer.L02", bone_a="j_hito_b_l", bone_b="iv_hito_c_l", parent="f_pointer.L01", roll=(-135.0), is_connected=True),
        req_bones=["j_hito_b_l", "iv_hito_c_l"],
        b_collection="Fingers",
        is_optional=True
    ),
    GenerativeBone(
        ref="tgt",
        data=ExtensionBone(name=["f_pointer.L03", "f_pointer.L02"], bone_a=["f_pointer.L02", "f_pointer.L01"], parent=["f_pointer.L02", "f_pointer.L01"], roll=(-135.0), is_connected=True),
        req_bones=["f_pointer.L01"],
        b_collection="Fingers"
    ),

    #Middle L
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="f_middle.L01", bone_a="j_naka_a_l", bone_b="j_naka_b_l", parent="hand.L", roll=(-135.0)),
        req_bones=["j_naka_a_l", "j_naka_b_l"],
        settings=RigifySettings(bone_name="f_middle.L01", rigify_type="limbs.super_finger", tweak_coll="Fingers (Details)", make_extra_ik_control=True),
        b_collection="Fingers"
    ),
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="f_middle.L02", bone_a="j_naka_b_l", bone_b="iv_naka_c_l", parent="f_middle.L01", roll=(-135.0), is_connected=True),
        req_bones=["j_naka_b_l", "iv_naka_c_l"],
        b_collection="Fingers",
        is_optional=True
    ),
    GenerativeBone(
        ref="tgt",
        data=ExtensionBone(name=["f_middle.L03", "f_middle.L02"], bone_a=["f_middle.L02", "f_middle.L01"], parent=["f_middle.L02", "f_middle.L01"], roll=(-135.0), is_connected=True),
        req_bones=["f_middle.L01"],
        b_collection="Fingers"
    ),

    #Ring L
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="f_ring.L01", bone_a="j_kusu_a_l", bone_b="j_kusu_b_l", parent="hand.L", roll=(-135.0)),
        req_bones=["j_kusu_a_l", "j_kusu_b_l"],
        settings=RigifySettings(bone_name="f_ring.L01", rigify_type="limbs.super_finger", tweak_coll="Fingers (Details)", make_extra_ik_control=True),
        b_collection="Fingers"
    ),
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="f_ring.L02", bone_a="j_kusu_b_l", bone_b="iv_kusu_c_l", parent="f_ring.L01", roll=(-135.0), is_connected=True),
        req_bones=["j_kusu_b_l", "iv_kusu_c_l"],
        b_collection="Fingers",
        is_optional=True
    ),
    GenerativeBone(
        ref="tgt",
        data=ExtensionBone(name=["f_ring.L03", "f_ring.L02"], bone_a=["f_ring.L02", "f_ring.L01"], parent=["f_ring.L02", "f_ring.L01"], roll=(-135.0), is_connected=True),
        req_bones=["f_ring.L01"],
        b_collection="Fingers"
    ),

    #Pinky L
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="f_pinky.L01", bone_a="j_ko_a_l", bone_b="j_ko_b_l", parent="hand.L", roll=(-135.0)),
        req_bones=["j_ko_a_l", "j_ko_b_l"],
        settings=RigifySettings(bone_name="f_pinky.L01", rigify_type="limbs.super_finger", tweak_coll="Fingers (Details)", make_extra_ik_control=True),
        b_collection="Fingers"
    ),
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="f_pinky.L02", bone_a="j_ko_b_l", bone_b="iv_ko_c_l", parent="f_pinky.L01", roll=(-135.0), is_connected=True),
        req_bones=["j_ko_b_l", "iv_ko_c_l"],
        b_collection="Fingers",
        is_optional=True
    ),
    GenerativeBone(
        ref="tgt",
        data=ExtensionBone(name=["f_pinky.L03", "f_pinky.L02"], bone_a=["f_pinky.L02", "f_pinky.L01"], parent=["f_pinky.L02", "f_pinky.L01"], roll=(-135.0), is_connected=True),
        req_bones=["f_pinky.L01"],
        b_collection="Fingers"
    ),
]

RIGHT_HAND: list[GenerativeBone] = [
    #Thumb R
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="f_thumb.R01", bone_a="j_oya_a_r", bone_b="j_oya_b_r", parent="hand.R"),
        req_bones=["j_oya_a_r", "j_oya_b_r"],
        settings=RigifySettings(bone_name="f_thumb.R01", rigify_type="limbs.super_finger", tweak_coll="Fingers (Details)", make_extra_ik_control=True),
        b_collection="Fingers"
    ),
    GenerativeBone(
        ref="tgt",
        data=ExtensionBone(name="f_thumb.R02", bone_a="f_thumb.R01", parent="f_thumb.R01", is_connected=True),
        req_bones=["f_thumb.R01"],
        b_collection="Fingers"
    ),

    #Pointer R
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="f_pointer.R01", bone_a="j_hito_a_r", bone_b="j_hito_b_r", parent="hand.R", roll=(135.0)),
        req_bones=["j_hito_a_r", "j_hito_b_r"],
        settings=RigifySettings(bone_name="f_pointer.R01", rigify_type="limbs.super_finger", tweak_coll="Fingers (Details)", make_extra_ik_control=True),
        b_collection="Fingers"
    ),
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="f_pointer.R02", bone_a="j_hito_b_r", bone_b="iv_hito_c_r", parent="f_pointer.R01", roll=(135.0), is_connected=True),
        req_bones=["j_hito_b_r", "iv_hito_c_r"],
        b_collection="Fingers",
        is_optional=True
    ),
    GenerativeBone(
        ref="tgt",
        data=ExtensionBone(name=["f_pointer.R03", "f_pointer.R02"], bone_a=["f_pointer.R02", "f_pointer.R01"], parent=["f_pointer.R02", "f_pointer.R01"], roll=(135.0), is_connected=True),
        req_bones=["f_pointer.R01"],
        b_collection="Fingers"
    ),

    #Middle R
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="f_middle.R01", bone_a="j_naka_a_r", bone_b="j_naka_b_r", parent="hand.R", roll=(135.0)),
        req_bones=["j_naka_a_r", "j_naka_b_r"],
        settings=RigifySettings(bone_name="f_middle.R01", rigify_type="limbs.super_finger", tweak_coll="Fingers (Details)", make_extra_ik_control=True),
        b_collection="Fingers"
    ),
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="f_middle.R02", bone_a="j_naka_b_r", bone_b="iv_naka_c_r", parent="f_middle.R01", roll=(135.0), is_connected=True),
        req_bones=["j_naka_b_r", "iv_naka_c_r"],
        b_collection="Fingers",
        is_optional=True
    ),
    GenerativeBone(
        ref="tgt",
        data=ExtensionBone(name=["f_middle.R03", "f_middle.R02"], bone_a=["f_middle.R02", "f_middle.R01"], parent=["f_middle.R02", "f_middle.R01"], roll=(135.0), is_connected=True),
        req_bones=["f_middle.R01"],
        b_collection="Fingers"
    ),

    #Ring R
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="f_ring.R01", bone_a="j_kusu_a_r", bone_b="j_kusu_b_r", parent="hand.R", roll=(135.0)),
        req_bones=["j_kusu_a_r", "j_kusu_b_r"],
        settings=RigifySettings(bone_name="f_ring.R01", rigify_type="limbs.super_finger", tweak_coll="Fingers (Details)", make_extra_ik_control=True),
        b_collection="Fingers"
    ),
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="f_ring.R02", bone_a="j_kusu_b_r", bone_b="iv_kusu_c_r", parent="f_ring.R01", roll=(135.0), is_connected=True),
        req_bones=["j_kusu_b_r", "iv_kusu_c_r"],
        b_collection="Fingers",
        is_optional=True
    ),
    GenerativeBone(
        ref="tgt",
        data=ExtensionBone(name=["f_ring.R03", "f_ring.R02"], bone_a=["f_ring.R02", "f_ring.R01"], parent=["f_ring.R02", "f_ring.R01"], roll=(135.0), is_connected=True),
        req_bones=["f_ring.R01"],
        b_collection="Fingers"
    ),

    #Pinky R
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="f_pinky.R01", bone_a="j_ko_a_r", bone_b="j_ko_b_r", parent="hand.R", roll=(135.0)),
        req_bones=["j_ko_a_r", "j_ko_b_r"],
        settings=RigifySettings(bone_name="f_pinky.R01", rigify_type="limbs.super_finger", tweak_coll="Fingers (Details)", make_extra_ik_control=True),
        b_collection="Fingers"
    ),
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="f_pinky.R02", bone_a="j_ko_b_r", bone_b="iv_ko_c_r", parent="f_pinky.R01", roll=(135.0), is_connected=True),
        req_bones=["j_ko_b_r", "iv_ko_c_r"],
        b_collection="Fingers",
        is_optional=True
    ),
    GenerativeBone(
        ref="tgt",
        data=ExtensionBone(name=["f_pinky.R03", "f_pinky.R02"], bone_a=["f_pinky.R02", "f_pinky.R01"], parent=["f_pinky.R02", "f_pinky.R01"], roll=(135.0), is_connected=True),
        req_bones=["f_pinky.R01"],
        b_collection="Fingers"
    ),
]

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
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="neck", bone_a="j_kubi", bone_b="j_kao", parent="spine.03", is_connected=False),
        req_bones=["j_kubi", "j_kao"],
        settings=RigifySettings(bone_name="neck", rigify_type="basic.super_copy", super_copy_widget_type="circle"),
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

EYES_GEN_INFO: dict[list[str, str], EyeBone] = {
    ("Face (Secondary)", "Eye.L"): EyeBone(
        outer_bones=[
            SkinBone(bone_a="j_f_mabup_02out_l", name="lid.T.L"),
            SkinBone(bone_a="j_f_mabup_01_l", name="lid.T.L.002"),
            SkinBone(bone_a="j_f_mabdn_03in_l", name="lid.B.L"),
            SkinBone(bone_a="j_f_mabdn_01_l", name="lid.B.L.002"),
        ],
        bridges=[
            BridgeBone(bone_a="lid.T.L", bone_b="lid.T.L.002", segments=1, offset_factor=mathutils.Vector((0.0, -0.001, 0.001)), is_connected=True),
            BridgeBone(bone_a="lid.T.L.002", bone_b="lid.B.L", segments=1, offset_factor=mathutils.Vector((0.0, 0.0, 0.003)), is_connected=False),
            BridgeBone(bone_a="lid.B.L", bone_b="lid.B.L.002", segments=1, offset_factor=mathutils.Vector((-0.002, 0.0, 0.001)), is_connected=True),
            BridgeBone(bone_a="lid.B.L.002", bone_b="lid.T.L", segments=1, offset_factor=mathutils.Vector((0.003, -0.001, -0.003)), is_connected=False),
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
            SkinBone(bone_a="j_f_mabup_02out_r", name="lid.T.R"),
            SkinBone(bone_a="j_f_mabup_01_r", name="lid.T.R.002"),
            SkinBone(bone_a="j_f_mabdn_03in_r", name="lid.B.R"),
            SkinBone(bone_a="j_f_mabdn_01_r", name="lid.B.R.002"),
        ],
        bridges=[
            BridgeBone(bone_a="lid.T.R", bone_b="lid.T.R.002", segments=1, offset_factor=mathutils.Vector((0.0, -0.001, 0.001)), is_connected=True),
            BridgeBone(bone_a="lid.T.R.002", bone_b="lid.B.R", segments=1, offset_factor=mathutils.Vector((0.0, 0.0, 0.003)), is_connected=False),
            BridgeBone(bone_a="lid.B.R", bone_b="lid.B.R.002", segments=1, offset_factor=mathutils.Vector((0.002, 0.0, 0.001)), is_connected=True),
            BridgeBone(bone_a="lid.B.R.002", bone_b="lid.T.R", segments=1, offset_factor=mathutils.Vector((-0.003, -0.001, -0.003)), is_connected=False),
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


