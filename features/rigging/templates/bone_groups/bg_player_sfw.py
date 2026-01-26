import bpy
import mathutils

from .....core.generators import ConnectBone, ExtensionBone, SkinBone, BridgeBone, CenterBone, CopyBone, RegexBoneGroup
from .....core.shared import PoseOperations, BoneGroup, TransformLink
from .....core import rigify


# Individual bone list (for backwards compatibility and direct access)
ARM_R = BoneGroup(
        name="Right Arm",
        description="Right arm bones including upper arm, forearm, hand, and tweak bones",
        transform_link = [
            TransformLink(target="DEF-upper_arm.R", bone="j_ude_a_r", retarget="FK-upper_arm.R"),
            TransformLink(target="DEF-forearm.R", bone="j_ude_b_r", retarget="FK-forearm.R"),
            TransformLink(target="DEF-hand.R", bone="j_te_r", retarget="FK-hand.R"),
            TransformLink(target="DEF-forearm.R.001", bone="n_hte_r")
            ],
        bones = [
            #Right Clavicle
            ConnectBone(
                name="clavicle.R",
                bone_a="j_sako_r",
                bone_b="j_ude_a_r",
                parent="Spine.004",
                is_connected=False,
                req_bones=["j_sako_r"],
                pose_operations=PoseOperations(
                    rigify_settings=rigify.types.basic_super_copy(widget_type="shoulder"),
                    b_collection="Torso"
                )
            ),
            # Right Arm
            ConnectBone(
                name="upper_arm.R", 
                bone_a="j_ude_a_r", 
                bone_b="j_ude_b_r", 
                parent="clavicle.R",
                req_bones=["j_ude_a_r", "j_ude_b_r"],
                pose_operations=PoseOperations(
                    rigify_settings=rigify.types.limbs_arm(fk_coll="Arm.R (FK)", tweak_coll="Arm.R (Tweak)"), 
                    b_collection="Arm.R (IK)" 
                )
            ),
            ConnectBone(
                name="forearm.R", 
                bone_a="j_ude_b_r", 
                bone_b="j_te_r", 
                parent="upper_arm.R", 
                is_connected=True,
                req_bones=["j_ude_b_r", "j_te_r"],
                pose_operations=PoseOperations(
                    b_collection="Arm.R (IK)"
                )
            ),
            ExtensionBone(
                name="hand.R", 
                bone_a="j_te_r", 
                size_factor=0.6, 
                axis_type="local", 
                axis="Y", 
                is_connected=True, 
                parent="forearm.R",
                req_bones=["forearm.R"],
                pose_operations=PoseOperations(
                    b_collection="Arm.R (IK)"
                )
            ),
        ]
    )

ARM_L = BoneGroup(
        name="Left Arm",
        transform_link= [
            TransformLink(target="DEF-upper_arm.L", bone="j_ude_a_l", retarget="FK-upper_arm.L"),
            TransformLink(target="DEF-forearm.L", bone="j_ude_b_l", retarget="FK-forearm.L"),
            TransformLink(target="DEF-hand.L", bone="j_te_l", retarget="FK-hand.L"),
            TransformLink(target="DEF-forearm.L.001", bone="n_hte_l")
            ],
        bones = [
            #Left Clavicle
            ConnectBone(
                name="clavicle.L",
                bone_a="j_sako_l",
                bone_b="j_ude_a_l",
                parent="Spine.004",
                is_connected=False,
                req_bones=["j_sako_l"],
                pose_operations=PoseOperations(
                    rigify_settings=rigify.types.basic_super_copy(widget_type="shoulder"),
                    b_collection="Torso"
                )
            ),
            # Left Arm
            ConnectBone(
                name="upper_arm.L", 
                bone_a="j_ude_a_l", 
                bone_b="j_ude_b_l", 
                parent="clavicle.L",
                req_bones=["j_ude_a_l", "j_ude_b_l"],
                pose_operations=PoseOperations(
                    rigify_settings=rigify.types.limbs_arm(fk_coll="Arm.L (FK)", tweak_coll="Arm.L (Tweak)"),
                    b_collection="Arm.L (IK)"
                )
            ),
            ConnectBone(
                name="forearm.L", 
                bone_a="j_ude_b_l", 
                bone_b="j_te_l", 
                parent="upper_arm.L", 
                is_connected=True,
                req_bones=["j_ude_b_l", "j_te_l"],
                pose_operations=PoseOperations(
                    b_collection="Arm.L (IK)"
                )
            ),
            ExtensionBone(
                name="hand.L", 
                bone_a="j_te_l", 
                size_factor=0.6, 
                axis_type="local", 
                axis="Y", 
                is_connected=True, 
                parent="forearm.L",
                req_bones=["forearm.L"],
                pose_operations=PoseOperations(
                    b_collection="Arm.L (IK)"
                )
            ),
        ],
        description ="Left arm bones including the clavicle, upper arm, forearm, and hand bones."
    )

SPINE = BoneGroup(
        name="Spine",
        transform_link= [
            TransformLink(target="DEF-Spine.001", bone="j_kosi", retarget="FK-Spine.001"),
            TransformLink(target="DEF-Spine.002", bone="j_sebo_a", retarget="FK-Spine.002"),
            TransformLink(target="DEF-Spine.003", bone="j_sebo_b", retarget="FK-Spine.003"),
            TransformLink(target="DEF-Spine.004", bone="j_sebo_c", retarget="FK-Spine.004"),
            TransformLink(target="DEF-Chest.R", bone="j_mune_r"),
            TransformLink(target="DEF-Chest.L", bone="j_mune_l"),
        ],
        bones = [
            #Spine
            ConnectBone(
                name="Spine.001",
                bone_a="j_kosi",
                bone_b="j_kosi",
                parent="Torso",
                start="tail",
                end="head",
                is_connected=True,
                req_bones=["j_kosi"],
                pose_operations=PoseOperations(
                    rigify_settings=rigify.types.spines_basic_spine(fk_coll="Torso (Tweak)", tweak_coll="Torso (Tweak)", pivot_pos=1),
                    b_collection="Torso"
                )
            ),
            ConnectBone(
                name="Spine.002",
                bone_a="j_sebo_a",
                bone_b="j_sebo_b",
                parent="Spine.001",
                is_connected=True,
                req_bones=["j_sebo_a", "j_sebo_b"],
                pose_operations=PoseOperations(
                    b_collection="Torso"
                )
            ),
            ConnectBone(
                name="Spine.003",
                bone_a="j_sebo_b",
                bone_b="j_sebo_c",
                parent="Spine.002",
                is_connected=True,
                req_bones=["j_sebo_b", "j_sebo_c"],
                pose_operations=PoseOperations(
                    b_collection="Torso"
                )
            ),
            ConnectBone(
                name="Spine.004",
                bone_a="j_sebo_c",
                bone_b="j_kubi",
                parent="Spine.003",
                is_connected=True,
                req_bones=["j_sebo_c", "j_kubi"],
                pose_operations=PoseOperations(
                    b_collection="Torso"
                )
            ),
            #Chest
            ExtensionBone(
                name="Chest.R",
                bone_a="j_mune_r",
                parent="Spine.003",
                is_connected=False,
                start="head",
                axis_type="local",
                axis="Y",
                roll=-48,
                req_bones=["j_mune_r"],
                pose_operations=PoseOperations(
                    rigify_settings=rigify.types.basic_super_copy(widget_type="bone"),
                    b_collection="Torso",
                )
            ),
            ExtensionBone(
                name="Chest.L",
                bone_a="j_mune_l",
                parent="Spine.003",
                is_connected=False,
                start="head",
                axis_type="local",
                axis="Y",
                roll=-132,
                req_bones=["j_mune_l"],
                pose_operations=PoseOperations(
                    rigify_settings=rigify.types.basic_super_copy(widget_type="bone"),
                    b_collection="Torso",
                )
            ),
        ],
)

