from ......core.bone_generators import ConnectBone, ExtensionBone, CopyBone
from ......core.operations import ParentBoneOperation, ConstraintOperation, RigifyTypeOperation, CollectionOperation, WidgetOperation, BoneRestrictionOperation
from ......core.constraints import CopyLocationConstraint, CopyTransformsConstraint
from ......core.shared import PoseOperations, BoneGroup, TransformLink, RigModule
from ......core import rigify
from ......core.rigify.settings import UI_Collections, BoneCollection

SPINE = BoneGroup(
        name="spine",
        transform_link= [
            TransformLink(target="DEF-Spine.001", bone="J_Bip_C_Hips"),
            TransformLink(target="DEF-Spine.002", bone="J_Bip_C_Spine"),
            TransformLink(target="DEF-Spine.003", bone="J_Bip_C_Chest"),
            TransformLink(target="DEF-Spine.004", bone="J_Bip_C_UpperChest"),
            TransformLink(target="DEF-Chest.R", bone="J_Sec_R_Bust1"),
            TransformLink(target="DEF-Chest.L", bone="J_Sec_L_Bust1"),
            TransformLink(target="DEF-Chest.Tweak.R", bone="J_Sec_R_Bust2"),
            TransformLink(target="DEF-Chest.Tweak.L", bone="J_Sec_L_Bust2"),
            TransformLink(target="DEF-Neck", bone="J_Bip_C_Neck"),
            TransformLink(target="DEF-Head", bone="J_Bip_C_Head"),
        ],
        operations = [
            ## Scuffed root bone implementation ? since when has CopyTransformConstraint a BEFORE_FULL mix mode ? - Shino
            ConstraintOperation(time="Post", bone_name="Root", constraint=CopyTransformsConstraint(target_bone="root", target_space="WORLD", owner_space="WORLD", mix_mode="BEFORE_FULL", influence=1.0)),
            ## VRMs have Root and Hip bones connected ... we disconnect them kek - Shino
            ParentBoneOperation(time="Post", bone_name="J_Bip_C_Hips", parent=["Root"], is_connected=False),
        ],
        generators = [
            ##### Spine
            CopyBone(
                name="Spine.001",
                bone_a="J_Bip_C_Hips",
                is_connected=False,
                req_bones=["J_Bip_C_Hips"],
                operations=[
                            RigifyTypeOperation(time="Pre", bone_name="Spine.001", rigify_type=rigify.types.spines_basic_spine(fk_coll="Torso (Tweak)", tweak_coll="Torso (Tweak)", pivot_pos=1)),
                            CollectionOperation(time="Pre", bone_name="Spine.001", collection_name="Torso"),
                            ]
            ),
            CopyBone(
                name="Spine.002",
                bone_a="J_Bip_C_Spine",
                parent="Spine.001",
                is_connected=True,
                req_bones=["J_Bip_C_Spine"],
                operations=[
                            CollectionOperation(time="Pre", bone_name="Spine.002", collection_name="Torso"),
                            ]
            ),
            CopyBone(
                name="Spine.003",
                bone_a="J_Bip_C_Chest",
                parent="Spine.002",
                is_connected=True,
                req_bones=["J_Bip_C_Chest"],
                operations=[
                            CollectionOperation(time="Pre", bone_name="Spine.003", collection_name="Torso"),
                            ]
            ),
            CopyBone(
                name="Spine.004",
                bone_a="J_Bip_C_UpperChest",
                parent="Spine.003",
                is_connected=True,
                req_bones=["J_Bip_C_UpperChest"],
                operations=[
                            CollectionOperation(time="Pre", bone_name="Spine.004", collection_name="Torso"),
                            ]
            ),

            ##### Chest
            CopyBone(
                name="Chest.R",
                bone_a="J_Sec_R_Bust1",
                is_optional=True,
                parent="Spine.003",
                operations=[
                            RigifyTypeOperation(time="Pre", bone_name="Chest.R", rigify_type=rigify.types.basic_super_copy(widget_type="bone")),
                            CollectionOperation(time="Pre", bone_name="Chest.R", collection_name="Torso"),
                            ]
            ),
            CopyBone(
                name="Chest.Tweak.R",
                bone_a="J_Sec_R_Bust2",
                is_optional=True,
                parent="Chest.R",
                is_connected=True,
                operations=[
                            RigifyTypeOperation(time="Pre", bone_name="Chest.Tweak.R", rigify_type=rigify.types.basic_super_copy(widget_type="bone")),
                            CollectionOperation(time="Pre", bone_name="Chest.Tweak.R", collection_name="Torso"),
                            ]
            ),

            CopyBone(
                name="Chest.L",
                bone_a="J_Sec_L_Bust1",
                is_optional=True,
                parent="Spine.003",
                operations=[
                            RigifyTypeOperation(time="Pre", bone_name="Chest.L", rigify_type=rigify.types.basic_super_copy(widget_type="bone")),
                            CollectionOperation(time="Pre", bone_name="Chest.L", collection_name="Torso"),
                            ]
            ),
            CopyBone(
                name="Chest.Tweak.L",
                bone_a="J_Sec_L_Bust2",
                is_optional=True,
                parent="Chest.L",
                is_connected=True,
                operations=[
                            RigifyTypeOperation(time="Pre", bone_name="Chest.Tweak.L", rigify_type=rigify.types.basic_super_copy(widget_type="bone")),
                            CollectionOperation(time="Pre", bone_name="Chest.Tweak.L", collection_name="Torso"),
                            ]
            ),

            ##### Head
            CopyBone(
            name="Neck",
            bone_a="J_Bip_C_Neck",
            parent=["Spine.004", "J_Bip_C_UpperChest"],
            req_bones=["J_Bip_C_Neck"],
            operations=[
                        RigifyTypeOperation(time="Pre", bone_name="Neck", rigify_type=rigify.types.spines_super_head()),
                        CollectionOperation(time="Pre", bone_name="Neck", collection_name="Head"),
                ]
            ),
            CopyBone(
                name="Head",
                bone_a="J_Bip_C_Head",
                parent="Neck",
                is_connected=True,
                req_bones=["J_Bip_C_Head"],
                operations=[CollectionOperation(time="Pre", bone_name="Head", collection_name="Head")]
            ),
        ],
)

def get_rig_module() -> RigModule:
    return RigModule(
        name="VRM-Default",
        type="Generation",
        bone_groups=[SPINE],
        ui_collections = UI_Collections([
            BoneCollection(name="Head", ui=True, color_set="Head", row_index=1, title="Head"),
            BoneCollection(name="Torso", ui=True, color_set="Torso", row_index=2, title="Torso"),
        ]),
        operations = [
            BoneRestrictionOperation(time="Post", bone_name="tweak_Spine.001", hide_select=True, hide=True),
            BoneRestrictionOperation(time="Post", bone_name="tweak_Spine.002", hide_select=True, hide=True),
            BoneRestrictionOperation(time="Post", bone_name="tweak_Spine.003", hide_select=True, hide=True),
            BoneRestrictionOperation(time="Post", bone_name="tweak_Spine.004", hide_select=True, hide=True),
            BoneRestrictionOperation(time="Post", bone_name="tweak_Spine.005", hide_select=True, hide=True),

            BoneRestrictionOperation(time="Post", bone_name="tweak_Neck", hide_select=True, hide=True),
        ]
    )
    