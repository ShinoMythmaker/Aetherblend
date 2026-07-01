from ......core.rigify.settings import UI_Collections, BoneCollection
from ......core.bone_generators import ConnectBone, CopyBone, ExtensionBone, ParallelBone
from ......core.operations import BoneRestrictionOperation, ParentBoneOperation, PropOverrideOperation, RigifyTypeOperation, CollectionOperation, ConstraintOperation
from ......core.constraints import DampedTrackConstraint
from ......core.shared import PoseOperations, BoneGroup, TransformLink, RigModule
from ......core import rigify

LEG_R = BoneGroup(
        name="Right Leg",
        transform_link= [
            TransformLink(target="DEF-thigh.R.001", bone="J_Bip_R_UpperLeg", retarget="FK-upper_leg.R"),
            TransformLink(target="DEF-shin.R.001", bone="J_Bip_R_LowerLeg", retarget="FK-lower_leg.R"),
            TransformLink(target="DEF-foot.R", bone="J_Bip_R_Foot", retarget="FK-foot.R"),
            TransformLink(target="DEF-toe.R", bone="J_Bip_R_ToeBase", retarget="FK-toe.R"),
            ],
        generators = [
            # Right Leg
            CopyBone(
                name="thigh.R", 
                bone_a="J_Bip_R_UpperLeg",
                req_bones=["J_Bip_R_UpperLeg"],
                operations=[ParentBoneOperation(time="Pre", bone_name="thigh.R", parent=["Spine.001", "j_kosi"], is_connected=False),
                            RigifyTypeOperation(time="Pre", bone_name="thigh.R", rigify_type=rigify.types.limbs_leg( fk_coll="Leg.R (FK)", tweak_coll="Leg.R (Tweak)")), 
                            CollectionOperation(time="Pre", bone_name="thigh.R", collection_name="Leg.R (IK)")]
            ),
            CopyBone(
                name="shin.R", 
                bone_a="J_Bip_R_LowerLeg", 
                parent="thigh.R", 
                is_connected=True,
                req_bones=["J_Bip_R_LowerLeg"],
                operations=[CollectionOperation(time="Pre", bone_name="shin.R", collection_name="Leg.R (IK)")]
            ),

            ## Helper Bones for proper Foot gen
            ParallelBone(
                name="heel_pivot.R.helper",
                bone_a="shin.R",
                bone_b="Root",
                parent="shin.R",
                is_connected=False,
                axis_type="armature",
                axis="Z",
                start="tail",
                end="head",
                coordinate="Z",
                req_bones=["shin.R"],
                operations=[CollectionOperation(time="Pre", bone_name="heel_pivot.R.helper", collection_name="Leg.R (IK)")]
            ),
            ParallelBone(
                name="foot.R.helper",
                bone_a="J_Bip_R_Foot",
                bone_b="Root",
                parent="J_Bip_R_Foot",
                is_connected=False,
                axis_type="armature",
                axis="Z",
                start="tail",
                end="head",
                coordinate="Z",
                req_bones=["J_Bip_R_Foot"],
                operations=[CollectionOperation(time="Pre", bone_name="foot.R.helper", collection_name="Leg.R (IK)")]
            ),

            ParallelBone(
                name="toe.R.helper",
                bone_a="J_Bip_R_ToeBase",
                bone_b="J_Bip_R_ToeBase",
                parent="J_Bip_R_ToeBase",
                is_connected=False,
                axis_type="armature",
                axis="Z",
                start="tail",
                end="head",
                coordinate="Z",
                req_bones=["J_Bip_R_ToeBase"],
                operations=[CollectionOperation(time="Pre", bone_name="toe.R.helper", collection_name="Leg.R (IK)")]
            ),

            ## Foot and Heel
            ConnectBone(
                name="foot.R", 
                bone_a="J_Bip_R_Foot", 
                bone_b="J_Bip_R_ToeBase",
                parent="shin.R",
                end="head",
                is_connected=True,
                req_bones=["J_Bip_R_Foot"],
                operations=[CollectionOperation(time="Pre", bone_name="foot.R", collection_name="Leg.R (IK)")]
            ),
            ConnectBone(
                name="toe.R",
                bone_a="J_Bip_R_ToeBase",
                bone_b="toe.R.helper",
                parent="foot.R",
                end="tail",
                is_connected=True,
                req_bones=["J_Bip_R_ToeBase"],
                operations=[CollectionOperation(time="Pre", bone_name="toe.R", collection_name="Leg.R (IK)")]
            ),
            ExtensionBone(
                name="heel_pivot.R",
                bone_a="heel_pivot.R.helper",
                parent="foot.R",
                is_connected=False,
                axis_type="armature",
                axis="Y",
                size_factor=1.0,
                req_bones=["heel_pivot.R.helper"],
                operations=[CollectionOperation(time="Pre", bone_name="heel_pivot.R", collection_name="Leg.R (IK)")]
            ),
        ],
)

