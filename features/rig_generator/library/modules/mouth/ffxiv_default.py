"""Mouth module: jaw, lips, teeth and tongue."""
from typing import NamedTuple

import bpy

from ....definitions import RigModule
from ....instructions import *
from ....rigify.settings import BoneCollection, UI_Collections

PRIMARY = "Face (Primary)"
SECONDARY = "Face (Secondary)"
MISC = "Face (Misc)"
SCALE_ALL = [True, True, True, True]


class Side(NamedTuple):
    """Naming of one face side."""

    suffix: str
    source: str


RIGHT = Side(".R", "r")
LEFT = Side(".L", "l")

# Main lip chain per row: the chain's first bone starts at the mouth center, then the source bones follow.
ROWS = (
    ("T", "Mouth.Center", ("ulip_02", "umlip_02", "uslip")),
    ("B", "Mouth.Center.001", ("dlip_02", "dmlip_02", "dslip")),
)
# Secondary lips per row: the source bones of the first and the second bone, each running from the first to the second name.
SECONDARY_LIPS = (
    ("T", ("ulip_01", "umlip_01"), ("umlip_01", "uslip")),
    ("B", ("dlip_01", "dmlip_01"), ("dmlip_01", "dslip")),
)


class Module(RigModule):
    name = "XIV-Automated"
    ui_collections = UI_Collections([
        BoneCollection(name=PRIMARY, ui=True, color_set="Face_Primary", row_index=1, title=PRIMARY, visible=True),
        BoneCollection(name=SECONDARY, ui=True, color_set="Face_Secondary", row_index=1, title=SECONDARY, visible=False),
        BoneCollection(name=MISC, ui=True, color_set="Face_Secondary", row_index=2, title=MISC, visible=False),
    ])

    def meta_edit(self, rig: bpy.types.Object) -> None:
        center(rig, "jaw_master_ref", ["j_f_dlip_01_r", "j_f_dlip_01_l"], axis="Y", parent="Head")
        connect(rig, "jaw_master", "j_f_ago", "jaw_master_ref", parent="Head")

        center(rig, "Mouth.Center", ["j_f_ulip_02_r", "j_f_ulip_02_l"], axis="Z", parent="Head")
        center(rig, "Mouth.Center.001", ["j_f_dlip_02_r", "j_f_dlip_02_l"], axis="Z", parent="Head")

        for side in (RIGHT, LEFT):
            self._lips_edit(rig, side)

        extend(rig, "Teeth.T", "j_f_hagukiup", axis="Y", start_point="head", parent="Head")
        extend(rig, "Teeth.B", "j_f_hagukidn", axis="Y", start_point="head", parent="jaw_master")

        connect(rig, "Tongue", "j_f_bero_01", "j_f_bero_02", parent="jaw_master")
        connect(rig, "Tongue.001", "j_f_bero_02", "j_f_bero_03", parent="Tongue", connected=True)
        extend(rig, "Tongue.002", "Tongue.001", axis="Y", parent="Tongue.001", connected=True)

    def meta_pose(self, rig: bpy.types.Object) -> None:
        rigify.face_skin_jaw(rig, "jaw_master", jaw_mouth_influence=1)
        collection(rig, ["jaw_master"], PRIMARY)
        collection(rig, ["jaw_master_ref", "Mouth.Center", "Mouth.Center.001"], "MCH")
        link(rig, "j_f_ago", "DEF-jaw_master")

        for side in (RIGHT, LEFT):
            self._lips_pose(rig, side)

        for teeth, source in (("Teeth.T", "j_f_hagukiup"), ("Teeth.B", "j_f_hagukidn")):
            rigify.basic_super_copy(rig, teeth, widget_type="teeth")
            collection(rig, [teeth], MISC)
            link(rig, source, f"DEF-{teeth}")

        rigify.skin_stretchy_chain(rig, "Tongue", control_orientation_bone="Mouth.Center")
        collection(rig, ["Tongue", "Tongue.001", "Tongue.002"], MISC)
        for name, source in (("Tongue", "j_f_bero_01"), ("Tongue.001", "j_f_bero_02"), ("Tongue.002", "j_f_bero_03")):
            link(rig, source, f"DEF-{name}")

    def final_edit(self, rig: bpy.types.Object) -> None:
        # The secondary lips follow the offset bones rigify made for the main lips.
        for side in (RIGHT, LEFT):
            for row, _, _ in SECONDARY_LIPS:
                parent(rig, f"Lip.Sec.{row}{side.suffix}", f"MCH-Lip_offset.{row}{side.suffix}.001")
                parent(rig, f"Lip.Sec.{row}{side.suffix}.001", f"MCH-Lip_offset.{row}{side.suffix}.002")

    def final_pose(self, rig: bpy.types.Object) -> None:
        for teeth in ("Teeth.T", "Teeth.B"):
            widget(rig, teeth, rotation_degrees=(0.0, 0.0, 180.0), scale_factor=1.7)
        widget(rig, "jaw_master_mouth", scale=(0.6, 1.0, 0.3))
        for side in (RIGHT, LEFT):
            for row in "TB":
                for suffix in ("", ".001"):
                    widget(rig, f"Lip.Middle.{row}{side.suffix}{suffix}", scale_factor=0.1)

    @staticmethod
    def _lips_edit(rig: bpy.types.Object, side: Side) -> None:
        s, x = side.source, side.suffix
        for row, center_bone, sources in ROWS:
            lip = f"Lip.{row}{x}"
            names = [lip, f"{lip}.001", f"{lip}.002", f"{lip}.003"]
            starts = [center_bone, f"j_f_{sources[0]}_{s}", f"j_f_{sources[1]}_{s}", f"j_f_{sources[2]}_{s}"]
            ends = [f"j_f_{sources[0]}_{s}", f"j_f_{sources[1]}_{s}", f"j_f_{sources[2]}_{s}", f"Corner{x}"]
            for index, (name, start, end) in enumerate(zip(names, starts, ends)):
                connect(
                    rig, name, start, end,
                    parent="jaw_master" if index == 0 else names[index - 1],
                    connected=index > 0,
                )

        for row, first, second in SECONDARY_LIPS:
            lip = f"Lip.Sec.{row}{x}"
            connect(rig, lip, f"j_f_{first[0]}_{s}", f"j_f_{first[1]}_{s}", parent="Head")
            connect(rig, f"{lip}.001", f"j_f_{second[0]}_{s}", f"j_f_{second[1]}_{s}", parent=lip, connected=True)

        connect(rig, f"Lip.T{x}.001.glue", f"j_f_hana_{s}", f"j_f_ulip_01_{s}", parent="Head")

    @staticmethod
    def _lips_pose(rig: bpy.types.Object, side: Side) -> None:
        s, x = side.source, side.suffix
        for row, _, sources in ROWS:
            lip = f"Lip.{row}{x}"
            rigify.skin_stretchy_chain(
                rig,
                lip,
                control_orientation_bone="Mouth.Center",
                falloff_length=True,
                falloff=[0.0, 0.0, -1.0],
                primary_collection=PRIMARY,
                use_scale=SCALE_ALL,
            )
            collection(rig, [lip, f"{lip}.001", f"{lip}.002", f"{lip}.003"], SECONDARY)
            for number, source in enumerate(sources, start=1):
                link(rig, f"j_f_{source}_{s}", f"DEF-{lip}.00{number}")

        for row, first, second in SECONDARY_LIPS:
            lip = f"Lip.Sec.{row}{x}"
            rigify.skin_basic_chain(rig, lip, control_orientation_bone="Mouth.Center")
            collection(rig, [lip, f"{lip}.001"], SECONDARY)
            link(rig, f"j_f_{first[0]}_{s}", f"DEF-{lip}")
            link(rig, f"j_f_{second[0]}_{s}", f"DEF-{lip}.001")

        glue = f"Lip.T{x}.001.glue"
        rigify.skin_glue(
            rig,
            glue,
            relink_constraints=True,
            use_tail=True,
            reparent_tail=True,
            add_constraint="COPY_LOCATION_OWNER",
            add_constraint_influence=0.2,
        )
        collection(rig, [glue], "MCH")