LEG_R = BoneGroup(
        name="Right Leg",
        transform_link= [
            TransformLink(target="DEF-thigh.R.001", bone="j_asi_a_r", retarget="FK-upper_leg.R"),
            TransformLink(target="DEF-shin.R.001", bone="j_asi_c_r", retarget="FK-lower_leg.R"),
            TransformLink(target="DEF-foot.R", bone="j_asi_d_r", retarget="FK-foot.R"),
            TransformLink(target="DEF-toe.R", bone="j_asi_e_r", retarget="FK-toe.R"),
            ],
        bones = [
            # Right Leg
            ConnectBone(
                name="thigh.R", 
                bone_a="j_asi_a_r",
                bone_b="j_asi_c_r",
                parent="Spine.001",
                req_bones=["j_asi_a_r", "j_asi_c_r"],
                pose_operations=PoseOperations(
                    rigify_settings=rigify.types.limbs_leg(fk_coll="Leg.R (FK)", tweak_coll="Leg.R (Tweak)"),
                    b_collection="Leg.R (IK)"
                )
            ),
            ConnectBone(
                name="shin.R", 
                bone_a="j_asi_c_r", 
                bone_b="j_asi_d_r", 
                parent="thigh.R", 
                is_connected=True,
                req_bones=["j_asi_c_r", "j_asi_d_r"],
                pose_operations=PoseOperations(
                    b_collection="Leg.R (IK)"
                )
            ),
            ConnectBone(
                name="foot.R", 
                bone_a="j_asi_d_r", 
                bone_b="j_asi_e_r", 
                parent="shin.R",
                is_connected=True,
                req_bones=["j_asi_d_r", "j_asi_e_r"],
                pose_operations=PoseOperations(
                    b_collection="Leg.R (IK)"
                )
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
                pose_operations=PoseOperations(
                    b_collection="Leg.R (IK)"
                )
            ),
            ExtensionBone(
                name="heel_pivot.R.helper",
                bone_a="j_asi_e_r",
                parent="shin.R",
                is_connected=False,
                axis_type="local",
                axis="Y",
                start="head",
                size_factor=-4.0,
                req_bones=["j_asi_e_r"],
                pose_operations=PoseOperations(
                    b_collection="Leg.R (IK)"
                )
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
                pose_operations=PoseOperations(
                    b_collection="Leg.R (IK)"
                )
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
        bones = [
            # Left Leg
            ConnectBone(
                name="thigh.L", 
                bone_a="j_asi_a_l",
                bone_b="j_asi_c_l",
                parent="Spine.001",
                req_bones=["j_asi_a_l", "j_asi_c_l"],
                pose_operations=PoseOperations(
                    rigify_settings=rigify.types.limbs_leg( fk_coll="Leg.L (FK)", tweak_coll="Leg.L (Tweak)"),
                    b_collection="Leg.L (IK)"
                )
            ),
            ConnectBone(
                name="shin.L", 
                bone_a="j_asi_c_l", 
                bone_b="j_asi_d_l", 
                parent="thigh.L", 
                is_connected=True,
                req_bones=["j_asi_c_l", "j_asi_d_l"],
                pose_operations=PoseOperations(
                    b_collection="Leg.L (IK)"
                )
            ),
            ConnectBone(
                name="foot.L", 
                bone_a="j_asi_d_l", 
                bone_b="j_asi_e_l", 
                parent="shin.L",
                is_connected=True,
                req_bones=["j_asi_d_l", "j_asi_e_l"],
                pose_operations=PoseOperations(
                    b_collection="Leg.L (IK)"
                )
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
                pose_operations=PoseOperations(
                    b_collection="Leg.L (IK)"
                )
            ),
            ExtensionBone(
                name="heel_pivot.L.helper",
                bone_a="j_asi_e_l",
                parent="shin.L",
                is_connected=False,
                axis_type="local",
                axis="Y",
                start="head",
                size_factor=-4.0,
                req_bones=["j_asi_e_l"],
                pose_operations=PoseOperations(
                    b_collection="Leg.L (IK)"
                )
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
                pose_operations=PoseOperations(
                    b_collection="Leg.L (IK)"
                )
            )
        ],
)

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
        bones = [
            #Front
            ConnectBone(
                name="Skirt_Front.R",
                bone_a="j_sk_f_a_r",
                bone_b="j_sk_f_b_r",
                parent="Spine.001",
                is_connected=False,
                req_bones=["j_sk_f_a_r", "j_sk_f_b_r"],
                pose_operations=PoseOperations(
                    rigify_settings=rigify.types.skin_stretchy_chain(skin_chain_pivot_pos=0, primary_layer_extra="Skirt", skin_chain_falloff_length=True, skin_chain_falloff_spherical=[True, False, True]),
                    b_collection="Skirt (Tweak)"
                )
            ),
            ConnectBone(
                name="Skirt_Front.R.001",
                bone_a="j_sk_f_b_r",
                bone_b="j_sk_f_c_r",
                parent="Skirt_Front.R",
                is_connected=True,
                req_bones=["j_sk_f_b_r", "j_sk_f_c_r"],
                pose_operations=PoseOperations(
                    b_collection="Skirt"
                )
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
                pose_operations=PoseOperations(
                    b_collection="Skirt"
                )
            ),
            #Side
            ConnectBone(
                name="Skirt_Side.R",
                bone_a="j_sk_s_a_r",
                bone_b="j_sk_s_b_r",
                parent="Spine.001",
                is_connected=False,
                req_bones=["j_sk_s_a_r", "j_sk_s_b_r"],
                pose_operations=PoseOperations(
                    rigify_settings=rigify.types.skin_stretchy_chain(skin_chain_pivot_pos=0, primary_layer_extra="Skirt", skin_chain_falloff_length=True, skin_chain_falloff_spherical=[True, False, True]),
                    b_collection="Skirt (Tweak)"
                )
            ),
            ConnectBone(
                name="Skirt_Side.R.001",
                bone_a="j_sk_s_b_r",
                bone_b="j_sk_s_c_r",
                parent="Skirt_Side.R",
                is_connected=True,
                req_bones=["j_sk_s_b_r", "j_sk_s_c_r"],
                pose_operations=PoseOperations(
                    b_collection="Skirt"
                )
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
                pose_operations=PoseOperations(
                    b_collection="Skirt"
                )
            ),
            #Back
            ConnectBone(
                name="Skirt_Back.R",
                bone_a="j_sk_b_a_r",
                bone_b="j_sk_b_b_r",
                parent="Spine.001",
                is_connected=False,
                req_bones=["j_sk_b_a_r", "j_sk_b_b_r"],
                pose_operations=PoseOperations(
                    rigify_settings=rigify.types.skin_stretchy_chain(skin_chain_pivot_pos=0, primary_layer_extra="Skirt", skin_chain_falloff_length=True, skin_chain_falloff_spherical=[True, False, True]),
                    b_collection="Skirt (Tweak)"
                )
            ),
            ConnectBone(
                name="Skirt_Back.R.001",
                bone_a="j_sk_b_b_r",
                bone_b="j_sk_b_c_r",
                parent="Skirt_Back.R",
                is_connected=True,
                req_bones=["j_sk_b_b_r", "j_sk_b_c_r"],
                pose_operations=PoseOperations(
                    b_collection="Skirt"
                )
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
                pose_operations=PoseOperations(
                    b_collection="Skirt"
                )
            ),
             #Front
            ConnectBone(
                name="Skirt_Front.R.mch",
                bone_a="shin.R",
                bone_b="Skirt_Front.R.002",
                parent="shin.R",
                is_connected=False,
                end="tail",
                req_bones=["Skirt_Front.R.002"],
                pose_operations=PoseOperations(
                    rigify_settings=rigify.types.skin_basic_chain(skin_chain_priority=1, skin_control_orientation_bone="Skirt_Front.R.002"),
                    b_collection="Skirt MCH"
                )
            ),
            ConnectBone(
                name="Skirt_Side.R.mch",
                bone_a="shin.R",
                bone_b="Skirt_Side.R.002",
                parent="shin.R",
                is_connected=False,
                end="tail",
                req_bones=["Skirt_Side.R.002"],
                pose_operations=PoseOperations(
                    rigify_settings=rigify.types.skin_basic_chain(skin_chain_priority=1, skin_control_orientation_bone="Skirt_Side.R.002"),
                    b_collection="Skirt MCH"
                )
            ),
            ConnectBone(
                name="Skirt_Back.R.mch",
                bone_a="shin.R",
                bone_b="Skirt_Back.R.002",
                parent="shin.R",
                is_connected=False,
                end="tail",
                req_bones=["Skirt_Back.R.002"],
                pose_operations=PoseOperations(
                    rigify_settings=rigify.types.skin_basic_chain(skin_chain_priority=1, skin_control_orientation_bone="Skirt_Back.R.002"),
                    b_collection="Skirt MCH"
                )
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
        bones = [
            #Front
            ConnectBone(
                name="Skirt_Front.L",
                bone_a="j_sk_f_a_l",
                bone_b="j_sk_f_b_l",
                parent="Spine.001",
                is_connected=False,
                req_bones=["j_sk_f_a_l", "j_sk_f_b_l"],
                pose_operations=PoseOperations(
                    rigify_settings=rigify.types.skin_stretchy_chain(skin_chain_pivot_pos=0, primary_layer_extra="Skirt", skin_chain_falloff_length=True, skin_chain_falloff_spherical=[True, False, True]),
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
                    rigify_settings=rigify.types.skin_stretchy_chain(skin_chain_pivot_pos=0, primary_layer_extra="Skirt", skin_chain_falloff_length=True, skin_chain_falloff_spherical=[True, False, True]),
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
                    rigify_settings=rigify.types.skin_stretchy_chain(skin_chain_pivot_pos=0, primary_layer_extra="Skirt", skin_chain_falloff_length=True, skin_chain_falloff_spherical=[True, False, True]),
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
            #Front
            ConnectBone(
                name="Skirt_Front.L.mch",
                bone_a="shin.L",
                bone_b="Skirt_Front.L.002",
                parent="shin.L",
                is_connected=False,
                end="tail",
                req_bones=["Skirt_Front.L.002"],
                pose_operations=PoseOperations(
                    rigify_settings=rigify.types.skin_basic_chain(skin_chain_priority=1, skin_control_orientation_bone="Skirt_Front.L.002"),
                    b_collection="Skirt MCH"
                )
            ),
            #Side
            ConnectBone(
                name="Skirt_Side.L.mch",
                bone_a="shin.L",
                bone_b="Skirt_Side.L.002",
                parent="shin.L",
                is_connected=False,
                end="tail",
                req_bones=["Skirt_Side.L.002"],
                pose_operations=PoseOperations(
                    rigify_settings=rigify.types.skin_basic_chain(skin_chain_priority=1, skin_control_orientation_bone="Skirt_Side.L.002"),
                    b_collection="Skirt MCH"
                )
            ),
            #Back
            ConnectBone(
                name="Skirt_Back.L.mch",
                bone_a="shin.L",
                bone_b="Skirt_Back.L.002",
                parent="shin.L",
                is_connected=False,
                end="tail",
                req_bones=["Skirt_Back.L.002"],
                pose_operations=PoseOperations(
                    rigify_settings=rigify.types.skin_basic_chain(skin_chain_priority=1, skin_control_orientation_bone="Skirt_Back.L.002"),
                    b_collection="Skirt MCH"
                )
            ),
        ],
)

IV_HAND_R = BoneGroup(
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
    bones=[
        #Palm Control - Very cool stuff, thank you rigify - Oats
        ExtensionBone(
            name="palm.01.R",
            bone_a="j_hito_a_r",
            parent="hand.R",
            is_connected=False,
            axis_type="local",
            axis="Y",
            start="head",
            roll=135,
            req_bones=["j_hito_a_r"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.limbs_super_palm(palm_both_sides=True),
                b_collection="Fingers.R"
            )
        ),
        ExtensionBone(
            name="palm.02.R",
            bone_a="j_naka_a_r",
            parent="hand.R",
            is_connected=False,
            axis_type="local",
            axis="Y",
            start="head",
            roll=135,
            req_bones=["j_naka_a_r"],
            pose_operations=PoseOperations(
                b_collection="Fingers.R"
            )
        ),
        ExtensionBone(
            name="palm.03.R",
            bone_a="j_kusu_a_r",
            parent="hand.R",
            is_connected=False,
            axis_type="local",
            axis="Y",
            start="head",
            roll=135,
            req_bones=["j_kusu_a_r"],
            pose_operations=PoseOperations(
                b_collection="Fingers.R"
            )
        ),
        ExtensionBone(
            name="palm.04.R",
            bone_a="j_ko_a_r",
            parent="hand.R",
            is_connected=False,
            axis_type="local",
            axis="Y",
            start="head",
            roll=135,
            req_bones=["j_ko_a_r"],
            pose_operations=PoseOperations(
                b_collection="Fingers.R"
            )
        ),
        #Thumb
        ConnectBone(
            name="thumb.R",
            bone_a="j_oya_a_r",
            bone_b="j_oya_b_r",
            parent="hand.R",
            roll=15,
            is_connected=False,
            req_bones=["j_oya_a_r", "j_oya_b_r"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.limbs_super_finger(),
                b_collection="Fingers.R",
            )
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
            pose_operations=PoseOperations(
                b_collection="Fingers.R",
            )
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
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.limbs_super_finger(),
                b_collection="Fingers.R",
            )
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
            pose_operations=PoseOperations(
                b_collection="Fingers.R",
            )
        ),
        ExtensionBone(
            name="index.R.002",
            bone_a="iv_hito_c_r",
            parent="index.R.001",
            is_connected=True,
            axis_type="local",
            axis="Y",
            start="head",
            req_bones=["iv_hito_c_r"],
            pose_operations=PoseOperations(
                b_collection="Fingers.R",
            )
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
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.limbs_super_finger(),
                b_collection="Fingers.R",
            )
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
            pose_operations=PoseOperations(
                b_collection="Fingers.R",
            )
        ),
        ExtensionBone(
            name="middle.R.002",
            bone_a="iv_naka_c_r",
            parent="middle.R.001",
            is_connected=True,
            axis_type="local",
            axis="Y",
            start="head",
            req_bones=["iv_naka_c_r"],
            pose_operations=PoseOperations(
                b_collection="Fingers.R",
            )
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
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.limbs_super_finger(),
                b_collection="Fingers.R",
            )
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
            pose_operations=PoseOperations(
                b_collection="Fingers.R",
            )
        ),
        ExtensionBone(
            name="ring.R.002",
            bone_a="iv_kusu_c_r",
            parent="ring.R.001",
            is_connected=True,
            axis_type="local",
            axis="Y",
            start="head",
            req_bones=["iv_kusu_c_r"],
            pose_operations=PoseOperations(
                b_collection="Fingers.R",
            )
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
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.limbs_super_finger(),
                b_collection="Fingers.R",
            )
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
            pose_operations=PoseOperations(
                b_collection="Fingers.R",
            )
        ),
        ExtensionBone(
            name="pinky.R.002",
            bone_a="iv_ko_c_r",
            parent="pinky.R.001",
            is_connected=True,
            axis_type="local",
            axis="Y",
            start="head",
            req_bones=["iv_ko_c_r"],
            pose_operations=PoseOperations(
                b_collection="Fingers.R",
            )
        ),
    ],
)

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
    bones=[
        #Palm Control - Very cool stuff, thank you rigify - Oats
        ExtensionBone(
            name="palm.01.R",
            bone_a="j_hito_a_r",
            parent="hand.R",
            is_connected=False,
            axis_type="local",
            axis="Y",
            start="head",
            roll=135,
            req_bones=["j_hito_a_r"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.limbs_super_palm(palm_both_sides=True),
                b_collection="Fingers.R"
            )
        ),
        ExtensionBone(
            name="palm.02.R",
            bone_a="j_naka_a_r",
            parent="hand.R",
            is_connected=False,
            axis_type="local",
            axis="Y",
            start="head",
            roll=135,
            req_bones=["j_naka_a_r"],
            pose_operations=PoseOperations(
                b_collection="Fingers.R"
            )
        ),
        ExtensionBone(
            name="palm.03.R",
            bone_a="j_kusu_a_r",
            parent="hand.R",
            is_connected=False,
            axis_type="local",
            axis="Y",
            start="head",
            roll=135,
            req_bones=["j_kusu_a_r"],
            pose_operations=PoseOperations(
                b_collection="Fingers.R"
            )
        ),
        ExtensionBone(
            name="palm.04.R",
            bone_a="j_ko_a_r",
            parent="hand.R",
            is_connected=False,
            axis_type="local",
            axis="Y",
            start="head",
            roll=135,
            req_bones=["j_ko_a_r"],
            pose_operations=PoseOperations(
                b_collection="Fingers.R"
            )
        ),
        #Thumb
        ConnectBone(
            name="thumb.R",
            bone_a="j_oya_a_r",
            bone_b="j_oya_b_r",
            parent="hand.R",
            roll=15,
            is_connected=False,
            req_bones=["j_oya_a_r", "j_oya_b_r"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.limbs_super_finger(),
                b_collection="Fingers.R",
            )
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
            pose_operations=PoseOperations(
                b_collection="Fingers.R",
            )
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
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.limbs_super_finger(),
                b_collection="Fingers.R",
            )
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
            pose_operations=PoseOperations(
                b_collection="Fingers.R",
            )
        ),
        ExtensionBone(
            name="index.R.002",
            bone_a="iv_hito_c_r",
            parent="index.R.001",
            is_connected=True,
            axis_type="local",
            axis="Y",
            start="head",
            req_bones=["iv_hito_c_r"],
            pose_operations=PoseOperations(
                b_collection="Fingers.R",
            )
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
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.limbs_super_finger(),
                b_collection="Fingers.R",
            )
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
            pose_operations=PoseOperations(
                b_collection="Fingers.R",
            )
        ),
        ExtensionBone(
            name="middle.R.002",
            bone_a="iv_naka_c_r",
            parent="middle.R.001",
            is_connected=True,
            axis_type="local",
            axis="Y",
            start="head",
            req_bones=["iv_naka_c_r"],
            pose_operations=PoseOperations(
                b_collection="Fingers.R",
            )
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
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.limbs_super_finger(),
                b_collection="Fingers.R",
            )
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
            pose_operations=PoseOperations(
                b_collection="Fingers.R",
            )
        ),
        ExtensionBone(
            name="ring.R.002",
            bone_a="iv_kusu_c_r",
            parent="ring.R.001",
            is_connected=True,
            axis_type="local",
            axis="Y",
            start="head",
            req_bones=["iv_kusu_c_r"],
            pose_operations=PoseOperations(
                b_collection="Fingers.R",
            )
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
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.limbs_super_finger(),
                b_collection="Fingers.R",
            )
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
            pose_operations=PoseOperations(
                b_collection="Fingers.R",
            )
        ),
        ExtensionBone(
            name="pinky.R.002",
            bone_a="iv_ko_c_r",
            parent="pinky.R.001",
            is_connected=True,
            axis_type="local",
            axis="Y",
            start="head",
            req_bones=["iv_ko_c_r"],
            pose_operations=PoseOperations(
                b_collection="Fingers.R",
            )
        ),
    ],
)

