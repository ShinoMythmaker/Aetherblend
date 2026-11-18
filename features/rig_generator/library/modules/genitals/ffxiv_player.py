"""FFXIV player genital controls selected by sex and IVCS mode."""

import bpy

from .... import definitions
from . import _female, _male


class Module(definitions.RigModule):
    """Build only the selected anatomy when IVCS is enabled."""

    name = "FFXIV Player Genitals"

    def __init__(self) -> None:
        self.parts: list[definitions.RigModule] = []

    # ------------------------------------------------------------------------

    def meta_edit(self, rig: bpy.types.Object) -> None:
        """Select anatomy once and build only the requested genital controls."""
        self.parts = []
        if self.toggles is None:
            raise ValueError(f"{self.name} requires template toggles")
        if self.toggles.ivcs == "OFF":
            return
        sex = self.toggles.sex
        if sex == "OFF":
            return
        if sex not in {"FEMALE", "MALE"}:
            raise ValueError(f"Unknown sex mode: {sex}")
        if sex == "FEMALE":
            self.parts.append(_female.Module())
        if sex == "MALE":
            self.parts.append(_male.Module())
        for part in self.parts:
            part.toggles = self.toggles
            part.meta_edit(rig)

    # ------------------------------------------------------------------------

    def meta_pose(self, rig: bpy.types.Object) -> None:
        """Configure only the anatomy selected during meta editing."""
        for part in self.parts:
            part.meta_pose(rig)

    # ------------------------------------------------------------------------

    def final_edit(self, rig: bpy.types.Object) -> None:
        """Apply final hierarchy changes only to the selected anatomy."""
        for part in self.parts:
            part.final_edit(rig)

    # ------------------------------------------------------------------------

    def final_pose(self, rig: bpy.types.Object) -> None:
        """Configure widgets only for the selected anatomy."""
        for part in self.parts:
            part.final_pose(rig)
