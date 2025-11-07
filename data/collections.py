from . schemas import MetaRigCollectionInfo


META_RIG_COLLECTIONS_INFO: list[MetaRigCollectionInfo] = [
    MetaRigCollectionInfo(name="Face", color_type="FK", row_index=1, title="Face"),
    MetaRigCollectionInfo(name="Face (Primary)", color_type="IK", row_index=2, title="(Primary)"),
    MetaRigCollectionInfo(name="Face (Secondary)", color_type="Special", row_index=2, title="(Secondary)"),

    MetaRigCollectionInfo(name="Torso", color_type="Special", row_index=4, title="Torso"),
    MetaRigCollectionInfo(name="Torso (Tweak)", color_type="Tweak", row_index=5, title="(Tweak)"),

    MetaRigCollectionInfo(name="Fingers", color_type="Extra", row_index=7, title="Fingers"),
    MetaRigCollectionInfo(name="Fingers (Details)", color_type="FK", row_index=8, title="(Details)"),

    MetaRigCollectionInfo(name="Arm.L (IK)", color_type="IK", row_index=10, title="IK.L"),
    MetaRigCollectionInfo(name="Arm.L (FK)", color_type="FK", row_index=11, title="FK.L"),
    MetaRigCollectionInfo(name="Arm.L (Tweak)", color_type="Tweak", row_index=12, title="Tweak.L"),
    MetaRigCollectionInfo(name="Arm.R (IK)", color_type="IK", row_index=10, title="IK.R"),
    MetaRigCollectionInfo(name="Arm.R (FK)", color_type="FK", row_index=11, title="FK.R"),
    MetaRigCollectionInfo(name="Arm.R (Tweak)", color_type="Tweak", row_index=12, title="Tweak.R"),

    MetaRigCollectionInfo(name="Leg.L (IK)", color_type="IK", row_index=14, title="IK.L"),
    MetaRigCollectionInfo(name="Leg.L (FK)", color_type="FK", row_index=15, title="FK.L"),
    MetaRigCollectionInfo(name="Leg.L (Tweak)", color_type="Tweak", row_index=16, title="Tweak.L"),
    MetaRigCollectionInfo(name="Leg.R (IK)", color_type="IK", row_index=14, title="IK.R"),
    MetaRigCollectionInfo(name="Leg.R (FK)", color_type="FK", row_index=15, title="FK.R"),
    MetaRigCollectionInfo(name="Leg.R (Tweak)", color_type="Tweak", row_index=16, title="Tweak.R"),

    MetaRigCollectionInfo(name="Tail", color_type="Special", row_index=18, title="Tail"),
    MetaRigCollectionInfo(name="Tail (Tweak)", color_type="Tweak", row_index=19, title="Tweaks"),
]