IV_HAND_L = BoneGroup(
    name="Left Hand with IVCS bones",
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
    bones=[
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
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.limbs_super_palm(palm_both_sides=True),
                b_collection="Fingers.L"
            )
        ),
        ExtensionBone(
            name="palm.02.L",
            bone_a="j_naka_a_l",
            parent="hand.L",
            is_connected=False,
            axis_type="local",
            axis="Y",
            start="head",
            roll=-135,
            req_bones=["j_naka_a_l"],
            pose_operations=PoseOperations(
                b_collection="Fingers.L"
            )
        ),
        ExtensionBone(
            name="palm.03.L",
            bone_a="j_kusu_a_l",
            parent="hand.L",
            is_connected=False,
            axis_type="local",
            axis="Y",
            start="head",
            roll=-135,
            req_bones=["j_kusu_a_l"],
            pose_operations=PoseOperations(
                b_collection="Fingers.L"
            )
        ),
        ExtensionBone(
            name="palm.04.L",
            bone_a="j_ko_a_l",
            parent="hand.L",
            is_connected=False,
            axis_type="local",
            axis="Y",
            start="head",
            roll=-135,
            req_bones=["j_ko_a_l"],
            pose_operations=PoseOperations(
                b_collection="Fingers.L"
            )
        ),
        #Thumb
        ConnectBone(
            name="thumb.L",
            bone_a="j_oya_a_l",
            bone_b="j_oya_b_l",
            parent="hand.L",
            is_connected=False,
            roll=-15,
            req_bones=["j_oya_a_l", "j_oya_b_l"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.limbs_super_finger(),
                b_collection="Fingers.L",
            )
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
            pose_operations=PoseOperations(
                b_collection="Fingers.L",
            )
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
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.limbs_super_finger(),
                b_collection="Fingers.L",
            )
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
            pose_operations=PoseOperations(
                b_collection="Fingers.L",
            )
        ),
        ExtensionBone(
            name="index.L.002",
            bone_a="iv_hito_c_l",
            parent="index.L.001",
            is_connected=True,
            axis_type="local",
            axis="Y",
            start="head",
            req_bones=["iv_hito_c_l"],
            pose_operations=PoseOperations(
                b_collection="Fingers.L",
            )
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
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.limbs_super_finger(),
                b_collection="Fingers.L",
            )
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
            pose_operations=PoseOperations(
                b_collection="Fingers.L",
            )
        ),
        ExtensionBone(
            name="middle.L.002",
            bone_a="iv_naka_c_l",
            parent="middle.L.001",
            is_connected=True,
            axis_type="local",
            axis="Y",
            start="head",
            req_bones=["iv_naka_c_l"],
            pose_operations=PoseOperations(
                b_collection="Fingers.L",
            )
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
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.limbs_super_finger(),
                b_collection="Fingers.L",
            )
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
            pose_operations=PoseOperations(
                b_collection="Fingers.L",
            )
        ),
        ExtensionBone(
            name="ring.L.002",
            bone_a="iv_kusu_c_l",
            parent="ring.L.001",
            is_connected=True,
            axis_type="local",
            axis="Y",
            start="head",
            req_bones=["iv_kusu_c_l"],
            pose_operations=PoseOperations(
                b_collection="Fingers.L",
            )
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
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.limbs_super_finger(),
                b_collection="Fingers.L",
            )
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
            pose_operations=PoseOperations(
                b_collection="Fingers.L",
            )
        ),
        ExtensionBone(
            name="pinky.L.002",
            bone_a="iv_ko_c_l",
            parent="pinky.L.001",
            is_connected=True,
            axis_type="local",
            axis="Y",
            start="head",
            req_bones=["iv_ko_c_l"],
            pose_operations=PoseOperations(
                b_collection="Fingers.L",
            )
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
    bones=[
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
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.limbs_super_palm(palm_both_sides=True),
                b_collection="Fingers.L"
            )
        ),
        ExtensionBone(
            name="palm.02.L",
            bone_a="j_naka_a_l",
            parent="hand.L",
            is_connected=False,
            axis_type="local",
            axis="Y",
            start="head",
            roll=-135,
            req_bones=["j_naka_a_l"],
            pose_operations=PoseOperations(
                b_collection="Fingers.L"
            )
        ),
        ExtensionBone(
            name="palm.03.L",
            bone_a="j_kusu_a_l",
            parent="hand.L",
            is_connected=False,
            axis_type="local",
            axis="Y",
            start="head",
            roll=-135,
            req_bones=["j_kusu_a_l"],
            pose_operations=PoseOperations(
                b_collection="Fingers.L"
            )
        ),
        ExtensionBone(
            name="palm.04.L",
            bone_a="j_ko_a_l",
            parent="hand.L",
            is_connected=False,
            axis_type="local",
            axis="Y",
            start="head",
            roll=-135,
            req_bones=["j_ko_a_l"],
            pose_operations=PoseOperations(
                b_collection="Fingers.L"
            )
        ),
        #Thumb
        ConnectBone(
            name="thumb.L",
            bone_a="j_oya_a_l",
            bone_b="j_oya_b_l",
            parent="hand.L",
            is_connected=False,
            roll=-15,
            req_bones=["j_oya_a_l", "j_oya_b_l"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.limbs_super_finger(),
                b_collection="Fingers.L",
            )
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
            pose_operations=PoseOperations(
                b_collection="Fingers.L",
            )
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
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.limbs_super_finger(),
                b_collection="Fingers.L",
            )
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
            pose_operations=PoseOperations(
                b_collection="Fingers.L",
            )
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
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.limbs_super_finger(),
                b_collection="Fingers.L",
            )
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
            pose_operations=PoseOperations(
                b_collection="Fingers.L",
            )
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
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.limbs_super_finger(),
                b_collection="Fingers.L",
            )
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
            pose_operations=PoseOperations(
                b_collection="Fingers.L",
            )
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
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.limbs_super_finger(),
                b_collection="Fingers.L",
            )
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
            pose_operations=PoseOperations(
                b_collection="Fingers.L",
            )
        ),
    ],
),


