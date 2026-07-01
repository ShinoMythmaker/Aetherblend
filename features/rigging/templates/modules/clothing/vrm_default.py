from ......core.rigify.settings import UI_Collections, BoneCollection
from ......core.operations import ParentBoneOperation, ConstraintOperation, RigifyTypeOperation, CollectionOperation, DriverOperation, CustomPropertyOperation
from ......core.constraints import DampedTrackConstraint
from ......core.bone_generators import ConnectBone, ExtensionBone, RegexBoneGroup
from ......core.shared import PoseOperations, BoneGroup, TransformLink, RigModule
from ......core import rigify
from ......core.drivers import TransformChannelVariable, Driver, SinglePropertyVariable
from ......core.custom_properties import FloatProperty

SKIRT = BoneGroup(
        name="Skirt",
        transform_link=[],
        generators=[
            # Skirt Sides
            RegexBoneGroup(
                name="Skirt Right",
                pattern=r"^J_Sec_.*Skirt.*",
                original_parent=True,
                b_collection="Skirt",
                prefix="Skirt"
            ),
        ]
)

CLOTHING = BoneGroup(
        name="Clothing",
        transform_link=[],
        generators=[
            # Upper Arms
            RegexBoneGroup(
                name="Tops",
                pattern=r"^J_Sec_.*Tops.*",
                original_parent=True,
                b_collection="Clothing",
                prefix="CLOTH"
            ),
            RegexBoneGroup(
                name="Hood",
                pattern=r"^J_Sec_.*Hood.*",
                original_parent=True,
                b_collection="Clothing",
                prefix="CLOTH"
            ),
        ]
)


def get_rig_module() -> RigModule:
    return RigModule(
        name="VRM-Default",
        type="Generation",
        bone_groups=[SKIRT, CLOTHING],
        ui_collections = UI_Collections([
            BoneCollection(name="Clothing", ui=True, color_set="Head", row_index=1, title="Clothing", visible=False),
            BoneCollection(name="Skirt", ui=True, color_set="Head", row_index=2, title="Skirt", visible=False), 
        ],
        ),
        ui_flags = ["Skirt Automation"],
    )
