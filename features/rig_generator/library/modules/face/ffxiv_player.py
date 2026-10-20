"""FFXIV player face, including the selected manual or automated mouth."""

import bpy

from ......utils import object as object_utils
from .... import definitions
from .... import instructions as abi
from . import _mouth_automatic, _mouth_manual


class Module(definitions.RigModule):
    """Build facial controls and the template-selected mouth in every rig stage."""

    name = "FFXIV Player Face"
    ui_flags = ("Eye Lid Edit Mode",)

    def __init__(self) -> None:
        self._mouth: definitions.RigModule | None = None

    def meta_edit(self, rig: bpy.types.Object) -> None:
        """Select the mouth mode and build the face before its mouth chains."""
        if self.toggles is None:
            raise ValueError(f"{self.name} requires template toggles")
        mode = self.toggles.mouth
        if mode not in {"AUTOMATIC", "MANUAL"}:
            raise ValueError(f"Unknown mouth mode: {mode}")
        self._mouth = _mouth_manual.Module() if mode == "MANUAL" else _mouth_automatic.Module()
        self._mouth.toggles = self.toggles
        self._face_meta_edit(rig)
        self._mouth.meta_edit(rig)

    def meta_pose(self, rig: bpy.types.Object) -> None:
        """Configure both face and selected mouth controls."""
        self._face_meta_pose(rig)
        if self._mouth is not None:
            self._mouth.meta_pose(rig)

    def final_edit(self, rig: bpy.types.Object) -> None:
        """Apply generated face and selected mouth hierarchies."""
        self._face_final_edit(rig)
        if self._mouth is not None:
            self._mouth.final_edit(rig)

    def final_pose(self, rig: bpy.types.Object) -> None:
        """Apply face automation and the selected mouth's widgets."""
        self._face_final_pose(rig)
        if self._mouth is not None:
            self._mouth.final_pose(rig)

    # ------------------------------------------------------------------------

    def _face_meta_edit(self, rig: bpy.types.Object) -> None:
        """Build the facial chains and optional eye controls."""
        # Brow chains
        for side in definitions.SIDES:
            abi.connect(rig, f"Brow{side.suffix}", f"j_f_mayu_{side.source}", f"j_f_mmayu_{side.source}", parent="Head")
            abi.connect(
                rig,
                f"Brow{side.suffix}.001",
                f"j_f_mmayu_{side.source}",
                f"j_f_miken_01_{side.source}",
                parent=f"Brow{side.suffix}",
                connected=True,
            )
            abi.connect(
                rig,
                f"Brow{side.suffix}.002",
                f"j_f_miken_01_{side.source}",
                f"j_f_miken_02_{side.source}",
                parent=f"Brow{side.suffix}.001",
                connected=True,
            )
            abi.extend(
                rig,
                f"Brow{side.suffix}.003",
                f"Brow{side.suffix}.002",
                axis="Y",
                parent=f"Brow{side.suffix}.002",
                connected=True,
            )

        # Mouth corner and cheek chains
        for side in definitions.SIDES:
            abi.center(
                rig,
                f"Corner{side.suffix}",
                [f"j_f_uslip_{side.source}", f"j_f_dslip_{side.source}", f"j_f_shoho_{side.source}"],
                axis="Y",
                parent="Head",
            )
            abi.connect(rig, f"Cheek{side.suffix}", f"Corner{side.suffix}", f"j_f_shoho_{side.source}", parent="Head")
            abi.connect(
                rig,
                f"Cheek.B{side.suffix}",
                f"j_f_shoho_{side.source}",
                f"j_f_hoho_{side.source}",
                parent=f"Cheek{side.suffix}",
                connected=True,
            )
            abi.connect(
                rig, f"Cheek.B{side.suffix}.001", f"j_f_dhoho_{side.source}", f"j_f_hoho_{side.source}", parent="Head"
            )
            abi.connect(
                rig, f"Cheek.T{side.suffix}", f"j_f_hoho_{side.source}", f"j_f_dmemoto_{side.source}", parent="Head"
            )
            abi.connect(
                rig, f"Cheek.T{side.suffix}.001", f"j_f_dmemoto_{side.source}", f"j_f_hana_{side.source}", parent="Head"
            )

        # Nose and face suppressor
        abi.center(rig, "NoseRef", ["j_f_miken_02_r", "j_f_miken_02_l"], axis="Z", parent="Head")
        abi.connect(rig, "Nose", "j_f_uhana", "NoseRef", parent="Head")
        abi.extend(rig, "Face.Suppressor", "NoseRef", axis="Y", start_point="head", parent="Head")

        # Nose, nostril and glue chains
        for side in definitions.SIDES:
            abi.connect(
                rig,
                f"Nose{side.suffix}",
                f"j_f_dmiken_{side.source}",
                f"Brow{side.suffix}.003",
                end_point="tail",
                parent="Head",
            )
            abi.connect(rig, f"Nostril{side.suffix}", f"j_f_hana_{side.source}", "j_f_uhana", parent="Head")
            abi.connect(rig, f"Nostril.Glue{side.suffix}", f"j_f_hana_{side.source}", "j_f_uhana", parent="Head")
            abi.connect(
                rig,
                f"Nostril.Glue{side.suffix}.001",
                f"Cheek.T{side.suffix}.001",
                f"Nostril{side.suffix}",
                parent="Head",
            )
            abi.connect(
                rig, f"Cheek.B{side.suffix}.glue", f"j_f_dhoho_{side.source}", f"j_f_shoho_{side.source}", parent="Head"
            )
            abi.connect(
                rig, f"Cheek.T{side.suffix}.glue", f"j_f_dhoho_{side.source}", f"j_f_hoho_{side.source}", parent="Head"
            )

        # Eyes and lid controls
        meshes = object_utils.find_by_armature_and_material_property(
            rig.data.rigify_target_rig or rig, "ShaderPackage", "characterocclusion.shpk"
        )
        occlusion_mesh = meshes[0] if meshes else None
        if occlusion_mesh:
            source_rig = rig.data.rigify_target_rig
            for side in definitions.SIDES:
                # Lid corners and centers follow the heaviest source weights on the occlusion mesh.
                abi.heaviest_vertex(
                    rig,
                    f"lid.T{side.suffix}",
                    f"j_f_mabup_02out_{side.source}",
                    occlusion_mesh,
                    source_rig=source_rig,
                )
                abi.heaviest_vertex(
                    rig,
                    f"lid.T{side.suffix}.002",
                    f"j_f_mabup_01_{side.source}",
                    occlusion_mesh,
                    source_rig=source_rig,
                )
                abi.heaviest_vertex(
                    rig,
                    f"lid.B{side.suffix}",
                    f"j_f_mabdn_03in_{side.source}",
                    occlusion_mesh,
                    source_rig=source_rig,
                )
                abi.heaviest_vertex(
                    rig,
                    f"lid.B{side.suffix}.002",
                    f"j_f_mabdn_01_{side.source}",
                    occlusion_mesh,
                    source_rig=source_rig,
                )
                abi.copy(rig, f"Eye{side.suffix}", f"j_f_eyepuru_{side.source}", parent="Head")

                # Lid bridges
                abi.bridge(
                    rig,
                    f"lid.T{side.suffix}.001",
                    f"lid.T{side.suffix}",
                    f"lid.T{side.suffix}.002",
                    offset=(0.0 if side is definitions.LEFT else -0.0, -0.001, 0.001),
                    start_parent=f"Eye{side.suffix}",
                    connect_end=True,
                )
                abi.bridge(
                    rig,
                    f"lid.T{side.suffix}.003",
                    f"lid.T{side.suffix}.002",
                    f"lid.B{side.suffix}",
                    offset=(0.0 if side is definitions.LEFT else -0.0, 0.0, 0.003),
                    start_parent=None,
                    connect_end=False,
                )
                abi.bridge(
                    rig,
                    f"lid.B{side.suffix}.001",
                    f"lid.B{side.suffix}",
                    f"lid.B{side.suffix}.002",
                    offset=(-0.002 if side is definitions.LEFT else 0.002, 0.0, 0.001),
                    start_parent=f"Eye{side.suffix}",
                    connect_end=True,
                )
                abi.bridge(
                    rig,
                    f"lid.B{side.suffix}.003",
                    f"lid.B{side.suffix}.002",
                    f"lid.T{side.suffix}",
                    offset=(0.003 if side is definitions.LEFT else -0.003, -0.001, -0.003),
                    start_parent=None,
                    connect_end=False,
                )

                # Lid trackers
                abi.connect(
                    rig,
                    f"eye_tracker.B{side.suffix}.001",
                    f"j_f_mabdn_03in_{side.source}",
                    f"lid.B{side.suffix}.001",
                    parent=f"Eye{side.suffix}",
                )
                abi.connect(
                    rig,
                    f"eye_tracker.B{side.suffix}.002",
                    f"j_f_mabdn_01_{side.source}",
                    f"lid.B{side.suffix}.002",
                    parent=f"Eye{side.suffix}",
                )
                abi.connect(
                    rig,
                    f"eye_tracker.B{side.suffix}.003",
                    f"j_f_mabdn_02out_{side.source}",
                    f"lid.B{side.suffix}.003",
                    parent=f"Eye{side.suffix}",
                )
                abi.connect(
                    rig,
                    f"eye_tracker.T{side.suffix}.001",
                    f"j_f_mabup_02out_{side.source}",
                    f"lid.T{side.suffix}.001",
                    parent=f"Eye{side.suffix}",
                )
                abi.connect(
                    rig,
                    f"eye_tracker.T{side.suffix}.002",
                    f"j_f_mabup_01_{side.source}",
                    f"lid.T{side.suffix}.002",
                    parent=f"Eye{side.suffix}",
                )
                abi.connect(
                    rig,
                    f"eye_tracker.T{side.suffix}.003",
                    f"j_f_mabup_03in_{side.source}",
                    f"lid.T{side.suffix}.003",
                    parent=f"Eye{side.suffix}",
                )
                abi.connect(
                    rig,
                    f"Lower.Lid{side.suffix}.Glue",
                    f"lid.B{side.suffix}.002",
                    f"j_f_hoho_{side.source}",
                    parent="Head",
                )
                abi.connect(
                    rig,
                    f"Upper.Lid{side.suffix}.Glue",
                    f"lid.T{side.suffix}.002",
                    f"j_f_miken_02_{side.source}",
                    parent="Head",
                )

            # Iris, pupil and lid controls
            for bone in ("Iris.Ctrl.Master", "Iris.Ctrl"):
                abi.offset(rig, bone, "Eye.L", (0.0025, 0.015, 0.051), parent="Eye.L")
            for bone in ("Pupil.Ctrl.Master", "Pupil.Ctrl"):
                abi.offset(rig, bone, "Eye.L", (0.0025, 0.015, 0.058), parent="Eye.L")
            for bone in ("Lid.Ctrl.Master", "Lid.Ctrl"):
                abi.offset(rig, bone, "Eye.L", (0.01, 0.015, 0.035), parent="Eye.L")

            # Lower lid anchors
            for side in definitions.SIDES:
                for number in (1, 2, 3):
                    abi.extend(
                        rig,
                        f"lid.anchor.B{side.suffix}.00{number}",
                        f"lid.B{side.suffix}.00{number}",
                        axis="Z",
                        axis_space="global",
                        start_point="head",
                        parent=f"lid.B{side.suffix}.00{number}",
                    )
        else:
            print("[AetherBlend] No eye occlusion mesh found; the eyes are skipped.")

    # ------------------------------------------------------------------------

    def _face_meta_pose(self, rig: bpy.types.Object) -> None:
        """Configure facial rig types, collections and source mappings."""
        for side in definitions.SIDES:
            # Brow controls and mappings
            abi.rigify.skin_stretchy_chain(
                rig,
                f"Brow{side.suffix}",
                control_orientation_bone="Head",
                falloff_length=True,
                use_scale=[True, True, True, True],
                primary_collection="Face (Primary)",
            )
            abi.collection(rig, [f"Brow{side.suffix}"], "Face (Secondary)")
            abi.collection(
                rig, [f"Brow{side.suffix}.001", f"Brow{side.suffix}.002", f"Brow{side.suffix}.003"], "Face (Primary)"
            )
            abi.link(rig, f"j_f_mayu_{side.source}", f"DEF-Brow{side.suffix}")
            abi.link(rig, f"j_f_mmayu_{side.source}", f"DEF-Brow{side.suffix}.001")
            abi.link(rig, f"j_f_miken_01_{side.source}", f"DEF-Brow{side.suffix}.002")
            abi.link(rig, f"j_f_miken_02_{side.source}", f"DEF-Brow{side.suffix}.003")

            # Cheek controls and mappings
            abi.rigify.skin_stretchy_chain(
                rig,
                f"Cheek{side.suffix}",
                control_orientation_bone="Head",
                falloff_length=True,
                use_scale=[True, True, True, True],
                primary_collection="Face (Primary)",
            )
            for chain in (f"Cheek.B{side.suffix}.001", f"Cheek.T{side.suffix}", f"Cheek.T{side.suffix}.001"):
                abi.rigify.skin_basic_chain(
                    rig, chain, control_orientation_bone="Head", use_scale=[True, True, True, True]
                )
            abi.collection(
                rig, [f"Cheek{side.suffix}", f"Cheek.B{side.suffix}", f"Cheek.T{side.suffix}"], "Face (Primary)"
            )
            abi.collection(rig, [f"Cheek.B{side.suffix}.001", f"Cheek.T{side.suffix}.001"], "Face (Secondary)")
            abi.collection(rig, [f"Corner{side.suffix}"], "MCH")
            abi.link(rig, f"j_f_shoho_{side.source}", f"DEF-Cheek.B{side.suffix}")
            abi.link(rig, f"j_f_dhoho_{side.source}", f"DEF-Cheek.B{side.suffix}.001")
            abi.link(rig, f"j_f_hoho_{side.source}", f"DEF-Cheek.T{side.suffix}")
            abi.link(rig, f"j_f_dmemoto_{side.source}", f"DEF-Cheek.T{side.suffix}.001")

            # Nose and nostril controls and mappings
            abi.rigify.skin_basic_chain(
                rig, f"Nose{side.suffix}", control_orientation_bone="Head", use_scale=[True, True, True, True]
            )
            abi.rigify.skin_basic_chain(
                rig,
                f"Nostril{side.suffix}",
                chain_priority=1,
                control_orientation_bone="Head",
                use_scale=[True, True, True, True],
            )
            abi.collection(rig, [f"Nose{side.suffix}", f"Nostril{side.suffix}"], "Face (Primary)")
            abi.link(rig, f"j_f_dmiken_{side.source}", f"DEF-Nose{side.suffix}")
            abi.link(rig, f"j_f_hana_{side.source}", f"DEF-Nostril{side.suffix}")

            # Glue keeps the nostrils and cheeks following the surrounding chains.
            for bone in (
                f"Nostril.Glue{side.suffix}",
                f"Nostril.Glue{side.suffix}.001",
                f"Cheek.B{side.suffix}.glue",
                f"Cheek.T{side.suffix}.glue",
            ):
                abi.rigify.skin_glue(
                    rig,
                    bone,
                    relink_constraints=True,
                    use_tail=True,
                    reparent_tail=bone == f"Cheek.B{side.suffix}.glue",
                    add_constraint="COPY_LOCATION_OWNER",
                    add_constraint_influence=0.5,
                )
            abi.collection(
                rig,
                [
                    f"Nostril.Glue{side.suffix}",
                    f"Nostril.Glue{side.suffix}.001",
                    f"Cheek.B{side.suffix}.glue",
                    f"Cheek.T{side.suffix}.glue",
                ],
                "MCH",
            )

            # Eye and lid controls
            if f"Eye{side.suffix}" in rig.pose.bones:
                abi.rigify.skin_stretchy_chain(
                    rig,
                    f"lid.T{side.suffix}",
                    pivot_position=2,
                    control_orientation_bone="Head",
                    falloff=[0.0, 1.0, 0.0],
                    falloff_length=True,
                    falloff_spherical=[False, False, False],
                    primary_collection="Face (Primary)",
                )
                abi.rigify.skin_stretchy_chain(
                    rig,
                    f"lid.B{side.suffix}",
                    pivot_position=2,
                    control_orientation_bone="Head",
                    primary_collection="Face (Primary)",
                )
                abi.rigify.face_skin_eye(rig, f"Eye{side.suffix}")
                abi.collection(rig, [f"Eye{side.suffix}"], "Face (Primary)")
                abi.collection(
                    rig,
                    [
                        f"lid.T{side.suffix}",
                        f"lid.T{side.suffix}.001",
                        f"lid.T{side.suffix}.002",
                        f"lid.T{side.suffix}.003",
                        f"lid.B{side.suffix}",
                        f"lid.B{side.suffix}.001",
                        f"lid.B{side.suffix}.002",
                        f"lid.B{side.suffix}.003",
                    ],
                    "Face (Secondary)",
                )

                # Lid trackers
                abi.rigify.skin_basic_chain(rig, f"eye_tracker.B{side.suffix}.001")
                abi.rigify.skin_basic_chain(rig, f"eye_tracker.B{side.suffix}.002")
                abi.rigify.skin_basic_chain(rig, f"eye_tracker.B{side.suffix}.003")
                abi.rigify.skin_basic_chain(rig, f"eye_tracker.T{side.suffix}.001")
                abi.rigify.skin_basic_chain(rig, f"eye_tracker.T{side.suffix}.002")
                abi.rigify.skin_basic_chain(rig, f"eye_tracker.T{side.suffix}.003")
                abi.collection(
                    rig,
                    [
                        f"eye_tracker.B{side.suffix}.001",
                        f"eye_tracker.B{side.suffix}.002",
                        f"eye_tracker.B{side.suffix}.003",
                        f"eye_tracker.T{side.suffix}.001",
                        f"eye_tracker.T{side.suffix}.002",
                        f"eye_tracker.T{side.suffix}.003",
                    ],
                    "Face",
                )
                for bone in (f"Lower.Lid{side.suffix}.Glue", f"Upper.Lid{side.suffix}.Glue"):
                    abi.rigify.skin_glue(
                        rig,
                        bone,
                        relink_constraints=True,
                        use_tail=True,
                        reparent_tail=True,
                        add_constraint="COPY_LOCATION_OWNER",
                        add_constraint_influence=0.1,
                    )
                abi.collection(rig, [f"Lower.Lid{side.suffix}.Glue", f"Upper.Lid{side.suffix}.Glue"], "MCH")

                # Lid and eye source mappings
                abi.link(rig, f"j_f_mabdn_03in_{side.source}", f"lid.B{side.suffix}.001")
                abi.link(rig, f"j_f_mabdn_01_{side.source}", f"lid.B{side.suffix}.002")
                abi.link(rig, f"j_f_mabdn_02out_{side.source}", f"lid.B{side.suffix}.003")
                abi.link(rig, f"j_f_mabup_02out_{side.source}", f"lid.T{side.suffix}.001")
                abi.link(rig, f"j_f_mabup_01_{side.source}", f"lid.T{side.suffix}.002")
                abi.link(rig, f"j_f_mabup_03in_{side.source}", f"lid.T{side.suffix}.003")
                abi.link(rig, f"j_f_eyepuru_{side.source}", f"MCH-Eye{side.suffix}")

        # Macro controls and lid anchors
        if "Iris.Ctrl" in rig.pose.bones:
            for bone in (
                "Iris.Ctrl.Master",
                "Iris.Ctrl",
                "Pupil.Ctrl.Master",
                "Pupil.Ctrl",
                "Lid.Ctrl.Master",
                "Lid.Ctrl",
            ):
                abi.rigify.basic_raw_copy(rig, bone)
            abi.collection(
                rig,
                ["Iris.Ctrl.Master", "Iris.Ctrl", "Pupil.Ctrl.Master", "Pupil.Ctrl", "Lid.Ctrl.Master", "Lid.Ctrl"],
                "Eyes (Macro)",
            )
            for side in definitions.SIDES:
                for number in (1, 2, 3):
                    abi.rigify.basic_raw_copy(rig, f"lid.anchor.B{side.suffix}.00{number}")
            abi.collection(
                rig,
                [
                    "lid.anchor.B.L.001",
                    "lid.anchor.B.L.002",
                    "lid.anchor.B.L.003",
                    "lid.anchor.B.R.001",
                    "lid.anchor.B.R.002",
                    "lid.anchor.B.R.003",
                ],
                "Eyes_Anchors",
            )

        # Nose control
        abi.rigify.skin_basic_chain(
            rig, "Nose", chain_priority=2, control_orientation_bone="Head", use_scale=[True, True, True, True]
        )
        abi.collection(rig, ["Nose"], "Face (Primary)")
        abi.link(rig, "j_f_uhana", "DEF-Nose")

        # Face suppressor
        abi.rigify.skin_anchor(rig, "Face.Suppressor", hide=True)
        abi.collection(rig, ["Face.Suppressor", "NoseRef"], "MCH")

    # ------------------------------------------------------------------------

    def _face_final_edit(self, rig: bpy.types.Object) -> None:
        """Parent the macro controls to the generated head."""
        # Eye control hierarchy
        for control in ("Iris", "Pupil", "Lid"):
            if abi.has_bone(rig, f"{control}.Ctrl.Master"):
                abi.parent(rig, f"{control}.Ctrl.Master", "head")
                abi.parent(rig, f"{control}.Ctrl", f"{control}.Ctrl.Master")

    # ------------------------------------------------------------------------

    def _face_final_pose(self, rig: bpy.types.Object) -> None:
        """Configure facial widgets and optional eye automation."""
        # Head follow and face widgets
        abi.prop(rig, "head", "head_follow", 1)

        abi.widget(rig, "Nose", scale_factor=0.6)
        for side in definitions.SIDES:
            abi.widget(rig, f"Cheek.T{side.suffix}", scale_factor=0.6)
            abi.widget(rig, f"Cheek.B{side.suffix}.001", scale_factor=0.4)
            abi.widget(rig, f"Cheek.B{side.suffix}", scale_factor=0.7)
            abi.widget(rig, f"Nose{side.suffix}", scale_factor=1.0)
            abi.widget(rig, f"Nostril{side.suffix}", scale_factor=0.6)

        # Eye widgets and automation
        if "Iris.Ctrl" in rig.pose.bones:
            # Iris control frame
            abi.widget(
                rig,
                "Iris.Ctrl.Master",
                widget_name="IrisSliderFrame",
                rotation_degrees=(90.0, -90.0, 180.0),
                wire_width=1.2,
                scale_to_bone_length=False,
                color_set="CUSTOM",
                custom_color_normal=(0.443137, 0.541176, 1.0),
                custom_color_select=(0.443137, 0.541176, 1.0),
                custom_color_active=(0.443137, 0.541176, 1.0),
            )
            abi.pose(rig, "Iris.Ctrl.Master", scale=(0.007, 0.007, 0.007))
            abi.restrict(
                rig, "Iris.Ctrl.Master", lock_location=True, lock_rotation=True, lock_scale=True, hide_select=True
            )

            # Pupil control frame
            abi.widget(
                rig,
                "Pupil.Ctrl.Master",
                widget_name="PupilSliderFrame",
                rotation_degrees=(90.0, -90.0, 180.0),
                wire_width=1.2,
                scale_to_bone_length=False,
                color_set="CUSTOM",
                custom_color_normal=(0.443137, 0.541176, 1.0),
                custom_color_select=(0.443137, 0.541176, 1.0),
                custom_color_active=(0.443137, 0.541176, 1.0),
            )
            abi.pose(rig, "Pupil.Ctrl.Master", scale=(0.007, 0.007, 0.007))
            abi.restrict(
                rig, "Pupil.Ctrl.Master", lock_location=True, lock_rotation=True, lock_scale=True, hide_select=True
            )

            # Lid control frame
            abi.widget(
                rig,
                "Lid.Ctrl.Master",
                widget_name="EyeTriangle",
                rotation_degrees=(90.0, 0.0, 0.0),
                wire_width=1.2,
                scale_to_bone_length=False,
                color_set="CUSTOM",
                custom_color_normal=(1.0, 0.435294, 0.733333),
                custom_color_select=(1.0, 0.435294, 0.733333),
                custom_color_active=(1.0, 0.435294, 0.733333),
            )
            abi.pose(rig, "Lid.Ctrl.Master", scale=(0.015, 0.015, 0.015))
            abi.restrict(
                rig, "Lid.Ctrl.Master", lock_location=True, lock_rotation=True, lock_scale=True, hide_select=True
            )

            # Iris and pupil sliders
            for bone in ("Iris.Ctrl", "Pupil.Ctrl"):
                abi.widget(
                    rig,
                    bone,
                    widget_name="Slider",
                    rotation_degrees=(90.0, -90.0, 180.0),
                    wire_width=1.3,
                    scale_to_bone_length=False,
                )
                abi.restrict(rig, bone, lock_location=(True, True, False), lock_rotation=True, lock_scale=True)
                abi.constraints.limit_location(
                    rig, bone, minimum=(None, None, -1.0), maximum=(None, None, 1.0), use_transform_limit=True
                )

            # Lid control
            abi.widget(
                rig,
                "Lid.Ctrl",
                widget_name="Circle",
                rotation_degrees=(180.0, 90.0, 90.0),
                scale=(0.08, 0.08, 0.08),
                wire_width=1.3,
                scale_to_bone_length=False,
            )
            abi.restrict(rig, "Lid.Ctrl", lock_location=(False, True, False), lock_rotation=True, lock_scale=True)
            abi.constraints.limit_location(
                rig,
                "Lid.Ctrl",
                minimum=(-0.667, None, -1.0),
                maximum=(0.667, None, 0.0),
                use_transform_limit=True,
            )

            for side in definitions.SIDES:
                # Lower lid anchor widgets
                for number in (1, 2, 3):
                    abi.widget(
                        rig,
                        f"lid.anchor.B{side.suffix}.00{number}",
                        widget_name="Pointer",
                        color_set="THEME01",
                        wire_width=2.0,
                    )
                    abi.restrict(
                        rig,
                        f"lid.anchor.B{side.suffix}.00{number}",
                        lock_rotation=True,
                        lock_scale=True,
                        inherit_rotation=False,
                        inherit_scale="NONE",
                    )

                # Closing the eye pulls each upper lid onto the opposite-numbered lower anchor.
                abi.constraints.copy_location(
                    rig,
                    f"lid.T{side.suffix}.003",
                    f"lid.anchor.B{side.suffix}.001",
                    name="AB_EyeLidControl",
                    target_space="POSE",
                    owner_space="POSE",
                    influence=0.0,
                )
                abi.driver(
                    rig,
                    f"lid.T{side.suffix}.003",
                    "influence",
                    constraint="AB_EyeLidControl",
                    expression=(
                        "min(1, max(0, (-y / 1) - max(0, x / 0.667)))"
                        if side is definitions.LEFT
                        else "min(1, max(0, (-y / 1) - max(0, -x / 0.667)))"
                    ),
                    variables={
                        "x": abi.TransformVariable("Lid.Ctrl", "LOC_X"),
                        "y": abi.TransformVariable("Lid.Ctrl", "LOC_Z"),
                    },
                )
                abi.constraints.copy_location(
                    rig,
                    f"lid.T{side.suffix}.002",
                    f"lid.anchor.B{side.suffix}.002",
                    name="AB_EyeLidControl",
                    target_space="POSE",
                    owner_space="POSE",
                    influence=0.0,
                )
                abi.driver(
                    rig,
                    f"lid.T{side.suffix}.002",
                    "influence",
                    constraint="AB_EyeLidControl",
                    expression=(
                        "min(1, max(0, (-y / 1) - max(0, x / 0.667)))"
                        if side is definitions.LEFT
                        else "min(1, max(0, (-y / 1) - max(0, -x / 0.667)))"
                    ),
                    variables={
                        "x": abi.TransformVariable("Lid.Ctrl", "LOC_X"),
                        "y": abi.TransformVariable("Lid.Ctrl", "LOC_Z"),
                    },
                )
                abi.constraints.copy_location(
                    rig,
                    f"lid.T{side.suffix}.001",
                    f"lid.anchor.B{side.suffix}.003",
                    name="AB_EyeLidControl",
                    target_space="POSE",
                    owner_space="POSE",
                    influence=0.0,
                )
                abi.driver(
                    rig,
                    f"lid.T{side.suffix}.001",
                    "influence",
                    constraint="AB_EyeLidControl",
                    expression=(
                        "min(1, max(0, (-y / 1) - max(0, x / 0.667)))"
                        if side is definitions.LEFT
                        else "min(1, max(0, (-y / 1) - max(0, -x / 0.667)))"
                    ),
                    variables={
                        "x": abi.TransformVariable("Lid.Ctrl", "LOC_X"),
                        "y": abi.TransformVariable("Lid.Ctrl", "LOC_Z"),
                    },
                )

            # Iris and pupil scale drivers retain the original computed float strings.
            for side in definitions.SIDES:
                for index in (0, 2):
                    abi.driver(
                        rig,
                        f"j_f_irisprm_{side.source}",
                        "scale",
                        index=index,
                        expression="1 + (0.30000000000000004 * var if var < 0 else 0.5 * var)",
                        variables={"var": abi.TransformVariable("Iris.Ctrl", "LOC_Z")},
                    )
                abi.driver(
                    rig,
                    f"j_f_irisprm_{side.source}",
                    "scale",
                    index=1,
                    expression="1 + (0.5 * var if var < 0 else 1.2999999999999998 * var)",
                    variables={"var": abi.TransformVariable("Pupil.Ctrl", "LOC_Z")},
                )

            # The iris shader reads these mesh properties to undo the scale of the iris bone.
            meshes = object_utils.find_by_armature_and_material_property(
                rig.data.rigify_target_rig or rig, "ShaderPackage", "iris.shpk"
            )
            iris_mesh = meshes[0] if meshes else None
            if iris_mesh:
                abi.object_driver(
                    rig,
                    iris_mesh,
                    '["Eye Scale X"]',
                    expression="1/iris",
                    variables={"iris": abi.TransformVariable("j_f_irisprm_l", "SCALE_X")},
                )
                abi.object_driver(
                    rig,
                    iris_mesh,
                    '["Eye Scale Y"]',
                    expression="1/iris",
                    variables={"iris": abi.TransformVariable("j_f_irisprm_l", "SCALE_Z")},
                )
                abi.object_driver(
                    rig,
                    iris_mesh,
                    '["Pupil Scale"]',
                    expression="iris-1",
                    variables={"iris": abi.TransformVariable("j_f_irisprm_l", "SCALE_Y")},
                )
