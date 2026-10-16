"""Face module: brows, cheeks, nose, nostrils and eyes as skin chains."""
from typing import NamedTuple

import bpy

from ......utils import object as object_utils
from ....instructions import *
from ....module import RigModule
from ....rigify.settings import BoneCollection, UI_Collections

PRIMARY = "Face (Primary)"
SECONDARY = "Face (Secondary)"
SCALE_ALL = [True, True, True, True]

OCCLUSION_SHADER = "characterocclusion.shpk"
IRIS_SHADER = "iris.shpk"
SLIDER_COLOR = (0.443137, 0.541176, 1.0)
LID_COLOR = (1.0, 0.435294, 0.733333)
IRIS_RANGE = (0.7, 1.5)
PUPIL_RANGE = (0.5, 2.3)
LID_EXPRESSION = "min(1, max(0, (-y / 1) - max(0, {x} / 0.667)))"


class Side(NamedTuple):
    """Naming of one face side."""

    suffix: str
    source: str


RIGHT = Side(".R", "r")
LEFT = Side(".L", "l")
SIDES = (RIGHT, LEFT)

# Lid bone numbers 001..003 and the source bone each one follows.
UPPER_LID_SOURCES = ("j_f_mabup_02out", "j_f_mabup_01", "j_f_mabup_03in")
LOWER_LID_SOURCES = ("j_f_mabdn_03in", "j_f_mabdn_01", "j_f_mabdn_02out")
LID_BRIDGES = (
    # (name, start, end, left offset, whether the end bone attaches to the bridge); the right side mirrors x of lower bridges
    ("T.001", "T", "T.002", (0.0, -0.001, 0.001), True),
    ("T.003", "T.002", "B", (0.0, 0.0, 0.003), False),
    ("B.001", "B", "B.002", (-0.002, 0.0, 0.001), True),
    ("B.003", "B.002", "T", (0.003, -0.001, -0.003), False),
)


class Side(NamedTuple):
    """Naming of one face side."""

    suffix: str
    source: str


RIGHT = Side(".R", "r")
LEFT = Side(".L", "l")
SIDES = (RIGHT, LEFT)


