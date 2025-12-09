from .. schemas import GenerativeBone, ConnectBone, ExtensionBone, RigifySettings

THUMB_L: list[GenerativeBone] = [
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="f_thumb.L.001", bone_a="j_oya_a_l", bone_b="j_oya_b_l", parent="hand.L"),
        req_bones=["j_oya_a_l", "j_oya_b_l"],
        settings=RigifySettings(bone_name="f_thumb.L.001", rigify_type="limbs.super_finger", tweak_coll="Fingers (Details)", make_extra_ik_control=True),
        b_collection="Fingers"
    ),
    GenerativeBone(
        ref="tgt",
        data=ExtensionBone(name="f_thumb.L.002", bone_a="f_thumb.L.001", parent="f_thumb.L.001", is_connected=True, size_factor=0.6),
        req_bones=["f_thumb.L.001"],
        b_collection="Fingers"
    ),
]

POINTER_L_IV: list[GenerativeBone] = [
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="f_pointer.L.001", bone_a="j_hito_a_l", bone_b="j_hito_b_l", parent="hand.L", roll=(-135.0)),
        req_bones=["j_hito_a_l", "j_hito_b_l"],
        settings=RigifySettings(bone_name="f_pointer.L.001", rigify_type="limbs.super_finger", tweak_coll="Fingers (Details)", make_extra_ik_control=True),
        b_collection="Fingers"
    ),
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="f_pointer.L.002", bone_a="j_hito_b_l", bone_b="iv_hito_c_l", parent="f_pointer.L.001", roll=(-135.0), is_connected=True),
        req_bones=["j_hito_b_l", "iv_hito_c_l"],
        b_collection="Fingers",
    ),
    GenerativeBone(
        ref="tgt",
        data=ExtensionBone(name="f_pointer.L.003", bone_a="f_pointer.L.002", parent="f_pointer.L.002", roll=(-135.0), is_connected=True),
        req_bones=["f_pointer.L.002"],
        b_collection="Fingers"
    ),
]

POINTER_L: list[GenerativeBone] = [
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="f_pointer.L.001", bone_a="j_hito_a_l", bone_b="j_hito_b_l", parent="hand.L", roll=(-135.0)),
        req_bones=["j_hito_a_l", "j_hito_b_l"],
        settings=RigifySettings(bone_name="f_pointer.L.001", rigify_type="limbs.super_finger", tweak_coll="Fingers (Details)", make_extra_ik_control=True),
        b_collection="Fingers"
    ),
    GenerativeBone(
        ref="tgt",
        data=ExtensionBone(name="f_pointer.L.002", bone_a="f_pointer.L.001", parent="f_pointer.L.001", roll=(-135.0), is_connected=True),
        req_bones=["f_pointer.L.001"],
        b_collection="Fingers"
    ),
]

MIDDLE_L: list[GenerativeBone] = [
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="f_middle.L.001", bone_a="j_naka_a_l", bone_b="j_naka_b_l", parent="hand.L", roll=(-135.0)),
        req_bones=["j_naka_a_l", "j_naka_b_l"],
        settings=RigifySettings(bone_name="f_middle.L.001", rigify_type="limbs.super_finger", tweak_coll="Fingers (Details)", make_extra_ik_control=True),
        b_collection="Fingers"
    ),
    GenerativeBone(
        ref="tgt",
        data=ExtensionBone(name="f_middle.L.002", bone_a="f_middle.L.001", parent="f_middle.L.001", roll=(-135.0), is_connected=True),
        req_bones=["f_middle.L.001"],
        b_collection="Fingers"
    ),
]

MIDDLE_L_IV: list[GenerativeBone] = [
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="f_middle.L.001", bone_a="j_naka_a_l", bone_b="j_naka_b_l", parent="hand.L", roll=(-135.0)),
        req_bones=["j_naka_a_l", "j_naka_b_l"],
        settings=RigifySettings(bone_name="f_middle.L.001", rigify_type="limbs.super_finger", tweak_coll="Fingers (Details)", make_extra_ik_control=True),
        b_collection="Fingers"
    ),
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="f_middle.L.002", bone_a="j_naka_b_l", bone_b="iv_naka_c_l", parent="f_middle.L.001", roll=(-135.0), is_connected=True),
        req_bones=["j_naka_b_l", "iv_naka_c_l"],
        b_collection="Fingers",
        is_optional=True
    ),
    GenerativeBone(
        ref="tgt",
        data=ExtensionBone(name="f_middle.L.003", bone_a="f_middle.L.002", parent="f_middle.L.002", roll=(-135.0), is_connected=True),
        req_bones=["f_middle.L.002"],
        b_collection="Fingers"
    ),
]

