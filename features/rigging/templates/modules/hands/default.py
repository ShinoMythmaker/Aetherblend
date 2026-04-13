from ......core.generators import ConnectBone, ExtensionBone, CopyBone
from ......core.shared import PoseOperations, BoneGroup, TransformLink, RigModule
from ......core import rigify
from ......core.rigify.settings import UI_Collections, BoneCollection


HAND_R = BoneGroup(
    name="Right Hand",
    transform_link= [
        TransformLink(target="DEF-thumb.R", bone="j_oya_a_r"),
        TransformLink(target="DEF-thumb.R.001", bone="j_oya_b_r"),
        TransformLink(target="DEF-index.R", bone="j_hito_a_r"),
        TransformLink(target="DEF-index.R.001", bone="j_hito_b_r"),
        TransformLink(target="DEF-middle.R", bone="j_naka_a_r"),
        TransformLink(target="DEF-middle.R.001", bone="j_naka_b_r"),
        TransformLink(target="DEF-ring.R", bone="j_kusu_a_r"),
        TransformLink(target="DEF-ring.R.001", bone="j_kusu_b_r"),
        TransformLink(target="DEF-pinky.R", bone="j_ko_a_r"),
        TransformLink(target="DEF-pinky.R.001", bone="j_ko_b_r"),
    ],
    generators=[
        #Palm Control - Very cool stuff, thank you rigify - Oats
        ExtensionBone(
            name="palm.01.R",
            bone_a="j_hito_a_r",
            parent="hand.R",
            is_connected=False,
            axis_type="local",
            axis="Y",
            start="head",
            roll=135,
            req_bones=["j_hito_a_r"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.limbs_super_palm(palm_both_sides=True),
                b_collection="Fingers.R"
            )
        ),
        ExtensionBone(
            name="palm.02.R",
            bone_a="j_naka_a_r",
            parent="hand.R",
            is_connected=False,
            axis_type="local",
            axis="Y",
            start="head",
            roll=135,
            req_bones=["j_naka_a_r"],
            pose_operations=PoseOperations(
                b_collection="Fingers.R"
            )
        ),
        ExtensionBone(
            name="palm.03.R",
            bone_a="j_kusu_a_r",
            parent="hand.R",
            is_connected=False,
            axis_type="local",
            axis="Y",
            start="head",
            roll=135,
            req_bones=["j_kusu_a_r"],
            pose_operations=PoseOperations(
                b_collection="Fingers.R"
            )
        ),
        ExtensionBone(
            name="palm.04.R",
            bone_a="j_ko_a_r",
            parent="hand.R",
            is_connected=False,
            axis_type="local",
            axis="Y",
            start="head",
            roll=135,
            req_bones=["j_ko_a_r"],
            pose_operations=PoseOperations(
                b_collection="Fingers.R"
            )
        ),
        #Thumb
        CopyBone(
            name="DEF-thumb_master.R",
            source_bone="j_oya_a_r",
            parent="hand.R",
            req_bones=["hand.R", "j_oya_a_r"],
            pose_operations=PoseOperations(
                b_collection="DEF",
                rigify_settings=rigify.types.basic_raw_copy(relink_constraints=True, parent="DEF")
                )),
        ConnectBone(
            name="thumb.R",
            bone_a="j_oya_a_r",
            bone_b="j_oya_b_r",
            parent="DEF-thumb_master.R",
            is_connected=False,
            roll=-15,
            req_bones=["DEF-thumb_master.R", "j_oya_a_r", "j_oya_b_r"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.limbs_super_finger(make_extra_ik_control=True, extra_ik_layers_extra="Fingers.R (IK)"),
                b_collection="Fingers.R",
            )
        ),
        ExtensionBone(
            name="thumb.R.001",
            bone_a="j_oya_b_r",
            parent="thumb.R",
            is_connected=True,
            axis_type="local",
            axis="Y",
            start="head",
            size_factor=0.2,
            req_bones=["j_oya_b_r"],
            pose_operations=PoseOperations(
                b_collection="Fingers.R",
            )
        ),
        #Index
        ConnectBone(
            name="index.R",
            bone_a="j_hito_a_r",
            bone_b="j_hito_b_r",
            parent="palm.01.R",
            roll=135,
            is_connected=False,
            req_bones=["j_hito_a_r", "j_hito_b_r"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.limbs_super_finger(make_extra_ik_control=True, extra_ik_layers_extra="Fingers.R (IK)"),
                b_collection="Fingers.R",
            )
        ),
        ExtensionBone(
            name="index.R.001",
            bone_a="j_hito_b_r",
            parent="index.R",
            is_connected=True,
            axis_type="local",
            axis="Y",
            start="head",
            req_bones=["j_hito_b_r"],
            pose_operations=PoseOperations(
                b_collection="Fingers.R",
            )
        ),
        #Middle
        ConnectBone(
            name="middle.R",
            bone_a="j_naka_a_r",
            bone_b="j_naka_b_r",
            parent="palm.02.R",
            roll=135,
            is_connected=False,
            req_bones=["j_naka_a_r", "j_naka_b_r"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.limbs_super_finger(make_extra_ik_control=True, extra_ik_layers_extra="Fingers.R (IK)"),
                b_collection="Fingers.R",
            )
        ),
        ExtensionBone(
            name="middle.R.001",
            bone_a="j_naka_b_r",
            parent="middle.R",
            is_connected=True,
            axis_type="local",
            axis="Y",
            start="head",
            req_bones=["j_naka_b_r"],
            pose_operations=PoseOperations(
                b_collection="Fingers.R",
            )
        ),
        #Ring
        ConnectBone(
            name="ring.R",
            bone_a="j_kusu_a_r",
            bone_b="j_kusu_b_r",
            parent="palm.03.R",
            roll=135,
            is_connected=False,
            req_bones=["j_kusu_a_r", "j_kusu_b_r"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.limbs_super_finger(make_extra_ik_control=True, extra_ik_layers_extra="Fingers.R (IK)"),
                b_collection="Fingers.R",
            )
        ),
        ExtensionBone(
            name="ring.R.001",
            bone_a="j_kusu_b_r",
            parent="ring.R",
            is_connected=True,
            axis_type="local",
            axis="Y",
            start="head",
            req_bones=["j_kusu_b_r"],
            pose_operations=PoseOperations(
                b_collection="Fingers.R",
            )
        ),
        #Pinky
        ConnectBone(
            name="pinky.R",
            bone_a="j_ko_a_r",
            bone_b="j_ko_b_r",
            parent="palm.04.R",
            roll=135,
            is_connected=False,
            req_bones=["j_ko_a_r", "j_ko_b_r"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.limbs_super_finger(make_extra_ik_control=True, extra_ik_layers_extra="Fingers.R (IK)"),
                b_collection="Fingers.R",
            )
        ),
        ExtensionBone(
            name="pinky.R.001",
            bone_a="j_ko_b_r",
            parent="pinky.R",
            is_connected=True,
            axis_type="local",
            axis="Y",
            start="head",
            req_bones=["j_ko_b_r"],
            pose_operations=PoseOperations(
                b_collection="Fingers.R",
            )
        ),
    ],
)

