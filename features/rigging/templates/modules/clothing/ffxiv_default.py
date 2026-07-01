from ......core.rigify.settings import UI_Collections, BoneCollection
from ......core.operations import ParentBoneOperation, ConstraintOperation, RigifyTypeOperation, CollectionOperation, DriverOperation, CustomPropertyOperation
from ......core.constraints import DampedTrackConstraint
from ......core.bone_generators import ConnectBone, ExtensionBone
from ......core.shared import PoseOperations, BoneGroup, TransformLink, RigModule
from ......core import rigify
from ......core.drivers import TransformChannelVariable, Driver, SinglePropertyVariable
from ......core.custom_properties import FloatProperty

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
                    CollectionOperation(bone_name="Skirt_Front.R", collection_name="Skirt"),
                    ParentBoneOperation(bone_name="Skirt_Front.R", parent=["MCH-Skirt_Front.R"], time="Post")
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
                    CollectionOperation(bone_name="Skirt_Front.R.001", collection_name="Skirt"),
                ]
            ),
            ExtensionBone(
                name="Skirt_Front.R.002",
                bone_a="j_sk_f_c_r",
                parent="Skirt_Front.R.001",
                is_connected=True,
                axis_type="local",
                axis="Y",
                start="head",
                req_bones=["j_sk_f_c_r"],
                operations=[
                    CollectionOperation(bone_name="Skirt_Front.R.002", collection_name="Skirt"),
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
                    CollectionOperation(bone_name="Skirt_Side.R", collection_name="Skirt"),
                    ParentBoneOperation(bone_name="Skirt_Side.R", parent=["MCH-Skirt_Middle.R"], time="Post")
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
                    CollectionOperation(bone_name="Skirt_Side.R.001", collection_name="Skirt"),
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
                    CollectionOperation(bone_name="Skirt_Side.R.002", collection_name="Skirt"),
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
                    CollectionOperation(bone_name="Skirt_Back.R", collection_name="Skirt"),
                    ParentBoneOperation(bone_name="Skirt_Back.R", parent=["MCH-Skirt_Back.R"], time="Post")
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
                    CollectionOperation(bone_name="Skirt_Back.R.001", collection_name="Skirt"),
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
                    CollectionOperation(bone_name="Skirt_Back.R.002", collection_name="Skirt"),
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
                    ConstraintOperation(bone_name="MCH-thigh_driv_tgt.R", constraint=DampedTrackConstraint(target_bone="ORG-shin.R"), time="Post")
                ]
            ),
            ExtensionBone(
                name="MCH-shin_driv_tgt.R",
                bone_a="shin.R",
                parent="thigh.R",
                start="head",
                size_factor=0.3,
                req_bones=["shin.R"],
                operations=[
                    RigifyTypeOperation(bone_name="MCH-shin_driv_tgt.R", rigify_type=rigify.types.basic_raw_copy()),
                    CollectionOperation(bone_name="MCH-shin_driv_tgt.R", collection_name="MCH", time="Post"),
                    ConstraintOperation(bone_name="MCH-shin_driv_tgt.R", constraint=DampedTrackConstraint(target_bone="ORG-foot.R"), time="Post")
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
                    CustomPropertyOperation(property=FloatProperty(property_name="skirt_automation", property_value=1.0, min=0.0, max=1.0), time="Post"),
                    DriverOperation(
                        bone_name="MCH-Skirt_Front.R",
                        driver_name="Sk_f_a_r",
                        property=["rotation_quaternion", 1],
                        driver=Driver(
                            type="SCRIPTED",
                            expression="((RotX < 0) * (RotX * sk_auto) / (1 + (abs(RotX) - 0.8) * 0.1))",
                            variables=[
                                TransformChannelVariable(name="RotX", target_bone="MCH-thigh_driv_tgt.R", transform_type="ROT_X", rotation_mode="QUATERNION", transform_space="LOCAL_SPACE"),
                                SinglePropertyVariable(name= "sk_auto", data_path="skirt_automation")
                            ],
                        ),
                        time="Post"
                    ),
                    DriverOperation(
                        bone_name="MCH-Skirt_Front.R",
                        driver_name="Sk_f_a_r.001",
                        property=["rotation_quaternion", 3],
                        driver=Driver(
                            type="SCRIPTED",
                            expression="((RotZ > 0) * (RotZ * sk_auto) / (2 + (abs(RotZ) - 0.5) * 0.5))",
                            variables=[
                                TransformChannelVariable(name="RotZ", target_bone="MCH-thigh_driv_tgt.R", transform_type="ROT_Z", rotation_mode="QUATERNION", transform_space="LOCAL_SPACE"),
                                SinglePropertyVariable(name= "sk_auto", data_path="skirt_automation")
                            ],
                        ),
                        time="Post",
                    )
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
                    CollectionOperation(bone_name="MCH-Skirt_Front.R.001", collection_name="MCH", time="Post"),
                    DriverOperation(
                        bone_name="MCH-Skirt_Front.R.001",
                        driver_name="Sk_f_b_r",
                        property=["rotation_quaternion", 1],
                        driver=Driver(
                            type="SCRIPTED",
                            expression="((RotX > 0) * (RotX * sk_auto) / (2 + (abs(RotX) - 0.5) * 2)) * (abs(RotXThreshold) / (0.2 + abs(RotXThreshold))) if RotXThreshold < 0 else RotX * 0",
                            variables=[
                                TransformChannelVariable(name="RotX", target_bone="MCH-shin_driv_tgt.R", transform_type="ROT_X", rotation_mode="QUATERNION", transform_space="LOCAL_SPACE"),
                                TransformChannelVariable(name="RotXThreshold", target_bone="MCH-thigh_driv_tgt.R", transform_type="ROT_X", rotation_mode="QUATERNION", transform_space="LOCAL_SPACE"),
                                SinglePropertyVariable(name= "sk_auto", data_path="skirt_automation")
                            ],
                        ),
                        time="Post"
                    ),
                ]
            ),
            ExtensionBone(
                name="MCH-Skirt_Front.R.002",
                bone_a="j_sk_f_c_r",
                parent="MCH-Skirt_Front.R.001",
                is_connected=True,
                axis_type="local",
                axis="Y",
                start="head",
                req_bones=["j_sk_f_c_r"],
                operations=[
                    RigifyTypeOperation(bone_name="MCH-Skirt_Front.R.002", rigify_type=rigify.types.basic_raw_copy()),
                    CollectionOperation(bone_name="MCH-Skirt_Front.R.002", collection_name="MCH", time="Post")
                ]
            ),
            ConnectBone(
                name="MCH-Skirt_Middle.R",
                bone_a="j_sk_s_a_r",
                bone_b="j_sk_s_b_r",
                parent="Spine.001",
                is_connected=False,
                roll=-173,
                req_bones=["j_sk_s_a_r", "j_sk_s_b_r"],
                operations=[
                    RigifyTypeOperation(bone_name="MCH-Skirt_Middle.R", rigify_type=rigify.types.basic_raw_copy()),
                    CollectionOperation(bone_name="MCH-Skirt_Middle.R", collection_name="MCH", time="Post"),
                    DriverOperation(
                        bone_name="MCH-Skirt_Middle.R",
                        driver_name="Sk_s_a_r",
                        property=["rotation_quaternion", 1],
                        driver=Driver(
                            type="SCRIPTED",
                            expression="((RotX < 0) * (-RotX * sk_auto) / (3 + (abs(RotX) - 0.5) * 2))",
                            variables=[
                                TransformChannelVariable(name="RotX", target_bone="MCH-thigh_driv_tgt.R", transform_type="ROT_X", rotation_mode="QUATERNION", transform_space="LOCAL_SPACE"),
                                SinglePropertyVariable(name= "sk_auto", data_path="skirt_automation")
                            ],
                        ),
                        time="Post"
                    ),
                    DriverOperation(
                        bone_name="MCH-Skirt_Middle.R",
                        driver_name="Sk_s_a_r.001",
                        property=["rotation_quaternion", 3],
                        driver=Driver(
                            type="SCRIPTED",
                            expression="((RotZ > 0) * (-RotZ * sk_auto) / (1 + (abs(RotZ) - 0.1) * 1))",
                            variables=[
                                TransformChannelVariable(name="RotZ", target_bone="MCH-thigh_driv_tgt.R", transform_type="ROT_Z", rotation_mode="QUATERNION", transform_space="LOCAL_SPACE"),
                                SinglePropertyVariable(name= "sk_auto", data_path="skirt_automation")
                            ],
                        ),
                        time="Post",
                    )
                ]
            ),
            ConnectBone(
                name="MCH-Skirt_Middle.R.001",
                bone_a="j_sk_s_b_r",
                bone_b="j_sk_s_c_r",
                parent="MCH-Skirt_Middle.R",
                is_connected=True,
                roll=-173,
                req_bones=["j_sk_s_b_r", "j_sk_s_c_r"],
                operations=[
                    RigifyTypeOperation(bone_name="MCH-Skirt_Middle.R.001", rigify_type=rigify.types.basic_raw_copy()),
                    CollectionOperation(bone_name="MCH-Skirt_Middle.R.001", collection_name="MCH", time="Post"),
                    DriverOperation(
                        bone_name="MCH-Skirt_Middle.R.001",
                        driver_name="Sk_s_b_r",
                        property=["rotation_quaternion", 1],
                        driver=Driver(
                            type="SCRIPTED",
                            expression="((RotX > 0) * (-RotX * sk_auto) / (3 + (abs(RotX) - 0.2) * 2)) * (abs(RotXThreshold) / (0.2 + abs(RotXThreshold))) if RotXThreshold < 0 else RotX * 0",
                            variables=[
                                TransformChannelVariable(name="RotX", target_bone="MCH-shin_driv_tgt.R", transform_type="ROT_X", rotation_mode="QUATERNION", transform_space="LOCAL_SPACE"),
                                TransformChannelVariable(name="RotXThreshold", target_bone="MCH-thigh_driv_tgt.R", transform_type="ROT_X", rotation_mode="QUATERNION", transform_space="LOCAL_SPACE"),
                                SinglePropertyVariable(name= "sk_auto", data_path="skirt_automation")
                            ],
                        ),
                        time="Post"
                    ),
                ]
            ),
            ExtensionBone(
                name="MCH-Skirt_Middle.R.002",
                bone_a="j_sk_s_c_r",
                parent="MCH-Skirt_Middle.R.001",
                is_connected=True,
                axis_type="local",
                axis="Y",
                start="head",
                roll=-173,
                req_bones=["j_sk_s_c_r"],
                operations=[
                    RigifyTypeOperation(bone_name="MCH-Skirt_Middle.R.002", rigify_type=rigify.types.basic_raw_copy()),
                    CollectionOperation(bone_name="MCH-Skirt_Middle.R.002", collection_name="MCH", time="Post")
                ]
            ),
            ConnectBone(
                name="MCH-Skirt_Back.R",
                bone_a="j_sk_b_a_r",
                bone_b="j_sk_b_b_r",
                parent="Spine.001",
                is_connected=False,
                req_bones=["j_sk_b_a_r", "j_sk_b_b_r"],
                operations=[
                    RigifyTypeOperation(bone_name="MCH-Skirt_Back.R", rigify_type=rigify.types.basic_raw_copy()),
                    CollectionOperation(bone_name="MCH-Skirt_Back.R", collection_name="MCH", time="Post"),
                    DriverOperation(
                        bone_name="MCH-Skirt_Back.R",
                        driver_name="Sk_b_a_r",
                        property=["rotation_quaternion", 1],
                        driver=Driver(
                            type="SCRIPTED",
                            expression="((RotX < 0) * (RotX * sk_auto) / (5 + (abs(RotX) - 0.2) * 5)) + ((RotX > 0) * ((RotX * sk_auto) / (1 + (abs(RotX) + 0.1) * 0.2)))",
                            variables=[
                                TransformChannelVariable(name="RotX", target_bone="MCH-thigh_driv_tgt.R", transform_type="ROT_X", rotation_mode="QUATERNION", transform_space="LOCAL_SPACE"),
                                SinglePropertyVariable(name= "sk_auto", data_path="skirt_automation")
                            ],
                        ),
                        time="Post"
                    ),
                    DriverOperation(
                        bone_name="MCH-Skirt_Back.R",
                        driver_name="Sk_b_a_r.001",
                        property=["rotation_quaternion", 3],
                        driver=Driver(
                            type="SCRIPTED",
                            expression="((RotZ > 0) * (RotZ * sk_auto) / (2 + (abs(RotZ) - 0.1) * 3))",
                            variables=[
                                TransformChannelVariable(name="RotZ", target_bone="MCH-thigh_driv_tgt.R", transform_type="ROT_Z", rotation_mode="QUATERNION", transform_space="LOCAL_SPACE"),
                                SinglePropertyVariable(name= "sk_auto", data_path="skirt_automation")
                            ],
                        ),
                        time="Post",
                    )
                ]
            ),
            ConnectBone(
                name="MCH-Skirt_Back.R.001",
                bone_a="j_sk_b_b_r",
                bone_b="j_sk_b_c_r",
                parent="MCH-Skirt_Back.R",
                is_connected=True,
                req_bones=["j_sk_b_b_r", "j_sk_b_c_r"],
                operations=[
                    RigifyTypeOperation(bone_name="MCH-Skirt_Back.R.001", rigify_type=rigify.types.basic_raw_copy()),
                    CollectionOperation(bone_name="MCH-Skirt_Back.R.001", collection_name="MCH", time="Post"),
                    DriverOperation(
                        bone_name="MCH-Skirt_Back.R.001",
                        driver_name="Sk_b_b_r",
                        property=["rotation_quaternion", 1],
                        driver=Driver(
                            type="SCRIPTED",
                            expression="((RotX > 0) * (RotX * sk_auto) / (1 + (abs(RotX) + 0.5) * 0.3)) * (abs(RotXThreshold) / (0.5 + abs(RotXThreshold))) if RotXThreshold > 0 else RotX * 0",
                            variables=[
                                TransformChannelVariable(name="RotX", target_bone="MCH-shin_driv_tgt.R", transform_type="ROT_X", rotation_mode="QUATERNION", transform_space="LOCAL_SPACE"),
                                TransformChannelVariable(name="RotXThreshold", target_bone="MCH-thigh_driv_tgt.R", transform_type="ROT_X", rotation_mode="QUATERNION", transform_space="LOCAL_SPACE"),
                                SinglePropertyVariable(name= "sk_auto", data_path="skirt_automation")
                            ],
                        ),
                        time="Post"
                    ),
                ]
            ),
            ExtensionBone(
                name="MCH-Skirt_Back.R.002",
                bone_a="j_sk_b_c_r",
                parent="MCH-Skirt_Back.R.001",
                is_connected=True,
                axis_type="local",
                axis="Y",
                start="head",
                req_bones=["j_sk_b_c_r"],
                operations=[
                    RigifyTypeOperation(bone_name="MCH-Skirt_Back.R.002", rigify_type=rigify.types.basic_raw_copy()),
                    CollectionOperation(bone_name="MCH-Skirt_Back.R.002", collection_name="MCH", time="Post")
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
                operations=[
                    RigifyTypeOperation(bone_name="Skirt_Front.L", rigify_type=rigify.types.basic_copy_chain()),
                    CollectionOperation(bone_name="Skirt_Front.L", collection_name="Skirt"),
                    ParentBoneOperation(bone_name="Skirt_Front.L", parent=["MCH-Skirt_Front.L"], time="Post")
                ]
            ),
            ConnectBone(
                name="Skirt_Front.L.001",
                bone_a="j_sk_f_b_l",
                bone_b="j_sk_f_c_l",
                parent="Skirt_Front.L",
                is_connected=True,
                req_bones=["j_sk_f_b_l", "j_sk_f_c_l"],
                operations=[
                    CollectionOperation(bone_name="Skirt_Front.L.001", collection_name="Skirt"),
                ]
            ),
            ExtensionBone(
                name="Skirt_Front.L.002",
                bone_a="j_sk_f_c_l",
                parent="Skirt_Front.L.001",
                is_connected=True,
                axis_type="local",
                axis="Y",
                start="head",
                req_bones=["j_sk_f_c_l"],
                operations=[
                    CollectionOperation(bone_name="Skirt_Front.L.002", collection_name="Skirt"),
                ]
            ),
            #Side
            ConnectBone(
                name="Skirt_Side.L",
                bone_a="j_sk_s_a_l",
                bone_b="j_sk_s_b_l",
                parent="Spine.001",
                is_connected=False,
                req_bones=["j_sk_s_a_l", "j_sk_s_b_l"],
                operations=[
                    RigifyTypeOperation(bone_name="Skirt_Side.L", rigify_type=rigify.types.basic_copy_chain()),
                    CollectionOperation(bone_name="Skirt_Side.L", collection_name="Skirt"),
                    ParentBoneOperation(bone_name="Skirt_Side.L", parent=["MCH-Skirt_Middle.L"], time="Post")
                ]
            ),
            ConnectBone(
                name="Skirt_Side.L.001",
                bone_a="j_sk_s_b_l",
                bone_b="j_sk_s_c_l",
                parent="Skirt_Side.L",
                is_connected=True,
                req_bones=["j_sk_s_b_l", "j_sk_s_c_l"],
                operations=[
                    CollectionOperation(bone_name="Skirt_Side.L.001", collection_name="Skirt"),
                ]
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
                operations=[
                    CollectionOperation(bone_name="Skirt_Side.L.002", collection_name="Skirt"),
                ]
            ),
            #Back
            ConnectBone(
                name="Skirt_Back.L",
                bone_a="j_sk_b_a_l",
                bone_b="j_sk_b_b_l",
                parent="Spine.001",
                is_connected=False,
                req_bones=["j_sk_b_a_l", "j_sk_b_b_l"],
                operations=[
                    RigifyTypeOperation(bone_name="Skirt_Back.L", rigify_type=rigify.types.basic_copy_chain()),
                    CollectionOperation(bone_name="Skirt_Back.L", collection_name="Skirt"),
                    ParentBoneOperation(bone_name="Skirt_Back.L", parent=["MCH-Skirt_Back.L"], time="Post")
                ]
            ),
            ConnectBone(
                name="Skirt_Back.L.001",
                bone_a="j_sk_b_b_l",
                bone_b="j_sk_b_c_l",
                parent="Skirt_Back.L",
                is_connected=True,
                req_bones=["j_sk_b_b_l", "j_sk_b_c_l"],
                operations=[
                    CollectionOperation(bone_name="Skirt_Back.L.001", collection_name="Skirt"),
                ]
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
                operations=[
                    CollectionOperation(bone_name="Skirt_Back.L.002", collection_name="Skirt"),
                ]
            ),
            #DriverTGT
            ExtensionBone(
                name="MCH-thigh_driv_tgt.L",
                bone_a="thigh.L",
                parent="Spine.001",
                start="head",
                size_factor=0.3,
                req_bones=["thigh.L"],
                operations=[
                    RigifyTypeOperation(bone_name="MCH-thigh_driv_tgt.L", rigify_type=rigify.types.basic_raw_copy()),
                    CollectionOperation(bone_name="MCH-thigh_driv_tgt.L", collection_name="MCH", time="Post"),
                    ConstraintOperation(bone_name="MCH-thigh_driv_tgt.L", constraint=DampedTrackConstraint(target_bone="ORG-shin.L"), time="Post")
                ]
            ),
            ExtensionBone(
                name="MCH-shin_driv_tgt.L",
                bone_a="shin.L",
                parent="thigh.L",
                start="head",
                size_factor=0.3,
                req_bones=["shin.L"],
                operations=[
                    RigifyTypeOperation(bone_name="MCH-shin_driv_tgt.L", rigify_type=rigify.types.basic_raw_copy()),
                    CollectionOperation(bone_name="MCH-shin_driv_tgt.L", collection_name="MCH", time="Post"),
                    ConstraintOperation(bone_name="MCH-shin_driv_tgt.L", constraint=DampedTrackConstraint(target_bone="ORG-foot.L"), time="Post")
                ]
            ),
            # Driver Bones
            ConnectBone(
                name="MCH-Skirt_Front.L",
                bone_a="j_sk_f_a_l",
                bone_b="j_sk_f_b_l",
                parent="Spine.001",
                is_connected=False,
                req_bones=["j_sk_f_a_l", "j_sk_f_b_l"],
                operations=[
                    RigifyTypeOperation(bone_name="MCH-Skirt_Front.L", rigify_type=rigify.types.basic_raw_copy()),
                    CollectionOperation(bone_name="MCH-Skirt_Front.L", collection_name="MCH", time="Post"),
                    DriverOperation(
                        bone_name="MCH-Skirt_Front.L",
                        driver_name="Sk_f_a_l",
                        property=["rotation_quaternion", 1],
                        driver=Driver(
                            type="SCRIPTED",
                            expression="((RotX < 0) * (RotX * sk_auto) / (1 + (abs(RotX) - 0.8) * 0.1))",
                            variables=[
                                TransformChannelVariable(name="RotX", target_bone="MCH-thigh_driv_tgt.L", transform_type="ROT_X", rotation_mode="QUATERNION", transform_space="LOCAL_SPACE"),
                                SinglePropertyVariable(name= "sk_auto", data_path="skirt_automation")
                            ],
                        ),
                        time="Post"
                    ),
                    DriverOperation(
                        bone_name="MCH-Skirt_Front.L",
                        driver_name="Sk_f_a_l.001",
                        property=["rotation_quaternion", 3],
                        driver=Driver(
                            type="SCRIPTED",
                            expression="((RotZ < 0) * (RotZ * sk_auto) / (2 + (abs(RotZ) - 0.5) * 0.5))",
                            variables=[
                                TransformChannelVariable(name="RotZ", target_bone="MCH-thigh_driv_tgt.L", transform_type="ROT_Z", rotation_mode="QUATERNION", transform_space="LOCAL_SPACE"),
                                SinglePropertyVariable(name= "sk_auto", data_path="skirt_automation")
                            ],
                        ),
                        time="Post",
                    )
                ]
            ),
            ConnectBone(
                name="MCH-Skirt_Front.L.001",
                bone_a="j_sk_f_b_l",
                bone_b="j_sk_f_c_l",
                parent="MCH-Skirt_Front.L",
                is_connected=True,
                req_bones=["j_sk_f_b_l", "j_sk_f_c_l"],
                operations=[
                    RigifyTypeOperation(bone_name="MCH-Skirt_Front.L.001", rigify_type=rigify.types.basic_raw_copy()),
                    CollectionOperation(bone_name="MCH-Skirt_Front.L.001", collection_name="MCH", time="Post"),
                    DriverOperation(
                        bone_name="MCH-Skirt_Front.L.001",
                        driver_name="Sk_f_b_l",
                        property=["rotation_quaternion", 1],
                        driver=Driver(
                            type="SCRIPTED",
                            expression="((RotX > 0) * (RotX * sk_auto) / (2 + (abs(RotX) - 0.5) * 2)) * (abs(RotXThreshold) / (0.2 + abs(RotXThreshold))) if RotXThreshold < 0 else RotX * 0",
                            variables=[
                                TransformChannelVariable(name="RotX", target_bone="MCH-shin_driv_tgt.L", transform_type="ROT_X", rotation_mode="QUATERNION", transform_space="LOCAL_SPACE"),
                                TransformChannelVariable(name="RotXThreshold", target_bone="MCH-thigh_driv_tgt.L", transform_type="ROT_X", rotation_mode="QUATERNION", transform_space="LOCAL_SPACE"),
                                SinglePropertyVariable(name= "sk_auto", data_path="skirt_automation")
                            ],
                        ),
                        time="Post"
                    ),
                ]
            ),
            ExtensionBone(
                name="MCH-Skirt_Front.L.002",
                bone_a="j_sk_f_c_l",
                parent="MCH-Skirt_Front.L.001",
                is_connected=True,
                axis_type="local",
                axis="Y",
                start="head",
                req_bones=["j_sk_f_c_l"],
                operations=[
                    RigifyTypeOperation(bone_name="MCH-Skirt_Front.L.002", rigify_type=rigify.types.basic_raw_copy()),
                    CollectionOperation(bone_name="MCH-Skirt_Front.L.002", collection_name="MCH", time="Post")
                ]
            ),
            ConnectBone(
                name="MCH-Skirt_Middle.L",
                bone_a="j_sk_s_a_l",
                bone_b="j_sk_s_b_l",
                parent="Spine.001",
                is_connected=False,
                roll=-7,
                req_bones=["j_sk_s_a_l", "j_sk_s_b_l"],
                operations=[
                    RigifyTypeOperation(bone_name="MCH-Skirt_Middle.L", rigify_type=rigify.types.basic_raw_copy()),
                    CollectionOperation(bone_name="MCH-Skirt_Middle.L", collection_name="MCH", time="Post"),
                    DriverOperation(
                        bone_name="MCH-Skirt_Middle.L",
                        driver_name="Sk_s_a_l",
                        property=["rotation_quaternion", 1],
                        driver=Driver(
                            type="SCRIPTED",
                            expression="((RotX < 0) * (RotX * sk_auto) / (3 + (abs(RotX) - 0.5) * 2))",
                            variables=[
                                TransformChannelVariable(name="RotX", target_bone="MCH-thigh_driv_tgt.L", transform_type="ROT_X", rotation_mode="QUATERNION", transform_space="LOCAL_SPACE"),
                                SinglePropertyVariable(name= "sk_auto", data_path="skirt_automation")
                            ],
                        ),
                        time="Post"
                    ),
                    DriverOperation(
                        bone_name="MCH-Skirt_Middle.L",
                        driver_name="Sk_s_a_l.001",
                        property=["rotation_quaternion", 3],
                        driver=Driver(
                            type="SCRIPTED",
                            expression="((RotZ < 0) * (RotZ * sk_auto) / (1 + (abs(RotZ) - 0.1) * 1))",
                            variables=[
                                TransformChannelVariable(name="RotZ", target_bone="MCH-thigh_driv_tgt.L", transform_type="ROT_Z", rotation_mode="QUATERNION", transform_space="LOCAL_SPACE"),
                                SinglePropertyVariable(name= "sk_auto", data_path="skirt_automation")
                            ],
                        ),
                        time="Post",
                    )
                ]
            ),
            ConnectBone(
                name="MCH-Skirt_Middle.L.001",
                bone_a="j_sk_s_b_l",
                bone_b="j_sk_s_c_l",
                parent="MCH-Skirt_Middle.L",
                is_connected=True,
                roll=-7,
                req_bones=["j_sk_s_b_l", "j_sk_s_c_l"],
                operations=[
                    RigifyTypeOperation(bone_name="MCH-Skirt_Middle.L.001", rigify_type=rigify.types.basic_raw_copy()),
                    CollectionOperation(bone_name="MCH-Skirt_Middle.L.001", collection_name="MCH", time="Post"),
                    DriverOperation(
                        bone_name="MCH-Skirt_Middle.L.001",
                        driver_name="Sk_s_b_l",
                        property=["rotation_quaternion", 1],
                        driver=Driver(
                            type="SCRIPTED",
                            expression="((RotX > 0) * (RotX * sk_auto) / (3 + (abs(RotX) - 0.2) * 2)) * (abs(RotXThreshold) / (0.2 + abs(RotXThreshold))) if RotXThreshold < 0 else RotX * 0",
                            variables=[
                                TransformChannelVariable(name="RotX", target_bone="MCH-shin_driv_tgt.L", transform_type="ROT_X", rotation_mode="QUATERNION", transform_space="LOCAL_SPACE"),
                                TransformChannelVariable(name="RotXThreshold", target_bone="MCH-thigh_driv_tgt.L", transform_type="ROT_X", rotation_mode="QUATERNION", transform_space="LOCAL_SPACE"),
                                SinglePropertyVariable(name= "sk_auto", data_path="skirt_automation")
                            ],
                        ),
                        time="Post"
                    ),
                ]
            ),
            ExtensionBone(
                name="MCH-Skirt_Middle.L.002",
                bone_a="j_sk_s_c_l",
                parent="MCH-Skirt_Middle.L.001",
                is_connected=True,
                axis_type="local",
                axis="Y",
                start="head",
                roll=-7,
                req_bones=["j_sk_s_c_l"],
                operations=[
                    RigifyTypeOperation(bone_name="MCH-Skirt_Middle.L.002", rigify_type=rigify.types.basic_raw_copy()),
                    CollectionOperation(bone_name="MCH-Skirt_Middle.L.002", collection_name="MCH", time="Post")
                ]
            ),
            ConnectBone(
                name="MCH-Skirt_Back.L",
                bone_a="j_sk_b_a_l",
                bone_b="j_sk_b_b_l",
                parent="Spine.001",
                is_connected=False,
                req_bones=["j_sk_b_a_l", "j_sk_b_b_l"],
                operations=[
                    RigifyTypeOperation(bone_name="MCH-Skirt_Back.L", rigify_type=rigify.types.basic_raw_copy()),
                    CollectionOperation(bone_name="MCH-Skirt_Back.L", collection_name="MCH", time="Post"),
                    DriverOperation(
                        bone_name="MCH-Skirt_Back.L",
                        driver_name="Sk_b_a_l",
                        property=["rotation_quaternion", 1],
                        driver=Driver(
                            type="SCRIPTED",
                            expression="((RotX < 0) * (RotX * sk_auto) / (5 + (abs(RotX) - 0.2) * 5)) + ((RotX > 0) * ((RotX * sk_auto) / (1 + (abs(RotX) + 0.1) * 0.2)))",
                            variables=[
                                TransformChannelVariable(name="RotX", target_bone="MCH-thigh_driv_tgt.L", transform_type="ROT_X", rotation_mode="QUATERNION", transform_space="LOCAL_SPACE"),
                                SinglePropertyVariable(name= "sk_auto", data_path="skirt_automation")
                            ],
                        ),
                        time="Post"
                    ),
                    DriverOperation(
                        bone_name="MCH-Skirt_Back.L",
                        driver_name="Sk_b_a_l.001",
                        property=["rotation_quaternion", 3],
                        driver=Driver(
                            type="SCRIPTED",
                            expression="((RotZ < 0) * (RotZ * sk_auto) / (2 + (abs(RotZ) - 0.1) * 3))",
                            variables=[
                                TransformChannelVariable(name="RotZ", target_bone="MCH-thigh_driv_tgt.L", transform_type="ROT_Z", rotation_mode="QUATERNION", transform_space="LOCAL_SPACE"),
                                SinglePropertyVariable(name= "sk_auto", data_path="skirt_automation")
                            ],
                        ),
                        time="Post",
                    )
                ]
            ),
            ConnectBone(
                name="MCH-Skirt_Back.L.001",
                bone_a="j_sk_b_b_l",
                bone_b="j_sk_b_c_l",
                parent="MCH-Skirt_Back.L",
                is_connected=True,
                req_bones=["j_sk_b_b_l", "j_sk_b_c_l"],
                operations=[
                    RigifyTypeOperation(bone_name="MCH-Skirt_Back.L.001", rigify_type=rigify.types.basic_raw_copy()),
                    CollectionOperation(bone_name="MCH-Skirt_Back.L.001", collection_name="MCH", time="Post"),
                    DriverOperation(
                        bone_name="MCH-Skirt_Back.L.001",
                        driver_name="Sk_b_b_l",
                        property=["rotation_quaternion", 1],
                        driver=Driver(
                            type="SCRIPTED",
                            expression="((RotX > 0) * (RotX * sk_auto) / (1 + (abs(RotX) + 0.5) * 0.3)) * (abs(RotXThreshold) / (0.5 + abs(RotXThreshold))) if RotXThreshold > 0 else RotX * 0",
                            variables=[
                                TransformChannelVariable(name="RotX", target_bone="MCH-shin_driv_tgt.L", transform_type="ROT_X", rotation_mode="QUATERNION", transform_space="LOCAL_SPACE"),
                                TransformChannelVariable(name="RotXThreshold", target_bone="MCH-thigh_driv_tgt.L", transform_type="ROT_X", rotation_mode="QUATERNION", transform_space="LOCAL_SPACE"),
                                SinglePropertyVariable(name= "sk_auto", data_path="skirt_automation")
                            ],
                        ),
                        time="Post"
                    ),
                ]
            ),
            ExtensionBone(
                name="MCH-Skirt_Back.L.002",
                bone_a="j_sk_b_c_l",
                parent="MCH-Skirt_Back.L.001",
                is_connected=True,
                axis_type="local",
                axis="Y",
                start="head",
                req_bones=["j_sk_b_c_l"],
                operations=[
                    RigifyTypeOperation(bone_name="MCH-Skirt_Back.L.002", rigify_type=rigify.types.basic_raw_copy()),
                    CollectionOperation(bone_name="MCH-Skirt_Back.L.002", collection_name="MCH", time="Post")
                ]
            ),
        ]
)

def get_rig_module() -> RigModule:
    return RigModule(
        name="XIV-Default",
        type="Generation",
        bone_groups=[SKIRT_R, SKIRT_L],
        ui_collections = UI_Collections([
            BoneCollection(name="Skirt", ui=True, color_set="Head", row_index=1, title="Skirt", visible=False),
        ],
        ),
        ui_flags = ["Skirt Automation"],
    )
