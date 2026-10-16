from .... import rigify
from ....bone_generators import ExtensionBone
from ....operations import CollectionOperation, ParentBoneOperation, RigifyTypeOperation
from ....rigify.settings import BoneCollection, UI_Collections
from ....shared import BoneGroup, RigModule, TransformLink

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
            parent="Head",
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
            parent="Head",
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
        name="XIV-Miqo",
        type="Generation",
        bone_groups=[MIQO_EARS],
        ui_collections = UI_Collections([
            BoneCollection(name="Head", ui=True, color_set="Head", row_index=0, title="Head", visible=True),
        ])
    )
