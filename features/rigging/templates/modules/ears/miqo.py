from ......core.generators import ExtensionBone
from ......core.shared import PoseOperations, BoneGroup, TransformLink, RigModule
from ......core import rigify
        

MIQO_EARS = BoneGroup(
    name="Miqo Ears",
    transform_link=[
        TransformLink(target="DEF-Ear.R", bone="j_mimi_r"),
        TransformLink(target="DEF-Ear.L", bone="j_mimi_l")
    ],
    generators=[
        ExtensionBone(
            name="Ear.R",
            bone_a="j_mimi_r",
            parent="Head",
            is_connected=False,
            axis_type="local",
            axis="Y",
            start="head",
            roll=150,
            req_bones=["j_mimi_r"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.basic_super_copy(widget_type="bone"),
                b_collection="Head",
            )
        ),
        ExtensionBone(
            name="Ear.L",
            bone_a="j_mimi_l",
            parent="Head",
            is_connected=False,
            axis_type="local",
            axis="Y",
            start="head",
            roll=-150,
            req_bones=["j_mimi_l"],
            pose_operations=PoseOperations(
                rigify_settings=rigify.types.basic_super_copy(widget_type="bone"),
                b_collection="Head",
            )
        ),
    ]
)

def get_rig_module() -> RigModule:
    rig_module = RigModule(
        name="Miqo",
        type="Generation",
        bone_groups=[MIQO_EARS]
    )
    return rig_module