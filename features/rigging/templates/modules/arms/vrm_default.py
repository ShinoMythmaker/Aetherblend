from ......core.rigify.settings import UI_Collections, BoneCollection
from ......core.operations import BoneRestrictionOperation, ParentBoneOperation, ConstraintOperation, CollectionOperation, PropOverrideOperation, RigifyTypeOperation, DriverOperation, WidgetOperation
from ......core.bone_generators import ConnectBone, ExtensionBone, CopyBone
from ......core.shared import PoseOperations, BoneGroup, TransformLink, RigModule
from ......core import rigify
from ......core.drivers import TransformChannelVariable, Driver, SinglePropertyVariable

ARM_R = BoneGroup(
        name="Right Arm",
        description="Right arm bones including upper arm, forearm, hand, and tweak bones",
        transform_link = [
            TransformLink(target="DEF-upper_arm.R", bone="J_Bip_R_UpperArm", retarget="FK-upper_arm.R"),
            TransformLink(target="DEF-forearm.R", bone="J_Bip_R_LowerArm", retarget="FK-forearm.R"),
            TransformLink(target="DEF-hand.R", bone="J_Bip_R_Hand", retarget="FK-hand.R"),
            TransformLink(target="DEF-clavicle.R", bone="J_Bip_R_Shoulder"),
            ],
        generators = [
            #Right Clavicle
            CopyBone(
                name="clavicle.R",
                bone_a="J_Bip_R_Shoulder",
                req_bones=["J_Bip_R_Shoulder"],
                parent="Spine.004",
                operations=[ParentBoneOperation(time="Pre", bone_name="clavicle.R", parent=["Spine.004", "J_Bip_C_Chest"], is_connected=False), 
                    RigifyTypeOperation(time="Pre", bone_name="clavicle.R", rigify_type=rigify.types.basic_super_copy(widget_type="shoulder")), 
                    CollectionOperation(time="Pre", bone_name="clavicle.R", collection_name="Torso")
                ]
            ),
            # Right Arm
            CopyBone(
                name="upper_arm.R", 
                bone_a="J_Bip_R_UpperArm", 
                parent="clavicle.R",
                req_bones=["J_Bip_R_UpperArm"],
                operations=[
                    RigifyTypeOperation(time="Pre", bone_name="upper_arm.R", rigify_type=rigify.types.limbs_arm(rotation_axis="z", auto_align_extremity=True, fk_coll="Arm.R (FK)", tweak_coll="Arm.R (Tweak)")), 
                    CollectionOperation(time="Pre", bone_name="upper_arm.R", collection_name="Arm.R (IK)")
                ]
            ),
            CopyBone(
                name="forearm.R", 
                bone_a="J_Bip_R_LowerArm", 
                parent="upper_arm.R",
                is_connected=True,
                req_bones=["J_Bip_R_LowerArm"],
                operations=[
                    CollectionOperation(time="Pre", bone_name="forearm.R", collection_name="Arm.R (IK)")
                ]
            ),
            CopyBone(
                name="hand.R", 
                bone_a="J_Bip_R_Hand", 
                parent="forearm.R",
                is_connected=True,
                req_bones=["J_Bip_R_Hand"],
                operations=[
                    CollectionOperation(time="Pre", bone_name="hand.R", collection_name="Arm.R (IK)")
                ]
            ),
        ]
    )

