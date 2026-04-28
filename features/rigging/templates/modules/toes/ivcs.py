from ......core.bone_generators import ConnectBone, ExtensionBone
from ......core.shared import PoseOperations, BoneGroup, RigModule, TransformLink
from ......core.operations import ParentBoneOperation, RigifyTypeOperation, CollectionOperation
from ......core import rigify
from ......core.rigify.settings import UI_Collections, BoneCollection

IV_TOES_R = BoneGroup(
    name="IVCS Toes Right",
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
    ],
    generators=[
        #Toes Right
        ConnectBone(
            name="Hallux_Toe.R",
            bone_a="iv_asi_oya_a_r",
            bone_b="iv_asi_oya_b_r",
            parent="toe.R",
            is_connected=False,
            req_bones=["iv_asi_oya_a_r", "iv_asi_oya_b_r"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Hallux_Toe.R", parent=["toe.R", "j_asi_e_r"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Hallux_Toe.R", rigify_type=rigify.types.limbs_super_finger()),
                        CollectionOperation(time="Pre", bone_name="Hallux_Toe.R", collection_name="IVCS_Toes.R"),
            ]
        ),
        ExtensionBone(
            name="Hallux_Toe.R.001",
            bone_a="iv_asi_oya_b_r",
            parent="Hallux_Toe.R",
            is_connected=True,
            axis_type="local",
            axis="Y",
            req_bones=["iv_asi_oya_b_r"],
            operations=[CollectionOperation(time="Pre", bone_name="Hallux_Toe.R.001", collection_name="IVCS_Toes.R")]
        ),
        ConnectBone(
            name="Index_Toe.R",
            bone_a="iv_asi_hito_a_r",
            bone_b="iv_asi_hito_b_r",
            parent="toe.R",
            is_connected=False,
            req_bones=["iv_asi_hito_a_r", "iv_asi_hito_b_r"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Index_Toe.R", parent=["toe.R", "j_asi_e_r"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Index_Toe.R", rigify_type=rigify.types.limbs_super_finger()),
                        CollectionOperation(time="Pre", bone_name="Index_Toe.R", collection_name="IVCS_Toes.R"),
            ]
        ),
        ExtensionBone(
            name="Index_Toe.R.001",
            bone_a="iv_asi_hito_b_r",
            parent="Index_Toe.R",
            is_connected=True,
            axis_type="local",
            axis="Y",
            req_bones=["iv_asi_hito_b_r"],
            operations=[CollectionOperation(time="Pre", bone_name="Index_Toe.R.001", collection_name="IVCS_Toes.R")]
        ),
        ConnectBone(
            name="Middle_Toe.R",
            bone_a="iv_asi_naka_a_r",
            bone_b="iv_asi_naka_b_r",
            parent="toe.R",
            is_connected=False,
            req_bones=["iv_asi_naka_a_r", "iv_asi_naka_b_r"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Middle_Toe.R", parent=["toe.R", "j_asi_e_r"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Middle_Toe.R", rigify_type=rigify.types.limbs_super_finger()),
                        CollectionOperation(time="Pre", bone_name="Middle_Toe.R", collection_name="IVCS_Toes.R"),
            ]
        ),
        ExtensionBone(
            name="Middle_Toe.R.001",
            bone_a="iv_asi_naka_b_r",
            parent="Middle_Toe.R",
            is_connected=True,
            axis_type="local",
            axis="Y",
            req_bones=["iv_asi_naka_b_r"],
            operations=[CollectionOperation(time="Pre", bone_name="Middle_Toe.R.001", collection_name="IVCS_Toes.R")]
        ),
        ConnectBone(
            name="Ring_Toe.R",
            bone_a="iv_asi_kusu_a_r",
            bone_b="iv_asi_kusu_b_r",
            parent="toe.R",
            is_connected=False,
            req_bones=["iv_asi_kusu_a_r", "iv_asi_kusu_b_r"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Ring_Toe.R", parent=["toe.R", "j_asi_e_r"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Ring_Toe.R", rigify_type=rigify.types.limbs_super_finger()),
                        CollectionOperation(time="Pre", bone_name="Ring_Toe.R", collection_name="IVCS_Toes.R"),
            ]
        ),
        ExtensionBone(
            name="Ring_Toe.R.001",
            bone_a="iv_asi_kusu_b_r",
            parent="Ring_Toe.R",
            is_connected=True,
            axis_type="local",
            axis="Y",
            req_bones=["iv_asi_kusu_b_r"],
            operations=[CollectionOperation(time="Pre", bone_name="Ring_Toe.R.001", collection_name="IVCS_Toes.R")]
        ),
        ConnectBone(
            name="Pinky_Toe.R",
            bone_a="iv_asi_ko_a_r",
            bone_b="iv_asi_ko_b_r",
            parent="toe.R",
            is_connected=False,
            req_bones=["iv_asi_ko_a_r", "iv_asi_ko_b_r"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Pinky_Toe.R", parent=["toe.R", "j_asi_e_r"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Pinky_Toe.R", rigify_type=rigify.types.limbs_super_finger()),
                        CollectionOperation(time="Pre", bone_name="Pinky_Toe.R", collection_name="IVCS_Toes.R"),
            ]
        ),
        ExtensionBone(
            name="Pinky_Toe.R.001",
            bone_a="iv_asi_ko_b_r",
            parent="Pinky_Toe.R",
            is_connected=True,
            axis_type="local",
            axis="Y",
            req_bones=["iv_asi_ko_b_r"],
            operations=[CollectionOperation(time="Pre", bone_name="Pinky_Toe.R.001", collection_name="IVCS_Toes.R")]
        ),
    ]
)