RING_L: list[GenerativeBone] = [
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="f_ring.L.001", bone_a="j_kusu_a_l", bone_b="j_kusu_b_l", parent="hand.L", roll=(-135.0)),
        req_bones=["j_kusu_a_l", "j_kusu_b_l"],
        settings=RigifySettings(bone_name="f_ring.L.001", rigify_type="limbs.super_finger", tweak_coll="Fingers (Details)", make_extra_ik_control=True),
        b_collection="Fingers"
    ),
    GenerativeBone(
        ref="tgt",
        data=ExtensionBone(name="f_ring.L.002", bone_a="f_ring.L.001", parent="f_ring.L.001", roll=(-135.0), is_connected=True),
        req_bones=["f_ring.L.001"],
        b_collection="Fingers"
    ),
]

RING_L_IV: list[GenerativeBone] = [
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="f_ring.L.001", bone_a="j_kusu_a_l", bone_b="j_kusu_b_l", parent="hand.L", roll=(-135.0)),
        req_bones=["j_kusu_a_l", "j_kusu_b_l"],
        settings=RigifySettings(bone_name="f_ring.L.001", rigify_type="limbs.super_finger", tweak_coll="Fingers (Details)", make_extra_ik_control=True),
        b_collection="Fingers"
    ),
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="f_ring.L.002", bone_a="j_kusu_b_l", bone_b="iv_kusu_c_l", parent="f_ring.L.001", roll=(-135.0), is_connected=True),
        req_bones=["j_kusu_b_l", "iv_kusu_c_l"],
        b_collection="Fingers",
        is_optional=True
    ),
    GenerativeBone(
        ref="tgt",
        data=ExtensionBone(name="f_ring.L.003", bone_a="f_ring.L.002", parent="f_ring.L.002", roll=(-135.0), is_connected=True),
        req_bones=["f_ring.L.002"],
        b_collection="Fingers"
    ),
]

PINKY_L: list[GenerativeBone] = [
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="f_pinky.L.001", bone_a="j_ko_a_l", bone_b="j_ko_b_l", parent="hand.L", roll=(-135.0)),
        req_bones=["j_ko_a_l", "j_ko_b_l"],
        settings=RigifySettings(bone_name="f_pinky.L.001", rigify_type="limbs.super_finger", tweak_coll="Fingers (Details)", make_extra_ik_control=True),
        b_collection="Fingers"
    ),
    GenerativeBone(
        ref="tgt",
        data=ExtensionBone(name="f_pinky.L.002", bone_a="f_pinky.L.001", parent="f_pinky.L.001", roll=(-135.0), is_connected=True),
        req_bones=["f_pinky.L.001"],
        b_collection="Fingers"
    ),
]

PINKY_L_IV: list[GenerativeBone] = [
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="f_pinky.L.001", bone_a="j_ko_a_l", bone_b="j_ko_b_l", parent="hand.L", roll=(-135.0)),
        req_bones=["j_ko_a_l", "j_ko_b_l"],
        settings=RigifySettings(bone_name="f_pinky.L.001", rigify_type="limbs.super_finger", tweak_coll="Fingers (Details)", make_extra_ik_control=True),
        b_collection="Fingers"
    ),
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="f_pinky.L.002", bone_a="j_ko_b_l", bone_b="iv_ko_c_l", parent="f_pinky.L.001", roll=(-135.0), is_connected=True),
        req_bones=["j_ko_b_l", "iv_ko_c_l"],
        b_collection="Fingers",
        is_optional=True
    ),
    GenerativeBone(
        ref="tgt",
        data=ExtensionBone(name="f_pinky.L.003", bone_a="f_pinky.L.002", parent="f_pinky.L.002", roll=(-135.0), is_connected=True),
        req_bones=["f_pinky.L.002"],
        b_collection="Fingers"
    ),
]

