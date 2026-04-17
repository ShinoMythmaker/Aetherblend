from ......core.rigify.settings import UI_Collections, BoneCollection
from ......core.generators import ConnectBone, ExtensionBone, ParallelBone
from ......core.operations import ParentBoneOperation, RigifyTypeOperation, CollectionOperation
from ......core.shared import PoseOperations, BoneGroup, TransformLink, RigModule
from ......core import rigify

LEG_R = BoneGroup(
        name="Right Leg",
        transform_link= [
            TransformLink(target="DEF-thigh.R.001", bone="j_asi_a_r", retarget="FK-upper_leg.R"),
            TransformLink(target="DEF-shin.R.001", bone="j_asi_c_r", retarget="FK-lower_leg.R"),
            TransformLink(target="DEF-foot.R", bone="j_asi_d_r", retarget="FK-foot.R"),
            TransformLink(target="DEF-toe.R", bone="j_asi_e_r", retarget="FK-toe.R"),
            ],
        generators = [
            # Right Leg
            ConnectBone(
                name="thigh.R", 
                bone_a="j_asi_a_r",
                bone_b="j_asi_c_r",
                parent="Spine.001",
                req_bones=["j_asi_a_r", "j_asi_c_r"],
                operations=[ParentBoneOperation(time="Pre", bone_name="thigh.R", parent=["Spine.001", "j_kosi"], is_connected=False),
                            RigifyTypeOperation(time="Pre", bone_name="thigh.R", rigify_type=rigify.types.limbs_leg( fk_coll="Leg.R (FK)", tweak_coll="Leg.R (Tweak)")), 
                            CollectionOperation(time="Pre", bone_name="thigh.R", collection_name="Leg.R")]
            ),
            ConnectBone(
                name="shin.R", 
                bone_a="j_asi_c_r", 
                bone_b="j_asi_d_r", 
                parent="thigh.R", 
                is_connected=True,
                req_bones=["j_asi_c_r", "j_asi_d_r"],
                operations=[CollectionOperation(time="Pre", bone_name="shin.R", collection_name="Leg.R")]
            ),
            ConnectBone(
                name="foot.R", 
                bone_a="j_asi_d_r", 
                bone_b="j_asi_e_r", 
                parent="shin.R",
                is_connected=True,
                req_bones=["j_asi_d_r", "j_asi_e_r"],
                operations=[CollectionOperation(time="Pre", bone_name="foot.R", collection_name="Leg.R (IK)")]
            ),
            ExtensionBone(
                name="toe.R",
                bone_a="j_asi_e_r",
                parent="foot.R",
                is_connected=True,
                axis_type="local",
                axis="Y",
                start="head",
                req_bones=["j_asi_e_r"],
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
            )
        ],
)

LEG_L = BoneGroup(
        name="Left Leg",
        transform_link= [
            TransformLink(target="DEF-thigh.L.001", bone="j_asi_a_l", retarget="FK-upper_leg.L"),
            TransformLink(target="DEF-shin.L.001", bone="j_asi_c_l", retarget="FK-lower_leg.L"),
            TransformLink(target="DEF-foot.L", bone="j_asi_d_l", retarget="FK-foot.L"),
            TransformLink(target="DEF-toe.L", bone="j_asi_e_l", retarget="FK-toe.L"),
            ],
        generators = [
            # Left Leg
            ConnectBone(
                name="thigh.L", 
                bone_a="j_asi_a_l",
                bone_b="j_asi_c_l",
                parent="Spine.001",
                req_bones=["j_asi_a_l", "j_asi_c_l"],
                operations=[ParentBoneOperation(time="Pre", bone_name="thigh.L", parent=["Spine.001", "j_kosi"], is_connected=False),
                            RigifyTypeOperation(time="Pre", bone_name="thigh.L", rigify_type=rigify.types.limbs_leg( fk_coll="Leg.L (FK)", tweak_coll="Leg.L (Tweak)")), 
                            CollectionOperation(time="Pre", bone_name="thigh.L", collection_name="Leg.L")]
            ),
            ConnectBone(
                name="shin.L", 
                bone_a="j_asi_c_l", 
                bone_b="j_asi_d_l", 
                parent="thigh.L", 
                is_connected=True,
                req_bones=["j_asi_c_l", "j_asi_d_l"],
                operations=[CollectionOperation(time="Pre", bone_name="shin.L", collection_name="Leg.L (IK)")]
            ),
            ConnectBone(
                name="foot.L", 
                bone_a="j_asi_d_l", 
                bone_b="j_asi_e_l", 
                parent="shin.L",
                is_connected=True,
                req_bones=["j_asi_d_l", "j_asi_e_l"],
                operations=[CollectionOperation(time="Pre", bone_name="foot.L", collection_name="Leg.L (IK)")]
            ),
            ExtensionBone(
                name="toe.L",
                bone_a="j_asi_e_l",
                parent="foot.L",
                is_connected=True,
                axis_type="local",
                axis="Y",
                start="head",
                req_bones=["j_asi_e_l"],
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
            )
        ],
)

def get_rig_module() -> RigModule:
    return RigModule(
        name="Default",
        type="Generation",
        bone_groups=[LEG_L, LEG_R],
        ui = UI_Collections([
            BoneCollection(name="Leg.L (IK)", ui=True, color_set="IK_Left", row_index=1, title="Leg IK.L"),
            BoneCollection(name="Leg.L (FK)", ui=True, color_set="FK_Left", row_index=2, title="Leg FK.L", visible=False),
            BoneCollection(name="Leg.L (Tweak)", ui=True, color_set="Tweak_Left", row_index=3, title="Tweak.L", visible=False),
            BoneCollection(name="Leg.R (IK)", ui=True, color_set="IK_Right", row_index=1, title="Leg IK.R"),
            BoneCollection(name="Leg.R (FK)", ui=True, color_set="FK_Right", row_index=2, title="Leg FK.R", visible=False),
            BoneCollection(name="Leg.R (Tweak)", ui=True, color_set="Tweak_Right", row_index=3, title="Tweak.R", visible=False),
        ])
    )