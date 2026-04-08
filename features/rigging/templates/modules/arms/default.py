from ......core.rigify.settings import UI_Collections, BoneCollection

from ......core.generators import ConnectBone, ExtensionBone
from ......core.shared import PoseOperations, BoneGroup, TransformLink, RigModule
from ......core import rigify

ARM_R = BoneGroup(
        name="Right Arm",
        description="Right arm bones including upper arm, forearm, hand, and tweak bones",
        transform_link = [
            TransformLink(target="DEF-upper_arm.R", bone="j_ude_a_r", retarget="FK-upper_arm.R"),
            TransformLink(target="DEF-forearm.R", bone="j_ude_b_r", retarget="FK-forearm.R"),
            TransformLink(target="DEF-hand.R", bone="j_te_r", retarget="FK-hand.R"),
            TransformLink(target="DEF-clavicle.R", bone="j_sako_r"),
            TransformLink(target="DEF-forearm.R.001", bone="n_hte_r"),
            TransformLink(target="DEF-elbow.R", bone="n_hhiji_r")
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
            ExtensionBone(
                name="elbow.R",
                bone_a="n_hhiji_r",
                size_factor=0.5,
                axis_type="local",
                axis="Y",
                start="head",
                parent="forearm.R",
                is_connected=False,
                req_bones=["n_hhiji_r"],
                pose_operations=PoseOperations(
                    rigify_settings=rigify.types.basic_super_copy(widget_type="pivot_cross"),
                    b_collection="Arm.R (Tweak)"
                )
            )
        ]
    )

ARM_L = BoneGroup(
        name="Left Arm",
        transform_link= [
            TransformLink(target="DEF-upper_arm.L", bone="j_ude_a_l", retarget="FK-upper_arm.L"),
            TransformLink(target="DEF-forearm.L", bone="j_ude_b_l", retarget="FK-forearm.L"),
            TransformLink(target="DEF-hand.L", bone="j_te_l", retarget="FK-hand.L"),
            TransformLink(target="DEF-clavicle.L", bone="j_sako_l"),
            TransformLink(target="DEF-forearm.L.001", bone="n_hte_l"),
            TransformLink(target="DEF-elbow.L", bone="n_hhiji_l")
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
            ExtensionBone(
                name="elbow.L",
                bone_a="n_hhiji_l",
                size_factor=0.5,
                axis_type="local",
                axis="Y",
                start="head",
                parent="forearm.L",
                is_connected=False,
                req_bones=["n_hhiji_l"],
                pose_operations=PoseOperations(
                    rigify_settings=rigify.types.basic_super_copy(widget_type="pivot_cross"),
                    b_collection="Arm.L (Tweak)"
                )
            )
        ],
        description ="Left arm bones including the clavicle, upper arm, forearm, and hand bones."
    )

def get_rig_module() -> RigModule:
    return RigModule(
        name="Default",
        type="Generation",
        bone_groups=[ARM_L, ARM_R],
        ui = UI_Collections([
            BoneCollection(name="Arm.L (IK)", ui=True, color_set="IK_Left", row_index=1, title="Arm IK.L"),
            BoneCollection(name="Arm.L (FK)", ui=True, color_set="FK_Left", row_index=2, title="Arm FK.L", visible=False),
            BoneCollection(name="Arm.L (Tweak)", ui=True, color_set="Tweak_Left", row_index=3, title="Tweak.L", visible=False),
            BoneCollection(name="Arm.R (IK)", ui=True, color_set="IK_Right", row_index=1, title="Arm IK.R"),
            BoneCollection(name="Arm.R (FK)", ui=True, color_set="FK_Right", row_index=2, title="Arm FK.R", visible=False),
            BoneCollection(name="Arm.R (Tweak)", ui=True, color_set="Tweak_Right", row_index=3, title="Tweak.R", visible=False),
        ])
    )
    