TAIL = BoneGroup(
    name="Tail",
    transform_link= [
        TransformLink(target="DEF-Tail", bone="n_sippo_a"),
        TransformLink(target="DEF-Tail.001", bone="n_sippo_b"),
        TransformLink(target="DEF-Tail.002", bone="n_sippo_c"),
        TransformLink(target="DEF-Tail.003", bone="n_sippo_d"),
    ],
    bones=[
        ConnectBone(
            name="Tail",
            bone_a="n_sippo_a",
            bone_b="n_sippo_b",
            parent="Spine.001",
            is_connected=False,
            req_bones=["n_sippo_a", "n_sippo_b"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.basic_copy_chain(),
                b_collection="Tail"
            )
        ),
        ConnectBone(
            name="Tail.001",
            bone_a="n_sippo_b",
            bone_b="n_sippo_c",
            parent="Tail",
            is_connected=True,
            req_bones=["n_sippo_b", "n_sippo_c"],
            pose_operations=PoseOperations(
                b_collection="Tail"
            )
        ),
        ConnectBone(
            name="Tail.002",
            bone_a="n_sippo_c",
            bone_b="n_sippo_d",
            parent="Tail.001",
            is_connected=True,
            req_bones=["n_sippo_c", "n_sippo_d"],
            pose_operations=PoseOperations(
                b_collection="Tail"
            )
        ),
        ConnectBone(
            name="Tail.003",
            bone_a="n_sippo_d",
            bone_b="n_sippo_e",
            parent="Tail.002",
            is_connected=True,
            req_bones=["n_sippo_d", "n_sippo_e"],
            pose_operations=PoseOperations(
                b_collection="Tail"
            )
        ),
    ]
)

