from ......core.rigify.settings import UI_Collections, BoneCollection
from ......core.bone_generators import ConnectBone, CopyBone, ExtensionBone, ParallelBone
from ......core.operations import ParentBoneOperation, PropOverrideOperation, RigifyTypeOperation, CollectionOperation, ConstraintOperation
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


            CopyBone(
                name="foot.R", 
                bone_a="J_Bip_R_Foot", 
                parent="shin.R",
                is_connected=True,
                req_bones=["J_Bip_R_Foot"],
                operations=[CollectionOperation(time="Pre", bone_name="foot.R", collection_name="Leg.R (IK)")]
            ),
            CopyBone(
                name="toe.R",
                bone_a="J_Bip_R_ToeBase",
                parent="foot.R",
                is_connected=True,
                req_bones=["J_Bip_R_ToeBase"],
                operations=[CollectionOperation(time="Pre", bone_name="toe.R", collection_name="Leg.R (IK)")]
            ),

            ParallelBone(
                name="heel_pivot.R.helper",
                bone_a="toe.R",
                bone_b="shin.R",
                parent="shin.R",
                is_connected=False,
                axis_type="local",
                axis="Y",
                start="head",
                end="tail",
                coordinate="Y",
                req_bones=["toe.R", "shin.R"],
                operations=[CollectionOperation(time="Pre", bone_name="heel_pivot.R.helper", collection_name="Leg.R (IK)")]
            ),
            ExtensionBone(
                name="heel_pivot.R",
                bone_a="heel_pivot.R.helper",
                parent="foot.R",
                is_connected=False,
                axis_type="local",
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


            CopyBone(
                name="foot.L", 
                bone_a="J_Bip_L_Foot", 
                parent="shin.L",
                is_connected=True,
                req_bones=["J_Bip_L_Foot"],
                operations=[CollectionOperation(time="Pre", bone_name="foot.L", collection_name="Leg.L (IK)")]
            ),
            CopyBone(
                name="toe.L",
                bone_a="J_Bip_L_ToeBase",
                parent="foot.L",
                is_connected=True,
                req_bones=["J_Bip_L_ToeBase"],
                operations=[CollectionOperation(time="Pre", bone_name="toe.L", collection_name="Leg.L (IK)")]
            ),

            ParallelBone(
                name="heel_pivot.L.helper",
                bone_a="toe.L",
                bone_b="shin.L",
                parent="shin.L",
                is_connected=False,
                axis_type="local",
                axis="Y",
                start="head",
                end="tail",
                coordinate="Y",
                req_bones=["toe.L", "shin.L"],
                operations=[CollectionOperation(time="Pre", bone_name="heel_pivot.L.helper", collection_name="Leg.L (IK)")]
            ),
            ExtensionBone(
                name="heel_pivot.L",
                bone_a="heel_pivot.L.helper",
                parent="foot.L",
                is_connected=False,
                axis_type="local",
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
            BoneCollection(name="Leg.L (Tweak)", ui=True, color_set="Tweak_Left", row_index=3, title="Tweak.L", visible=False),
            BoneCollection(name="Leg.R (IK)", ui=True, color_set="IK_Right", row_index=1, title="Leg IK.R"),
            BoneCollection(name="Leg.R (FK)", ui=True, color_set="FK_Right", row_index=2, title="Leg FK.R", visible=False),
            BoneCollection(name="Leg.R (Tweak)", ui=True, color_set="Tweak_Right", row_index=3, title="Tweak.R", visible=False),
        ]),
        operations=[
            PropOverrideOperation(bone_name="thigh_parent.L", property_name="IK_Stretch", value=0),
            PropOverrideOperation(bone_name="thigh_parent.R", property_name="IK_Stretch", value=0),
        ]
    )