THUMB_R: list[GenerativeBone] = [
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="f_thumb.R.001", bone_a="j_oya_a_r", bone_b="j_oya_b_r", parent="hand.R"),
        req_bones=["j_oya_a_r", "j_oya_b_r"],
        settings=RigifySettings(bone_name="f_thumb.R.001", rigify_type="limbs.super_finger", tweak_coll="Fingers (Details)", make_extra_ik_control=True),
        b_collection="Fingers"
    ),
    GenerativeBone(
        ref="tgt",
        data=ExtensionBone(name="f_thumb.R.002", bone_a="f_thumb.R.001", parent="f_thumb.R.001", is_connected=True, size_factor=0.6),
        req_bones=["f_thumb.R.001"],
        b_collection="Fingers"
    ),
]

POINTER_R: list[GenerativeBone] = [
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="f_pointer.R.001", bone_a="j_hito_a_r", bone_b="j_hito_b_r", parent="hand.R", roll=(135.0)),
        req_bones=["j_hito_a_r", "j_hito_b_r"],
        settings=RigifySettings(bone_name="f_pointer.R.001", rigify_type="limbs.super_finger", tweak_coll="Fingers (Details)", make_extra_ik_control=True),
        b_collection="Fingers"
    ),
    GenerativeBone(
        ref="tgt",
        data=ExtensionBone(name="f_pointer.R.002", bone_a="f_pointer.R.001", parent="f_pointer.R.001", roll=(135.0), is_connected=True),
        req_bones=["f_pointer.R.001"],
        b_collection="Fingers"
    ),
]

POINTER_R_IV: list[GenerativeBone] = [
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="f_pointer.R.001", bone_a="j_hito_a_r", bone_b="j_hito_b_r", parent="hand.R", roll=(135.0)),
        req_bones=["j_hito_a_r", "j_hito_b_r"],
        settings=RigifySettings(bone_name="f_pointer.R.001", rigify_type="limbs.super_finger", tweak_coll="Fingers (Details)", make_extra_ik_control=True),
        b_collection="Fingers"
    ),
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="f_pointer.R.002", bone_a="j_hito_b_r", bone_b="iv_hito_c_r", parent="f_pointer.R.001", roll=(135.0), is_connected=True),
        req_bones=["j_hito_b_r", "iv_hito_c_r"],
        b_collection="Fingers",
        is_optional=True
    ),
    GenerativeBone(
        ref="tgt",
        data=ExtensionBone(name="f_pointer.R.003", bone_a="f_pointer.R.002", parent="f_pointer.R.002", roll=(135.0), is_connected=True),
        req_bones=["f_pointer.R.002"],
        b_collection="Fingers"
    ),
]

MIDDLE_R: list[GenerativeBone] = [
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="f_middle.R.001", bone_a="j_naka_a_r", bone_b="j_naka_b_r", parent="hand.R", roll=(135.0)),
        req_bones=["j_naka_a_r", "j_naka_b_r"],
        settings=RigifySettings(bone_name="f_middle.R.001", rigify_type="limbs.super_finger", tweak_coll="Fingers (Details)", make_extra_ik_control=True),
        b_collection="Fingers"
    ),
    GenerativeBone(
        ref="tgt",
        data=ExtensionBone(name="f_middle.R.002", bone_a="f_middle.R.001", parent="f_middle.R.001", roll=(135.0), is_connected=True),
        req_bones=["f_middle.R.001"],
        b_collection="Fingers"
    ),
]

MIDDLE_R_IV: list[GenerativeBone] = [
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="f_middle.R.001", bone_a="j_naka_a_r", bone_b="j_naka_b_r", parent="hand.R", roll=(135.0)),
        req_bones=["j_naka_a_r", "j_naka_b_r"],
        settings=RigifySettings(bone_name="f_middle.R.001", rigify_type="limbs.super_finger", tweak_coll="Fingers (Details)", make_extra_ik_control=True),
        b_collection="Fingers"
    ),
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="f_middle.R.002", bone_a="j_naka_b_r", bone_b="iv_naka_c_r", parent="f_middle.R.001", roll=(135.0), is_connected=True),
        req_bones=["j_naka_b_r", "iv_naka_c_r"],
        b_collection="Fingers",
        is_optional=True
    ),
    GenerativeBone(
        ref="tgt",
        data=ExtensionBone(name="f_middle.R.003", bone_a="f_middle.R.002", parent="f_middle.R.002", roll=(135.0), is_connected=True),
        req_bones=["f_middle.R.002"],
        b_collection="Fingers"
    ),
]