class Module(RigModule):
    name = "XIV-Default"
    ui_flags = ["Eye Lid Edit Mode"]
    ui_collections = UI_Collections([
        BoneCollection(name="Head", ui=True, color_set="Head", row_index=1, title="Head"),
        BoneCollection(name=PRIMARY, ui=True, color_set="Face_Primary", row_index=2, title=PRIMARY, visible=True),
        BoneCollection(name=SECONDARY, ui=True, color_set="Face_Secondary", row_index=2, title=SECONDARY, visible=False),
        BoneCollection(name="Eyes (Macro)", ui=True, color_set="Face_Primary", row_index=3, title="Eyes (Macro)", visible=True),
    ])

    def meta_edit(self, rig: bpy.types.Object) -> None:
        for side in SIDES:
            self._brow_edit(rig, side)
        for side in SIDES:
            self._cheek_edit(rig, side)

        center(rig, "NoseRef", ["j_f_miken_02_r", "j_f_miken_02_l"], axis="Z", parent="Head")
        connect(rig, "Nose", "j_f_uhana", "NoseRef", parent="Head")
        extend(rig, "Face.Suppressor", "NoseRef", axis="Y", start_point="head", parent="Head")

        for side in SIDES:
            self._nose_edit(rig, side)

        occlusion_mesh = self._find_mesh(rig, OCCLUSION_SHADER)
        if occlusion_mesh:
            for side in SIDES:
                self._eye_edit(rig, side, occlusion_mesh)
            self._eye_controls_edit(rig)
        else:
            print("[AetherBlend] No eye occlusion mesh found; the eyes are skipped.")

    def meta_pose(self, rig: bpy.types.Object) -> None:
        for side in SIDES:
            self._brow_pose(rig, side)
            self._cheek_pose(rig, side)
            self._nose_pose(rig, side)
            if f"Eye{side.suffix}" in rig.pose.bones:
                self._eye_pose(rig, side)
        if "Iris.Ctrl" in rig.pose.bones:
            self._eye_controls_pose(rig)

        rigify.skin_basic_chain(rig, "Nose", chain_priority=2, control_orientation_bone="Head", use_scale=SCALE_ALL)
        collection(rig, ["Nose"], PRIMARY)
        link(rig, "j_f_uhana", "DEF-Nose")

        rigify.skin_anchor(rig, "Face.Suppressor", hide=True)
        collection(rig, ["Face.Suppressor", "NoseRef"], "MCH")

    def final_edit(self, rig: bpy.types.Object) -> None:
        for control in ("Iris", "Pupil", "Lid"):
            if has_bone(rig, f"{control}.Ctrl.Master"):
                parent(rig, f"{control}.Ctrl.Master", "head")
                parent(rig, f"{control}.Ctrl", f"{control}.Ctrl.Master")

    def final_pose(self, rig: bpy.types.Object) -> None:
        prop(rig, "head", "head_follow", 1)

        widget(rig, "Nose", scale_factor=0.6)
        for side in SIDES:
            widget(rig, f"Cheek.T{side.suffix}", scale_factor=0.6)
            widget(rig, f"Cheek.B{side.suffix}.001", scale_factor=0.4)
            widget(rig, f"Cheek.B{side.suffix}", scale_factor=0.7)
            widget(rig, f"Nose{side.suffix}", scale_factor=1.0)
            widget(rig, f"Nostril{side.suffix}", scale_factor=0.6)

        if "Iris.Ctrl" in rig.pose.bones:
            self._eye_controls_final_pose(rig)

    @staticmethod
    def _find_mesh(rig: bpy.types.Object, shader: str) -> bpy.types.Object | None:
        """The first mesh deformed by the character's armature that uses the given shader package."""
        original = rig.data.rigify_target_rig or rig
        meshes = object_utils.find_by_armature_and_material_property(original, "ShaderPackage", shader)
        return meshes[0] if meshes else None

    @staticmethod
    def _eye_edit(rig: bpy.types.Object, side: Side, occlusion_mesh: bpy.types.Object) -> None:
        s, x = side.source, side.suffix
        source_rig = rig.data.rigify_target_rig
        eye = f"Eye{x}"

        # Lid corners and centers sit on the eye occlusion mesh where each source bone weighs the most.
        for lid, source in ((f"lid.T{x}", UPPER_LID_SOURCES[0]), (f"lid.T{x}.002", UPPER_LID_SOURCES[1]),
                            (f"lid.B{x}", LOWER_LID_SOURCES[0]), (f"lid.B{x}.002", LOWER_LID_SOURCES[1])):
            heaviest_vertex(rig, lid, f"{source}_{s}", occlusion_mesh, source_rig=source_rig)

        copy(rig, eye, f"j_f_eyepuru_{s}", parent="Head")

        mirror = -1.0 if side is RIGHT else 1.0
        for name, start, end, (offset_x, offset_y, offset_z), connect_end in LID_BRIDGES:
            bridge(
                rig,
                f"lid.{name[0]}{x}{name[1:]}",
                f"lid.{start[0]}{x}{start[1:]}",
                f"lid.{end[0]}{x}{end[1:]}",
                offset=(offset_x * mirror, offset_y, offset_z),
                start_parent=eye if connect_end else None,
                connect_end=connect_end,
            )

        for sources, row in ((LOWER_LID_SOURCES, "B"), (UPPER_LID_SOURCES, "T")):
            for index, source in enumerate(sources, start=1):
                connect(rig, f"eye_tracker.{row}{x}.00{index}", f"{source}_{s}", f"lid.{row}{x}.00{index}", parent=eye)

        connect(rig, f"Lower.Lid{x}.Glue", f"lid.B{x}.002", f"j_f_hoho_{s}", parent="Head")
        connect(rig, f"Upper.Lid{x}.Glue", f"lid.T{x}.002", f"j_f_miken_02_{s}", parent="Head")

    @staticmethod
    def _eye_pose(rig: bpy.types.Object, side: Side) -> None:
        s, x = side.source, side.suffix
        rigify.skin_stretchy_chain(
            rig,
            f"lid.T{x}",
            pivot_position=2,
            control_orientation_bone="Head",
            falloff=[0.0, 1.0, 0.0],
            falloff_length=True,
            falloff_spherical=[False, False, False],
            primary_collection=PRIMARY,
        )
        rigify.skin_stretchy_chain(rig, f"lid.B{x}", pivot_position=2, control_orientation_bone="Head", primary_collection=PRIMARY)
        rigify.face_skin_eye(rig, f"Eye{x}")
        collection(rig, [f"Eye{x}"], PRIMARY)

        lids = [f"lid.{row}{x}{number}" for row in "TB" for number in ("", ".001", ".002", ".003")]
        collection(rig, lids, SECONDARY)

        trackers = [f"eye_tracker.{row}{x}.00{index}" for row in "BT" for index in (1, 2, 3)]
        for tracker in trackers:
            rigify.skin_basic_chain(rig, tracker)
        collection(rig, trackers, "Face")

        glue_bones = [f"Lower.Lid{x}.Glue", f"Upper.Lid{x}.Glue"]
        for glue_bone in glue_bones:
            rigify.skin_glue(
                rig,
                glue_bone,
                relink_constraints=True,
                use_tail=True,
                reparent_tail=True,
                add_constraint="COPY_LOCATION_OWNER",
                add_constraint_influence=0.1,
            )
        collection(rig, glue_bones, "MCH")

        for row, sources in (("B", LOWER_LID_SOURCES), ("T", UPPER_LID_SOURCES)):
            for index, source in enumerate(sources, start=1):
                link(rig, f"{source}_{s}", f"lid.{row}{x}.00{index}")
        link(rig, f"j_f_eyepuru_{s}", f"MCH-Eye{x}")

    @staticmethod
    def _eye_controls_edit(rig: bpy.types.Object) -> None:
        for name, source_height in (("Iris", 0.051), ("Pupil", 0.058)):
            for bone in (f"{name}.Ctrl.Master", f"{name}.Ctrl"):
                offset(rig, bone, "Eye.L", (0.0025, 0.015, source_height), parent="Eye.L")
        for bone in ("Lid.Ctrl.Master", "Lid.Ctrl"):
            offset(rig, bone, "Eye.L", (0.01, 0.015, 0.035), parent="Eye.L")

        for side in SIDES:
            for number in (1, 2, 3):
                lid = f"lid.B{side.suffix}.00{number}"
                extend(rig, f"lid.anchor.B{side.suffix}.00{number}", lid, axis="Z", axis_space="global", start_point="head", parent=lid)

    @staticmethod
    def _eye_controls_pose(rig: bpy.types.Object) -> None:
        controls = [f"{name}.Ctrl{part}" for name in ("Iris", "Pupil", "Lid") for part in (".Master", "")]
        for control in controls:
            rigify.basic_raw_copy(rig, control)
        collection(rig, controls, "Eyes (Macro)")

        anchors = [f"lid.anchor.B{side.suffix}.00{number}" for side in SIDES for number in (1, 2, 3)]
        for anchor in anchors:
            rigify.basic_raw_copy(rig, anchor)
        collection(rig, anchors, "Eyes_Anchors")

    @staticmethod
    def _eye_controls_final_pose(rig: bpy.types.Object) -> None:
        frames = (
            ("Iris.Ctrl.Master", "IrisSliderFrame", (90.0, -90.0, 180.0), SLIDER_COLOR, 0.007),
            ("Pupil.Ctrl.Master", "PupilSliderFrame", (90.0, -90.0, 180.0), SLIDER_COLOR, 0.007),
            ("Lid.Ctrl.Master", "EyeTriangle", (90.0, 0.0, 0.0), LID_COLOR, 0.015),
        )
        for bone, shape, rotation, color, size in frames:
            widget(
                rig, bone, widget_name=shape, rotation_degrees=rotation, wire_width=1.2, scale_to_bone_length=False,
                color_set="CUSTOM", custom_color_normal=color, custom_color_select=color, custom_color_active=color,
            )
            pose(rig, bone, scale=(size, size, size))
            restrict(rig, bone, lock_location=True, lock_rotation=True, lock_scale=True, hide_select=True)

        for bone in ("Iris.Ctrl", "Pupil.Ctrl"):
            widget(rig, bone, widget_name="Slider", rotation_degrees=(90.0, -90.0, 180.0), wire_width=1.3, scale_to_bone_length=False)
            restrict(rig, bone, lock_location=(True, True, False), lock_rotation=True, lock_scale=True)
            constraints.limit_location(rig, bone, minimum=(None, None, -1.0), maximum=(None, None, 1.0), use_transform_limit=True)

        widget(rig, "Lid.Ctrl", widget_name="Circle", rotation_degrees=(180.0, 90.0, 90.0), scale=(0.08, 0.08, 0.08), wire_width=1.3, scale_to_bone_length=False)
        restrict(rig, "Lid.Ctrl", lock_location=(False, True, False), lock_rotation=True, lock_scale=True)
        constraints.limit_location(
            rig, "Lid.Ctrl", minimum=(-0.667, None, -1.0), maximum=(0.667, None, 0.0), use_transform_limit=True,
        )

        for side in SIDES:
            for number in (1, 2, 3):
                anchor = f"lid.anchor.B{side.suffix}.00{number}"
                widget(rig, anchor, widget_name="Pointer", color_set="THEME01", wire_width=2.0)
                restrict(rig, anchor, lock_rotation=True, lock_scale=True, inherit_rotation=False, inherit_scale="NONE")

            # Closing the eye with Lid.Ctrl pulls the upper lid onto the matching lower anchor.
            x_term = "x" if side is LEFT else "-x"
            for upper, anchor_number in ((3, 1), (2, 2), (1, 3)):
                lid = f"lid.T{side.suffix}.00{upper}"
                constraints.copy_location(
                    rig, lid, f"lid.anchor.B{side.suffix}.00{anchor_number}",
                    name="AB_EyeLidControl", target_space="POSE", owner_space="POSE", influence=0.0,
                )
                driver(
                    rig, lid, "influence", constraint="AB_EyeLidControl",
                    expression=LID_EXPRESSION.format(x=x_term),
                    variables={
                        "x": TransformVariable("Lid.Ctrl", "LOC_X"),
                        "y": TransformVariable("Lid.Ctrl", "LOC_Z"),
                    },
                )

        for side in SIDES:
            iris = f"j_f_irisprm_{side.source}"
            iris_minimum, iris_maximum = IRIS_RANGE
            pupil_minimum, pupil_maximum = PUPIL_RANGE
            iris_expression = f"1 + ({1 - iris_minimum} * var if var < 0 else {iris_maximum - 1} * var)"
            pupil_expression = f"1 + ({1 - pupil_minimum} * var if var < 0 else {pupil_maximum - 1} * var)"
            for index in (0, 2):
                driver(rig, iris, "scale", index=index, expression=iris_expression, variables={"var": TransformVariable("Iris.Ctrl", "LOC_Z")})
            driver(rig, iris, "scale", index=1, expression=pupil_expression, variables={"var": TransformVariable("Pupil.Ctrl", "LOC_Z")})

        # The iris shader reads these properties from the iris mesh to undo the scale of the iris bone.
        iris_mesh = Module._find_mesh(rig, IRIS_SHADER)
        if iris_mesh:
            for property_name, expression, channel in (
                ("Eye Scale X", "1/iris", "SCALE_X"),
                ("Eye Scale Y", "1/iris", "SCALE_Z"),
                ("Pupil Scale", "iris-1", "SCALE_Y"),
            ):
                object_driver(
                    rig, iris_mesh, f'["{property_name}"]',
                    expression=expression,
                    variables={"iris": TransformVariable("j_f_irisprm_l", channel)},
                )

    @staticmethod
    def _brow_edit(rig: bpy.types.Object, side: Side) -> None:
        s = side.source
        brow = f"Brow{side.suffix}"
        connect(rig, brow, f"j_f_mayu_{s}", f"j_f_mmayu_{s}", parent="Head")
        connect(rig, f"{brow}.001", f"j_f_mmayu_{s}", f"j_f_miken_01_{s}", parent=brow, connected=True)
        connect(rig, f"{brow}.002", f"j_f_miken_01_{s}", f"j_f_miken_02_{s}", parent=f"{brow}.001", connected=True)
        extend(rig, f"{brow}.003", f"{brow}.002", axis="Y", parent=f"{brow}.002", connected=True)

    @staticmethod
    def _brow_pose(rig: bpy.types.Object, side: Side) -> None:
        s = side.source
        brow = f"Brow{side.suffix}"
        rigify.skin_stretchy_chain(
            rig,
            brow,
            control_orientation_bone="Head",
            falloff_length=True,
            use_scale=SCALE_ALL,
            primary_collection=PRIMARY,
        )
        collection(rig, [brow], SECONDARY)
        collection(rig, [f"{brow}.001", f"{brow}.002", f"{brow}.003"], PRIMARY)

        link(rig, f"j_f_mayu_{s}", f"DEF-{brow}")
        link(rig, f"j_f_mmayu_{s}", f"DEF-{brow}.001")
        link(rig, f"j_f_miken_01_{s}", f"DEF-{brow}.002")
        link(rig, f"j_f_miken_02_{s}", f"DEF-{brow}.003")

    @staticmethod
    def _cheek_edit(rig: bpy.types.Object, side: Side) -> None:
        s, x = side.source, side.suffix
        center(rig, f"Corner{x}", [f"j_f_uslip_{s}", f"j_f_dslip_{s}", f"j_f_shoho_{s}"], axis="Y", parent="Head")
        connect(rig, f"Cheek{x}", f"Corner{x}", f"j_f_shoho_{s}", parent="Head")
        connect(rig, f"Cheek.B{x}", f"j_f_shoho_{s}", f"j_f_hoho_{s}", parent=f"Cheek{x}", connected=True)
        connect(rig, f"Cheek.B{x}.001", f"j_f_dhoho_{s}", f"j_f_hoho_{s}", parent="Head")
        connect(rig, f"Cheek.T{x}", f"j_f_hoho_{s}", f"j_f_dmemoto_{s}", parent="Head")
        connect(rig, f"Cheek.T{x}.001", f"j_f_dmemoto_{s}", f"j_f_hana_{s}", parent="Head")

    @staticmethod
    def _cheek_pose(rig: bpy.types.Object, side: Side) -> None:
        s, x = side.source, side.suffix
        rigify.skin_stretchy_chain(
            rig,
            f"Cheek{x}",
            control_orientation_bone="Head",
            falloff_length=True,
            use_scale=SCALE_ALL,
            primary_collection=PRIMARY,
        )
        for chain in (f"Cheek.B{x}.001", f"Cheek.T{x}", f"Cheek.T{x}.001"):
            rigify.skin_basic_chain(rig, chain, control_orientation_bone="Head", use_scale=SCALE_ALL)

        collection(rig, [f"Cheek{x}", f"Cheek.B{x}", f"Cheek.T{x}"], PRIMARY)
        collection(rig, [f"Cheek.B{x}.001", f"Cheek.T{x}.001"], SECONDARY)
        collection(rig, [f"Corner{x}"], "MCH")

        link(rig, f"j_f_shoho_{s}", f"DEF-Cheek.B{x}")
        link(rig, f"j_f_dhoho_{s}", f"DEF-Cheek.B{x}.001")
        link(rig, f"j_f_hoho_{s}", f"DEF-Cheek.T{x}")
        link(rig, f"j_f_dmemoto_{s}", f"DEF-Cheek.T{x}.001")

    @staticmethod
    def _nose_edit(rig: bpy.types.Object, side: Side) -> None:
        s, x = side.source, side.suffix
        connect(rig, f"Nose{x}", f"j_f_dmiken_{s}", f"Brow{x}.003", end_point="tail", parent="Head")
        connect(rig, f"Nostril{x}", f"j_f_hana_{s}", "j_f_uhana", parent="Head")

        # Glue bones keep the nostrils and cheeks following the surrounding chains.
        connect(rig, f"Nostril.Glue{x}", f"j_f_hana_{s}", "j_f_uhana", parent="Head")
        connect(rig, f"Nostril.Glue{x}.001", f"Cheek.T{x}.001", f"Nostril{x}", parent="Head")
        connect(rig, f"Cheek.B{x}.glue", f"j_f_dhoho_{s}", f"j_f_shoho_{s}", parent="Head")
        connect(rig, f"Cheek.T{x}.glue", f"j_f_dhoho_{s}", f"j_f_hoho_{s}", parent="Head")

    @staticmethod
    def _nose_pose(rig: bpy.types.Object, side: Side) -> None:
        s, x = side.source, side.suffix
        rigify.skin_basic_chain(rig, f"Nose{x}", control_orientation_bone="Head", use_scale=SCALE_ALL)
        rigify.skin_basic_chain(rig, f"Nostril{x}", chain_priority=1, control_orientation_bone="Head", use_scale=SCALE_ALL)
        collection(rig, [f"Nose{x}", f"Nostril{x}"], PRIMARY)

        link(rig, f"j_f_dmiken_{s}", f"DEF-Nose{x}")
        link(rig, f"j_f_hana_{s}", f"DEF-Nostril{x}")

        glue_bones = [f"Nostril.Glue{x}", f"Nostril.Glue{x}.001", f"Cheek.B{x}.glue", f"Cheek.T{x}.glue"]
        for glue_bone in glue_bones:
            rigify.skin_glue(
                rig,
                glue_bone,
                relink_constraints=True,
                use_tail=True,
                reparent_tail=glue_bone == f"Cheek.B{x}.glue",
                add_constraint="COPY_LOCATION_OWNER",
                add_constraint_influence=0.5,
            )
        collection(rig, glue_bones, "MCH")