HEAD = BoneGroup(
    name="Head",
    transform_link= [
        TransformLink(target="DEF-Neck", bone="j_kubi"),
        TransformLink(target="DEF-Head", bone="j_kao"),
        TransformLink(target="DEF-jaw_master", bone="j_f_ago"),
        TransformLink(target="DEF-Cheek.B.R", bone="j_f_shoho_r"),
        TransformLink(target="DEF-Cheek.B.R.001", bone="j_f_dhoho_r"),
        TransformLink(target="DEF-Cheek.T.R", bone="j_f_hoho_r"),
        TransformLink(target="DEF-Cheek.T.R.001", bone="j_f_dmemoto_r"),
        TransformLink(target="DEF-Cheek.B.L", bone="j_f_shoho_l"),
        TransformLink(target="DEF-Cheek.B.L.001", bone="j_f_dhoho_l"),
        TransformLink(target="DEF-Cheek.T.L", bone="j_f_hoho_l"),
        TransformLink(target="DEF-Cheek.T.L.001", bone="j_f_dmemoto_l"),
        TransformLink(target="DEF-Nose", bone="j_f_uhana"),
        TransformLink(target="DEF-Nose.R", bone="j_f_dmiken_r"),
        TransformLink(target="DEF-Nostril.R", bone="j_f_hana_r"),
        TransformLink(target="DEF-Nose.L", bone="j_f_dmiken_l"),
        TransformLink(target="DEF-Nostril.L", bone="j_f_hana_l"),
        TransformLink(target="DEF-Lip.T.R.001", bone="j_f_ulip_01_r"),
        TransformLink(target="DEF-Lip.T.R.002", bone="j_f_umlip_01_r"),
        TransformLink(target="DEF-Lip.T.R.003", bone="j_f_uslip_r"),
        TransformLink(target="DEF-Lip.B.R.001", bone="j_f_dlip_01_r"),
        TransformLink(target="DEF-Lip.B.R.002", bone="j_f_dmlip_01_r"),
        TransformLink(target="DEF-Lip.B.R.003", bone="j_f_dslip_r"),
        TransformLink(target="DEF-Lip.T.L.001", bone="j_f_ulip_01_l"),
        TransformLink(target="DEF-Lip.T.L.002", bone="j_f_umlip_01_l"),
        TransformLink(target="DEF-Lip.T.L.003", bone="j_f_uslip_l"),
        TransformLink(target="DEF-Lip.B.L.001", bone="j_f_dlip_01_l"),
        TransformLink(target="DEF-Lip.B.L.002", bone="j_f_dmlip_01_l"),
        TransformLink(target="DEF-Lip.B.L.003", bone="j_f_dslip_l"),
        TransformLink(target="Lip.T.L.001", bone="j_f_ulip_02_l"),
        TransformLink(target="Lip.T.L.002", bone="j_f_umlip_02_l"),
        TransformLink(target="Lip.T.R.001", bone="j_f_ulip_02_r"),
        TransformLink(target="Lip.T.R.002", bone="j_f_umlip_02_r"),
        TransformLink(target="Lip.B.L.001", bone="j_f_dlip_02_l"),
        TransformLink(target="Lip.B.L.002", bone="j_f_dmlip_02_l"),
        TransformLink(target="Lip.B.R.001", bone="j_f_dlip_02_r"),
        TransformLink(target="Lip.B.R.002", bone="j_f_dmlip_02_r"),
        TransformLink(target="DEF-Teeth.T", bone="j_f_hagukiup"),
        TransformLink(target="DEF-Teeth.B", bone="j_f_hagukidn"),
        TransformLink(target="DEF-Tongue", bone="j_f_bero_03"),
        TransformLink(target="DEF-Tongue.001", bone="j_f_bero_02"),
        TransformLink(target="DEF-Tongue.002", bone="j_f_bero_01"),
        TransformLink(target="DEF-Ear.R", bone="j_mimi_r"),
        TransformLink(target="DEF-Ear.L", bone="j_mimi_l")
    ],
    bones=[
        ConnectBone(
            name="Neck",
            bone_a="j_kubi",
            bone_b="j_kao",
            parent="Spine.004",
            is_connected=False,
            req_bones=["j_kubi", "j_kao"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.spines_super_head(),
                b_collection="Head"
            )
        ),
        ExtensionBone(
            name="Head",
            bone_a="j_kao",
            parent="Neck",
            is_connected=True,
            axis_type="armature",
            axis="Z",
            size_factor=20.0,
            req_bones=["j_kao"],
            pose_operations=PoseOperations(
                b_collection="Head"
            )
        ),
        #Cheek Right
        ConnectBone(
            name="Cheek.B.R",
            bone_a="j_f_shoho_r",
            bone_b="j_kao",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_shoho_r", "j_kao"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head"),
                b_collection="Face (Primary)"
            )
        ),
        ConnectBone(
            name="Cheek.B.R.001",
            bone_a="j_f_dhoho_r",
            bone_b="j_kao",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_dhoho_r", "j_kao"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head"),
                b_collection="Face (Secondary)"
            )
        ),
        ConnectBone(
            name="Cheek.T.R",
            bone_a="j_f_hoho_r",
            bone_b="j_kao",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_hoho_r", "j_kao"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head"),
                b_collection="Face (Primary)"
            )
        ),
        ConnectBone(
            name="Cheek.T.R.001",
            bone_a="j_f_dmemoto_r",
            bone_b="j_kao",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_dmemoto_r", "j_kao"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head"),
                b_collection="Face (Secondary)"
            )
        ),
        #Cheek Left
        ConnectBone(
            name="Cheek.B.L",
            bone_a="j_f_shoho_l",
            bone_b="j_kao",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_shoho_l", "j_kao"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head"),
                b_collection="Face (Primary)"
            )
        ),
        ConnectBone(
            name="Cheek.B.L.001",
            bone_a="j_f_dhoho_l",
            bone_b="j_kao",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_dhoho_l", "j_kao"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head"),
                b_collection="Face (Secondary)"
            )
        ),
        ConnectBone(
            name="Cheek.T.L",
            bone_a="j_f_hoho_l",
            bone_b="j_kao",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_hoho_l", "j_kao"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head"),
                b_collection="Face (Primary)"
            )
        ),
        ConnectBone(
            name="Cheek.T.L.001",
            bone_a="j_f_dmemoto_l",
            bone_b="j_kao",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_dmemoto_l", "j_kao"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head"),
                b_collection="Face (Secondary)"
            )
        ),
        #Nose Centre
        ConnectBone(
            name="Nose",
            bone_a="j_f_uhana",
            bone_b="j_kao",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_uhana", "j_kao"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head"),
                b_collection="Face (Secondary)"
            )
        ),
        #Nose Right
        ConnectBone(
            name="Nose.R",
            bone_a="j_f_dmiken_r",
            bone_b="j_kao",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_dmiken_r", "j_kao"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head"),
                b_collection="Face (Secondary)"
            )
        ),
        ConnectBone(
            name="Nostril.R",
            bone_a="j_f_hana_r",
            bone_b="j_kao",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_hana_r", "j_kao"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head"),
                b_collection="Face (Secondary)"
            )
        ),
        #Nose Left
        ConnectBone(
            name="Nose.L",
            bone_a="j_f_dmiken_l",
            bone_b="j_kao",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_dmiken_l", "j_kao"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head"),
                b_collection="Face (Secondary)"
            )
        ),
        ConnectBone(
            name="Nostril.L",
            bone_a="j_f_hana_l",
            bone_b="j_kao",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_hana_l", "j_kao"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(skin_control_orientation_bone="Head"),
                b_collection="Face (Secondary)"
            )
        ),
        
        #Anchor
        ExtensionBone(

            name="Face.Suppressor",
            bone_a="j_kao",
            parent="j_kao",
            is_connected=False,
            axis_type="local",
            axis="Y",
            start="head",
            size_factor=1.0,
            req_bones=["j_kao"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_anchor(skin_anchor_hide=True),
                b_collection="Face"
            )
        ),
        #Jaw
        CenterBone(
            name="jaw_master_ref",
            ref_bones=["j_f_dlip_01_r", "j_f_dlip_01_l"],
            parent="Head",
            axis="Y",
            inverted=False,
            req_bones=["j_f_dlip_01_r", "j_f_dlip_01_l"],
            pose_operations=PoseOperations(
                b_collection="MCH",
            ),
        ),
        ConnectBone(
            name="jaw_master",
            bone_a="j_f_ago",
            bone_b="jaw_master_ref",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_ago", "jaw_master_ref"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.face_skin_jaw(jaw_mouth_influence=1.0),
                b_collection="Face (Primary)"
            )
        ),
        #Mouth Center Reference
        CenterBone(
            name="Mouth.Center",
            ref_bones=["j_f_ulip_01_r", "j_f_ulip_01_l"],
            parent="Head",
            axis="Y",
            inverted=False,
            req_bones=["j_f_ulip_01_r", "j_f_ulip_01_l"],
            pose_operations=PoseOperations(
                b_collection="MCH",
            ),
        ),
        #Mouth Right
        ConnectBone(
            name="Lip.T.R",
            bone_a="Mouth.Center",
            bone_b="j_f_ulip_01_r",
            parent="jaw_master",
            is_connected=False,
            req_bones=["j_f_ulip_01_r", "Mouth.Center"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_stretchy_chain(skin_control_orientation_bone="Head", skin_chain_falloff_length=True, skin_chain_falloff=[0.0, 0.0, -1.0], primary_layer_extra="Face (Primary)"),
                b_collection="Face (Secondary)"
            )
        ),
        ConnectBone(
            name="Lip.T.R.001",
            bone_a="j_f_ulip_01_r",
            bone_b="j_f_umlip_01_r",
            parent="Lip.T.R",
            is_connected=True,
            req_bones=["j_f_umlip_01_r", "j_f_ulip_01_r"],
            pose_operations=PoseOperations(
                b_collection="Face"
            )
        ),
        ConnectBone(
            name="Lip.B.R",
            bone_a="jaw_master_ref",
            bone_b="j_f_dlip_01_r",
            parent="jaw_master",
            is_connected=False,
            req_bones=["j_f_dlip_01_r", "jaw_master_ref"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_stretchy_chain(skin_control_orientation_bone="Head", skin_chain_falloff_length=True, skin_chain_falloff=[0.0, 0.0, -1.0], primary_layer_extra="Face (Primary)"),
                b_collection="Face (Secondary)"
            )
        ),
        ConnectBone(
            name="Lip.B.R.001",
            bone_a="j_f_dlip_01_r",
            bone_b="j_f_dmlip_01_r",
            parent="Lip.B.R",
            is_connected=True,
            req_bones=["j_f_dmlip_01_r", "j_f_dlip_01_r"],
            pose_operations=PoseOperations(
                b_collection="Face"
            )
        ),
        
        #This is a reference point for the last bone in the chain
        CenterBone(
            name="Corner.R",
            ref_bones=["j_f_uslip_r", "j_f_dslip_r", "Cheek.B.R"],
            parent="Head",
            axis="Y",
            inverted=False,
            req_bones=["j_f_uslip_r", "j_f_dslip_r", "Cheek.B.R"],
            pose_operations=PoseOperations(
                b_collection="MCH",
            ),
        ),
        ConnectBone(
            name="Lip.T.R.002",
            bone_a="j_f_umlip_01_r",
            bone_b="j_f_uslip_r",
            parent="Lip.T.R.001",
            is_connected=True,
            req_bones=["j_f_uslip_r", "j_f_umlip_01_r"],
            pose_operations=PoseOperations(
                 b_collection="Face"
            )
        ),
        ConnectBone(
            name="Lip.T.R.003",
            bone_a="j_f_uslip_r",
            bone_b="Corner.R",
            parent="Lip.T.R.002",
            is_connected=True,
            req_bones=["j_f_uslip_r", "Corner.R"],
            pose_operations=PoseOperations(
                    b_collection="Face"
            )
        ),
        ConnectBone(
            name="Lip.B.R.002",
            bone_a="j_f_dmlip_01_r",
            bone_b="j_f_dslip_r",
            parent="Lip.B.R.001",
            is_connected=True,
            req_bones=["j_f_dmlip_01_r", "j_f_dslip_r"],
            pose_operations=PoseOperations(
                 b_collection="Face"
            )
        ),
        ConnectBone(
            name="Lip.B.R.003",
            bone_a="j_f_dslip_r",
            bone_b="Corner.R",
            parent="Lip.B.R.002",
            is_connected=True,
            req_bones=["j_f_dslip_r", "Corner.R"],
            pose_operations=PoseOperations(
                    b_collection="Face"
            )
        ),

        #Left Mouth
        ConnectBone(
            name="Lip.T.L",
            bone_a="Mouth.Center",
            bone_b="j_f_ulip_01_l",
            parent="jaw_master",
            is_connected=False,
            req_bones=["j_f_ulip_01_l", "Mouth.Center"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_stretchy_chain(skin_control_orientation_bone="Head", skin_chain_falloff_length=True, skin_chain_falloff=[0.0, 0.0, -1.0], primary_layer_extra="Face (Primary)"),
                b_collection="Face (Secondary)"
            )
        ),
        ConnectBone(
            name="Lip.T.L.001",
            bone_a="j_f_ulip_01_l",
            bone_b="j_f_umlip_01_l",
            parent="Lip.T.L",
            is_connected=True,
            req_bones=["j_f_umlip_01_l", "j_f_ulip_01_l"],
            pose_operations=PoseOperations(
                b_collection="Face"
            )
        ),
        ConnectBone(
            name="Lip.B.L",
            bone_a="jaw_master_ref",
            bone_b="j_f_dlip_01_l",
            parent="jaw_master",
            is_connected=False,
            req_bones=["j_f_dlip_01_l", "jaw_master_ref"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_stretchy_chain(skin_control_orientation_bone="Head", skin_chain_falloff_length=True, skin_chain_falloff=[0.0, 0.0, -1.0], primary_layer_extra="Face (Primary)"),
                b_collection="Face (Secondary)"
            )
        ),
        ConnectBone(
            name="Lip.B.L.001",
            bone_a="j_f_dlip_01_l",
            bone_b="j_f_dmlip_01_l",
            parent="Lip.B.L",
            is_connected=True,
            req_bones=["j_f_dmlip_01_l", "j_f_dlip_01_l"],
            pose_operations=PoseOperations(
                b_collection="Face"
            )
        ),
        #This is a reference point for the last bone in the chain
        CenterBone(
            name="Corner.L",
            ref_bones=["j_f_uslip_l", "j_f_dslip_l", "Cheek.B.L"],
            parent="Head",
            axis="Y",
            inverted=False,
            req_bones=["j_f_uslip_l", "j_f_dslip_l", "Cheek.B.L"],
             pose_operations=PoseOperations(
                b_collection="MCH"
             ),
        ),
        ConnectBone(
           name = "Lip.T.L.002",
           bone_a = "j_f_umlip_01_l",
           bone_b = "j_f_uslip_l",
           parent = "Lip.T.L.001",
           is_connected = True,
           req_bones = ["j_f_umlip_01_l", "j_f_uslip_l"],
           pose_operations = PoseOperations(
               b_collection = "Face"
           )
       ),
        ConnectBone(
           name = "Lip.T.L.003",
           bone_a = "j_f_uslip_l",
           bone_b = "Corner.L",
           parent = "Lip.T.L.002",
           is_connected = True,
           req_bones = ["j_f_uslip_l", "Corner.L"],
           pose_operations = PoseOperations(
               b_collection = "Face"
          )
       ),
        ConnectBone(
           name = "Lip.B.L.002",
           bone_a = "j_f_dmlip_01_l",
           bone_b = "j_f_dslip_l",
           parent = "Lip.B.L.001",
           is_connected = True,
           req_bones = ["j_f_dmlip_01_l", "j_f_dslip_l"],
           pose_operations = PoseOperations(
               b_collection = "Face"
          )
       ),
        ConnectBone(
           name = "Lip.B.L.003",
           bone_a = "j_f_dslip_l",
           bone_b = "Corner.L",
           parent = "Lip.B.L.002",
           is_connected = True,
           req_bones = ["Corner.L", "j_f_dslip_l"],
           pose_operations = PoseOperations(
               b_collection = "Face"
          )
       ),
        #Teeth
        ExtensionBone(
            name="Teeth.T",
            bone_a="j_f_hagukiup",
            size_factor=1,
            axis_type="local",
            axis="Y",
            parent="Head",
            start="head",
            is_connected=False,
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.basic_super_copy(widget_type="teeth"),
                b_collection="Mouth"
            )
        ),
        ExtensionBone(
            name="Teeth.B",
            bone_a="j_f_hagukidn",
            size_factor=1,
            axis_type="local",
            axis="Y",
            parent="jaw_master",
            start="head",
            is_connected=False,
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.basic_super_copy(widget_type="teeth"),
                b_collection="Mouth"
            )
        ),
        #Tongue
        ConnectBone(
            name="Tongue",
            bone_a="j_f_bero_03",
            bone_b="j_f_bero_02",
            parent="jaw_master",
            is_connected=False,
            req_bones=["j_f_bero_03", "j_f_bero_02"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.face_basic_tongue(),
                b_collection="Mouth"
            )
        ),
        ConnectBone(
            name="Tongue.001",
            bone_a="j_f_bero_02",
            bone_b="j_f_bero_01",
            parent="Tongue",
            is_connected=True,
            req_bones=["j_f_bero_02", "j_f_bero_01"],
            pose_operations=PoseOperations(
                b_collection="Mouth"
            )
        ),
        ExtensionBone(
            name="Tongue.002",
            bone_a="Tongue.001",
            parent="Tongue.001",
            is_connected=True,
            axis_type="local",
            axis="Y",
            req_bones=["Tongue.001"],
            pose_operations=PoseOperations(
                b_collection="Mouth"
            )
        ),
        #Nose Glue
        ConnectBone(
            name="Nostril.Glue.R",
            bone_a="j_f_hana_r",
            bone_b="j_f_uhana",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_hana_r", "j_f_uhana"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5),
                b_collection="MCH"
            )
        ),
        ConnectBone(
            name="Nostril.Glue.L",
            bone_a="j_f_hana_l",
            bone_b="j_f_uhana",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_hana_l", "j_f_uhana"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5),
                b_collection="MCH"
            )
        ),
        ConnectBone(
            name="Nostril.Glue.R.001",
            bone_a="Cheek.T.R.001", 
            bone_b="Nostril.R",
            parent="Head",
            is_connected=False,
            req_bones=["Cheek.T.R.001", "Nostril.R"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5),
                b_collection="MCH"
            ),
        ),
        ConnectBone(
            name="Nostril.Glue.L.001",
            bone_a="Cheek.T.L.001", 
            bone_b="Nostril.L",
            parent="Head",
            is_connected=False,
            req_bones=["Cheek.T.L.001", "Nostril.L"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5),
                b_collection="MCH"
            ),
        ),
        #Cheek Glue Bones Right
        ConnectBone(
            name="Cheek.B.R.glue",
            bone_a="j_f_dhoho_r",
            bone_b="j_f_shoho_r",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_shoho_r", "j_f_dhoho_r"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5),
                b_collection="MCH"
            )
        ),
        ConnectBone(
            name="Cheek.T.R.glue",
            bone_a="j_f_dhoho_r",
            bone_b="j_f_hoho_r",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_hoho_r", "j_f_dhoho_r"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5),
                b_collection="MCH"
            )
        ),
        #Cheek Glue Bones Left
        ConnectBone(
            name="Cheek.B.L.glue",
            bone_a="j_f_dhoho_l",
            bone_b="j_f_shoho_l",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_shoho_l", "j_f_dhoho_l"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5),
                b_collection="MCH"
            )
        ),
        ConnectBone(
            name="Cheek.T.L.glue",
            bone_a="j_f_dhoho_l",
            bone_b="j_f_hoho_l",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_hoho_l", "j_f_dhoho_l"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5),
                b_collection="MCH"
            )
        ),
        #Nostril Glue Bones
        ConnectBone(
            name="Nostril.Glue.R",
            bone_a="j_f_hana_r",
            bone_b="j_f_uhana",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_hana_r", "j_f_uhana"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5),
                b_collection="MCH"
            )
        ),
        ConnectBone(
            name="Nostril.Glue.L",
            bone_a="j_f_hana_l",
            bone_b="j_f_uhana",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_hana_l", "j_f_uhana"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5),
                b_collection="MCH"
            )
        ),
        ConnectBone(
            name="Nostril.Glue.R.001",
            bone_a="Cheek.T.R.001", 
            bone_b="Nostril.R",
            parent="Head",
            is_connected=False,
            req_bones=["Cheek.T.R.001", "Nostril.R"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5),
                b_collection="MCH"
            ),
        ),
        ConnectBone(
            name="Nostril.Glue.L.001",
            bone_a="Cheek.T.L.001", 
            bone_b="Nostril.L",
            parent="Head",
            is_connected=False,
            req_bones=["Cheek.T.L.001", "Nostril.L"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5),
                b_collection="MCH"
            ),
        ),
        #Lip Glue Bones
        ConnectBone(
            name="Lip.T.R.001.glue",
            bone_a="j_f_hana_r",
            bone_b="j_f_ulip_01_r",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_hana_r", "j_f_ulip_01_r"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.2, skin_glue_tail_reparent=True),
                b_collection="MCH"
            )
        ),
        ConnectBone(
            name="Lip.T.L.001.glue",
            bone_a="j_f_hana_l",
            bone_b="j_f_ulip_01_l",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_hana_l", "j_f_ulip_01_l"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.2, skin_glue_tail_reparent=True),
                b_collection="MCH"
            )
        ),
        #Mouth Corner Glue Bones
        ConnectBone(
            name="Mouth.Corner.glue.L",
            bone_a="j_f_shoho_l",
            bone_b="Corner.L",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_shoho_l", "Corner.L"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5, skin_glue_tail_reparent=True),
                b_collection="MCH"
            )
        ),
        ConnectBone(
            name="Mouth.Corner.glue.R",
            bone_a="j_f_shoho_r",
            bone_b="Corner.R",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_shoho_r", "Corner.R"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.5, skin_glue_tail_reparent=True),
                b_collection="MCH"
            )
        ),
        #Ears
        ExtensionBone(
            name="Ear.R",
            bone_a="j_mimi_r",
            parent="Head",
            is_connected=False,
            axis_type="local",
            axis="Y",
            start="head",
            req_bones=["j_mimi_r"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.basic_super_copy(widget_type="bone"),
                b_collection="Head",
            )
        ),
        ExtensionBone(
            name="Ear.L",
            bone_a="j_mimi_l",
            parent="Head",
            is_connected=False,
            axis_type="local",
            axis="Y",
            start="head",
            req_bones=["j_mimi_l"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.basic_super_copy(widget_type="bone"),
                b_collection="Head",
            )
        )    
    ]
)

