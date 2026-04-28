from ......core.generators import ConnectBone, ExtensionBone
from ......core.operations import ParentBoneOperation, RigifyTypeOperation, CollectionOperation
from ......core.shared import PoseOperations, BoneGroup, RigModule, TransformLink
from ......core import rigify
from ......core.rigify.settings import UI_Collections, BoneCollection

GENITALS_F = BoneGroup(
    name="Female Genitals",
    transform_link=[
        TransformLink(target="DEF-Clitoris", bone="iv_kuritto"),
        TransformLink(target="DEF-Vulva.R", bone="iv_inshin_r"),
        TransformLink(target="DEF-Vulva.L", bone="iv_inshin_l"),
        TransformLink(target="DEF-Vulva", bone="iv_omanko"),
    ],
    generators=[
        ConnectBone(
            name="Clitoris",
            bone_a="iv_kuritto",
            bone_b="j_kosi",
            parent=["Spine.001", "j_kosi"],
            is_connected=False,
            req_bones=["iv_kuritto", "j_kosi"],
            operations=[
                RigifyTypeOperation(bone_name="Clitoris", rigify_type=rigify.types.skin_basic_chain(skin_control_orientation_bone="Spine.001")),
                CollectionOperation(bone_name="Clitoris", collection_name="Genitals (Female)")
                ]
        ),
        ConnectBone(
            name="Vulva.R",
            bone_a="iv_inshin_r",
            bone_b="j_kosi",
            parent="Spine.001",
            is_connected=False,
            req_bones=["iv_inshin_r", "j_kosi"],
            operations=[
                RigifyTypeOperation(bone_name="Vulva.R", rigify_type=rigify.types.skin_basic_chain(skin_control_orientation_bone="Spine.001")),
                CollectionOperation(bone_name="Vulva.R", collection_name="Genitals (Female)")
            ]
        ),
        ConnectBone(
            name="Vulva.L",
            bone_a="iv_inshin_l",
            bone_b="j_kosi",
            parent="Spine.001",
            is_connected=False,
            req_bones=["iv_inshin_l", "j_kosi"],
            operations=[
                RigifyTypeOperation(bone_name="Vulva.L", rigify_type=rigify.types.skin_basic_chain(skin_control_orientation_bone="Spine.001")),
                CollectionOperation(bone_name="Vulva.L", collection_name="Genitals (Female)")
            ]
        ),
        ConnectBone(
            name="Vulva",
            bone_a="iv_omanko",
            bone_b="j_kosi",
            parent="Spine.001",
            is_connected=False,
            req_bones=["iv_omanko", "j_kosi"],
            operations=[
                RigifyTypeOperation(bone_name="Vulva", rigify_type=rigify.types.skin_basic_chain(skin_control_orientation_bone="Spine.001")),
                CollectionOperation(bone_name="Vulva", collection_name="Genitals (Female)")
            ]
        ),
        ExtensionBone(
            name="Anchor_V",
            bone_a="Clitoris",
            parent="Spine.001",
            is_connected=False,
            start="tail",
            req_bones=["Clitoris"],
            operations=[
                RigifyTypeOperation(bone_name="Anchor_V", rigify_type=rigify.types.skin_anchor(skin_anchor_hide=True)),
                CollectionOperation(bone_name="Anchor_V", collection_name="Genitals (Female)")
            ]
        )
    ]
)

def get_rig_module() -> RigModule:
    return RigModule(
        name="IVCS Female",
        type="Generation",
        bone_groups=[GENITALS_F],
        ui = UI_Collections([
            BoneCollection(name="Genitals (Female)", ui=True, color_set="IVCS", row_index=1, title="Genitals (Female)", visible=False),
        ])
    )