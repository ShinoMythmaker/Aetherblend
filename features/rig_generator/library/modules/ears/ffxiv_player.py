"""Miqo'te and Viera ear controls selected by the template's ears property."""

import bpy

from .... import definitions
from .... import instructions as abi

_PREFIXES = {"DEFAULT": "j_mimi", "VIERA_A": "j_zera", "VIERA_B": "j_zerb", "VIERA_C": "j_zerc", "VIERA_D": "j_zerd"}


class Module(definitions.RigModule):
    """Build only the selected ear style, checking its source bones locally."""

    name = "FFXIV Player Ears"
    _enabled: bool = False
    _prefix: str = ""

    def meta_edit(self, rig: bpy.types.Object) -> None:
        """Create Miqo'te controls or a two-bone Viera chain on each side."""
        if self.toggles is None:
            raise ValueError(f"{self.name} requires template toggles with an ears property")
        self._prefix = _PREFIXES[self.toggles.ears]
        viera = self._prefix != "j_mimi"
        sources = [f"{self._prefix}{segment}_{side.source}" for side in definitions.SIDES for segment in (("_a", "_b") if viera else ("",))]
        self._enabled = abi.require_bones(rig, sources, f"{self.name} ({self.toggles.ears})")
        if not self._enabled:
            return

        for side in definitions.SIDES:
            if viera:
                abi.connect(
                    rig,
                    f"V_Ear{side.suffix}",
                    f"{self._prefix}_a_{side.source}",
                    f"{self._prefix}_b_{side.source}",
                    parent=["Head", "j_kao"],
                )
                abi.connect(
                    rig,
                    f"V_Ear{side.suffix}.001",
                    f"{self._prefix}_b_{side.source}",
                    f"{self._prefix}_b_{side.source}",
                    start_point="head",
                    end_point="tail",
                    parent=f"V_Ear{side.suffix}",
                    connected=True,
                )
            else:
                abi.extend(
                    rig,
                    f"Ear{side.suffix}",
                    f"j_mimi_{side.source}",
                    start_point="head",
                    roll=-150 if side is definitions.LEFT else 150,
                    parent=["Head", "j_kao"],
                )

    def meta_pose(self, rig: bpy.types.Object) -> None:
        """Configure controls and map only the selected ears to deform bones."""
        if not self._enabled:
            return
        for side in definitions.SIDES:
            if self._prefix != "j_mimi":
                abi.rigify.basic_copy_chain(rig, f"V_Ear{side.suffix}")
                abi.collection(rig, [f"V_Ear{side.suffix}", f"V_Ear{side.suffix}.001"], "Head")
                abi.link(rig, f"{self._prefix}_a_{side.source}", f"DEF-V_Ear{side.suffix}")
                abi.link(rig, f"{self._prefix}_b_{side.source}", f"DEF-V_Ear{side.suffix}.001")
            else:
                abi.rigify.basic_super_copy(rig, f"Ear{side.suffix}", widget_type="bone")
                abi.collection(rig, [f"Ear{side.suffix}"], "Head")
                abi.link(rig, f"j_mimi_{side.source}", f"DEF-Ear{side.suffix}")
