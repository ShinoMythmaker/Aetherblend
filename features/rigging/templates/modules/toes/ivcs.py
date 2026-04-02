from ......core.generators import ConnectBone, ExtensionBone
from ......core.shared import PoseOperations, BoneGroup, RigModule, TransformLink
from ......core import rigify

IV_TOES = BoneGroup(
    name="IVCS Toes",
    transform_link=[
        TransformLink(target="DEF-Hallux_Toe.R", bone="iv_asi_oya_a_r"),
        TransformLink(target="DEF-Hallux_Toe.R.001", bone="iv_asi_oya_b_r"),
        TransformLink(target="DEF-Index_Toe.R", bone="iv_asi_hito_a_r"),
        TransformLink(target="DEF-Index_Toe.R.001", bone="iv_asi_hito_b_r"),
        TransformLink(target="DEF-Middle_Toe.R", bone="iv_asi_naka_a_r"),
        TransformLink(target="DEF-Middle_Toe.R.001", bone="iv_asi_naka_b_r"),
        TransformLink(target="DEF-Ring_Toe.R", bone="iv_asi_kusu_a_r"),
        TransformLink(target="DEF-Ring_Toe.R.001", bone="iv_asi_kusu_b_r"),
        TransformLink(target="DEF-Pinky_Toe.R", bone="iv_asi_ko_a_r"),
        TransformLink(target="DEF-Pinky_Toe.R.001", bone="iv_asi_ko_b_r"),
        TransformLink(target="DEF-Hallux_Toe.L", bone="iv_asi_oya_a_l"),
        TransformLink(target="DEF-Hallux_Toe.L.001", bone="iv_asi_oya_b_l"),
        TransformLink(target="DEF-Index_Toe.L", bone="iv_asi_hito_a_l"),
        TransformLink(target="DEF-Index_Toe.L.001", bone="iv_asi_hito_b_l"),
        TransformLink(target="DEF-Middle_Toe.L", bone="iv_asi_naka_a_l"),
        TransformLink(target="DEF-Middle_Toe.L.001", bone="iv_asi_naka_b_l"),
        TransformLink(target="DEF-Ring_Toe.L", bone="iv_asi_kusu_a_l"),
        TransformLink(target="DEF-Ring_Toe.L.001", bone="iv_asi_kusu_b_l"),
        TransformLink(target="DEF-Pinky_Toe.L", bone="iv_asi_ko_a_l"),
        TransformLink(target="DEF-Pinky_Toe.L.001", bone="iv_asi_ko_b_l"),
    ],
    bones=[
        #Toes Right
        ConnectBone(
            name="Hallux_Toe.R",
            bone_a="iv_asi_oya_a_r",
            bone_b="iv_asi_oya_b_r",
            parent="j_asi_e_r",
            is_connected=False,
            req_bones=["iv_asi_oya_a_r", "iv_asi_oya_b_r"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.limbs_super_finger(),
                b_collection="IVCS",
            )
        ),
        ExtensionBone(
            name="Hallux_Toe.R.001",
            bone_a="iv_asi_oya_b_r",
            parent="Hallux_Toe.R",
            is_connected=True,
            axis_type="local",
            axis="Y",
            req_bones=["iv_asi_oya_b_r"],
            pose_operations=PoseOperations(
                b_collection="IVCS"
            )
        ),
        ConnectBone(
            name="Index_Toe.R",
            bone_a="iv_asi_hito_a_r",
            bone_b="iv_asi_hito_b_r",
            parent="j_asi_e_r",
            is_connected=False,
            req_bones=["iv_asi_hito_a_r", "iv_asi_hito_b_r"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.limbs_super_finger(),
                b_collection="IVCS",
            )
        ),
        ExtensionBone(
            name="Index_Toe.R.001",
            bone_a="iv_asi_hito_b_r",
            parent="Index_Toe.R",
            is_connected=True,
            axis_type="local",
            axis="Y",
            req_bones=["iv_asi_hito_b_r"],
            pose_operations=PoseOperations(
                b_collection="IVCS"
            )
        ),
        ConnectBone(
            name="Middle_Toe.R",
            bone_a="iv_asi_naka_a_r",
            bone_b="iv_asi_naka_b_r",
            parent="j_asi_e_r",
            is_connected=False,
            req_bones=["iv_asi_naka_a_r", "iv_asi_naka_b_r"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.limbs_super_finger(),
                b_collection="IVCS",
            )
        ),
        ExtensionBone(
            name="Middle_Toe.R.001",
            bone_a="iv_asi_naka_b_r",
            parent="Middle_Toe.R",
            is_connected=True,
            axis_type="local",
            axis="Y",
            req_bones=["iv_asi_naka_b_r"],
            pose_operations=PoseOperations(
                b_collection="IVCS"
            )
        ),
        ConnectBone(
            name="Ring_Toe.R",
            bone_a="iv_asi_kusu_a_r",
            bone_b="iv_asi_kusu_b_r",
            parent="j_asi_e_r",
            is_connected=False,
            req_bones=["iv_asi_kusu_a_r", "iv_asi_kusu_b_r"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.limbs_super_finger(),
                b_collection="IVCS",
            )
        ),
        ExtensionBone(
            name="Ring_Toe.R.001",
            bone_a="iv_asi_kusu_b_r",
            parent="Ring_Toe.R",
            is_connected=True,
            axis_type="local",
            axis="Y",
            req_bones=["iv_asi_kusu_b_r"],
            pose_operations=PoseOperations(
                b_collection="IVCS"
            )
        ),
        ConnectBone(
            name="Pinky_Toe.R",
            bone_a="iv_asi_ko_a_r",
            bone_b="iv_asi_ko_b_r",
            parent="j_asi_e_r",
            is_connected=False,
            req_bones=["iv_asi_ko_a_r", "iv_asi_ko_b_r"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.limbs_super_finger(),
                b_collection="IVCS",
            )
        ),
        ExtensionBone(
            name="Pinky_Toe.R.001",
            bone_a="iv_asi_ko_b_r",
            parent="Pinky_Toe.R",
            is_connected=True,
            axis_type="local",
            axis="Y",
            req_bones=["iv_asi_ko_b_r"],
            pose_operations=PoseOperations(
                b_collection="IVCS"
            )
        ),
        #Toes Left
        ConnectBone(
            name="Hallux_Toe.L",
            bone_a="iv_asi_oya_a_l",
            bone_b="iv_asi_oya_b_l",
            parent="j_asi_e_l",
            is_connected=False,
            req_bones=["iv_asi_oya_a_l", "iv_asi_oya_b_l"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.limbs_super_finger(),
                b_collection="IVCS",
            )
        ),
        ExtensionBone(
            name="Hallux_Toe.L.001",
            bone_a="iv_asi_oya_b_l",
            parent="Hallux_Toe.L",
            is_connected=True,
            axis_type="local",
            axis="Y",
            req_bones=["iv_asi_oya_b_l"],
            pose_operations=PoseOperations(
                b_collection="IVCS"
            )
        ),
        ConnectBone(
            name="Index_Toe.L",
            bone_a="iv_asi_hito_a_l",
            bone_b="iv_asi_hito_b_l",
            parent="j_asi_e_l",
            is_connected=False,
            req_bones=["iv_asi_hito_a_l", "iv_asi_hito_b_l"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.limbs_super_finger(),
                b_collection="IVCS",
            )
        ),
        ExtensionBone(
            name="Index_Toe.L.001",
            bone_a="iv_asi_hito_b_l",
            parent="Index_Toe.L",
            is_connected=True,
            axis_type="local",
            axis="Y",
            req_bones=["iv_asi_hito_b_l"],
            pose_operations=PoseOperations(
                b_collection="IVCS"
            )
        ),
        ConnectBone(
            name="Middle_Toe.L",
            bone_a="iv_asi_naka_a_l",
            bone_b="iv_asi_naka_b_l",
            parent="j_asi_e_l",
            is_connected=False,
            req_bones=["iv_asi_naka_a_l", "iv_asi_naka_b_l"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.limbs_super_finger(),
                b_collection="IVCS",
            )
        ),
        ExtensionBone(
            name="Middle_Toe.L.001",
            bone_a="iv_asi_naka_b_l",
            parent="Middle_Toe.L",
            is_connected=True,
            axis_type="local",
            axis="Y",
            req_bones=["iv_asi_naka_b_l"],
            pose_operations=PoseOperations(
                b_collection="IVCS"
            )
        ),
        ConnectBone(
            name="Ring_Toe.L",
            bone_a="iv_asi_kusu_a_l",
            bone_b="iv_asi_kusu_b_l",
            parent="j_asi_e_l",
            is_connected=False,
            req_bones=["iv_asi_kusu_a_l", "iv_asi_kusu_b_l"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.limbs_super_finger(),
                b_collection="IVCS",
            )
        ),
        ExtensionBone(
            name="Ring_Toe.L.001",
            bone_a="iv_asi_kusu_b_l",
            parent="Ring_Toe.L",
            is_connected=True,
            axis_type="local",
            axis="Y",
            req_bones=["iv_asi_kusu_b_l"],
            pose_operations=PoseOperations(
                b_collection="IVCS"
            )
        ),
        ConnectBone(
            name="Pinky_Toe.L",
            bone_a="iv_asi_ko_a_l",
            bone_b="iv_asi_ko_b_l",
            parent="j_asi_e_l",
            is_connected=False,
            req_bones=["iv_asi_ko_a_l", "iv_asi_ko_b_l"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.limbs_super_finger(),
                b_collection="IVCS",
            )
        ),
        ExtensionBone(
            name="Pinky_Toe.L.001",
            bone_a="iv_asi_ko_b_l",
            parent="Pinky_Toe.L",
            is_connected=True,
            axis_type="local",
            axis="Y",
            req_bones=["iv_asi_ko_b_l"],
            pose_operations=PoseOperations(
                b_collection="IVCS"
            )
        ),
    ]
)

def get_rig_module() -> RigModule:
    rig_module = RigModule(
        name="IVCS Toes",
        type="toes",
        bone_groups=[IV_TOES]
    )
    return rig_module