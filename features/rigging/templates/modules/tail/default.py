from ......core.generators import ConnectBone, ExtensionBone
from ......core.shared import PoseOperations, BoneGroup, TransformLink, RigModule
from ......core import rigify
from ......core.rigify.settings import UI_Collections, BoneCollection

TAIL = BoneGroup(
    name="Tail",
    transform_link= [
        TransformLink(target="DEF-Tail", bone="n_sippo_a"),
        TransformLink(target="DEF-Tail.001", bone="n_sippo_b"),
        TransformLink(target="DEF-Tail.002", bone="n_sippo_c"),
        TransformLink(target="DEF-Tail.003", bone="n_sippo_d"),
        TransformLink(target="DEF-Tail.004", bone="n_sippo_e"),
    ],
    generators=[
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
        ExtensionBone(
            name="Tail.004",
            bone_a="Tail.003",
            parent="Tail.003",
            is_connected=True,
            axis_type="local",
            axis="Y",
            size_factor=1,
            req_bones=["n_sippo_e"],
            pose_operations=PoseOperations(
                b_collection="Tail"
            )
        )
    ]
)

def get_rig_module() -> RigModule:
    return RigModule(
        name="Default",
        type="Generation",
        bone_groups=[TAIL],
        ui = UI_Collections([
            BoneCollection(name="Tail", ui=True, color_set="Torso_Tweak", row_index=1, title="Tail"),
        ])
    )
