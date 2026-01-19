from ..bone_gen import ConnectBone, ExtensionBone, PoseOperations, BoneGroup, link
from .. import rigify

# Individual bone list (for backwards compatibility and direct access)
ARM_R = BoneGroup(
        name="Right Arm",
        description="Right arm bones including upper arm, forearm, hand, and tweak bones",
        linking = [
            link(target="DEF-upper_arm.R", bone="j_ude_a_r", retarget="FK-upper_arm.R"),
            link(target="DEF-forearm.R", bone="j_ude_b_r", retarget="FK-forearm.R"),
            link(target="DEF-hand.R", bone="j_te_r", retarget="FK-hand.R"),
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
                    b_collection="Arm.R (IK)"  #b_collection should be a class
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
                bone_a="forearm.R", 
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
            ExtensionBone(
                name="wrist.R", 
                bone_a="n_hte_r", 
                size_factor=1, 
                axis_type="local", 
                axis="Y", 
                start="head", 
                parent="hand.R", 
                is_connected=False, 
                req_bones=["n_hte_r"],
                pose_operations=PoseOperations(
                    rigify_settings=rigify.types.basic_super_copy(widget_type="sphere"),
                    b_collection="Arm.R (Tweak)"
                )
            ),
            ExtensionBone(
                name="elbow.R", 
                bone_a="n_hhiji_r", 
                axis_type="local", 
                axis="Y", 
                start="head", 
                parent="forearm.R", 
                is_connected=False, 
                size_factor=0.5, 
                roll=45,
                req_bones=["n_hhiji_r"],
                pose_operations=PoseOperations(
                    rigify_settings=rigify.types.basic_super_copy(widget_type="sphere"),
                    b_collection="Arm.R (Tweak)"
                )
            ),
            ExtensionBone(
                name="shoulder_tweak.R", 
                bone_a="n_hkata_r", 
                axis_type="local", 
                axis="Y", 
                start="head", 
                parent="upper_arm.R", 
                is_connected=False, 
                size_factor=0.5, 
                roll=45,
                req_bones=["n_hkata_r"],
                pose_operations=PoseOperations(
                    rigify_settings=rigify.types.basic_super_copy(widget_type="sphere"),
                    b_collection="Arm.R (Tweak)"
                )
            ),
        ]
    )

ARM_L = BoneGroup(
        name="Left Arm",
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
                bone_a="forearm.L", 
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
            ExtensionBone(
                name="wrist.L", 
                bone_a="n_hte_l", 
                size_factor=1, 
                axis_type="local", 
                axis="Y", 
                start="head", 
                parent="hand.L", 
                is_connected=False, 
                req_bones=["n_hte_l"],
                pose_operations=PoseOperations(
                    rigify_settings=rigify.types.basic_super_copy(widget_type="sphere"),
                    b_collection="Arm.L (Tweak)"
                )
            ),
            ExtensionBone(
                name="elbow.L", 
                bone_a="n_hhiji_l", 
                axis_type="local", 
                axis="Y", 
				start = "head",
				parent = "forearm.L",
				is_connected = False,
				size_factor = 0.5,
				roll = 45,
				req_bones = ["n_hhiji_l"],
				pose_operations = PoseOperations(
					rigify_settings = rigify.types.basic_super_copy(widget_type = "sphere"),
					b_collection = "Arm.L (Tweak)"
				)
			),
			ExtensionBone(
				name = "shoulder_tweak.L",
				bone_a = "n_hkata_l",
				axis_type = "local",
				axis = "Y",
				start = "head",
				parent = "upper_arm.L",
				is_connected = False,
				size_factor = 0.5,
				roll = 45,
				req_bones = ["n_hkata_l"],
				pose_operations = PoseOperations(
					rigify_settings = rigify.types.basic_super_copy(widget_type ="sphere"),
					b_collection ="Arm.L (Tweak)"
				)
			),
        ],
        description ="Left arm bones including the clavicle, upper arm, forearm, hand, and tweak bones"
    )

SPINE = BoneGroup(
        name="Spine",
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
                    rigify_settings=rigify.types.spines_basic_spine(fk_coll="Spine (FK)", tweak_coll="Spine (Tweak)", pivot_pos=1),
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
        bones = [
            # Right Leg
            ConnectBone(
                name="thigh.R", 
                bone_a="j_asi_a_r",
                bone_b="j_asi_c_r",
                parent="Spine.001",
                req_bones=["j_asi_a_r", "j_asi_c_r"],
                pose_operations=PoseOperations(
                    rigify_settings=rigify.types.limbs_leg(),
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
        bones = [
            # Left Leg
            ConnectBone(
                name="thigh.L", 
                bone_a="j_asi_a_l",
                bone_b="j_asi_c_l",
                parent="Spine.001",
                req_bones=["j_asi_a_l", "j_asi_c_l"],
                pose_operations=PoseOperations(
                    rigify_settings=rigify.types.limbs_leg(),
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
        bones = [
            ConnectBone(
                name="Skirt_Front.R",
                bone_a="j_sk_f_a_r",
                bone_b="j_sk_f_b_r",
                parent="Spine.001",
                is_connected=False,
                req_bones=["j_sk_f_a_r", "j_sk_f_b_r"],
                pose_operations=PoseOperations(
                    rigify_settings=rigify.types.skin_stretchy_chain(skin_chain_pivot_pos=1),
                    b_collection="Skirt"
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
        ],
)
            
