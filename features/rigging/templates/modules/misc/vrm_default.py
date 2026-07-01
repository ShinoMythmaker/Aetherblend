from ......core.rigify.settings import UI_Collections, BoneCollection
from ......core.operations import ParentBoneOperation, ConstraintOperation, RigifyTypeOperation, CollectionOperation, DriverOperation, CustomPropertyOperation
from ......core.constraints import DampedTrackConstraint
from ......core.bone_generators import ConnectBone, ExtensionBone, RegexBoneGroup
from ......core.shared import PoseOperations, BoneGroup, TransformLink, RigModule
from ......core import rigify
from ......core.drivers import TransformChannelVariable, Driver, SinglePropertyVariable
from ......core.custom_properties import FloatProperty

OPT = BoneGroup(
        name="Optional",
        transform_link=[],
        generators=[
            # Miscellaneous
            RegexBoneGroup(
                name="Misc",
                pattern=r"^J_Opt.*",
                original_parent=True,
                b_collection="Misc",
                prefix="OPT"
            ),
        ]
)


def get_rig_module() -> RigModule:
    return RigModule(
        name="VRM-Default",
        type="Generation",
        bone_groups=[OPT],
        ui_collections = UI_Collections([
            BoneCollection(name="Misc", ui=True, color_set="Head", row_index=1, title="Misc", visible=False),
        ],
        ),
    )
