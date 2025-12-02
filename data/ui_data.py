from .schemas import MetaRigCollectionInfo, ConstraintUIController


META_RIG_COLLECTIONS_INFO: list[MetaRigCollectionInfo] = [
    MetaRigCollectionInfo(name="Face", color_type="FK", row_index=1, title="Face"),
    MetaRigCollectionInfo(name="Face (Primary)", color_type="IK", row_index=2, title="(Primary)", visible=False),
    MetaRigCollectionInfo(name="Face (Secondary)", color_type="Special", row_index=2, title="(Secondary)", visible=False),
    MetaRigCollectionInfo(name="Hair", color_type="IK", row_index=3, title="Hair", visible=False),
    MetaRigCollectionInfo(name="Accessory", color_type="Special", row_index=3, title="Accessory", visible=False),

    MetaRigCollectionInfo(name="Torso", color_type="Special", row_index=5, title="Torso"),
    MetaRigCollectionInfo(name="Torso (Tweak)", color_type="Tweak", row_index=6, title="(Tweak)", visible=False),

    MetaRigCollectionInfo(name="Fingers", color_type="Extra", row_index=8, title="Fingers"),
    MetaRigCollectionInfo(name="Fingers (Details)", color_type="FK", row_index=9, title="(Details)", visible=False),
    MetaRigCollectionInfo(name="Toes", color_type="Extra", row_index=8, title="Toes"),
    MetaRigCollectionInfo(name="Toes (Details)", color_type="FK", row_index=9, title="(Details)", visible=False),

    MetaRigCollectionInfo(name="Arm.L (IK)", color_type="IK", row_index=11, title="Arm IK.L"),
    MetaRigCollectionInfo(name="Arm.L (FK)", color_type="FK", row_index=12, title="FK.L", visible=False),
    MetaRigCollectionInfo(name="Arm.L (Tweak)", color_type="Tweak", row_index=13, title="Tweak.L", visible=False),
    MetaRigCollectionInfo(name="Arm.R (IK)", color_type="IK", row_index=11, title="Arm IK.R"),
    MetaRigCollectionInfo(name="Arm.R (FK)", color_type="FK", row_index=12, title="FK.R", visible=False),
    MetaRigCollectionInfo(name="Arm.R (Tweak)", color_type="Tweak", row_index=13, title="Tweak.R", visible=False),

    MetaRigCollectionInfo(name="Leg.L (IK)", color_type="IK", row_index=15, title="Leg IK.L"),
    MetaRigCollectionInfo(name="Leg.L (FK)", color_type="FK", row_index=16, title="FK.L", visible=False),
    MetaRigCollectionInfo(name="Leg.L (Tweak)", color_type="Tweak", row_index=17, title="Tweak.L", visible=False),
    MetaRigCollectionInfo(name="Leg.R (IK)", color_type="IK", row_index=15, title="Leg IK.R"),
    MetaRigCollectionInfo(name="Leg.R (FK)", color_type="FK", row_index=16, title="FK.R", visible=False),
    MetaRigCollectionInfo(name="Leg.R (Tweak)", color_type="Tweak", row_index=17, title="Tweak.R", visible=False),

    MetaRigCollectionInfo(name="Tail", color_type="Special", row_index=19, title="Tail"),
    MetaRigCollectionInfo(name="Tail (Tweak)", color_type="Tweak", row_index=20, title="Tweaks", visible=False),

    MetaRigCollectionInfo(name="Skirt", color_type="Special", row_index=22, title="Skirt", visible=False),
    MetaRigCollectionInfo(name="Skirt (Tweak)", color_type="Tweak", row_index=23, title="Tweak", visible=False),

    MetaRigCollectionInfo(name="Genitals (Male)", color_type="FK", row_index=25, title="Genitals (Male)"),
    MetaRigCollectionInfo(name="Tweak (Male)", color_type="Tweak", row_index=26, title="Tweak (Male)"),
    MetaRigCollectionInfo(name="Genitals (Female)", color_type="FK", row_index=25, title="Genitals (Female)"),
    MetaRigCollectionInfo(name="Tweak (Female)", color_type="Tweak", row_index=26, title="Tweak (Female)"),

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
    ),
    "eye_lid_brow_follow.L": ConstraintUIController(
        name="eye_lid_brow_follow.L",
        target_bone="lid.T.L.002",
        target_constraint="Copy Location",
        rename_constraint="eye_lid_brow_follow.L",
        property_name="influence",
        title="Eyelid Brow Follow L",
        ui_element="slider"
    ),
    "eye_lid_brow_follow.R": ConstraintUIController(
        name="eye_lid_brow_follow.R",
        target_bone="lid.T.R.002",
        target_constraint="Copy Location",
        rename_constraint="eye_lid_brow_follow.R",
        property_name="influence",
        title="Eyelid Brow Follow R",
        ui_element="slider"
    ),
    "eye_lid_cheek_follow.L": ConstraintUIController(
        name="eye_lid_cheek_follow.L",
        target_bone="lid.B.L.002",
        target_constraint="Copy Location",
        rename_constraint="eye_lid_cheek_follow.L",
        property_name="influence",
        title="Eyelid Cheek Follow L",
        ui_element="slider"
    ),
    "eye_lid_cheek_follow.R": ConstraintUIController(
        name="eye_lid_cheek_follow.R",
        target_bone="lid.B.R.002",
        target_constraint="Copy Location",
        rename_constraint="eye_lid_cheek_follow.R",
        property_name="influence",
        title="Eyelid Cheek Follow R",
        ui_element="slider"
    ),
    "nose_tip_follow": ConstraintUIController(
        name="nose_tip_follow",
        target_bone="Nose_end",
        target_constraint="Copy Location",
        rename_constraint="nose_tip_follow",
        property_name="influence",
        title="Nose Tip Follow",
        ui_element="slider"
    ),
    "nostril_follow.L": ConstraintUIController(
        name="nostril_follow.L",
        target_bone="Nose.L.001",
        target_constraint="Copy Location",
        rename_constraint="nostril_follow.L",
        property_name="influence",
        title="Nostril Follow L",
        ui_element="slider"
    ),
    "nostril_follow.R": ConstraintUIController(
        name="nostril_follow.R",
        target_bone="Nose.R.001",
        target_constraint="Copy Location",
        rename_constraint="nostril_follow.R",
        property_name="influence",
        title="Nostril Follow R",
        ui_element="slider"
    ),
    "glabella_follow.L": ConstraintUIController(
        name="glabella_follow.L",
        target_bone="Nose.L",
        target_constraint="Copy Location",
        rename_constraint="glabella_follow.L",
        property_name="influence",
        title="Glabella Nose Follow L",
        ui_element="slider"
    ),
     "glabella_follow.R": ConstraintUIController(
        name="glabella_follow.R",
        target_bone="Nose.R",
        target_constraint="Copy Location",
        rename_constraint="glabella_follow.R",
        property_name="influence",
        title="Glabella Nose Follow R",
        ui_element="slider"
     ),
     "glabella_follow.L.001": ConstraintUIController(
        name="glabella_follow.L.001",
        target_bone="Nose.L",
        target_constraint="Copy Location.001",
        rename_constraint="glabella_follow.L.001",
        property_name="influence",
        title="Glabella Brow Follow L",
        ui_element="slider"
    ),
     "glabella_follow.R.001": ConstraintUIController(
        name="glabella_follow.R.001",
        target_bone="Nose.R",
        target_constraint="Copy Location.001",
        rename_constraint="glabella_follow.R.001",
        property_name="influence",
        title="Glabella Brow Follow R",
        ui_element="slider"
     ),

     "cheek_follow.L": ConstraintUIController(
         name="cheek_follow.L",
         target_bone="Cheek.B.L",
         target_constraint="Copy Location",
         rename_constraint="cheek_follow.L",
         property_name="influence",
         title="Cheek Follow L",
         ui_element="slider"
     ),
    "cheek_follow.R": ConstraintUIController(
         name="cheek_follow.R",
         target_bone="Cheek.B.R",
         target_constraint="Copy Location",
         rename_constraint="cheek_follow.R",
         property_name="influence",
         title="Cheek Follow R",
         ui_element="slider"
     ),

    }

