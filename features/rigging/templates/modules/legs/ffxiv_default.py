from ......core.rigify.settings import UI_Collections, BoneCollection
from ......core.bone_generators import ConnectBone, ExtensionBone, ParallelBone
from ......core.operations import ParentBoneOperation, PropOverrideOperation, RigifyTypeOperation, CollectionOperation, ConstraintOperation
from ......core.constraints import DampedTrackConstraint
from ......core.shared import PoseOperations, BoneGroup, TransformLink, RigModule
from ......core import rigify

LEG_R = BoneGroup(
        name="Right Leg",
        transform_link= [
            TransformLink(target="DEF-thigh.R.001", bone="j_asi_a_r", retarget="FK-upper_leg.R"),
            TransformLink(target="DEF-shin.R.001", bone="j_asi_c_r", retarget="FK-lower_leg.R"),
            TransformLink(target="DEF-foot.R", bone="j_asi_d_r", retarget="FK-foot.R"),
            TransformLink(target="DEF-toe.R", bone="j_asi_e_r", retarget="FK-toe.R"),
            TransformLink(target="DEF-knee.R", bone="j_asi_b_r"),
            TransformLink(target="DEF-knee.L", bone="j_asi_b_l")
            ],
        generators = [
            # Right Leg
            ConnectBone(
                name="thigh.R", 
                bone_a="j_asi_a_r",
                bone_b="j_asi_b_r",
                parent="Spine.001",
                roll=-90,
                end="tail",
                req_bones=["j_asi_a_r", "j_asi_c_r"],
                operations=[ParentBoneOperation(time="Pre", bone_name="thigh.R", parent=["Spine.001", "j_kosi"], is_connected=False),
                            RigifyTypeOperation(time="Pre", bone_name="thigh.R", rigify_type=rigify.types.limbs_leg( fk_coll="Leg.R (FK)", tweak_coll="Leg.R (Tweak)")), 
                            CollectionOperation(time="Pre", bone_name="thigh.R", collection_name="Leg.R (IK)")]
            ),
            ConnectBone(
                name="shin.R", 
                bone_a="j_asi_b_r", 
                bone_b="j_asi_d_r", 
                parent="thigh.R", 
                roll=-90,
                start="tail",
                is_connected=True,
                req_bones=["j_asi_c_r", "j_asi_d_r"],
                operations=[CollectionOperation(time="Pre", bone_name="shin.R", collection_name="Leg.R (IK)")]
            ),
            ConnectBone(
                name="foot.R", 
                bone_a="j_asi_d_r", 
                bone_b="j_asi_e_r", 
                parent="shin.R",
                is_connected=True,
                roll=-90,
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
            ),
            #MCH Bone
            ExtensionBone(
                name="MCH-knee.R",
                bone_a="j_asi_b_r",
                parent="spine.001", #Rigify's leg will get mad if I use the leg bones as parent, can just reparent with an operation
                start="head",
                is_connected=False,
                axis_type="local",
                axis="Y",
                size_factor=1.5,
                req_bones=["thigh.R"],
                operations=[
                    RigifyTypeOperation(bone_name="MCH-knee.R", rigify_type=rigify.types.basic_raw_copy()),
                    CollectionOperation(bone_name="MCH-knee.R", collection_name="MCH"),
                    ParentBoneOperation(time="Post", bone_name="MCH-knee.R", parent=["DEF-thigh.R.001"]),
                    ConstraintOperation(time="Post", bone_name="MCH-knee.R", constraint=DampedTrackConstraint(target_bone="MCH-knee_target.R"))
                ]
            ),
            ExtensionBone(
                name="knee.R",
                bone_a="j_asi_b_r",
                parent="spine.001", #Rigify's leg will get mad if I use the leg bones as parent, can just reparent with an operation
                start="head",
                is_connected=False,
                axis_type="local",
                axis="Y",
                size_factor=1.5,
                req_bones=["thigh.R"],
                operations=[
                    RigifyTypeOperation(bone_name="knee.R", rigify_type=rigify.types.basic_super_copy()),
                    CollectionOperation(bone_name="knee.R", collection_name="MCH"),
                    ParentBoneOperation(time="Post", bone_name="knee.R", parent=["MCH-knee.R"])
                ]
            ),
            # MCH Bones 
            # This has gotta be the biggest brain idea I've had in a while - Oats
            ExtensionBone(
                name="MCH-knee_target.R",
                bone_a="j_asi_c_r",
                parent="spine.001",
                start="head",
                is_connected=False,
                axis_type="local",
                axis="Y",
                size_factor=0.2,
                req_bones=["shin.R"],
                operations=[
                    RigifyTypeOperation(bone_name="MCH-knee_target.R", rigify_type=rigify.types.basic_raw_copy()),
                    CollectionOperation(bone_name="MCH-knee_target.R", collection_name="MCH"),
                    ParentBoneOperation(time="Post", bone_name="MCH-knee_target.R", parent=["DEF-shin.R"])
                ]
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
                bone_b="j_asi_b_l",
                parent="Spine.001",
                roll=-90,
                end="tail",
                req_bones=["j_asi_a_l", "j_asi_c_l"],
                operations=[ParentBoneOperation(time="Pre", bone_name="thigh.L", parent=["Spine.001", "j_kosi"], is_connected=False),
                            RigifyTypeOperation(time="Pre", bone_name="thigh.L", rigify_type=rigify.types.limbs_leg( fk_coll="Leg.L (FK)", tweak_coll="Leg.L (Tweak)")), 
                            CollectionOperation(time="Pre", bone_name="thigh.L", collection_name="Leg.L (IK)")]
            ),
            ConnectBone(
                name="shin.L", 
                bone_a="j_asi_b_l", 
                bone_b="j_asi_d_l", 
                parent="thigh.L",
                roll=-90,
                start="tail",
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
            ),
            #MCH Bone
            ExtensionBone(
                name="MCH-knee.L",
                bone_a="j_asi_b_l",
                parent="spine.001", #Rigify's leg will get mad if I use the leg bones as parent, can just reparent with an operation
                start="head",
                is_connected=False,
                axis_type="local",
                axis="Y",
                size_factor=1.5,
                req_bones=["thigh.L"],
                operations=[
                    RigifyTypeOperation(bone_name="MCH-knee.L", rigify_type=rigify.types.basic_raw_copy()),
                    CollectionOperation(bone_name="MCH-knee.L", collection_name="MCH"),
                    ParentBoneOperation(time="Post", bone_name="MCH-knee.L", parent=["DEF-thigh.L.001"]),
                    ConstraintOperation(time="Post", bone_name="MCH-knee.L", constraint=DampedTrackConstraint(target_bone="MCH-knee_target.L"))
                ]
            ),
            ExtensionBone(
                name="knee.L",
                bone_a="j_asi_b_l",
                parent="spine.001", #Rigify's leg will get mad if I use the leg bones as parent, can just reparent with an operation
                start="head",
                is_connected=False,
                axis_type="local",
                axis="Y",
                size_factor=1.5,
                req_bones=["thigh.L"],
                operations=[
                    RigifyTypeOperation(bone_name="knee.L", rigify_type=rigify.types.basic_super_copy()),
                    CollectionOperation(bone_name="knee.L", collection_name="MCH"),
                    ParentBoneOperation(time="Post", bone_name="knee.L", parent=["MCH-knee.L"])
                ]
            ),
            # MCH Bones 
            # This has gotta be the biggest brain idea I've had in a while - Oats
            ExtensionBone(
                name="MCH-knee_target.L",
                bone_a="j_asi_c_l",
                parent="spine.001",
                start="head",
                is_connected=False,
                axis_type="local",
                axis="Y",
                size_factor=0.2,
                req_bones=["shin.L"],
                operations=[
                    RigifyTypeOperation(bone_name="MCH-knee_target.L", rigify_type=rigify.types.basic_raw_copy()),
                    CollectionOperation(bone_name="MCH-knee_target.L", collection_name="MCH"),
                    ParentBoneOperation(time="Post", bone_name="MCH-knee_target.L", parent=["DEF-shin.L"])
                ]
            )
        ],
)

def get_rig_module() -> RigModule:
    return RigModule(
        name="XIV-Default",
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