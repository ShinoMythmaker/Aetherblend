"""Viera ears shared by every ear variant; a variant only sets the bone prefix."""

import bpy

from ....definitions import RigModule
from ....instructions import *

HEAD_COLLECTION = "Head"
SIDES = (".R", ".L")


class VieraEars(RigModule):
    prefix = ""

    def meta_edit(self, rig: bpy.types.Object) -> None:
        for suffix in SIDES:
            lower, upper = (f"{self.prefix}_a_{suffix[1].lower()}", f"{self.prefix}_b_{suffix[1].lower()}")
            connect(rig, f"V_Ear{suffix}", lower, upper, parent=["Head", "j_kao"])
            connect(
                rig,
                f"V_Ear{suffix}.001",
                upper,
                upper,
                start_point="head",
                end_point="tail",
                parent=f"V_Ear{suffix}",
                connected=True,
            )

    def meta_pose(self, rig: bpy.types.Object) -> None:
        for suffix in SIDES:
            side = suffix[1].lower()
            rigify.basic_copy_chain(rig, f"V_Ear{suffix}")
            collection(rig, [f"V_Ear{suffix}", f"V_Ear{suffix}.001"], HEAD_COLLECTION)

            link(rig, f"{self.prefix}_a_{side}", f"DEF-V_Ear{suffix}")
            link(rig, f"{self.prefix}_b_{side}", f"DEF-V_Ear{suffix}.001")