UI_CONTROLLER_MAPPING: dict[str, list[ConstraintUIController]] = {
    # Eyes

    "lid.T.L.002": [UI_CONTROLLERS["eye_lid_close.L"], UI_CONTROLLERS["eye_lid_brow_follow.L"]],
    "lid.T.R.002": [UI_CONTROLLERS["eye_lid_close.R"], UI_CONTROLLERS["eye_lid_brow_follow.R"]],
    "eye_common": [UI_CONTROLLERS["eye_lid_close.L"], UI_CONTROLLERS["eye_lid_close.R"]],

    "brow.T.L.002": [UI_CONTROLLERS["eye_lid_brow_follow.L"]],
    "brow.T.R.002": [UI_CONTROLLERS["eye_lid_brow_follow.R"]],
    "lid.B.L.002": [UI_CONTROLLERS["eye_lid_cheek_follow.L"]],
    "lid.B.R.002": [UI_CONTROLLERS["eye_lid_cheek_follow.R"]],
    "Cheek.T.L": [UI_CONTROLLERS["eye_lid_cheek_follow.L"]],
    "Cheek.T.R": [UI_CONTROLLERS["eye_lid_cheek_follow.R"]],

    "Nose": [UI_CONTROLLERS["nose_tip_follow"], UI_CONTROLLERS["glabella_follow.L"], UI_CONTROLLERS["glabella_follow.R"]],
    "Nose_end": [UI_CONTROLLERS["nostril_follow.L"], UI_CONTROLLERS["nostril_follow.R"]],
    "Nose.R": [UI_CONTROLLERS["glabella_follow.R"], UI_CONTROLLERS["glabella_follow.R.001"]],
    "Nose.L": [UI_CONTROLLERS["glabella_follow.L"], UI_CONTROLLERS["glabella_follow.L.001"]],
    "Nose.R.001": [UI_CONTROLLERS["nostril_follow.R"]],
    "Nose.L.001": [UI_CONTROLLERS["nostril_follow.L"]],
    "brow_end.T.L.003": [UI_CONTROLLERS["glabella_follow.L.001"]],
    "brow_end.T.R.003": [UI_CONTROLLERS["glabella_follow.R.001"]],

    "Lip.Master_end.B.L.001": [UI_CONTROLLERS["cheek_follow.L"]],
    "Lip.Master_end.B.R.001": [UI_CONTROLLERS["cheek_follow.R"]],
    "Cheek.B.R": [UI_CONTROLLERS["cheek_follow.R"]],
    "Cheek.B.L": [UI_CONTROLLERS["cheek_follow.L"]]
    }