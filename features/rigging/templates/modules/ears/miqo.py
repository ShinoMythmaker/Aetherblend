from ......core.generators import ExtensionBone
from ......core.operations import CollectionOperation, ParentBoneOperation, RigifyTypeOperation
from ......core.shared import PoseOperations, BoneGroup, TransformLink, RigModule
from ......core import rigify
from ......core.rigify.settings import UI_Collections, BoneCollection

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
            axis_type="local",
            axis="Y",
            start="head",
            roll=150,
            req_bones=["j_mimi_r"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Ear.R", parent=["Head", "j_kao"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Ear.R", rigify_type=rigify.types.basic_super_copy(widget_type="bone")),
                        CollectionOperation(time="Pre", bone_name="Ear.R", collection_name="Head"),
                        ]
        ),
        ExtensionBone(
            name="Ear.L",
            bone_a="j_mimi_l",
            axis_type="local",
            axis="Y",
            start="head",
            roll=-150,
            req_bones=["j_mimi_l"],
            operations=[ParentBoneOperation(time="Pre", bone_name="Ear.L", parent=["Head", "j_kao"], is_connected=False),
                        RigifyTypeOperation(time="Pre", bone_name="Ear.L", rigify_type=rigify.types.basic_super_copy(widget_type="bone")),
                        CollectionOperation(time="Pre", bone_name="Ear.L", collection_name="Head"),
                        ]
        ),
    ]
)

def get_rig_module() -> RigModule:
    return RigModule(
        name="Miqo",
        type="Generation",
        bone_groups=[MIQO_EARS],
        ui = UI_Collections([
            BoneCollection(name="Head", ui=True, color_set="Head", row_index=0, title="Head", visible=True),
        ])
    )