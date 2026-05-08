from ......core.generators import ConnectBone, ExtensionBone
from ......core.operations import ParentBoneOperation, RigifyTypeOperation, CollectionOperation
from ......core.shared import PoseOperations, BoneGroup, RigModule, TransformLink
from ......core import rigify

GENITALS_M = BoneGroup(
    name="Male Genitals",
    transform_link=[
        TransformLink(target="DEF-Penis", bone="iv_ochinko_a"),
        TransformLink(target="DEF-Penis.001", bone="iv_ochinko_b"),
        TransformLink(target="DEF-Penis.002", bone="iv_ochinko_c"),
        TransformLink(target="DEF-Penis.003", bone="iv_ochinko_d"),
        TransformLink(target="DEF-Penis.004", bone="iv_ochinko_e"),
        TransformLink(target="DEF-Penis.005", bone="iv_ochinko_f"),
        TransformLink(target="DEF-Testicle.R", bone="iv_kougan_r"),
        TransformLink(target="DEF-Testicle.L", bone="iv_kougan_l")
    ],
    generators=[
        ConnectBone(
            name="Penis",
            bone_a="iv_ochinko_a",
            bone_b="iv_ochinko_b",
            parent=["Spine.001", "j_kosi"],
            is_connected=False,
            req_bones=["iv_ochinko_a", "iv_ochinko_b"],
            operations=[
                RigifyTypeOperation(bone_name="Penis", rigify_type=rigify.types.skin_stretchy_chain()),
                CollectionOperation(bone_name="Penis", collection_name="Genitals (Male)")
            ]
        ),
        ConnectBone(
            name="Penis.001",
            bone_a="iv_ochinko_b",
            bone_b="iv_ochinko_c",
            parent="Penis",
            is_connected=True,
            req_bones=["iv_ochinko_b", "iv_ochinko_c"],
            operations=[
                CollectionOperation(bone_name="Penis.001", collection_name="Genitals (Male)")
            ]
        ),
        ConnectBone(
            name="Penis.002",
            bone_a="iv_ochinko_c",
            bone_b="iv_ochinko_d",
            parent="Penis.001",
            is_connected=True,
            req_bones=["iv_ochinko_c", "iv_ochinko_d"],
            operations=[
                CollectionOperation(bone_name="Penis.002", collection_name="Genitals (Male)")
            ],
        ),
        ConnectBone(
            name="Penis.003",
            bone_a="iv_ochinko_d",
            bone_b="iv_ochinko_e",
            parent="Penis.002",
            is_connected=True,
            req_bones=["iv_ochinko_d", "iv_ochinko_e"],
            operations=[
                CollectionOperation(bone_name="Penis.003", collection_name="Genitals (Male)")
            ]
        ),
        ConnectBone(
            name="Penis.004",
            bone_a="iv_ochinko_e",
            bone_b="iv_ochinko_f",
            parent="Penis.003",
            is_connected=True,
            req_bones=["iv_ochinko_e", "iv_ochinko_f"],
            operations=[
                CollectionOperation(bone_name="Penis.004", collection_name="Genitals (Male)")
            ],
        ),
        ExtensionBone(
            name="Penis.005",
            bone_a="iv_ochinko_f",
            parent="Penis.004",
            is_connected=True,
            req_bones=["iv_ochinko_f"],
            operations=[
                CollectionOperation(bone_name="Penis.005", collection_name="Genitals (Male)")
            ]
        ),
        ExtensionBone(
            name="Testicle.R",
            bone_a="iv_kougan_r",
            parent=["Spine.001", "j_kosi"],
            is_connected=False,
            start="head",
            size_factor=0.5,
            req_bones=["iv_kougan_r"],
            operations=[
                RigifyTypeOperation(bone_name="Testicle.R", rigify_type=rigify.types.skin_basic_chain(skin_control_orientation_bone="Spine.001")),
                CollectionOperation(bone_name="Testicle.R", collection_name="Genitals (Male)")
            ]
        ),
        ExtensionBone(
            name="Testicle.L",
            bone_a="iv_kougan_l",
            parent=["Spine.001", "j_kosi"],
            is_connected=False,
            start="head",
            size_factor=0.5,
            req_bones=["iv_kougan_l"],
            operations=[
                RigifyTypeOperation(bone_name="Testicle.L", rigify_type=rigify.types.skin_basic_chain(skin_control_orientation_bone="Spine.001")),
                CollectionOperation(bone_name="Testicle.L", collection_name="Genitals (Male)")
            ]
        )
    ]
)

def get_rig_module() -> RigModule:
    rig_module = RigModule(
        name="IVCS Male",
        type="Generation",
        bone_groups=[GENITALS_M]
    )
    return rig_module