HAND_L = BoneGroup(
        name="Left Hand",
    transform_link= [
        TransformLink(target="DEF-thumb.L", bone="j_oya_a_l"),
        TransformLink(target="DEF-thumb.L.001", bone="j_oya_b_l"),
        TransformLink(target="DEF-index.L", bone="j_hito_a_l"),
        TransformLink(target="DEF-index.L.001", bone="j_hito_b_l"),
        TransformLink(target="DEF-middle.L", bone="j_naka_a_l"),
        TransformLink(target="DEF-middle.L.001", bone="j_naka_b_l"),
        TransformLink(target="DEF-ring.L", bone="j_kusu_a_l"),
        TransformLink(target="DEF-ring.L.001", bone="j_kusu_b_l"),
        TransformLink(target="DEF-pinky.L", bone="j_ko_a_l"),
        TransformLink(target="DEF-pinky.L.001", bone="j_ko_b_l"),
    ],
    generators=[
        #Palm Control - Very cool stuff, thank you rigify - Oats
        ExtensionBone(
            name="palm.01.L",
            bone_a="j_hito_a_l",
            parent="hand.L",
            is_connected=False,
            axis_type="local",
            axis="Y",
            start="head",
            roll=-135,
            req_bones=["j_hito_a_l"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.limbs_super_palm(palm_both_sides=True),
                b_collection="Fingers.L"
            )
        ),
        ExtensionBone(
            name="palm.02.L",
            bone_a="j_naka_a_l",
            parent="hand.L",
            is_connected=False,
            axis_type="local",
            axis="Y",
            start="head",
            roll=-135,
            req_bones=["j_naka_a_l"],
            pose_operations=PoseOperations(
                b_collection="Fingers.L"
            )
        ),
        ExtensionBone(
            name="palm.03.L",
            bone_a="j_kusu_a_l",
            parent="hand.L",
            is_connected=False,
            axis_type="local",
            axis="Y",
            start="head",
            roll=-135,
            req_bones=["j_kusu_a_l"],
            pose_operations=PoseOperations(
                b_collection="Fingers.L"
            )
        ),
        ExtensionBone(
            name="palm.04.L",
            bone_a="j_ko_a_l",
            parent="hand.L",
            is_connected=False,
            axis_type="local",
            axis="Y",
            start="head",
            roll=-135,
            req_bones=["j_ko_a_l"],
            pose_operations=PoseOperations(
                b_collection="Fingers.L"
            )
        ),
        #Thumb
        CopyBone(
            name="DEF-thumb_master.L",
            source_bone="j_oya_a_l",
            parent="hand.L",
            req_bones=["hand.L", "j_oya_a_l"],
            pose_operations=PoseOperations(
                b_collection="DEF",
                rigify_settings=rigify.types.basic_raw_copy(relink_constraints=True, parent="DEF")
                )),
        ConnectBone(
            name="thumb.L",
            bone_a="j_oya_a_l",
            bone_b="j_oya_b_l",
            parent="DEF-thumb_master.L",
            is_connected=False,
            roll=-15,
            req_bones=["DEF-thumb_master.L", "j_oya_a_l", "j_oya_b_l"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.limbs_super_finger(make_extra_ik_control=True, extra_ik_layers_extra="Fingers.L (IK)"),
                b_collection="Fingers.L",
            )
        ),
        ExtensionBone(
            name="thumb.L.001",
            bone_a="j_oya_b_l",
            parent="thumb.L",
            is_connected=True,
            axis_type="local",
            axis="Y",
            start="head",
            size_factor=0.2,
            req_bones=["j_oya_b_l"],
            pose_operations=PoseOperations(
                b_collection="Fingers.L",
            )
        ),
        #Index
        ConnectBone(
            name="index.L",
            bone_a="j_hito_a_l",
            bone_b="j_hito_b_l",
            parent="palm.01.L",
            roll=-135,
            is_connected=False,
            req_bones=["j_hito_a_l", "j_hito_b_l"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.limbs_super_finger(make_extra_ik_control=True, extra_ik_layers_extra="Fingers.L (IK)"),
                b_collection="Fingers.L",
            )
        ),
        ExtensionBone(
            name="index.L.001",
            bone_a="j_hito_b_l",
            parent="index.L",
            is_connected=True,
            axis_type="local",
            axis="Y",
            start="head",
            req_bones=["j_hito_b_l"],
            pose_operations=PoseOperations(
                b_collection="Fingers.L",
            )
        ),
        #Middle
        ConnectBone(
            name="middle.L",
            bone_a="j_naka_a_l",
            bone_b="j_naka_b_l",
            parent="palm.02.L",
            roll=-135,
            is_connected=False,
            req_bones=["j_naka_a_l", "j_naka_b_l"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.limbs_super_finger(make_extra_ik_control=True, extra_ik_layers_extra="Fingers.L (IK)"),
                b_collection="Fingers.L",
            )
        ),
        ExtensionBone(
            name="middle.L.001",
            bone_a="j_naka_b_l",
            parent="middle.L",
            is_connected=True,
            axis_type="local",
            axis="Y",
            start="head",
            req_bones=["j_naka_b_l"],
            pose_operations=PoseOperations(
                b_collection="Fingers.L",
            )
        ),
        #Ring
        ConnectBone(
            name="ring.L",
            bone_a="j_kusu_a_l",
            bone_b="j_kusu_b_l",
            parent="palm.03.L",
            roll=-135,
            is_connected=False,
            req_bones=["j_kusu_a_l", "j_kusu_b_l"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.limbs_super_finger(make_extra_ik_control=True, extra_ik_layers_extra="Fingers.L (IK)"),
                b_collection="Fingers.L",
            )
        ),
        ExtensionBone(
            name="ring.L.001",
            bone_a="j_kusu_b_l",
            parent="ring.L",
            is_connected=True,
            axis_type="local",
            axis="Y",
            start="head",
            req_bones=["j_kusu_b_l"],
            pose_operations=PoseOperations(
                b_collection="Fingers.L",
            )
        ),
        #Pinky
        ConnectBone(
            name="pinky.L",
            bone_a="j_ko_a_l",
            bone_b="j_ko_b_l",
            parent="palm.04.L",
            roll=-135,
            is_connected=False,
            req_bones=["j_ko_a_l", "j_ko_b_l"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.limbs_super_finger(make_extra_ik_control=True, extra_ik_layers_extra="Fingers.L (IK)"),
                b_collection="Fingers.L",
            )
        ),
        ExtensionBone(
            name="pinky.L.001",
            bone_a="j_ko_b_l",
            parent="pinky.L",
            is_connected=True,
            axis_type="local",
            axis="Y",
            start="head",
            req_bones=["j_ko_b_l"],
            pose_operations=PoseOperations(
                b_collection="Fingers.L",
            )
        ),
    ],
)

def get_rig_module() -> RigModule:
    return RigModule(
        name="Default",
        type="Generation",
        bone_groups=[HAND_L, HAND_R],
        ui=UI_Collections([ 
            BoneCollection(name="Fingers.L", ui=True, color_set="Fingers_Left", row_index=1, title="Fingers.L", visible=False),
            BoneCollection(name="Fingers.R", ui=True, color_set="Fingers_Right", row_index=1, title="Fingers.R", visible=False),
        ])
    )