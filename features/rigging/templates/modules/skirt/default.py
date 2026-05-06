from ......core.rigify.settings import UI_Collections, BoneCollection
from ......core.operations import ParentBoneOperation, ConstraintOperation, RigifyTypeOperation, CollectionOperation, DriverOperation
from ......core.constraints import DampedTrackConstraint
from ......core.bone_generators import ConnectBone, ExtensionBone
from ......core.shared import PoseOperations, BoneGroup, TransformLink, RigModule
from ......core import rigify
from ......core.drivers import TransformChannelVariable, Driver

SKIRT_R = BoneGroup(
        name="Skirt Right",
        transform_link= [
            TransformLink(target="DEF-Skirt_Front.R", bone="j_sk_f_a_r"),
            TransformLink(target="DEF-Skirt_Front.R.001", bone="j_sk_f_b_r"),
            TransformLink(target="DEF-Skirt_Front.R.002", bone="j_sk_f_c_r"),
            TransformLink(target="DEF-Skirt_Side.R", bone="j_sk_s_a_r"),
            TransformLink(target="DEF-Skirt_Side.R.001", bone="j_sk_s_b_r"),
            TransformLink(target="DEF-Skirt_Side.R.002", bone="j_sk_s_c_r"),
            TransformLink(target="DEF-Skirt_Back.R", bone="j_sk_b_a_r"),
            TransformLink(target="DEF-Skirt_Back.R.001", bone="j_sk_b_b_r"),
            TransformLink(target="DEF-Skirt_Back.R.002", bone="j_sk_b_c_r"),
            ],
        generators = [
            #Front
            ConnectBone(
                name="Skirt_Front.R",
                bone_a="j_sk_f_a_r",
                bone_b="j_sk_f_b_r",
                parent="Spine.001",
                is_connected=False,
                req_bones=["j_sk_f_a_r", "j_sk_f_b_r"],
                operations=[
                    RigifyTypeOperation(bone_name="Skirt_Front.R", rigify_type=rigify.types.basic_copy_chain()),
                    CollectionOperation(bone_name="Skirt_Front.R", collection_name="Skirt")
                ]
            ),
            ConnectBone(
                name="Skirt_Front.R.001",
                bone_a="j_sk_f_b_r",
                bone_b="j_sk_f_c_r",
                parent="Skirt_Front.R",
                is_connected=True,
                req_bones=["j_sk_f_b_r", "j_sk_f_c_r"],
                operations=[
                    CollectionOperation(bone_name="Skirt_Front.R.001", collection_name="Skirt")
                ]
            ),
            ExtensionBone(
                name="Skirt_Front.R.002",
                bone_a="j_sk_f_c_r",
                parent="Skirt_Front.R.001",
                is_connected=True,
                axis_type="local",
                axis="Y",
                start="tail",
                req_bones=["j_sk_f_c_r"],
                operations=[
                    CollectionOperation(bone_name="Skirt_Front.R.002", collection_name="Skirt")
                ]
            ),
            #Side
            ConnectBone(
                name="Skirt_Side.R",
                bone_a="j_sk_s_a_r",
                bone_b="j_sk_s_b_r",
                parent="Spine.001",
                is_connected=False,
                req_bones=["j_sk_s_a_r", "j_sk_s_b_r"],
                operations=[
                    RigifyTypeOperation(bone_name="Skirt_Side.R", rigify_type=rigify.types.basic_copy_chain()),
                    CollectionOperation(bone_name="Skirt_Side.R", collection_name="Skirt")
                ]
            ),
            ConnectBone(
                name="Skirt_Side.R.001",
                bone_a="j_sk_s_b_r",
                bone_b="j_sk_s_c_r",
                parent="Skirt_Side.R",
                is_connected=True,
                req_bones=["j_sk_s_b_r", "j_sk_s_c_r"],
                operations=[
                    CollectionOperation(bone_name="Skirt_Side.R.001", collection_name="Skirt")
                ]
            ),
            ExtensionBone(
                name="Skirt_Side.R.002",
                bone_a="j_sk_s_c_r",
                parent="Skirt_Side.R.001",
                is_connected=True,
                axis_type="local",
                axis="Y",
                start="head",
                req_bones=["j_sk_s_c_r"],
                operations=[
                    CollectionOperation(bone_name="Skirt_Side.R.002", collection_name="Skirt")
                ]
            ),
            #Back
            ConnectBone(
                name="Skirt_Back.R",
                bone_a="j_sk_b_a_r",
                bone_b="j_sk_b_b_r",
                parent="Spine.001",
                is_connected=False,
                req_bones=["j_sk_b_a_r", "j_sk_b_b_r"],
                operations=[
                    RigifyTypeOperation(bone_name="Skirt_Back.R", rigify_type=rigify.types.basic_copy_chain()),
                    CollectionOperation(bone_name="Skirt_Back.R", collection_name="Skirt")
                ]
            ),
            ConnectBone(
                name="Skirt_Back.R.001",
                bone_a="j_sk_b_b_r",
                bone_b="j_sk_b_c_r",
                parent="Skirt_Back.R",
                is_connected=True,
                req_bones=["j_sk_b_b_r", "j_sk_b_c_r"],
                operations=[
                    CollectionOperation(bone_name="Skirt_Back.R.001", collection_name="Skirt")
                ]
            ),
            ExtensionBone(
                name="Skirt_Back.R.002",
                bone_a="j_sk_b_c_r",
                parent="Skirt_Back.R.001",
                is_connected=True,
                axis_type="local",
                axis="Y",
                start="head",
                req_bones=["j_sk_b_c_r"],
                operations=[
                    CollectionOperation(bone_name="Skirt_Back.R.002", collection_name="Skirt")
                ]
            ),
            #DriverTGT
            ExtensionBone(
                name="MCH-thigh_driv_tgt.R",
                bone_a="thigh.R",
                parent="Spine.001",
                start="head",
                size_factor=0.3,
                req_bones=["thigh.R"],
                operations=[
                    RigifyTypeOperation(bone_name="MCH-thigh_driv_tgt.R", rigify_type=rigify.types.basic_raw_copy()),
                    CollectionOperation(bone_name="MCH-thigh_driv_tgt.R", collection_name="MCH", time="Post"),
                    ConstraintOperation(bone_name="MCH-thigh_driv_tgt.R", constraint=DampedTrackConstraint(target_bone="ORG-shin.R"))
                ]
            ),
            #Driver Bones
            ConnectBone(
                name="MCH-Skirt_Front.R",
                bone_a="j_sk_f_a_r",
                bone_b="j_sk_f_b_r",
                parent="Spine.001",
                is_connected=False,
                req_bones=["j_sk_f_a_r", "j_sk_f_b_r"],
                operations=[
                    RigifyTypeOperation(bone_name="MCH-Skirt_Front.R", rigify_type=rigify.types.basic_raw_copy()),
                    CollectionOperation(bone_name="MCH-Skirt_Front.R", collection_name="MCH", time="Post"),
                    DriverOperation(
                        bone_name="MCH-Skirt_Front.R",
                        driver_name="Sk_f_a_r",
                        property=["rotation_quaternion", 1],
                        driver=Driver(
                            type="SCRIPTED",
                            expression="-var * prop / (1.2 + abs(var) *-0.4) if var < 0 else -var * 1 / (2 + abs(var) *6)",
                            variables=[
                                TransformChannelVariable(target_bone="MCH-thigh_driv_tgt.R", transform_type="ROT_X", rotation_mode="QUATERNION", transform_space="LOCAL_SPACE"),
                            ],
                        ),
                    ),
                ]
            ),
            ConnectBone(
                name="MCH-Skirt_Front.R.001",
                bone_a="j_sk_f_b_r",
                bone_b="j_sk_f_c_r",
                parent="MCH-Skirt_Front.R",
                is_connected=True,
                req_bones=["j_sk_f_b_r", "j_sk_f_c_r"],
                operations=[
                    RigifyTypeOperation(bone_name="MCH-Skirt_Front.R.001", rigify_type=rigify.types.basic_raw_copy()),
                    CollectionOperation(bone_name="MCH-Skirt_Front.R.001", collection_name="MCH", time="Post")
                ]
            ),
            ExtensionBone(
                name="MCH-Skirt_Front.R.002",
                bone_a="j_sk_f_c_r",
                parent="MCH-Skirt_Front.R.001",
                is_connected=True,
                axis_type="local",
                axis="Y",
                start="tail",
                req_bones=["j_sk_f_c_r"],
                operations=[
                    RigifyTypeOperation(bone_name="MCH-Skirt_Front.R.002", rigify_type=rigify.types.basic_raw_copy()),
                    CollectionOperation(bone_name="MCH-Skirt_Front.R.002", collection_name="MCH", time="Post")
                ]
            ),
        ],
)

