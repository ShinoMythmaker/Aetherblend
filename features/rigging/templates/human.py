import bpy
import mathutils

from ....core.generators import ConnectBone, ExtensionBone, SkinBone, BridgeBone, CenterBone, CopyBone
from ....core.shared import PoseOperations, BoneGroup, link
from ....core import rigify

# Individual bone list (for backwards compatibility and direct access)
ARM_R = BoneGroup(
        name="Right Arm",
        description="Right arm bones including upper arm, forearm, hand, and tweak bones",
        linking = [
            link(target="DEF-upper_arm.R", bone="j_ude_a_r", retarget="FK-upper_arm.R"),
            link(target="DEF-forearm.R", bone="j_ude_b_r", retarget="FK-forearm.R"),
            link(target="DEF-hand.R", bone="j_te_r", retarget="FK-hand.R"),
            link(target="DEF-forearm.R.001", bone="n_hte_r")
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
        linking= [
            link(target="DEF-upper_arm.L", bone="j_ude_a_l", retarget="FK-upper_arm.L"),
            link(target="DEF-forearm.L", bone="j_ude_b_l", retarget="FK-forearm.L"),
            link(target="DEF-hand.L", bone="j_te_l", retarget="FK-hand.L"),
            link(target="DEF-forearm.L.001", bone="n_hte_l")
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
        linking= [
            link(target="DEF-Spine.001", bone="j_kosi", retarget="FK-Spine.001"),
            link(target="DEF-Spine.002", bone="j_sebo_a", retarget="FK-Spine.002"),
            link(target="DEF-Spine.003", bone="j_sebo_b", retarget="FK-Spine.003"),
            link(target="DEF-Spine.004", bone="j_sebo_c", retarget="FK-Spine.004"),
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
        ],
)

LEG_R = BoneGroup(
        name="Right Leg",
        linking= [
            link(target="DEF-thigh.R.001", bone="j_asi_a_r", retarget="FK-upper_leg.R"),
            link(target="DEF-shin.R.001", bone="j_asi_c_r", retarget="FK-lower_leg.R"),
            link(target="DEF-foot.R", bone="j_asi_d_r", retarget="FK-foot.R"),
            link(target="DEF-toe.R", bone="j_asi_e_r", retarget="FK-toe.R"),
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
                axis="X",
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
                axis="X",
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
        linking= [
            link(target="DEF-thigh.L.001", bone="j_asi_a_l", retarget="FK-upper_leg.L"),
            link(target="DEF-shin.L.001", bone="j_asi_c_l", retarget="FK-lower_leg.L"),
            link(target="DEF-foot.L", bone="j_asi_d_l", retarget="FK-foot.L"),
            link(target="DEF-toe.L", bone="j_asi_e_l", retarget="FK-toe.L"),
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
                axis="Z",
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
                axis="Z",
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
        linking= [
            link(target="DEF-Skirt_Front.R", bone="j_sk_f_a_r"),
            link(target="DEF-Skirt_Front.R.001", bone="j_sk_f_b_r"),
            link(target="DEF-Skirt_Front.R.002", bone="j_sk_f_c_r"),
            link(target="DEF-Skirt_Side.R", bone="j_sk_s_a_r"),
            link(target="DEF-Skirt_Side.R.001", bone="j_sk_s_b_r"),
            link(target="DEF-Skirt_Side.R.002", bone="j_sk_s_c_r"),
            link(target="DEF-Skirt_Back.R", bone="j_sk_b_a_r"),
            link(target="DEF-Skirt_Back.R.001", bone="j_sk_b_b_r"),
            link(target="DEF-Skirt_Back.R.002", bone="j_sk_b_c_r"),
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
        ],
)
            
SKIRT_R_MCH = BoneGroup(
        name="Skirt Right MCH",
        bones= [
            #Front
            ConnectBone(
                name="Skirt_Front.R.mch",
                bone_a="shin.R",
                bone_b="Skirt_Front.R.002",
                parent="shin.R",
                is_connected=False,
                end="tail",
                req_bones=["shin.R", "Skirt_Front.R.002"],
                pose_operations=PoseOperations(
                    rigify_settings=rigify.types.skin_basic_chain(skin_chain_priority=1, skin_control_orientation_bone="Skirt_Front.R.002"),
                    b_collection="Skirt MCH"
                )
            ),
            #Side
            ConnectBone(
                name="Skirt_Side.R.mch",
                bone_a="shin.R",
                bone_b="Skirt_Side.R.002",
                parent="shin.R",
                is_connected=False,
                end="tail",
                req_bones=["shin.R", "Skirt_Side.R.002"],
                pose_operations=PoseOperations(
                    rigify_settings=rigify.types.skin_basic_chain(skin_chain_priority=1, skin_control_orientation_bone="Skirt_Side.R.002"),
                    b_collection="Skirt MCH"
                )
            ),
            #Back
            ConnectBone(
                name="Skirt_Back.R.mch",
                bone_a="shin.R",
                bone_b="Skirt_Back.R.002",
                parent="shin.R",
                is_connected=False,
                end="tail",
                req_bones=["shin.R", "Skirt_Back.R.002"],
                pose_operations=PoseOperations(
                    rigify_settings=rigify.types.skin_basic_chain(skin_chain_priority=1, skin_control_orientation_bone="Skirt_Back.R.002"),
                    b_collection="Skirt MCH"
                )
            ),
        ],
)

SKIRT_L = BoneGroup(
        name="Skirt Left",
        linking= [
            link(target="DEF-Skirt_Front.L", bone="j_sk_f_a_l"),
            link(target="DEF-Skirt_Front.L.001", bone="j_sk_f_b_l"),
            link(target="DEF-Skirt_Front.L.002", bone="j_sk_f_c_l"),
            link(target="DEF-Skirt_Side.L", bone="j_sk_s_a_l"),
            link(target="DEF-Skirt_Side.L.001", bone="j_sk_s_b_l"),
            link(target="DEF-Skirt_Side.L.002", bone="j_sk_s_c_l"),
            link(target="DEF-Skirt_Back.L", bone="j_sk_b_a_l"),
            link(target="DEF-Skirt_Back.L.001", bone="j_sk_b_b_l"),
            link(target="DEF-Skirt_Back.L.002", bone="j_sk_b_c_l"),
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
        ],
)

SKIRT_L_MCH = BoneGroup(
        name="Skirt Left MCH",
        bones= [
            #Front
            ConnectBone(
                name="Skirt_Front.L.mch",
                bone_a="shin.L",
                bone_b="Skirt_Front.L.002",
                parent="shin.L",
                is_connected=False,
                end="tail",
                req_bones=["shin.L", "Skirt_Front.L.002"],
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
                req_bones=["shin.L", "Skirt_Side.L.002"],
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
                req_bones=["shin.L", "Skirt_Back.L.002"],
                pose_operations=PoseOperations(
                    rigify_settings=rigify.types.skin_basic_chain(skin_chain_priority=1, skin_control_orientation_bone="Skirt_Back.L.002"),
                    b_collection="Skirt MCH"
                )
            ),
        ],
)

HAND_R = BoneGroup(
    name="Right Hand",
    linking= [
        link(target="DEF-thumb.R", bone="j_oya_a_r"),
        link(target="DEF-thumb.R.001", bone="j_oya_b_r"),
        link(target="DEF-index.R", bone="j_hito_a_r"),
        link(target="DEF-index.R.001", bone="j_hito_b_r"),
        link(target="DEF-middle.R", bone="j_naka_a_r"),
        link(target="DEF-middle.R.001", bone="j_naka_b_r"),
        link(target="DEF-ring.R", bone="j_kusu_a_r"),
        link(target="DEF-ring.R.001", bone="j_kusu_b_r"),
        link(target="DEF-pinky.R", bone="j_ko_a_r"),
        link(target="DEF-pinky.R.001", bone="j_ko_b_r"),
    ],
    bones=[
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
            parent="hand.R",
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
        #Middle
        ConnectBone(
            name="middle.R",
            bone_a="j_naka_a_r",
            bone_b="j_naka_b_r",
            parent="hand.R",
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
        #Ring
        ConnectBone(
            name="ring.R",
            bone_a="j_kusu_a_r",
            bone_b="j_kusu_b_r",
            parent="hand.R",
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
        #Pinky
        ConnectBone(
            name="pinky.R",
            bone_a="j_ko_a_r",
            bone_b="j_ko_b_r",
            parent="hand.R",
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
    ],
)

HAND_L = BoneGroup(
    name="Left Hand",
    linking= [
        link(target="DEF-thumb.L", bone="j_oya_a_l"),
        link(target="DEF-thumb.L.001", bone="j_oya_b_l"),
        link(target="DEF-index.L", bone="j_hito_a_l"),
        link(target="DEF-index.L.001", bone="j_hito_b_l"),
        link(target="DEF-middle.L", bone="j_naka_a_l"),
        link(target="DEF-middle.L.001", bone="j_naka_b_l"),
        link(target="DEF-ring.L", bone="j_kusu_a_l"),
        link(target="DEF-ring.L.001", bone="j_kusu_b_l"),
        link(target="DEF-pinky.L", bone="j_ko_a_l"),
        link(target="DEF-pinky.L.001", bone="j_ko_b_l"),
    ],
    bones=[
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
            parent="hand.L",
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
            parent="hand.L",
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
            parent="hand.L",
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
            parent="hand.L",
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
)

TAIL = BoneGroup(
    name="Tail",
    linking= [
        link(target="DEF-Tail", bone="n_sippo_a"),
        link(target="DEF-Tail.001", bone="n_sippo_b"),
        link(target="DEF-Tail.002", bone="n_sippo_c"),
        link(target="DEF-Tail.003", bone="n_sippo_d"),
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
    linking= [
        link(target="DEF-Neck", bone="j_kubi"),
        link(target="DEF-Head", bone="j_kao"),
        link(target="DEF-jaw_master", bone="j_f_ago"),
        link(target="DEF-Cheek.B.R", bone="j_f_shoho_r"),
        link(target="DEF-Cheek.B.R.001", bone="j_f_dhoho_r"),
        link(target="DEF-Cheek.T.R", bone="j_f_hoho_r"),
        link(target="DEF-Cheek.B.L", bone="j_f_shoho_l"),
        link(target="DEF-Cheek.B.L.001", bone="j_f_dhoho_l"),
        link(target="DEF-Cheek.T.L", bone="j_f_hoho_l"),
        link(target="DEF-Lip.T.R", bone="j_f_ulip_01_r"),
        link(target="DEF-Lip.T.R.001", bone="j_f_umlip_01_r"),
        link(target="DEF-Lip.T.R.002", bone="j_f_uslip_r"),
        link(target="DEF-Lip.B.R", bone="j_f_dlip_01_r"),
        link(target="DEF-Lip.B.R.001", bone="j_f_dmlip_01_r"),
        link(target="DEF-Lip.B.R.002", bone="j_f_dslip_r"),
        link(target="DEF-Lip.T.L", bone="j_f_ulip_01_l"),
        link(target="DEF-Lip.T.L.001", bone="j_f_umlip_01_l"),
        link(target="DEF-Lip.T.L.002", bone="j_f_uslip_l"),
        link(target="DEF-Lip.B.L", bone="j_f_dlip_01_l"),
        link(target="DEF-Lip.B.L.001", bone="j_f_dmlip_01_l"),
        link(target="DEF-Lip.B.L.002", bone="j_f_dslip_l"),
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
                b_collection="Face"
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
    ]
)

LEFT_EYE = BoneGroup(
    name="Eyes",
    linking= [
        link(target="lid.B.L.001", bone="j_f_mabdn_03in_l"),
        link(target="lid.B.L.002", bone="j_f_mabdn_01_l"),
        link(target="lid.B.L.003", bone="j_f_mabdn_02out_l"),
        link(target="lid.T.L.001", bone="j_f_mabup_02out_l"),
        link(target="lid.T.L.002", bone="j_f_mabup_01_l"),
        link(target="lid.T.L.003", bone="j_f_mabup_03in_l"),
        link(target="MCH-Eye.L", bone="j_f_eyepuru_l"),
    ],
    bones=[

        ## Skin Bone, Basicly Corner Bones for the eyes
        SkinBone(
            name="lid.T.L", 
            bone_a="j_f_mabup_02out_l", 
            mesh_restriction="eye_occlusion",
            req_bones=["j_f_mabup_02out_l"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_stretchy_chain(skin_chain_pivot_pos=2, primary_layer_extra="Face (Primary)" ,skin_control_orientation_bone="Head", skin_chain_falloff_spherical=[False, True, False], skin_chain_falloff=[0.0, -2.0, 0.0], skin_chain_falloff_length=True), 
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
                b_collection="Face"
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
        ]
)  

RIGHT_EYE = BoneGroup(
    name="Eyes",
    linking= [
        link(target="lid.B.R.001", bone="j_f_mabdn_03in_r"),
        link(target="lid.B.R.002", bone="j_f_mabdn_01_r"),
        link(target="lid.B.R.003", bone="j_f_mabdn_02out_r"),
        link(target="lid.T.R.001", bone="j_f_mabup_02out_r"),
        link(target="lid.T.R.002", bone="j_f_mabup_01_r"),
        link(target="lid.T.R.003", bone="j_f_mabup_03in_r"),
        link(target="MCH-Eye.R", bone="j_f_eyepuru_r"),
    ],
    bones=[
        ## Skin Bone, Basicly Corner Bones for the eyes
        SkinBone(
            name="lid.T.R", 
            bone_a="j_f_mabup_02out_r", 
            mesh_restriction="eye_occlusion",
            req_bones=["j_f_mabup_02out_r"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_stretchy_chain(skin_chain_pivot_pos=2, primary_layer_extra="Face (Primary)" ,skin_control_orientation_bone="Head", skin_chain_falloff_spherical=[False, True, False], skin_chain_falloff=[0.0, -2.0, 0.0], skin_chain_falloff_length=True), 
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
                b_collection="Face"
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
            offset_factor=mathutils.Vector((0.003, -0.001, -0.003)),
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
    ]
)
