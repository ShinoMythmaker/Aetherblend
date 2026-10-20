"""Miqo'te and Viera ear controls selected by the template's ears property."""

import bpy

from .... import definitions
from .... import instructions as abi

_PREFIXES = {"A": "j_zera", "B": "j_zerb", "C": "j_zerc", "D": "j_zerd"}


class Module(definitions.RigModule):
    """Build only the selected ear style, checking its source bones locally."""

    name = "FFXIV Player Ears"
    _enabled: bool = False
    _default_enabled: bool = False
    _viera_enabled: bool = False
    _prefix: str = ""

    def meta_edit(self, rig: bpy.types.Object) -> None:
        """Create default controls and, when selected, two-bone Viera chains."""
        self._enabled = self._default_enabled = self._viera_enabled = False
        self._prefix = ""
        if self.toggles is None:
            raise ValueError(f"{self.name} requires template toggles with an ears property")
        for side in definitions.SIDES:
            abi.extend(rig,
                f"EarRing_A{side.suffix}",
                f"n_ear_a_{side.source}",
                start_point="head",
                axis="-X",
                parent=["Head", "j_kao"]                
            )
            abi.extend(rig,
                f"EarRing_B{side.suffix}",
                f"n_ear_b_{side.source}",
                start_point="head",
                axis="-X",
                parent=["EarRing_A{side.suffix}", f"n_ear_a_{side.source}"]
            )
        if self.toggles.ears == "NONE":
            return
        if self.toggles.ears not in {"DEFAULT", "VIERA"}:
            raise ValueError(f"Unknown ear style: {self.toggles.ears}")
        if self.toggles.ears == "VIERA":
            if self.toggles.viera_variant not in _PREFIXES:
                raise ValueError(f"Unknown Viera variant: {self.toggles.viera_variant}")
            self._prefix = _PREFIXES[self.toggles.viera_variant]
            sources = [f"{self._prefix}_{segment}_{side.source}" for side in definitions.SIDES for segment in "ab"]
            self._viera_enabled = abi.require_bones(rig, sources, f"{self.name} (Viera {self.toggles.viera_variant})")
        default_sources = [f"j_mimi_{side.source}" for side in definitions.SIDES]
        if self.toggles.ears == "DEFAULT" or any(name in rig.data.edit_bones for name in default_sources):
            self._default_enabled = abi.require_bones(rig, default_sources, f"{self.name} (Default)")
        self._enabled = self._default_enabled or self._viera_enabled

        for side in definitions.SIDES:
            if self._viera_enabled:
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
            if self._default_enabled:
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
        for side in definitions.SIDES:
            abi.rigify.basic_super_copy(rig, f"EarRing_A{side.suffix}", widget_type="bone"),
            abi.collection(rig, [f"EarRing_A{side.suffix}"], "Accessory"),
            abi.link(rig, f"n_ear_a_{side.source}", f"DEF-EarRing_A{side.suffix}")
            abi.rigify.basic_super_copy(rig, f"EarRing_B{side.suffix}", widget_type="bone"),
            abi.collection(rig, [f"EarRing_B{side.suffix}"], "Accessory"),
            abi.link(rig, f"n_ear_b_{side.source}", f"DEF-EarRing_B{side.suffix}")
        if not self._enabled:
            return
        for side in definitions.SIDES:
            if self._viera_enabled:
                abi.rigify.basic_copy_chain(rig, f"V_Ear{side.suffix}")
                abi.collection(rig, [f"V_Ear{side.suffix}", f"V_Ear{side.suffix}.001"], "Head")
                abi.link(rig, f"{self._prefix}_a_{side.source}", f"DEF-V_Ear{side.suffix}")
                abi.link(rig, f"{self._prefix}_b_{side.source}", f"DEF-V_Ear{side.suffix}.001")
            if self._default_enabled:
                abi.rigify.basic_super_copy(rig, f"Ear{side.suffix}", widget_type="bone")
                abi.collection(rig, [f"Ear{side.suffix}"], "Head")
                abi.link(rig, f"j_mimi_{side.source}", f"DEF-Ear{side.suffix}")