VIERA_EARS = BoneGroup(
    name="Viera Ears",
    transform_link=[
        TransformLink(target="DEF-V_Ear.R", bone="j_zera_a_r"),
        TransformLink(target="DEF-V_Ear.R.001", bone="j_zera_b_r"),
        TransformLink(target="DEF-V_Ear.R", bone="j_zerb_a_r"),
        TransformLink(target="DEF-V_Ear.R.001", bone="j_zerb_b_r"),
        TransformLink(target="DEF-V_Ear.R", bone="j_zerc_a_r"),
        TransformLink(target="DEF-V_Ear.R.001", bone="j_zerc_b_r"),
        TransformLink(target="DEF-V_Ear.R", bone="j_zerd_a_r"),
        TransformLink(target="DEF-V_Ear.R.001", bone="j_zerd_b_r"),

        TransformLink(target="DEF-V_Ear.L", bone="j_zera_a_l"),
        TransformLink(target="DEF-V_Ear.L.001", bone="j_zera_b_l"),
        TransformLink(target="DEF-V_Ear.L", bone="j_zerb_a_l"),
        TransformLink(target="DEF-V_Ear.L.001", bone="j_zerb_b_l"),
        TransformLink(target="DEF-V_Ear.L", bone="j_zerc_a_l"),
        TransformLink(target="DEF-V_Ear.L.001", bone="j_zerc_b_l"),
        TransformLink(target="DEF-V_Ear.L", bone="j_zerd_a_l"),
        TransformLink(target="DEF-V_Ear.L.001", bone="j_zerd_b_l"),
    ],
    bones=[
        ConnectBone(
            name="V_Ear.R",
            bone_a="j_zera_a_r",
            bone_b="j_zera_b_r",
            parent="Head",
            is_connected=False,
            req_bones=["j_zera_a_r", "j_zera_b_r"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.basic_copy_chain(),
                b_collection="Head",
            )
        ),
        ConnectBone(
            name="V_Ear.R.001",
            bone_a="j_zera_b_r",
            bone_b="j_zera_b_r",
            parent="V_Ear.R",
            is_connected=True,
            start="head",
            end="tail",
            req_bones=["j_zera_b_r", "j_zera_b_r"],
            pose_operations=PoseOperations(
                b_collection="Head",
            )
        ),
        ConnectBone(
            name="V_Ear.L",
            bone_a="j_zera_a_l",
            bone_b="j_zera_b_l",
            parent="Head",
            is_connected=False,
            req_bones=["j_zera_a_l", "j_zera_b_l"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.basic_copy_chain(),
                b_collection="Head",
            )
        ),
        ConnectBone(
            name="V_Ear.L.001",
            bone_a="j_zera_b_l",
            bone_b="j_zera_b_l",
            parent="V_Ear.L",
            is_connected=True,
            start="head",
            end="tail",
            req_bones=["j_zera_b_l", "j_zera_b_l"],
            pose_operations=PoseOperations(
                b_collection="Head",
            )
        ),
    ]
)

