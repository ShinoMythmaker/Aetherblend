from .schemas import MetaRigCollectionInfo, ConstraintUIController


META_RIG_COLLECTIONS_INFO: list[MetaRigCollectionInfo] = [
    MetaRigCollectionInfo(name="Face", color_type="FK", row_index=1, title="Face"),
    MetaRigCollectionInfo(name="Face (Primary)", color_type="IK", row_index=2, title="(Primary)", visible=False),
    MetaRigCollectionInfo(name="Face (Secondary)", color_type="Special", row_index=2, title="(Secondary)", visible=False),

    MetaRigCollectionInfo(name="Torso", color_type="Special", row_index=4, title="Torso"),
    MetaRigCollectionInfo(name="Torso (Tweak)", color_type="Tweak", row_index=5, title="(Tweak)", visible=False),

    MetaRigCollectionInfo(name="Fingers", color_type="Extra", row_index=7, title="Fingers"),
    MetaRigCollectionInfo(name="Fingers (Details)", color_type="FK", row_index=8, title="(Details)", visible=False),

    MetaRigCollectionInfo(name="Arm.L (IK)", color_type="IK", row_index=10, title="Arm IK.L"),
    MetaRigCollectionInfo(name="Arm.L (FK)", color_type="FK", row_index=11, title="FK.L", visible=False),
    MetaRigCollectionInfo(name="Arm.L (Tweak)", color_type="Tweak", row_index=12, title="Tweak.L", visible=False),
    MetaRigCollectionInfo(name="Arm.R (IK)", color_type="IK", row_index=10, title="Arm IK.R"),
    MetaRigCollectionInfo(name="Arm.R (FK)", color_type="FK", row_index=11, title="FK.R", visible=False),
    MetaRigCollectionInfo(name="Arm.R (Tweak)", color_type="Tweak", row_index=12, title="Tweak.R", visible=False),

    MetaRigCollectionInfo(name="Leg.L (IK)", color_type="IK", row_index=14, title="Leg IK.L"),
    MetaRigCollectionInfo(name="Leg.L (FK)", color_type="FK", row_index=15, title="FK.L", visible=False),
    MetaRigCollectionInfo(name="Leg.L (Tweak)", color_type="Tweak", row_index=16, title="Tweak.L", visible=False),
    MetaRigCollectionInfo(name="Leg.R (IK)", color_type="IK", row_index=14, title="Leg IK.R"),
    MetaRigCollectionInfo(name="Leg.R (FK)", color_type="FK", row_index=15, title="FK.R", visible=False),
    MetaRigCollectionInfo(name="Leg.R (Tweak)", color_type="Tweak", row_index=16, title="Tweak.R", visible=False),

    MetaRigCollectionInfo(name="Tail", color_type="Special", row_index=18, title="Tail"),
    MetaRigCollectionInfo(name="Tail (Tweak)", color_type="Tweak", row_index=19, title="Tweaks", visible=False),

    MetaRigCollectionInfo(name="Skirt", color_type="Special", row_index=21, title="Skirt", visible=False),
    MetaRigCollectionInfo(name="Skirt (Tweak)", color_type="Tweak", row_index=22, title="Tweak", visible=False),
]

UI_CONTROLLERS: dict[str, ConstraintUIController] = {
    "eye_lid_close.L": ConstraintUIController(
        name="eye_lid_close.L",
        target_bone="lid.T.L.002",
        target_constraint="eye_lid_close.L",
        property_name="influence",
        title="Eyelid Close L",
        ui_element="slider"
    ),
    "eye_lid_close.R": ConstraintUIController(
        name="eye_lid_close.R",
        target_bone="lid.T.R.002",
        target_constraint="eye_lid_close.R",
        property_name="influence",
        title="Eyelid Close R",
        ui_element="slider"
    )
    }

UI_CONTROLLER_MAPPING: dict[str, list[ConstraintUIController]] = {
    # Eyes

    "lid.T.L.002": [UI_CONTROLLERS["eye_lid_close.L"]],
    "lid.T.R.002": [UI_CONTROLLERS["eye_lid_close.R"]],
    "eye_common": [UI_CONTROLLERS["eye_lid_close.L"], UI_CONTROLLERS["eye_lid_close.R"]],
    }