ARM_L = BoneGroup(
        name="Left Arm",
        description="Left arm bones including upper arm, forearm, hand, and tweak bones",
        transform_link = [
            TransformLink(target="DEF-upper_arm.L", bone="J_Bip_L_UpperArm", retarget="FK-upper_arm.L"),
            TransformLink(target="DEF-forearm.L", bone="J_Bip_L_LowerArm", retarget="FK-forearm.L"),
            TransformLink(target="DEF-hand.L", bone="J_Bip_L_Hand", retarget="FK-hand.L"),
            TransformLink(target="DEF-clavicle.L", bone="J_Bip_L_Shoulder"),
            ],
        generators = [
            #Left Clavicle
            CopyBone(
                name="clavicle.L",
                bone_a="J_Bip_L_Shoulder",
                req_bones=["J_Bip_L_Shoulder"],
                parent="Spine.004",
                operations=[ParentBoneOperation(time="Pre", bone_name="clavicle.L", parent=["Spine.004", "J_Bip_C_Chest"], is_connected=False), 
                    RigifyTypeOperation(time="Pre", bone_name="clavicle.L", rigify_type=rigify.types.basic_super_copy(widget_type="shoulder")), 
                    CollectionOperation(time="Pre", bone_name="clavicle.L", collection_name="Torso")
                ]
            ),
            # Left Arm
            CopyBone(
                name="upper_arm.L", 
                bone_a="J_Bip_L_UpperArm", 
                parent="clavicle.L",
                req_bones=["J_Bip_L_UpperArm"],
                operations=[
                    RigifyTypeOperation(time="Pre", bone_name="upper_arm.L", rigify_type=rigify.types.limbs_arm(rotation_axis="z", auto_align_extremity=True, fk_coll="Arm.L (FK)", tweak_coll="Arm.L (Tweak)")), 
                    CollectionOperation(time="Pre", bone_name="upper_arm.L", collection_name="Arm.L (IK)")
                ]
            ),
            CopyBone(
                name="forearm.L", 
                bone_a="J_Bip_L_LowerArm", 
                parent="upper_arm.L",
                is_connected=True,
                req_bones=["J_Bip_L_LowerArm"],
                operations=[
                    CollectionOperation(time="Pre", bone_name="forearm.L", collection_name="Arm.L (IK)")
                ]
            ),
            CopyBone(
                name="hand.L", 
                bone_a="J_Bip_L_Hand", 
                parent="forearm.L",
                is_connected=True,
                req_bones=["J_Bip_L_Hand"],
                operations=[
                    CollectionOperation(time="Pre", bone_name="hand.L", collection_name="Arm.L (IK)")
                ]
            ),
        ]
    )

def get_rig_module() -> RigModule:
    return RigModule(
        name="VRM-Default",
        type="Generation",
        bone_groups=[ARM_L, ARM_R],
        ui_collections = UI_Collections([
            BoneCollection(name="Arm.L (IK)", ui=True, color_set="IK_Left", row_index=1, title="Arm IK.L"),
            BoneCollection(name="Arm.L (FK)", ui=True, color_set="FK_Left", row_index=2, title="Arm FK.L", visible=False),
            BoneCollection(name="Arm.R (IK)", ui=True, color_set="IK_Right", row_index=1, title="Arm IK.R"),
            BoneCollection(name="Arm.R (FK)", ui=True, color_set="FK_Right", row_index=2, title="Arm FK.R", visible=False),
        ]),
        operations=[
            PropOverrideOperation(bone_name="upper_arm_parent.L", property_name="IK_Stretch", value=0),
            PropOverrideOperation(bone_name="upper_arm_parent.R", property_name="IK_Stretch", value=0),

            WidgetOperation(bone_name="hand_ik.L", scale=(2,2,2)),
            WidgetOperation(bone_name="hand_ik.R", scale=(2,2,2)),

            BoneRestrictionOperation(time="Post", bone_name="upper_arm_tweak.L", hide_select=True, hide=True),
            BoneRestrictionOperation(time="Post", bone_name="upper_arm_tweak.R", hide_select=True, hide=True),
            BoneRestrictionOperation(time="Post", bone_name="upper_arm_tweak.L.001", hide_select=True, hide=True),
            BoneRestrictionOperation(time="Post", bone_name="upper_arm_tweak.R.001", hide_select=True, hide=True),
            BoneRestrictionOperation(time="Post", bone_name="forearm_tweak.L", hide_select=True, hide=True),
            BoneRestrictionOperation(time="Post", bone_name="forearm_tweak.R", hide_select=True, hide=True),
            BoneRestrictionOperation(time="Post", bone_name="forearm_tweak.L.001", hide_select=True, hide=True),
            BoneRestrictionOperation(time="Post", bone_name="forearm_tweak.R.001", hide_select=True, hide=True),
            BoneRestrictionOperation(time="Post", bone_name="hand_tweak.L", hide_select=True, hide=True),
            BoneRestrictionOperation(time="Post", bone_name="hand_tweak.R", hide_select=True, hide=True),
        ]
    )
    