IV_TOES_L = BoneGroup(
    name="IVCS Toes Left",
    transform_link=[
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
    generators=[
        #Toes Left
        ConnectBone(
            name="Hallux_Toe.L",
            bone_a="iv_asi_oya_a_l",
            bone_b="iv_asi_oya_b_l",
            parent="toe.L",
            is_connected=False,
            req_bones=["iv_asi_oya_a_l", "iv_asi_oya_b_l"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Hallux_Toe.L", parent=["toe.L", "j_asi_e_l"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Hallux_Toe.L", rigify_type=rigify.types.limbs_super_finger()),
                        CollectionOperation(time="Pre", bone_name="Hallux_Toe.L", collection_name="IVCS_Toes.L"),
            ]
        ),
        ExtensionBone(
            name="Hallux_Toe.L.001",
            bone_a="iv_asi_oya_b_l",
            parent="Hallux_Toe.L",
            is_connected=True,
            axis_type="local",
            axis="Y",
            req_bones=["iv_asi_oya_b_l"],
            operations=[CollectionOperation(time="Pre", bone_name="Hallux_Toe.L.001", collection_name="IVCS_Toes.L")]
        ),
        ConnectBone(
            name="Index_Toe.L",
            bone_a="iv_asi_hito_a_l",
            bone_b="iv_asi_hito_b_l",
            parent="toe.L",
            is_connected=False,
            req_bones=["iv_asi_hito_a_l", "iv_asi_hito_b_l"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Index_Toe.L", parent=["toe.L", "j_asi_e_l"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Index_Toe.L", rigify_type=rigify.types.limbs_super_finger()),
                        CollectionOperation(time="Pre", bone_name="Index_Toe.L", collection_name="IVCS_Toes.L"),
            ]
        ),
        ExtensionBone(
            name="Index_Toe.L.001",
            bone_a="iv_asi_hito_b_l",
            parent="Index_Toe.L",
            is_connected=True,
            axis_type="local",
            axis="Y",
            req_bones=["iv_asi_hito_b_l"],
            operations=[CollectionOperation(time="Pre", bone_name="Index_Toe.L.001", collection_name="IVCS_Toes.L")]
        ),
        ConnectBone(
            name="Middle_Toe.L",
            bone_a="iv_asi_naka_a_l",
            bone_b="iv_asi_naka_b_l",
            parent="toe.L",
            is_connected=False,
            req_bones=["iv_asi_naka_a_l", "iv_asi_naka_b_l"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Middle_Toe.L", parent=["toe.L", "j_asi_e_l"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Middle_Toe.L", rigify_type=rigify.types.limbs_super_finger()),
                        CollectionOperation(time="Pre", bone_name="Middle_Toe.L", collection_name="IVCS_Toes.L"),
            ]
        ),
        ExtensionBone(
            name="Middle_Toe.L.001",
            bone_a="iv_asi_naka_b_l",
            parent="Middle_Toe.L",
            is_connected=True,
            axis_type="local",
            axis="Y",
            req_bones=["iv_asi_naka_b_l"],
            operations=[CollectionOperation(time="Pre", bone_name="Middle_Toe.L.001", collection_name="IVCS_Toes.L")]
        ),
        ConnectBone(
            name="Ring_Toe.L",
            bone_a="iv_asi_kusu_a_l",
            bone_b="iv_asi_kusu_b_l",
            parent="toe.L",
            is_connected=False,
            req_bones=["iv_asi_kusu_a_l", "iv_asi_kusu_b_l"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Ring_Toe.L", parent=["toe.L", "j_asi_e_l"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Ring_Toe.L", rigify_type=rigify.types.limbs_super_finger()),
                        CollectionOperation(time="Pre", bone_name="Ring_Toe.L", collection_name="IVCS_Toes.L"),
            ]
        ),
        ExtensionBone(
            name="Ring_Toe.L.001",
            bone_a="iv_asi_kusu_b_l",
            parent="Ring_Toe.L",
            is_connected=True,
            axis_type="local",
            axis="Y",
            req_bones=["iv_asi_kusu_b_l"],
            operations=[CollectionOperation(time="Pre", bone_name="Ring_Toe.L.001", collection_name="IVCS_Toes.L")]
        ),
        ConnectBone(
            name="Pinky_Toe.L",
            bone_a="iv_asi_ko_a_l",
            bone_b="iv_asi_ko_b_l",
            parent="toe.L",
            is_connected=False,
            req_bones=["iv_asi_ko_a_l", "iv_asi_ko_b_l"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Pinky_Toe.L", parent=["toe.L", "j_asi_e_l"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Pinky_Toe.L", rigify_type=rigify.types.limbs_super_finger()),
                        CollectionOperation(time="Pre", bone_name="Pinky_Toe.L", collection_name="IVCS_Toes.L"),
            ]
        ),
        ExtensionBone(
            name="Pinky_Toe.L.001",
            bone_a="iv_asi_ko_b_l",
            parent="Pinky_Toe.L",
            is_connected=True,
            axis_type="local",
            axis="Y",
            req_bones=["iv_asi_ko_b_l"],
            operations=[CollectionOperation(time="Pre", bone_name="Pinky_Toe.L.001", collection_name="IVCS_Toes.L")]
        ),
    ]
)

def get_rig_module() -> RigModule:
    return RigModule(
        name="IVCS",
        type="Generation",
        bone_groups=[IV_TOES_L, IV_TOES_R],
        ui = UI_Collections([
            BoneCollection(name="IVCS_Toes.L", ui=True, color_set="IVCS", row_index=1, title="Toes.L", visible=False),
            BoneCollection(name="IVCS_Toes.R", ui=True, color_set="IVCS", row_index=1, title="Toes.R", visible=False),
        ])
    )