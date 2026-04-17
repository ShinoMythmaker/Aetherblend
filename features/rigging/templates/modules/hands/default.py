from ......core.generators import ConnectBone, ExtensionBone, CopyBone
from ......core.operations import ParentBoneOperation, RigifyTypeOperation, CollectionOperation
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
            axis_type="local",
            axis="Y",
            start="head",
            roll=135,
            req_bones=["j_hito_a_r"],
            operations=[ParentBoneOperation(time="Post", bone_name="palm.01.R", parent=["hand.R", "j_te_r"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="palm.01.R", rigify_type=rigify.types.limbs_super_palm(palm_both_sides=True)),
                        CollectionOperation(time="Pre", bone_name="palm.01.R", collection_name="Fingers.R"),
            ]
        ),
        ExtensionBone(
            name="palm.02.R",
            bone_a="j_naka_a_r",
            parent="hand.R",
            axis_type="local",
            axis="Y",
            start="head",
            roll=135,
            req_bones=["j_naka_a_r"],
            operations=[ParentBoneOperation(time="Post", bone_name="palm.02.R", parent=["hand.R", "j_te_r"], is_connected=False),
                        CollectionOperation(time="Pre", bone_name="palm.02.R", collection_name="Fingers.R"),
            ]
        ),
        ExtensionBone(
            name="palm.03.R",
            bone_a="j_kusu_a_r",
            parent="hand.R",
            axis_type="local",
            axis="Y",
            start="head",
            roll=135,
            req_bones=["j_kusu_a_r"],
            operations=[ParentBoneOperation(time="Post", bone_name="palm.03.R", parent=["hand.R", "j_te_r"], is_connected=False),
                        CollectionOperation(time="Pre", bone_name="palm.03.R", collection_name="Fingers.R"),
            ]
        ),
        ExtensionBone(
            name="palm.04.R",
            bone_a="j_ko_a_r",
            parent="hand.R",
            axis_type="local",
            axis="Y",
            start="head",
            roll=135,
            req_bones=["j_ko_a_r"],
            operations=[ParentBoneOperation(time="Post", bone_name="palm.04.R", parent=["hand.R", "j_te_r"], is_connected=False),
                        CollectionOperation(time="Pre", bone_name="palm.04.R", collection_name="Fingers.R"),
            ]
        ),
        #Thumb
        CopyBone(
            name="DEF-thumb_master.R",
            source_bone="j_oya_a_r",
            parent="hand.R",
            req_bones=["j_oya_a_r"],
            operations=[ParentBoneOperation(time="Pre", bone_name="DEF-thumb_master.R", parent=["hand.R", "j_te_r"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="DEF-thumb_master.R", rigify_type=rigify.types.basic_raw_copy(relink_constraints=True, parent="DEF")),
                        CollectionOperation(time="Pre", bone_name="DEF-thumb_master.R", collection_name="DEF")
            ]
        ),
        ConnectBone(
            name="thumb.R",
            bone_a="j_oya_a_r",
            bone_b="j_oya_b_r",
            parent="DEF-thumb_master.R",
            is_connected=False,
            roll=-15,
            req_bones=["DEF-thumb_master.R", "j_oya_a_r", "j_oya_b_r"],
            operations=[RigifyTypeOperation(time="Pre", bone_name="thumb.R", rigify_type=rigify.types.limbs_super_finger(make_extra_ik_control=True, extra_ik_layers_extra="Fingers.R (IK)")),
                        CollectionOperation(time="Pre", bone_name="thumb.R", collection_name="Fingers.R"),
            ]
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
            operations=[CollectionOperation(time="Pre", bone_name="thumb.R.001", collection_name="Fingers.R"),
            ]
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
            operations=[RigifyTypeOperation(time="Pre", bone_name="index.R", rigify_type=rigify.types.limbs_super_finger(make_extra_ik_control=True, extra_ik_layers_extra="Fingers.R (IK)")),
                        CollectionOperation(time="Pre", bone_name="index.R", collection_name="Fingers.R"),
            ]
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
            operations=[CollectionOperation(time="Pre", bone_name="index.R.001", collection_name="Fingers.R"),
            ]
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
            operations=[RigifyTypeOperation(time="Pre", bone_name="middle.R", rigify_type=rigify.types.limbs_super_finger(make_extra_ik_control=True, extra_ik_layers_extra="Fingers.R (IK)")),
                        CollectionOperation(time="Pre", bone_name="middle.R", collection_name="Fingers.R"),
            ]
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
            operations=[CollectionOperation(time="Pre", bone_name="middle.R.001", collection_name="Fingers.R"),
            ]
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
            operations=[RigifyTypeOperation(time="Pre", bone_name="ring.R", rigify_type=rigify.types.limbs_super_finger(make_extra_ik_control=True, extra_ik_layers_extra="Fingers.R (IK)")),
                        CollectionOperation(time="Pre", bone_name="ring.R", collection_name="Fingers.R"),
            ]
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
            operations=[CollectionOperation(time="Pre", bone_name="ring.R.001", collection_name="Fingers.R"),
            ]
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
            operations=[RigifyTypeOperation(time="Pre", bone_name="pinky.R", rigify_type=rigify.types.limbs_super_finger(make_extra_ik_control=True, extra_ik_layers_extra="Fingers.R (IK)")),
                        CollectionOperation(time="Pre", bone_name="pinky.R", collection_name="Fingers.R"),
            ]
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
            operations=[CollectionOperation(time="Pre", bone_name="pinky.R.001", collection_name="Fingers.R"),
            ]
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
            operations=[ParentBoneOperation(time="Post", bone_name="palm.01.L", parent=["hand.L", "j_te_l"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="palm.01.L", rigify_type=rigify.types.limbs_super_palm(palm_both_sides=True)),
                        CollectionOperation(time="Pre", bone_name="palm.01.L", collection_name="Fingers.L"),
            ]
        ),
        ExtensionBone(
            name="palm.02.L",
            bone_a="j_naka_a_l",
            parent=["hand.L", "j_te_l"],
            is_connected=False,
            axis_type="local",
            axis="Y",
            start="head",
            roll=-135,
            req_bones=["j_naka_a_l"],
            operations=[CollectionOperation(time="Pre", bone_name="palm.02.L", collection_name="Fingers.L")]
        ),
        ExtensionBone(
            name="palm.03.L",
            bone_a="j_kusu_a_l",
            parent=["hand.L", "j_te_l"],
            is_connected=False,
            axis_type="local",
            axis="Y",
            start="head",
            roll=-135,
            req_bones=["j_kusu_a_l"],
            operations=[CollectionOperation(time="Pre", bone_name="palm.03.L", collection_name="Fingers.L")]
        ),
        ExtensionBone(
            name="palm.04.L",
            bone_a="j_ko_a_l",
            parent=["hand.L", "j_te_l"],
            is_connected=False,
            axis_type="local",
            axis="Y",
            start="head",
            roll=-135,
            req_bones=["j_ko_a_l"],
            operations=[CollectionOperation(time="Pre", bone_name="palm.04.L", collection_name="Fingers.L")]
        ),
        #Thumb
        CopyBone(
            name="DEF-thumb_master.L",
            source_bone="j_oya_a_l",
            parent=["hand.L"],
            req_bones=["j_oya_a_l"],
            operations=[ParentBoneOperation(time="Pre", bone_name="DEF-thumb_master.L", parent=["hand.L", "j_te_l"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="DEF-thumb_master.L", rigify_type=rigify.types.basic_raw_copy(relink_constraints=True, parent="DEF")),
                        CollectionOperation(time="Pre", bone_name="DEF-thumb_master.L", collection_name="DEF")
            ]
        ),
        ConnectBone(
            name="thumb.L",
            bone_a="j_oya_a_l",
            bone_b="j_oya_b_l",
            parent="DEF-thumb_master.L",
            is_connected=False,
            roll=-15,
            req_bones=["DEF-thumb_master.L", "j_oya_a_l", "j_oya_b_l"],
            operations=[RigifyTypeOperation(time="Pre", bone_name="thumb.L", rigify_type=rigify.types.limbs_super_finger(make_extra_ik_control=True, extra_ik_layers_extra="Fingers.L (IK)")),
                        CollectionOperation(time="Pre", bone_name="thumb.L", collection_name="Fingers.L"),
            ]
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
            operations=[CollectionOperation(time="Pre", bone_name="thumb.L.001", collection_name="Fingers.L"),
            ]
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
            operations=[RigifyTypeOperation(time="Pre", bone_name="index.L", rigify_type=rigify.types.limbs_super_finger(make_extra_ik_control=True, extra_ik_layers_extra="Fingers.L (IK)")),
                        CollectionOperation(time="Pre", bone_name="index.L", collection_name="Fingers.L"),
            ]
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
            operations=[CollectionOperation(time="Pre", bone_name="index.L.001", collection_name="Fingers.L")]
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
            operations=[RigifyTypeOperation(time="Pre", bone_name="middle.L", rigify_type=rigify.types.limbs_super_finger(make_extra_ik_control=True, extra_ik_layers_extra="Fingers.L (IK)")),
                        CollectionOperation(time="Pre", bone_name="middle.L", collection_name="Fingers.L"),
            ]
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
            operations=[CollectionOperation(time="Pre", bone_name="middle.L.001", collection_name="Fingers.L")]
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
            operations=[RigifyTypeOperation(time="Pre", bone_name="ring.L", rigify_type=rigify.types.limbs_super_finger(make_extra_ik_control=True, extra_ik_layers_extra="Fingers.L (IK)")),
                        CollectionOperation(time="Pre", bone_name="ring.L", collection_name="Fingers.L"),
            ]
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
            operations=[CollectionOperation(time="Pre", bone_name="ring.L.001", collection_name="Fingers.L")]
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
            operations=[RigifyTypeOperation(time="Pre", bone_name="pinky.L", rigify_type=rigify.types.limbs_super_finger(make_extra_ik_control=True, extra_ik_layers_extra="Fingers.L (IK)")),
                        CollectionOperation(time="Pre", bone_name="pinky.L", collection_name="Fingers.L"),
            ]
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
            operations=[CollectionOperation(time="Pre", bone_name="pinky.L.001", collection_name="Fingers.L")]
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