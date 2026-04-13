from ......core.generators import ConnectBone, ExtensionBone
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
            parent="Spine.001",
            is_connected=False,
            req_bones=["iv_ochinko_a", "iv_ochinko_b"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_stretchy_chain(skin_control_orientation_bone="Spine.001"),
                b_collection="Genitals (Male)"
            )
        ),
        ConnectBone(
            name="Penis.001",
            bone_a="iv_ochinko_b",
            bone_b="iv_ochinko_c",
            parent="Penis",
            is_connected=True,
            req_bones=["iv_ochinko_b", "iv_ochinko_c"],
            pose_operations=PoseOperations(
                b_collection="Genitals (Male)"
            )
        ),
        ConnectBone(
            name="Penis.002",
            bone_a="iv_ochinko_c",
            bone_b="iv_ochinko_d",
            parent="Penis.001",
            is_connected=True,
            req_bones=["iv_ochinko_c", "iv_ochinko_d"],
            pose_operations=PoseOperations(
                b_collection="Genitals (Male)"
            )
        ),
        ConnectBone(
            name="Penis.003",
            bone_a="iv_ochinko_d",
            bone_b="iv_ochinko_e",
            parent="Penis.002",
            is_connected=True,
            req_bones=["iv_ochinko_d", "iv_ochinko_e"],
            pose_operations=PoseOperations(
                b_collection="Genitals (Male)"
            )
        ),
        ConnectBone(
            name="Penis.004",
            bone_a="iv_ochinko_e",
            bone_b="iv_ochinko_f",
            parent="Penis.003",
            is_connected=True,
            req_bones=["iv_ochinko_e", "iv_ochinko_f"],
            pose_operations=PoseOperations(
                b_collection="Genitals (Male)"
            )
        ),
        ExtensionBone(
            name="Penis.005",
            bone_a="iv_ochinko_f",
            parent="Penis.004",
            is_connected=True,
            req_bones=["iv_ochinko_f"],
            pose_operations=PoseOperations(
                b_collection="Genitals (Male)"
            )
        ),
        ExtensionBone(
            name="Testicle.R",
            bone_a="iv_kougan_r",
            parent="Spine.001",
            is_connected=False,
            start="head",
            size_factor=0.5,
            req_bones=["iv_kougan_r"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(skin_control_orientation_bone="Spine.001"),
                b_collection="Genitals (Male)"
            )
        ),
        ExtensionBone(
            name="Testicle.L",
            bone_a="iv_kougan_l",
            parent="Spine.001",
            is_connected=False,
            start="head",
            size_factor=0.5,
            req_bones=["iv_kougan_l"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(skin_control_orientation_bone="Spine.001"),
                b_collection="Genitals (Male)"
            )
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