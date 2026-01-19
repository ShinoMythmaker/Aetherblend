from ..bone_gen import ConnectBone, ExtensionBone, PoseOperations, BoneGroup
from .. import rigify

# Individual bone list (for backwards compatibility and direct access)
ARM_R = BoneGroup(
        name="Right Arm",
        description="Right arm bones including upper arm, forearm, hand, and tweak bones",
        #linking = link(target="DEF-upper_arm.R", bone="MCH-j_ude_a_r", retarget="FK-upper_arm.R"),
        bones = [
            # Right Arm
            ConnectBone(
                name="upper_arm.R", 
                bone_a="j_ude_a_r", 
                bone_b="j_ude_b_r", 
                parent="clavicle.R",
                req_bones=["j_ude_a_r", "j_ude_b_r"],
                pose_operations=PoseOperations(
                    rigify_settings=rigify.types.limbs_arm(bone_name="upper_arm.R", fk_coll="Arm.R (FK)", tweak_coll="Arm.R (Tweak)"), 
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
                    rigify_settings=rigify.types.basic_super_copy(bone_name="wrist.R", widget_type="sphere"),
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
                    rigify_settings=rigify.types.basic_super_copy(bone_name="elbow.R", widget_type="sphere"),
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
                    rigify_settings=rigify.types.basic_super_copy(bone_name="shoulder_tweak.R", widget_type="sphere"),
                    b_collection="Arm.R (Tweak)"
                )
            ),
        ]
    )