SKIRT_L = BoneGroup(
        name="Skirt Left",
        transform_link= [
            TransformLink(target="DEF-Skirt_Front.L", bone="j_sk_f_a_l"),
            TransformLink(target="DEF-Skirt_Front.L.001", bone="j_sk_f_b_l"),
            TransformLink(target="DEF-Skirt_Front.L.002", bone="j_sk_f_c_l"),
            TransformLink(target="DEF-Skirt_Side.L", bone="j_sk_s_a_l"),
            TransformLink(target="DEF-Skirt_Side.L.001", bone="j_sk_s_b_l"),
            TransformLink(target="DEF-Skirt_Side.L.002", bone="j_sk_s_c_l"),
            TransformLink(target="DEF-Skirt_Back.L", bone="j_sk_b_a_l"),
            TransformLink(target="DEF-Skirt_Back.L.001", bone="j_sk_b_b_l"),
            TransformLink(target="DEF-Skirt_Back.L.002", bone="j_sk_b_c_l"),
            ],
        generators = [
            #Front
            ConnectBone(
                name="Skirt_Front.L",
                bone_a="j_sk_f_a_l",
                bone_b="j_sk_f_b_l",
                parent="Spine.001",
                is_connected=False,
                req_bones=["j_sk_f_a_l", "j_sk_f_b_l"],
                pose_operations=PoseOperations(
                    rigify_settings=rigify.types.basic_copy_chain(),
                    b_collection="Skirt (Tweak)"
                )
            ),
            ConnectBone(
                name="Skirt_Front.L.001",
                bone_a="j_sk_f_b_l",
                bone_b="j_sk_f_c_l",
                parent="Skirt_Front.L",
                is_connected=True,
                req_bones=["j_sk_f_b_l", "j_sk_f_c_l"],
                pose_operations=PoseOperations(
                    b_collection="Skirt"
                )
            ),
            ExtensionBone(
                name="Skirt_Front.L.002",
                bone_a="j_sk_f_c_l",
                parent="Skirt_Front.L.001",
                is_connected=True,
                axis_type="local",
                axis="Y",
                start="tail",
                req_bones=["j_sk_f_c_l"],
                pose_operations=PoseOperations(
                    b_collection="Skirt"
                )
            ),
            #Side
            ConnectBone(
                name="Skirt_Side.L",
                bone_a="j_sk_s_a_l",
                bone_b="j_sk_s_b_l",
                parent="Spine.001",
                is_connected=False,
                req_bones=["j_sk_s_a_l", "j_sk_s_b_l"],
                pose_operations=PoseOperations(
                    rigify_settings=rigify.types.basic_copy_chain(),
                    b_collection="Skirt (Tweak)"
                )
            ),
            ConnectBone(
                name="Skirt_Side.L.001",
                bone_a="j_sk_s_b_l",
                bone_b="j_sk_s_c_l",
                parent="Skirt_Side.L",
                is_connected=True,
                req_bones=["j_sk_s_b_l", "j_sk_s_c_l"],
                pose_operations=PoseOperations(
                    b_collection="Skirt"
                )
            ),
            ExtensionBone(
                name="Skirt_Side.L.002",
                bone_a="j_sk_s_c_l",
                parent="Skirt_Side.L.001",
                is_connected=True,
                axis_type="local",
                axis="Y",
                start="head",
                req_bones=["j_sk_s_c_l"],
                pose_operations=PoseOperations(
                    b_collection="Skirt"
                )
            ),
            #Back
            ConnectBone(
                name="Skirt_Back.L",
                bone_a="j_sk_b_a_l",
                bone_b="j_sk_b_b_l",
                parent="Spine.001",
                is_connected=False,
                req_bones=["j_sk_b_a_l", "j_sk_b_b_l"],
                pose_operations=PoseOperations(
                    rigify_settings=rigify.types.basic_copy_chain(),
                    b_collection="Skirt (Tweak)"
                )
            ),
            ConnectBone(
                name="Skirt_Back.L.001",
                bone_a="j_sk_b_b_l",
                bone_b="j_sk_b_c_l",
                parent="Skirt_Back.L",
                is_connected=True,
                req_bones=["j_sk_b_b_l", "j_sk_b_c_l"],
                pose_operations=PoseOperations(
                    b_collection="Skirt"
                )
            ),
            ExtensionBone(
                name="Skirt_Back.L.002",
                bone_a="j_sk_b_c_l",
                parent="Skirt_Back.L.001",
                is_connected=True,
                axis_type="local",
                axis="Y",
                start="head",
                req_bones=["j_sk_b_c_l"],
                pose_operations=PoseOperations(
                    b_collection="Skirt"
                )
            ),
        ],
)

def get_rig_module() -> RigModule:
    return RigModule(
        name="Default",
        type="Generation",
        bone_groups=[SKIRT_R, SKIRT_L],
        ui = UI_Collections([
            BoneCollection(name="Skirt", ui=True, color_set="Head", row_index=1, title="Skirt", visible=False),
            BoneCollection(name="Skirt (Tweak)", ui=True, color_set="Head", row_index=2, title="Skirt (Tweak)", visible=False),
        ])
    )
