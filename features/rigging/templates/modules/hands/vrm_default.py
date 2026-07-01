from ......core.generators import ConnectBone, ExtensionBone, CopyBone
from ......core.operations import ParentBoneOperation, RigifyTypeOperation, CollectionOperation
from ......core.shared import PoseOperations, BoneGroup, RigModule, TransformLink
from ......core import rigify
from ......core.rigify.settings import UI_Collections, BoneCollection

HAND_L = BoneGroup(
    name="Left Hand",
    transform_link= [
        TransformLink(target="DEF-thumb.L", bone="J_Bip_L_Thumb1"),
        TransformLink(target="DEF-thumb.L.001", bone="J_Bip_L_Thumb2"),
        TransformLink(target="DEF-thumb.L.002", bone="J_Bip_L_Thumb3"),
        TransformLink(target="DEF-index.L", bone="J_Bip_L_Index1"),
        TransformLink(target="DEF-index.L.001", bone="J_Bip_L_Index2"),
        TransformLink(target="DEF-middle.L", bone="J_Bip_L_Middle1"),
        TransformLink(target="DEF-middle.L.001", bone="J_Bip_L_Middle2"),
        TransformLink(target="DEF-ring.L", bone="J_Bip_L_Ring1"),
        TransformLink(target="DEF-ring.L.001", bone="J_Bip_L_Ring2"),
        TransformLink(target="DEF-pinky.L", bone="J_Bip_L_Little1"),
        TransformLink(target="DEF-pinky.L.001", bone="J_Bip_L_Little2"),
        TransformLink(target="DEF-index.L.002", bone="J_Bip_L_Index3"),
        TransformLink(target="DEF-middle.L.002", bone="J_Bip_L_Middle3"),
        TransformLink(target="DEF-ring.L.002", bone="J_Bip_L_Ring3"),
        TransformLink(target="DEF-pinky.L.002", bone="J_Bip_L_Little3"),
    ],
    generators=[
        #Palm Control - Very cool stuff, thank you rigify - Oats
        CopyBone(
            name="palm.01.L",
            bone_a="J_Bip_L_Index1",
            parent="hand.L",
            is_connected=False,
            req_bones=["J_Bip_L_Index1"],
            operations=[ParentBoneOperation(time="Post", bone_name="palm.01.L", parent=["hand.L", "J_Bip_L_Hand"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="palm.01.L", rigify_type=rigify.types.limbs_super_palm(palm_both_sides=True)),
                        CollectionOperation(time="Pre", bone_name="palm.01.L", collection_name="Fingers.L"),
            ]
        ),
        CopyBone(
            name="palm.02.L",
            bone_a="J_Bip_L_Middle1",
            parent="hand.L",
            is_connected=False,
            req_bones=["J_Bip_L_Middle1"],
            operations=[ParentBoneOperation(time="Post", bone_name="palm.02.L", parent=["hand.L", "J_Bip_L_Hand"], is_connected=False),
                        CollectionOperation(time="Pre", bone_name="palm.02.L", collection_name="Fingers.L"),
            ]
        ),
        CopyBone(
            name="palm.03.L",
            bone_a="J_Bip_L_Ring1",
            parent="hand.L",
            is_connected=False,
            req_bones=["J_Bip_L_Ring1"],
            operations=[ParentBoneOperation(time="Post", bone_name="palm.03.L", parent=["hand.L", "J_Bip_L_Hand"], is_connected=False),
                        CollectionOperation(time="Pre", bone_name="palm.03.L", collection_name="Fingers.L"),
            ]
        ),
        CopyBone(
            name="palm.04.L",
            bone_a="J_Bip_L_Little1",
            parent="hand.L",
            is_connected=False,
            req_bones=["J_Bip_L_Little1"],
            operations=[ParentBoneOperation(time="Post", bone_name="palm.04.L", parent=["hand.L", "J_Bip_L_Hand"], is_connected=False),
                        CollectionOperation(time="Pre", bone_name="palm.04.L", collection_name="Fingers.L"),
            ]
        ),
        #Thumb
        CopyBone(
            name="DEF-thumb_master.L",
            bone_a="J_Bip_L_Thumb1",
            parent="hand.L",
            req_bones=["hand.L", "J_Bip_L_Thumb1"],
            operations=[ParentBoneOperation(time="Pre", bone_name="DEF-thumb_master.L", parent=["hand.L", "J_Bip_L_Hand"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="DEF-thumb_master.L", rigify_type=rigify.types.basic_raw_copy(relink_constraints=True, parent="DEF")),
                        CollectionOperation(time="Pre", bone_name="DEF-thumb_master.L", collection_name="DEF")
            ]
        ),
        CopyBone(
            name="thumb.L",
            bone_a="J_Bip_L_Thumb1",
            parent="DEF-thumb_master.L",
            is_connected=False,
            req_bones=["DEF-thumb_master.L", "J_Bip_L_Thumb1"],
            operations=[RigifyTypeOperation(time="Pre", bone_name="thumb.L", rigify_type=rigify.types.limbs_super_finger(primary_rotation_axis="Z",make_extra_ik_control=True, extra_ik_layers_extra="Fingers.L (IK)")),
                        CollectionOperation(time="Pre", bone_name="thumb.L", collection_name="Fingers.L"),
            ]
        ),
        CopyBone(
            name="thumb.L.001",
            bone_a="J_Bip_L_Thumb2",
            parent="thumb.L",
            is_connected=True,
            req_bones=["J_Bip_L_Thumb2"],
            operations=[CollectionOperation(time="Pre", bone_name="thumb.L.001", collection_name="Fingers.L"),
            ]
        ),
        CopyBone(
            name="thumb.L.002",
            bone_a="J_Bip_L_Thumb3",
            parent="thumb.L.001",
            is_connected=True,
            req_bones=["J_Bip_L_Thumb3"],
            operations=[CollectionOperation(time="Pre", bone_name="thumb.L.002", collection_name="Fingers.L"),
            ]
        ),
        #Index
        CopyBone(
            name="index.L",
            bone_a="J_Bip_L_Index1",
            parent="palm.01.L",
            is_connected=False,
            req_bones=["J_Bip_L_Index1"],
            operations=[RigifyTypeOperation(time="Pre", bone_name="index.L", rigify_type=rigify.types.limbs_super_finger(primary_rotation_axis="-X", make_extra_ik_control=True, extra_ik_layers_extra="Fingers.L (IK)")),
                        CollectionOperation(time="Pre", bone_name="index.L", collection_name="Fingers.L"),
            ]
        ),
        CopyBone(
            name="index.L.001",
            bone_a="J_Bip_L_Index2",
            parent="index.L",
            is_connected=True,
            req_bones=["J_Bip_L_Index2"],
            operations=[CollectionOperation(time="Pre", bone_name="index.L.001", collection_name="Fingers.L"),]
        ),
        CopyBone(
            name="index.L.002",
            bone_a="J_Bip_L_Index3",
            parent="index.L.001",
            is_connected=True,
            req_bones=["J_Bip_L_Index3"],
            operations=[CollectionOperation(time="Pre", bone_name="index.L.002", collection_name="Fingers.L"),
            ]
        ),
        #Middle
        CopyBone(
            name="middle.L",
            bone_a="J_Bip_L_Middle1",
            parent="palm.02.L",
            is_connected=False,
            req_bones=["J_Bip_L_Middle1",],
            operations=[RigifyTypeOperation(time="Pre", bone_name="middle.L", rigify_type=rigify.types.limbs_super_finger(primary_rotation_axis="-X",make_extra_ik_control=True, extra_ik_layers_extra="Fingers.L (IK)")),
                        CollectionOperation(time="Pre", bone_name="middle.L", collection_name="Fingers.L"),
            ]
        ),
        CopyBone(
            name="middle.L.001",
            bone_a="J_Bip_L_Middle2",
            parent="middle.L",
            is_connected=True,
            req_bones=["J_Bip_L_Middle2"],
            operations=[CollectionOperation(time="Pre", bone_name="middle.L.001", collection_name="Fingers.L"),
            ]
        ),
        CopyBone(
            name="middle.L.002",
            bone_a="J_Bip_L_Middle3",
            parent="middle.L.001",
            is_connected=True,
            req_bones=["J_Bip_L_Middle3"],
            operations=[CollectionOperation(time="Pre", bone_name="middle.L.002", collection_name="Fingers.L"),
            ]
        ),
        #Ring
        CopyBone(
            name="ring.L",
            bone_a="J_Bip_L_Ring1",
            parent="palm.03.L",
            is_connected=False,
            req_bones=["J_Bip_L_Ring1"],
            operations=[RigifyTypeOperation(time="Pre", bone_name="ring.L", rigify_type=rigify.types.limbs_super_finger(primary_rotation_axis="-X",make_extra_ik_control=True, extra_ik_layers_extra="Fingers.L (IK)")),
                        CollectionOperation(time="Pre", bone_name="ring.L", collection_name="Fingers.L"),
            ]
        ),
        CopyBone(
            name="ring.L.001",
            bone_a="J_Bip_L_Ring2",
            parent="ring.L",
            is_connected=True,
            req_bones=["J_Bip_L_Ring2"],
            operations=[CollectionOperation(time="Pre", bone_name="ring.L.001", collection_name="Fingers.L"),
            ]
        ),
        CopyBone(
            name="ring.L.002",
            bone_a="J_Bip_L_Ring3",
            parent="ring.L.001",
            is_connected=True,
            req_bones=["J_Bip_L_Ring3"],
            operations=[CollectionOperation(time="Pre", bone_name="ring.L.002", collection_name="Fingers.L"),
            ]
        ),
        #Pinky
        CopyBone(
            name="pinky.L",
            bone_a="J_Bip_L_Little1",
            parent="palm.04.L",
            is_connected=False,
            req_bones=["J_Bip_L_Little1"],
            operations=[RigifyTypeOperation(time="Pre", bone_name="pinky.L", rigify_type=rigify.types.limbs_super_finger(primary_rotation_axis="-X", make_extra_ik_control=True, extra_ik_layers_extra="Fingers.L (IK)")),
                        CollectionOperation(time="Pre", bone_name="pinky.L", collection_name="Fingers.L"),
            ]
        ),
        CopyBone(
            name="pinky.L.001",
            bone_a="J_Bip_L_Little2",
            parent="pinky.L",
            is_connected=True,
            req_bones=["J_Bip_L_Little2"],
            operations=[CollectionOperation(time="Pre", bone_name="pinky.L.001", collection_name="Fingers.L"),
            ]
        ),
        CopyBone(
            name="pinky.L.002",
            bone_a="J_Bip_L_Little3",
            parent="pinky.L.001",
            is_connected=True,
            req_bones=["J_Bip_L_Little3"],
            operations=[CollectionOperation(time="Pre", bone_name="pinky.L.002", collection_name="Fingers.L"),
            ]
        ),
    ],
)

HAND_R = BoneGroup(
    name="Right Hand",
    transform_link= [
        TransformLink(target="DEF-thumb.R", bone="J_Bip_R_Thumb1"),
        TransformLink(target="DEF-thumb.R.001", bone="J_Bip_R_Thumb2"),
        TransformLink(target="DEF-thumb.R.002", bone="J_Bip_R_Thumb3"),
        TransformLink(target="DEF-index.R", bone="J_Bip_R_Index1"),
        TransformLink(target="DEF-index.R.001", bone="J_Bip_R_Index2"),
        TransformLink(target="DEF-middle.R", bone="J_Bip_R_Middle1"),
        TransformLink(target="DEF-middle.R.001", bone="J_Bip_R_Middle2"),
        TransformLink(target="DEF-ring.R", bone="J_Bip_R_Ring1"),
        TransformLink(target="DEF-ring.R.001", bone="J_Bip_R_Ring2"),
        TransformLink(target="DEF-pinky.R", bone="J_Bip_R_Little1"),
        TransformLink(target="DEF-pinky.R.001", bone="J_Bip_R_Little2"),
        TransformLink(target="DEF-index.R.002", bone="J_Bip_R_Index3"),
        TransformLink(target="DEF-middle.R.002", bone="J_Bip_R_Middle3"),
        TransformLink(target="DEF-ring.R.002", bone="J_Bip_R_Ring3"),
        TransformLink(target="DEF-pinky.R.002", bone="J_Bip_R_Little3"),
    ],
    generators=[
        #Palm Control - Very cool stuff, thank you rigify - Oats
        CopyBone(
            name="palm.01.R",
            bone_a="J_Bip_R_Index1",
            parent="hand.R",
            is_connected=False,
            req_bones=["J_Bip_R_Index1"],
            operations=[ParentBoneOperation(time="Post", bone_name="palm.01.R", parent=["hand.R", "J_Bip_R_Hand"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="palm.01.R", rigify_type=rigify.types.limbs_super_palm(palm_both_sides=True)),
                        CollectionOperation(time="Pre", bone_name="palm.01.R", collection_name="Fingers.R"),
            ]
        ),
        CopyBone(
            name="palm.02.R",
            bone_a="J_Bip_R_Middle1",
            parent="hand.R",
            is_connected=False,
            req_bones=["J_Bip_R_Middle1"],
            operations=[ParentBoneOperation(time="Post", bone_name="palm.02.R", parent=["hand.R", "J_Bip_R_Hand"], is_connected=False),
                        CollectionOperation(time="Pre", bone_name="palm.02.R", collection_name="Fingers.R"),
            ]
        ),
        CopyBone(
            name="palm.03.R",
            bone_a="J_Bip_R_Ring1",
            parent="hand.R",
            is_connected=False,
            req_bones=["J_Bip_R_Ring1"],
            operations=[ParentBoneOperation(time="Post", bone_name="palm.03.R", parent=["hand.R", "J_Bip_R_Hand"], is_connected=False),
                        CollectionOperation(time="Pre", bone_name="palm.03.R", collection_name="Fingers.R"),
            ]
        ),
        CopyBone(
            name="palm.04.R",
            bone_a="J_Bip_R_Little1",
            parent="hand.R",
            is_connected=False,
            req_bones=["J_Bip_R_Little1"],
            operations=[ParentBoneOperation(time="Post", bone_name="palm.04.R", parent=["hand.R", "J_Bip_R_Hand"], is_connected=False),
                        CollectionOperation(time="Pre", bone_name="palm.04.R", collection_name="Fingers.R"),
            ]
        ),
        #Thumb
        CopyBone(
            name="DEF-thumb_master.R",
            bone_a="J_Bip_R_Thumb1",
            parent="hand.R",
            req_bones=["hand.R", "J_Bip_R_Thumb1"],
            operations=[ParentBoneOperation(time="Pre", bone_name="DEF-thumb_master.R", parent=["hand.R", "J_Bip_R_Hand"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="DEF-thumb_master.R", rigify_type=rigify.types.basic_raw_copy(relink_constraints=True, parent="DEF")),
                        CollectionOperation(time="Pre", bone_name="DEF-thumb_master.R", collection_name="DEF")
            ]
        ),
        CopyBone(
            name="thumb.R",
            bone_a="J_Bip_R_Thumb1",
            parent="DEF-thumb_master.R",
            is_connected=False,
            req_bones=["DEF-thumb_master.R", "J_Bip_R_Thumb1"],
            operations=[RigifyTypeOperation(time="Pre", bone_name="thumb.R", rigify_type=rigify.types.limbs_super_finger(primary_rotation_axis="Z",make_extra_ik_control=True, extra_ik_layers_extra="Fingers.R (IK)")),
                        CollectionOperation(time="Pre", bone_name="thumb.R", collection_name="Fingers.R"),
            ]
        ),
        CopyBone(
            name="thumb.R.001",
            bone_a="J_Bip_R_Thumb2",
            parent="thumb.R",
            is_connected=True,
            req_bones=["J_Bip_R_Thumb2"],
            operations=[CollectionOperation(time="Pre", bone_name="thumb.R.001", collection_name="Fingers.R"),
            ]
        ),
        CopyBone(
            name="thumb.R.002",
            bone_a="J_Bip_R_Thumb3",
            parent="thumb.R.001",
            is_connected=True,
            req_bones=["J_Bip_R_Thumb3"],
            operations=[CollectionOperation(time="Pre", bone_name="thumb.R.002", collection_name="Fingers.R"),
            ]
        ),
        #Index
        CopyBone(
            name="index.R",
            bone_a="J_Bip_R_Index1",
            parent="palm.01.R",
            is_connected=False,
            req_bones=["J_Bip_R_Index1"],
            operations=[RigifyTypeOperation(time="Pre", bone_name="index.R", rigify_type=rigify.types.limbs_super_finger(primary_rotation_axis="-X", make_extra_ik_control=True, extra_ik_layers_extra="Fingers.R (IK)")),
                        CollectionOperation(time="Pre", bone_name="index.R", collection_name="Fingers.R"),
            ]
        ),
        CopyBone(
            name="index.R.001",
            bone_a="J_Bip_R_Index2",
            parent="index.R",
            is_connected=True,
            req_bones=["J_Bip_R_Index2"],
            operations=[CollectionOperation(time="Pre", bone_name="index.R.001", collection_name="Fingers.R"),]
        ),
        CopyBone(
            name="index.R.002",
            bone_a="J_Bip_R_Index3",
            parent="index.R.001",
            is_connected=True,
            req_bones=["J_Bip_R_Index3"],
            operations=[CollectionOperation(time="Pre", bone_name="index.R.002", collection_name="Fingers.R"),
            ]
        ),
        #Middle
        CopyBone(
            name="middle.R",
            bone_a="J_Bip_R_Middle1",
            parent="palm.02.R",
            is_connected=False,
            req_bones=["J_Bip_R_Middle1",],
            operations=[RigifyTypeOperation(time="Pre", bone_name="middle.R", rigify_type=rigify.types.limbs_super_finger(primary_rotation_axis="-X",make_extra_ik_control=True, extra_ik_layers_extra="Fingers.R (IK)")),
                        CollectionOperation(time="Pre", bone_name="middle.R", collection_name="Fingers.R"),
            ]
        ),
        CopyBone(
            name="middle.R.001",
            bone_a="J_Bip_R_Middle2",
            parent="middle.R",
            is_connected=True,
            req_bones=["J_Bip_R_Middle2"],
            operations=[CollectionOperation(time="Pre", bone_name="middle.R.001", collection_name="Fingers.R"),
            ]
        ),
        CopyBone(
            name="middle.R.002",
            bone_a="J_Bip_R_Middle3",
            parent="middle.R.001",
            is_connected=True,
            req_bones=["J_Bip_R_Middle3"],
            operations=[CollectionOperation(time="Pre", bone_name="middle.R.002", collection_name="Fingers.R"),
            ]
        ),
        #Ring
        CopyBone(
            name="ring.R",
            bone_a="J_Bip_R_Ring1",
            parent="palm.03.R",
            is_connected=False,
            req_bones=["J_Bip_R_Ring1"],
            operations=[RigifyTypeOperation(time="Pre", bone_name="ring.R", rigify_type=rigify.types.limbs_super_finger(primary_rotation_axis="-X",make_extra_ik_control=True, extra_ik_layers_extra="Fingers.R (IK)")),
                        CollectionOperation(time="Pre", bone_name="ring.R", collection_name="Fingers.R"),
            ]
        ),
        CopyBone(
            name="ring.R.001",
            bone_a="J_Bip_R_Ring2",
            parent="ring.R",
            is_connected=True,
            req_bones=["J_Bip_R_Ring2"],
            operations=[CollectionOperation(time="Pre", bone_name="ring.R.001", collection_name="Fingers.R"),
            ]
        ),
        CopyBone(
            name="ring.R.002",
            bone_a="J_Bip_R_Ring3",
            parent="ring.R.001",
            is_connected=True,
            req_bones=["J_Bip_R_Ring3"],
            operations=[CollectionOperation(time="Pre", bone_name="ring.R.002", collection_name="Fingers.R"),
            ]
        ),
        #Pinky
        CopyBone(
            name="pinky.R",
            bone_a="J_Bip_R_Little1",
            parent="palm.04.R",
            is_connected=False,
            req_bones=["J_Bip_R_Little1"],
            operations=[RigifyTypeOperation(time="Pre", bone_name="pinky.R", rigify_type=rigify.types.limbs_super_finger(primary_rotation_axis="-X", make_extra_ik_control=True, extra_ik_layers_extra="Fingers.R (IK)")),
                        CollectionOperation(time="Pre", bone_name="pinky.R", collection_name="Fingers.R"),
            ]
        ),
        CopyBone(
            name="pinky.R.001",
            bone_a="J_Bip_R_Little2",
            parent="pinky.R",
            is_connected=True,
            req_bones=["J_Bip_R_Little2"],
            operations=[CollectionOperation(time="Pre", bone_name="pinky.R.001", collection_name="Fingers.R"),
            ]
        ),
        CopyBone(
            name="pinky.R.002",
            bone_a="J_Bip_R_Little3",
            parent="pinky.R.001",
            is_connected=True,
            req_bones=["J_Bip_R_Little3"],
            operations=[CollectionOperation(time="Pre", bone_name="pinky.R.002", collection_name="Fingers.R"),
            ]
        ),
    ],
)

def get_rig_module() -> RigModule:
    return RigModule(
        name="VRM-Default",
        type="Generation",
        bone_groups=[HAND_L, HAND_R],
        ui_collections = UI_Collections([
            BoneCollection(name="Fingers.L", ui=True, color_set="Fingers_Left", row_index=1, title="Fingers.L", visible=False),
            BoneCollection(name="Fingers.R", ui=True, color_set="Fingers_Right", row_index=1, title="Fingers.R", visible=False),
        ])
    )