LEG_L = BoneGroup(
        name="Left Leg",
        transform_link= [
            TransformLink(target="DEF-thigh.L.001", bone="J_Bip_L_UpperLeg", retarget="FK-upper_leg.L"),
            TransformLink(target="DEF-shin.L.001", bone="J_Bip_L_LowerLeg", retarget="FK-lower_leg.L"),
            TransformLink(target="DEF-foot.L", bone="J_Bip_L_Foot", retarget="FK-foot.L"),
            TransformLink(target="DEF-toe.L", bone="J_Bip_L_ToeBase", retarget="FK-toe.L"),
            ],
        generators = [
            # Left Leg
            CopyBone(
                name="thigh.L", 
                bone_a="J_Bip_L_UpperLeg",
                req_bones=["J_Bip_L_UpperLeg"],
                operations=[ParentBoneOperation(time="Pre", bone_name="thigh.L", parent=["Spine.001", "j_kosi"], is_connected=False),
                            RigifyTypeOperation(time="Pre", bone_name="thigh.L", rigify_type=rigify.types.limbs_leg( fk_coll="Leg.L (FK)", tweak_coll="Leg.L (Tweak)")), 
                            CollectionOperation(time="Pre", bone_name="thigh.L", collection_name="Leg.L (IK)")]
            ),
            CopyBone(
                name="shin.L", 
                bone_a="J_Bip_L_LowerLeg", 
                parent="thigh.L", 
                is_connected=True,
                req_bones=["J_Bip_L_LowerLeg"],
                operations=[CollectionOperation(time="Pre", bone_name="shin.L", collection_name="Leg.L (IK)")]
            ),

            ## Helper Bones for proper Foot gen
            ParallelBone(
                name="heel_pivot.L.helper",
                bone_a="shin.L",
                bone_b="Root",
                parent="shin.L",
                is_connected=False,
                axis_type="armature",
                axis="Z",
                start="tail",
                end="head",
                coordinate="Z",
                req_bones=["shin.L"],
                operations=[CollectionOperation(time="Pre", bone_name="heel_pivot.L.helper", collection_name="Leg.L (IK)")]
            ),
            ParallelBone(
                name="foot.L.helper",
                bone_a="J_Bip_L_Foot",
                bone_b="Root",
                parent="J_Bip_L_Foot",
                is_connected=False,
                axis_type="armature",
                axis="Z",
                start="tail",
                end="head",
                coordinate="Z",
                req_bones=["J_Bip_L_Foot"],
                operations=[CollectionOperation(time="Pre", bone_name="foot.L.helper", collection_name="Leg.L (IK)")]
            ),

            ParallelBone(
                name="toe.L.helper",
                bone_a="J_Bip_L_ToeBase",
                bone_b="J_Bip_L_ToeBase",
                parent="J_Bip_L_ToeBase",
                is_connected=False,
                axis_type="armature",
                axis="Z",
                start="tail",
                end="head",
                coordinate="Z",
                req_bones=["J_Bip_L_ToeBase"],
                operations=[CollectionOperation(time="Pre", bone_name="toe.L.helper", collection_name="Leg.L (IK)")]
            ),

            ## Foot and Heel
            ConnectBone(
                name="foot.L", 
                bone_a="J_Bip_L_Foot", 
                bone_b="J_Bip_L_ToeBase",
                parent="shin.L",
                end="head",
                is_connected=True,
                req_bones=["J_Bip_L_Foot"],
                operations=[CollectionOperation(time="Pre", bone_name="foot.L", collection_name="Leg.L (IK)")]
            ),
            ConnectBone(
                name="toe.L",
                bone_a="J_Bip_L_ToeBase",
                bone_b="toe.L.helper",
                parent="foot.L",
                end="tail",
                is_connected=True,
                req_bones=["J_Bip_L_ToeBase"],
                operations=[CollectionOperation(time="Pre", bone_name="toe.L", collection_name="Leg.L (IK)")]
            ),
            ExtensionBone(
                name="heel_pivot.L",
                bone_a="heel_pivot.L.helper",
                parent="foot.L",
                is_connected=False,
                axis_type="armature",
                axis="Y",
                size_factor=1.0,
                req_bones=["heel_pivot.L.helper"],
                operations=[CollectionOperation(time="Pre", bone_name="heel_pivot.L", collection_name="Leg.L (IK)")]
            ),
        ],
)

def get_rig_module() -> RigModule:
    return RigModule(
        name="VRM-Default",
        type="Generation",
        bone_groups=[LEG_L, LEG_R],
        ui_collections = UI_Collections([
            BoneCollection(name="Leg.L (IK)", ui=True, color_set="IK_Left", row_index=1, title="Leg IK.L"),
            BoneCollection(name="Leg.L (FK)", ui=True, color_set="FK_Left", row_index=2, title="Leg FK.L", visible=False),
            BoneCollection(name="Leg.R (IK)", ui=True, color_set="IK_Right", row_index=1, title="Leg IK.R"),
            BoneCollection(name="Leg.R (FK)", ui=True, color_set="FK_Right", row_index=2, title="Leg FK.R", visible=False),
        ]),
        operations=[
            PropOverrideOperation(bone_name="thigh_parent.L", property_name="IK_Stretch", value=0),
            PropOverrideOperation(bone_name="thigh_parent.R", property_name="IK_Stretch", value=0),
            BoneRestrictionOperation(time="Post", bone_name="thigh_tweak.L", hide_select=True, hide=True),
            BoneRestrictionOperation(time="Post", bone_name="thigh_tweak.R", hide_select=True, hide=True),
            BoneRestrictionOperation(time="Post", bone_name="thigh_tweak.L.001", hide_select=True, hide=True),
            BoneRestrictionOperation(time="Post", bone_name="thigh_tweak.R.001", hide_select=True, hide=True),
            BoneRestrictionOperation(time="Post", bone_name="shin_tweak.L", hide_select=True, hide=True),
            BoneRestrictionOperation(time="Post", bone_name="shin_tweak.R", hide_select=True, hide=True),
            BoneRestrictionOperation(time="Post", bone_name="shin_tweak.L.001", hide_select=True, hide=True),
            BoneRestrictionOperation(time="Post", bone_name="shin_tweak.R.001", hide_select=True, hide=True),
            BoneRestrictionOperation(time="Post", bone_name="foot_tweak.L", hide_select=True, hide=True),
            BoneRestrictionOperation(time="Post", bone_name="foot_tweak.R", hide_select=True, hide=True),
        ]
    )