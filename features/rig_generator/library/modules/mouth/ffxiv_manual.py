"""Mouth module: manual controls, one plain control per lip, teeth and tongue bone."""

import bpy

from ....definitions import RigModule
from ....instructions import *
from ....rigify.settings import BoneCollection, UI_Collections

PRIMARY = "Face (Primary)"
SECONDARY = "Face (Secondary)"
MISC = "Face (Misc)"
SIDES = ((".R", "r"), (".L", "l"))
ROWS = (
    ("T", "u", ("ulip_01", "umlip_01", "uslip")),
    ("B", "d", ("dlip_01", "dmlip_01", "dslip")),
)
# Inner lip sources (_02), parented to the first two main lip bones of the row.
INNER = {"T": ("ulip_02", "umlip_02"), "B": ("dlip_02", "dmlip_02")}
TONGUE = (("Tongue", "j_f_bero_01"), ("Tongue.001", "j_f_bero_02"), ("Tongue.002", "j_f_bero_03"))


class Module(RigModule):
    name = "XIV-Manual"
    ui_collections = UI_Collections(
        [
            BoneCollection(name=PRIMARY, ui=True, color_set="Face_Primary", row_index=1, title=PRIMARY, visible=True),
            BoneCollection(
                name=SECONDARY, ui=True, color_set="Face_Secondary", row_index=1, title=SECONDARY, visible=False
            ),
            BoneCollection(name=MISC, ui=True, color_set="Face_Secondary", row_index=2, title=MISC, visible=False),
        ]
    )

    def meta_edit(self, rig: bpy.types.Object) -> None:
        center(rig, "jaw_ref", ["j_f_dlip_01_r", "j_f_dlip_01_l"], axis="Y", parent="Head")
        connect(rig, "Jaw", "j_f_ago", "jaw_ref", parent="Head")

        for suffix, source in SIDES:
            for row, _, sources in ROWS:
                parent_bone = "Jaw" if row == "B" else "Head"
                for index, src in enumerate(sources):
                    extend(
                        rig,
                        f"Lip.{row}{suffix}{self._number(index)}",
                        f"j_f_{src}_{source}",
                        axis="Y",
                        start_point="head",
                        size_factor=0.3,
                        parent=parent_bone,
                    )
                for index, src in enumerate(INNER[row]):
                    extend(
                        rig,
                        f"Lip.{row}{suffix}.{index + 3:03d}",
                        f"j_f_{src}_{source}",
                        axis="Y",
                        start_point="head",
                        size_factor=0.3,
                        parent=f"Lip.{row}{suffix}{self._number(index)}",
                    )

        extend(rig, "Teeth.T", "j_f_hagukiup", axis="Y", start_point="head", parent="Head")
        extend(rig, "Teeth.B", "j_f_hagukidn", axis="Y", start_point="head", parent="Jaw")

        for index, (name, source) in enumerate(TONGUE):
            extend(
                rig,
                name,
                source,
                axis="Y",
                start_point="head",
                size_factor=0.3,
                parent="Jaw" if index == 0 else TONGUE[index - 1][0],
            )

    def meta_pose(self, rig: bpy.types.Object) -> None:
        collection(rig, ["jaw_ref"], "MCH")
        rigify.basic_super_copy(rig, "Jaw", widget_type="jaw")
        collection(rig, ["Jaw"], PRIMARY)
        link(rig, "j_f_ago", "DEF-Jaw")

        for suffix, source in SIDES:
            for row, _, sources in ROWS:
                for index, src in enumerate(sources):
                    name = f"Lip.{row}{suffix}{self._number(index)}"
                    rigify.basic_super_copy(rig, name, widget_type="circle")
                    collection(rig, [name], PRIMARY)
                    link(rig, f"j_f_{src}_{source}", f"DEF-{name}")
                for index, src in enumerate(INNER[row]):
                    name = f"Lip.{row}{suffix}.{index + 3:03d}"
                    rigify.basic_super_copy(rig, name, widget_type="circle")
                    collection(rig, [name], SECONDARY)
                    link(rig, f"j_f_{src}_{source}", f"DEF-{name}")

        for name, source in (("Teeth.T", "j_f_hagukiup"), ("Teeth.B", "j_f_hagukidn"), *TONGUE):
            rigify.basic_super_copy(rig, name, widget_type="teeth" if name.startswith("Teeth") else "circle")
            collection(rig, [name], MISC)
            link(rig, source, f"DEF-{name}")

    def final_pose(self, rig: bpy.types.Object) -> None:
        for teeth in ("Teeth.T", "Teeth.B"):
            widget(rig, teeth, rotation_degrees=(0.0, 0.0, 180.0), scale_factor=1.7)

    @staticmethod
    def _number(index: int) -> str:
        return "" if index == 0 else f".{index:03d}"
