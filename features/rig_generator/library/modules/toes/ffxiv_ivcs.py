"""IVCS toes: five toes per foot with finger-style Rigify controls."""

from typing import NamedTuple

import bpy

from ....definitions import RigModule
from ....instructions import *
from ....rigify.settings import BoneCollection, UI_Collections


class Toe(NamedTuple):
    """A toe's display name and the name used for it in the source bones."""

    name: str
    source: str


TOES = (
    Toe("Hallux", "oya"),
    Toe("Index", "hito"),
    Toe("Middle", "naka"),
    Toe("Ring", "kusu"),
    Toe("Pinky", "ko"),
)
SIDES = (".L", ".R")


class Module(RigModule):
    name = "XIV-IVCS"
    requires = [
        f"iv_asi_{toe.source}_{part}_{side[1].lower()}" for toe in TOES for part in ("a", "b") for side in SIDES
    ]
    ui_collections = UI_Collections(
        [
            BoneCollection(
                name=f"IVCS_Toes{side}", ui=True, color_set="IVCS", row_index=1, title=f"Toes{side}", visible=False
            )
            for side in SIDES
        ]
    )

    def meta_edit(self, rig: bpy.types.Object) -> None:
        for side in SIDES:
            for toe in TOES:
                base = f"{toe.name}_Toe{side}"
                source_base = f"iv_asi_{toe.source}_a_{side[1].lower()}"
                source_tip = f"iv_asi_{toe.source}_b_{side[1].lower()}"
                connect(rig, base, source_base, source_tip, parent=[f"toe{side}", f"j_asi_e_{side[1].lower()}"])
                extend(rig, f"{base}.001", source_tip, parent=base, connected=True)

    def meta_pose(self, rig: bpy.types.Object) -> None:
        for side in SIDES:
            for toe in TOES:
                base = f"{toe.name}_Toe{side}"
                rigify.limbs_super_finger(rig, base)
                collection(rig, [base, f"{base}.001"], f"IVCS_Toes{side}")

                link(rig, f"iv_asi_{toe.source}_a_{side[1].lower()}", f"DEF-{base}")
                link(rig, f"iv_asi_{toe.source}_b_{side[1].lower()}", f"DEF-{base}.001")
