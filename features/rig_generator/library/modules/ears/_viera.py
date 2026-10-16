"""Viera ears shared by every ear variant; a variant only sets the bone prefix."""

import bpy

from .... import definitions
from .... import instructions as abi


class VieraEars(definitions.RigModule):
    prefix = ""

    # ------------------------------------------------------------------------

    def meta_edit(self, rig: bpy.types.Object) -> None:
        for side in definitions.SIDES:
            # Ear chain
            abi.connect(
                rig,
                f"V_Ear{side.suffix}",
                f"{self.prefix}_a_{side.source}",
                f"{self.prefix}_b_{side.source}",
                parent=["Head", "j_kao"],
            )
            abi.connect(
                rig,
                f"V_Ear{side.suffix}.001",
                f"{self.prefix}_b_{side.source}",
                f"{self.prefix}_b_{side.source}",
                start_point="head",
                end_point="tail",
                parent=f"V_Ear{side.suffix}",
                connected=True,
            )

    # ------------------------------------------------------------------------

    def meta_pose(self, rig: bpy.types.Object) -> None:
        for side in definitions.SIDES:
            # Ear controls
            abi.rigify.basic_copy_chain(rig, f"V_Ear{side.suffix}")
            abi.collection(rig, [f"V_Ear{side.suffix}", f"V_Ear{side.suffix}.001"], "Head")

            # Source-to-deform mappings
            abi.link(rig, f"{self.prefix}_a_{side.source}", f"DEF-V_Ear{side.suffix}")
            abi.link(rig, f"{self.prefix}_b_{side.source}", f"DEF-V_Ear{side.suffix}.001")
