from ......core.generators import ConnectBone, ExtensionBone
from ......core.shared import PoseOperations, BoneGroup, RigModule, TransformLink
from ......core import rigify

GENITALS_F = BoneGroup(
    name="Female Genitals",
    transform_link=[
        TransformLink(target="DEF-Clitoris", bone="iv_kuritto"),
        TransformLink(target="DEF-Vulva.R", bone="iv_inshin_r"),
        TransformLink(target="DEF-Vulva.L", bone="iv_inshin_l"),
        TransformLink(target="DEF-Vulva", bone="iv_omanko"),
    ],
    bones=[
        ConnectBone(
            name="Clitoris",
            bone_a="iv_kuritto",
            bone_b="j_kosi",
            parent="Spine.001",
            is_connected=False,
            req_bones=["iv_kuritto", "j_kosi"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(skin_control_orientation_bone="Spine.001"),
                b_collection="Genitals (Female)",
            )
        ),
        ConnectBone(
            name="Vulva.R",
            bone_a="iv_inshin_r",
            bone_b="j_kosi",
            parent="Spine.001",
            is_connected=False,
            req_bones=["iv_inshin_r", "j_kosi"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(skin_control_orientation_bone="Spine.001"),
                b_collection="Genitals (Female)",
            )
        ),
        ConnectBone(
            name="Vulva.L",
            bone_a="iv_inshin_l",
            bone_b="j_kosi",
            parent="Spine.001",
            is_connected=False,
            req_bones=["iv_inshin_l", "j_kosi"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(skin_control_orientation_bone="Spine.001"),
                b_collection="Genitals (Female)",
            )
        ),
        ConnectBone(
            name="Vulva",
            bone_a="iv_omanko",
            bone_b="j_kosi",
            parent="Spine.001",
            is_connected=False,
            req_bones=["iv_omanko", "j_kosi"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_basic_chain(skin_control_orientation_bone="Spine.001"),
                b_collection="Genitals (Female)",
            )
        ),
        ExtensionBone(
            name="Anchor_V",
            bone_a="Clitoris",
            parent="Spine.001",
            is_connected=False,
            start="tail",
            req_bones=["Clitoris"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.skin_anchor(skin_anchor_hide=True),
                b_collection="MCH"
            )
        )
    ]
)

def get_rig_module() -> RigModule:
    rig_module = RigModule(
        name="IVCS Female",
        type="Generation",
        bone_groups=[GENITALS_F]
    )
    return rig_module