RING_R: list[GenerativeBone] = [
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="f_ring.R.001", bone_a="j_kusu_a_r", bone_b="j_kusu_b_r", parent="hand.R", roll=(135.0)),
        req_bones=["j_kusu_a_r", "j_kusu_b_r"],
        settings=RigifySettings(bone_name="f_ring.R.001", rigify_type="limbs.super_finger", tweak_coll="Fingers (Details)", make_extra_ik_control=True),
        b_collection="Fingers"
    ),
    GenerativeBone(
        ref="tgt",
        data=ExtensionBone(name="f_ring.R.002", bone_a="f_ring.R.001", parent="f_ring.R.001", roll=(135.0), is_connected=True),
        req_bones=["f_ring.R.001"],
        b_collection="Fingers"
    ),
]

RING_R_IV: list[GenerativeBone] = [
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="f_ring.R.001", bone_a="j_kusu_a_r", bone_b="j_kusu_b_r", parent="hand.R", roll=(135.0)),
        req_bones=["j_kusu_a_r", "j_kusu_b_r"],
        settings=RigifySettings(bone_name="f_ring.R.001", rigify_type="limbs.super_finger", tweak_coll="Fingers (Details)", make_extra_ik_control=True),
        b_collection="Fingers"
    ),
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="f_ring.R.002", bone_a="j_kusu_b_r", bone_b="iv_kusu_c_r", parent="f_ring.R.001", roll=(135.0), is_connected=True),
        req_bones=["j_kusu_b_r", "iv_kusu_c_r"],
        b_collection="Fingers",
        is_optional=True
    ),
    GenerativeBone(
        ref="tgt",
        data=ExtensionBone(name="f_ring.R.003", bone_a="f_ring.R.002", parent="f_ring.R.002", roll=(135.0), is_connected=True),
        req_bones=["f_ring.R.002"],
        b_collection="Fingers"
    ),
]

PINKY_R: list[GenerativeBone] = [
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="f_pinky.R.001", bone_a="j_ko_a_r", bone_b="j_ko_b_r", parent="hand.R", roll=(135.0)),
        req_bones=["j_ko_a_r", "j_ko_b_r"],
        settings=RigifySettings(bone_name="f_pinky.R.001", rigify_type="limbs.super_finger", tweak_coll="Fingers (Details)", make_extra_ik_control=True),
        b_collection="Fingers"
    ),
    GenerativeBone(
        ref="tgt",
        data=ExtensionBone(name="f_pinky.R.002", bone_a="f_pinky.R.001", parent="f_pinky.R.001", roll=(135.0), is_connected=True),
        req_bones=["f_pinky.R.001"],
        b_collection="Fingers"
    ),
]

PINKY_R_IV: list[GenerativeBone] = [
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="f_pinky.R.001", bone_a="j_ko_a_r", bone_b="j_ko_b_r", parent="hand.R", roll=(135.0)),
        req_bones=["j_ko_a_r", "j_ko_b_r"],
        settings=RigifySettings(bone_name="f_pinky.R.001", rigify_type="limbs.super_finger", tweak_coll="Fingers (Details)", make_extra_ik_control=True),
        b_collection="Fingers"
    ),
    GenerativeBone(
        ref="src",
        data=ConnectBone(name="f_pinky.R.002", bone_a="j_ko_b_r", bone_b="iv_ko_c_r", parent="f_pinky.R.001", roll=(135.0), is_connected=True),
        req_bones=["j_ko_b_r", "iv_ko_c_r"],
        b_collection="Fingers",
        is_optional=True
    ),
    GenerativeBone(
        ref="tgt",
        data=ExtensionBone(name="f_pinky.R.003", bone_a="f_pinky.R.002", parent="f_pinky.R.002", roll=(135.0), is_connected=True),
        req_bones=["f_pinky.R.002"],
        b_collection="Fingers"
    ),
]