BROW = BoneGroup(
    name="Brow",
    transform_link=[
        TransformLink(target="DEF-Brow.R", bone="j_f_mayu_r"),
        TransformLink(target="DEF-Brow.R.001", bone="j_f_mmayu_r"),
        TransformLink(target="DEF-Brow.R.002", bone="j_f_miken_01_r"),
        TransformLink(target="DEF-Brow.R.003", bone="j_f_miken_02_r"),
        TransformLink(target="DEF-Brow.L", bone="j_f_mayu_l"),
        TransformLink(target="DEF-Brow.L.001", bone="j_f_mmayu_l"),
        TransformLink(target="DEF-Brow.L.002", bone="j_f_miken_01_l"),
        TransformLink(target="DEF-Brow.L.003", bone="j_f_miken_02_l")
    ],
    bones=[
        ConnectBone(
            name="Brow.R",
            bone_a="j_f_mayu_r",
            bone_b="j_f_mmayu_r",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_mayu_r", "j_f_mmayu_r",],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_stretchy_chain(skin_chain_pivot_pos=0, skin_control_orientation_bone="Head", skin_chain_falloff_length=True, primary_layer_extra="Face (Primary)"),
                b_collection="Face (Secondary)",
            )
        ),
        ConnectBone(
            name="Brow.R.001",
            bone_a="j_f_mmayu_r",
            bone_b="j_f_miken_01_r",
            parent="Brow.R",
            is_connected=True,
            req_bones=["j_f_mmayu_r", "j_f_miken_01_r"],
            pose_operations=PoseOperations(
                b_collection="Face (Primary)",
            )
        ),
        ConnectBone(
            name="Brow.R.002",
            bone_a="j_f_miken_01_r",
            bone_b="j_f_miken_02_r",
            parent="Brow.R.001",
            is_connected=True,
            req_bones=["j_f_miken_01_r", "j_f_miken_02_r"],
            pose_operations=PoseOperations(
                b_collection="Face (Primary)",
            )
        ),
        ExtensionBone(
            name="Brow.R.003",
            bone_a="Brow.R.002",
            parent="Brow.R.002",
            is_connected=True,
            axis_type="local",
            axis="Y",
            req_bones=["j_f_miken_02_r"],
            pose_operations=PoseOperations(
                b_collection="Face (Primary)"
            )
        ),
        ConnectBone(
            name="Brow.L",
            bone_a="j_f_mayu_l",
            bone_b="j_f_mmayu_l",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_mayu_l", "j_f_mmayu_l",],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_stretchy_chain(skin_chain_pivot_pos=0, skin_control_orientation_bone="Head", skin_chain_falloff_length=True, primary_layer_extra="Face (Primary)"),
                b_collection="Face (Secondary)",
            )
        ),
        ConnectBone(
            name="Brow.L.001",
            bone_a="j_f_mmayu_l",
            bone_b="j_f_miken_01_l",
            parent="Brow.L",
            is_connected=True,
            req_bones=["j_f_mmayu_l", "j_f_miken_01_l"],
            pose_operations=PoseOperations(
                b_collection="Face (Primary)",
            )
        ),
        ConnectBone(
            name="Brow.L.002",
            bone_a="j_f_miken_01_l",
            bone_b="j_f_miken_02_l",
            parent="Brow.L.001",
            is_connected=True,
            req_bones=["j_f_miken_01_l", "j_f_miken_02_l"],
            pose_operations=PoseOperations(
                b_collection="Face (Primary)",
            )
        ),
        ExtensionBone(
            name="Brow.L.003",
            bone_a="Brow.L.002",
            parent="Brow.L.002",
            is_connected=True,
            axis_type="local",
            axis="Y",
            req_bones=["j_f_miken_02_l"],
            pose_operations=PoseOperations(
                b_collection="Face (Primary)"
            )
        )
    ]
)

LEFT_EYE = BoneGroup(
    name="Eyes",
    transform_link= [
        TransformLink(target="lid.B.L.001", bone="j_f_mabdn_03in_l"),
        TransformLink(target="lid.B.L.002", bone="j_f_mabdn_01_l"),
        TransformLink(target="lid.B.L.003", bone="j_f_mabdn_02out_l"),
        TransformLink(target="lid.T.L.001", bone="j_f_mabup_02out_l"),
        TransformLink(target="lid.T.L.002", bone="j_f_mabup_01_l"),
        TransformLink(target="lid.T.L.003", bone="j_f_mabup_03in_l"),
        TransformLink(target="MCH-Eye.L", bone="j_f_eyepuru_l"),
    ],
    bones=[

        ## Skin Bone, Basicly Corner Bones for the eyes
        SkinBone(
            name="lid.T.L", 
            bone_a="j_f_mabup_02out_l", 
            mesh_restriction="eye_occlusion",
            req_bones=["j_f_mabup_02out_l"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_stretchy_chain(skin_chain_pivot_pos=2, primary_layer_extra="Face (Primary)" ,skin_control_orientation_bone="Head", skin_chain_falloff_spherical=[False, False, False], skin_chain_falloff=[0.0, 1.0, 0.0], skin_chain_falloff_length=True), 
                b_collection="Face (Secondary)"
                )
        ),
        SkinBone(
            name="lid.T.L.002", 
            bone_a="j_f_mabup_01_l", 
            mesh_restriction="eye_occlusion",
            req_bones=["j_f_mabup_01_l"],
            pose_operations=PoseOperations(
                b_collection="Face (Secondary)"
                )
        ),
        SkinBone(
            name="lid.B.L", 
            bone_a="j_f_mabdn_03in_l", 
            mesh_restriction="eye_occlusion", 
            req_bones=["j_f_mabdn_03in_l"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_stretchy_chain(skin_chain_pivot_pos=2, primary_layer_extra="Face (Primary)" ,skin_control_orientation_bone="Head"), 
                b_collection="Face (Secondary)"
                )
        ),
        SkinBone(
            name="lid.B.L.002", 
            bone_a="j_f_mabdn_01_l", 
            mesh_restriction="eye_occlusion",
            req_bones=["j_f_mabdn_01_l"], 
            pose_operations=PoseOperations(
                b_collection="Face (Secondary)"
                )
        ),


        CopyBone(
            name="Eye.L",
            source_bone="j_f_eyepuru_l",
            req_bones=["j_f_eyepuru_l"],
            parent="Head",
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.face_skin_eye(),
                b_collection="Face (Primary)"
            )
        ),

        # CenterBone(
        #     name="Eye.L",
        #     ref_bones=["lid.T.L", "lid.T.L.002", "lid.B.L", "lid.B.L.002"],
        #     parent="Head",
        #     axis="Y",
        #     inverted=True,
        #     req_bones=["lid.T.L", "lid.T.L.002", "lid.B.L", "lid.B.L.002"],
        #     pose_operations=PoseOperations(
        #         rigify_settings=rigify.types.face_skin_eye(),
        #         b_collection="Face"
        #     )
        # ),

        BridgeBone(
            name="lid.T.L.001",
            bone_a="lid.T.L",
            bone_b="lid.T.L.002",
            offset_factor=mathutils.Vector((0.0, -0.001, 0.001)),
            is_connected=True,  
            parent="Eye.L",
            req_bones=["lid.T.L", "lid.T.L.002"],
            pose_operations=PoseOperations(
                b_collection="Face (Secondary)"
            )
        ), 

        BridgeBone(
            name="lid.T.L.003", 
            bone_a="lid.T.L.002",
            bone_b="lid.B.L",
            offset_factor=mathutils.Vector((0.0, 0.0, 0.003)),
            is_connected=False,
            req_bones=["lid.T.L.002", "lid.B.L"],
            pose_operations=PoseOperations(
                b_collection="Face (Secondary)"
            )
        ),
        BridgeBone(
            name="lid.B.L.001",
            bone_a="lid.B.L",
            bone_b="lid.B.L.002",
            offset_factor=mathutils.Vector((-0.002, 0.0, 0.001)),
            is_connected=True,
            parent="Eye.L",
            req_bones=["lid.B.L", "lid.B.L.002"],
            pose_operations=PoseOperations(
                b_collection="Face (Secondary)"
            )
        ),

        BridgeBone(
            name="lid.B.L.003",
            bone_a="lid.B.L.002",
            bone_b="lid.T.L",
            offset_factor=mathutils.Vector((0.003, -0.001, -0.003)),
            is_connected=False,
            req_bones=["lid.B.L.002", "lid.T.L"],
            pose_operations=PoseOperations(
                b_collection="Face (Secondary)"
            )
        ),


        ConnectBone(
            name="eye_tracker.B.L.001",
            bone_a="j_f_mabdn_03in_l",
            bone_b="lid.B.L.001",
            parent="Eye.L",
            is_connected=False,
            req_bones=["j_f_mabdn_03in_l", "j_f_eye_l"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(),
                b_collection="Face"
            )
        ),

        ConnectBone(
            name="eye_tracker.B.L.002",
            bone_a="j_f_mabdn_01_l",
            bone_b="lid.B.L.002",
            parent="Eye.L",
            is_connected=False,
            req_bones=["j_f_mabdn_01_l", "j_f_eye_l"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(),
                b_collection="Face"
            )
        ),

        ConnectBone(
            name="eye_tracker.B.L.003",
            bone_a="j_f_mabdn_02out_l",
            bone_b="lid.B.L.003",
            parent="Eye.L",
            is_connected=False,
            req_bones=["j_f_mabdn_02out_l", "j_f_eye_l"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(),
                b_collection="Face"
            )
        ),

        ConnectBone(
            name="eye_tracker.T.L.001",
            bone_a="j_f_mabup_02out_l",
            bone_b="lid.T.L.001",
            parent="Eye.L",
            is_connected=False,
            req_bones=["j_f_mabup_02out_l", "j_f_eye_l"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(),
                b_collection="Face"
            )
        ),

        ConnectBone(
            name="eye_tracker.T.L.002",
            bone_a="j_f_mabup_01_l",
            bone_b="lid.T.L.002",
            parent="Eye.L",
            is_connected=False,
            req_bones=["j_f_mabup_01_l", "j_f_eye_l"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(),
                b_collection="Face"
            )
        ),

        ConnectBone(
            name="eye_tracker.T.L.003",
            bone_a="j_f_mabup_03in_l",
            bone_b="lid.T.L.003",
            parent="Eye.L",
            is_connected=False,
            req_bones=["j_f_mabup_03in_l", "j_f_eye_l"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(),
                b_collection="Face"
            )
        ),
        #Glue Bones
        ConnectBone(
            name="Lower.Lid.L.Glue",
            bone_a="lid.B.L.002",
            bone_b="j_f_hoho_l",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_hoho_l", "lid.B.L.002"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.1, skin_glue_tail_reparent=True),
                b_collection="MCH"
            )
        ),
        ConnectBone(
            name="Upper.Lid.L.Glue",
            bone_a="lid.T.L.002",
            bone_b="j_f_miken_02_l",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_miken_02_l", "lid.T.L.002"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.1, skin_glue_tail_reparent=True),
                b_collection="MCH"
            )
        ),
    ]
)  

RIGHT_EYE = BoneGroup(
    name="Eyes",
    transform_link= [
        TransformLink(target="lid.B.R.001", bone="j_f_mabdn_03in_r"),
        TransformLink(target="lid.B.R.002", bone="j_f_mabdn_01_r"),
        TransformLink(target="lid.B.R.003", bone="j_f_mabdn_02out_r"),
        TransformLink(target="lid.T.R.001", bone="j_f_mabup_02out_r"),
        TransformLink(target="lid.T.R.002", bone="j_f_mabup_01_r"),
        TransformLink(target="lid.T.R.003", bone="j_f_mabup_03in_r"),
        TransformLink(target="MCH-Eye.R", bone="j_f_eyepuru_r"),
    ],
    bones=[
        ## Skin Bone, Basicly Corner Bones for the eyes
        SkinBone(
            name="lid.T.R", 
            bone_a="j_f_mabup_02out_r", 
            mesh_restriction="eye_occlusion",
            req_bones=["j_f_mabup_02out_r"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_stretchy_chain(skin_chain_pivot_pos=2, primary_layer_extra="Face (Primary)" ,skin_control_orientation_bone="Head", skin_chain_falloff_spherical=[False, False, False], skin_chain_falloff=[0.0, 1.0, 0.0], skin_chain_falloff_length=True), 
                b_collection="Face (Secondary)"
                )
        ),
        SkinBone(
            name="lid.T.R.002", 
            bone_a="j_f_mabup_01_r", 
            mesh_restriction="eye_occlusion",
            req_bones=["j_f_mabup_01_r"],
            pose_operations=PoseOperations(
                b_collection="Face (Secondary)"
                )
        ),
        SkinBone(
            name="lid.B.R", 
            bone_a="j_f_mabdn_03in_r", 
            mesh_restriction="eye_occlusion", 
            req_bones=["j_f_mabdn_03in_r"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_stretchy_chain(skin_chain_pivot_pos=2, primary_layer_extra="Face (Primary)" ,skin_control_orientation_bone="Head"), 
                b_collection="Face (Secondary)"
                )
        ),
        SkinBone(
            name="lid.B.R.002",
            bone_a="j_f_mabdn_01_r",
            mesh_restriction="eye_occlusion",
            req_bones=["j_f_mabdn_01_r"],
            pose_operations=PoseOperations(
                b_collection="Face (Secondary)"
                )
        ),
        CopyBone(
            name="Eye.R",
            source_bone="j_f_eyepuru_r",
            req_bones=["j_f_eyepuru_r"],
            parent="Head",
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.face_skin_eye(),
                b_collection="Face (Primary)"
                )
        ),
        BridgeBone(
            name="lid.T.R.001",
            bone_a="lid.T.R",
            bone_b="lid.T.R.002",
            offset_factor=mathutils.Vector((0.0, -0.001, 0.001)),
            is_connected=True,  
            parent="Eye.R",
            req_bones=["lid.T.R", "lid.T.R.002"],
            pose_operations=PoseOperations(
                b_collection="Face (Secondary)"
            )
        ),
        BridgeBone(
            name="lid.T.R.003", 
            bone_a="lid.T.R.002",
            bone_b="lid.B.R",
            offset_factor=mathutils.Vector((0.0, 0.0, 0.003)),
            is_connected=False,
            req_bones=["lid.T.R.002", "lid.B.R"],
            pose_operations=PoseOperations(
                b_collection="Face (Secondary)"
            )
        ),
        BridgeBone(
            name="lid.B.R.001",
            bone_a="lid.B.R",
            bone_b="lid.B.R.002",
            offset_factor=mathutils.Vector((-0.002, 0.0, 0.001)),
            is_connected=True,
            parent="Eye.R",
            req_bones=["lid.B.R", "lid.B.R.002"],
            pose_operations=PoseOperations(
                b_collection="Face (Secondary)"
            )
        ),
        BridgeBone(
            name="lid.B.R.003",
            bone_a="lid.B.R.002",
            bone_b="lid.T.R",
            offset_factor=mathutils.Vector((-0.003, -0.001, -0.003)),
            is_connected=False,
            req_bones=["lid.B.R.002", "lid.T.R"],
            pose_operations=PoseOperations(
                b_collection="Face (Secondary)"
            )
        ),

        ConnectBone(
            name="eye_tracker.B.R.001",
            bone_a="j_f_mabdn_03in_r",
            bone_b="lid.B.R.001",
            parent="Eye.R",
            is_connected=False,
            req_bones=["j_f_mabdn_03in_r", "j_f_eye_r"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(),
                b_collection="Face"
            )
        ),
        ConnectBone(
            name="eye_tracker.B.R.002",
            bone_a="j_f_mabdn_01_r",
            bone_b="lid.B.R.002",
            parent="Eye.R",
            is_connected=False,
            req_bones=["j_f_mabdn_01_r", "j_f_eye_r"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(),
                b_collection="Face"
            )
        ),
        ConnectBone(
            name="eye_tracker.B.R.003",
            bone_a="j_f_mabdn_02out_r",
            bone_b="lid.B.R.003",
            parent="Eye.R",
            is_connected=False,
            req_bones=["j_f_mabdn_02out_r", "j_f_eye_r"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(),
                b_collection="Face"
            )
        ),
        ConnectBone(
            name="eye_tracker.T.R.001",
            bone_a="j_f_mabup_02out_r",
            bone_b="lid.T.R.001",
            parent="Eye.R",
            is_connected=False,
            req_bones=["j_f_mabup_02out_r", "j_f_eye_r"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(),
                b_collection="Face"
            )
        ),
        ConnectBone(
            name="eye_tracker.T.R.002",
            bone_a="j_f_mabup_01_r",
            bone_b="lid.T.R.002",
            parent="Eye.R",
            is_connected=False,
            req_bones=["j_f_mabup_01_r", "j_f_eye_r"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(),
                b_collection="Face"
            )
        ),
        ConnectBone(
            name="eye_tracker.T.R.003",
            bone_a="j_f_mabup_03in_r",
            bone_b="lid.T.R.003",
            parent="Eye.R",
            is_connected=False,
            req_bones=["j_f_mabup_03in_r", "j_f_eye_r"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(),
                b_collection="Face"
            )
        ),
        #Glue Bones
        ConnectBone(
            name="Lower.Lid.R.Glue",
            bone_a="lid.B.R.002",
            bone_b="j_f_hoho_r",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_hoho_r", "lid.B.R.002"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.1, skin_glue_tail_reparent=True),
                b_collection="MCH"
            )
        ),
        ConnectBone(
            name="Upper.Lid.R.Glue",
            bone_a="lid.T.R.002",
            bone_b="j_f_miken_02_r",
            parent="Head",
            is_connected=False,
            req_bones=["j_f_miken_02_r", "lid.T.R.002"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_glue(relink_constraints=True, skin_glue_use_tail=True, skin_glue_add_constraint="COPY_LOCATION_OWNER", skin_glue_add_constraint_influence=0.1, skin_glue_tail_reparent=True),
                b_collection="MCH"
            )
        ),
    ]
)

HAIR = BoneGroup(
    name="Hair",
    transform_link=[],
    bones=[
        RegexBoneGroup(
            name="Hair",
            pattern=r"^j_ex_h.*",
            parent="Head",
            extension_size_factor=10.0,
            is_connected=False,
            req_bones=[],
            b_collection="Hair",
        ),
        RegexBoneGroup(
            name="Kami",
            pattern=r"^j_kami.*",
            parent="Head",
            extension_size_factor=10.0,
            is_connected=False,
            req_bones=[],
            b_collection="Hair",
        ),
        RegexBoneGroup(
            name="Accessory",
            pattern=r"^j_ex_met.*",
            parent="Head",
            extension_size_factor=10.0,
            is_connected=False,
            req_bones=[],
            b_collection="Accessory",
        )
    ]
)


BG_PLAYER_SFW = {
            "spine": [SPINE],
            "arm_r": [ARM_R],
            "arm_l": [ARM_L],
            "leg_r": [LEG_R],
            "leg_l": [LEG_L],
            "skirt_r": [SKIRT_R],   
            "skirt_l": [SKIRT_L],
            "hand_r": [IV_HAND_R, HAND_R],
            "hand_l": [IV_HAND_L, HAND_L],
            "tail": [TAIL],
            "head": [HEAD],
            "viera": [VIERA_EARS],
            "left_eye": [LEFT_EYE],
            "right_eye": [RIGHT_EYE],
            "brow": [BROW],
            "hair": [HAIR],
        }