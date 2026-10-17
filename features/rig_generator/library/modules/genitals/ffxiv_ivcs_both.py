"""Male and female IVCS genitals together."""

import bpy

from .... import definitions
from . import ffxiv_ivcs_female, ffxiv_ivcs_male


class Module(definitions.RigModule):
    name = "XIV-IVCS Both"

    def __init__(self) -> None:
        self.parts = [ffxiv_ivcs_female.Module(), ffxiv_ivcs_male.Module()]

    # ------------------------------------------------------------------------

    def meta_edit(self, rig: bpy.types.Object) -> None:
        for part in self.parts:
            part.meta_edit(rig)

    # ------------------------------------------------------------------------

    def meta_pose(self, rig: bpy.types.Object) -> None:
        for part in self.parts:
            part.meta_pose(rig)

    # ------------------------------------------------------------------------

    def final_edit(self, rig: bpy.types.Object) -> None:
        for part in self.parts:
            part.final_edit(rig)

    # ------------------------------------------------------------------------

    def final_pose(self, rig: bpy.types.Object) -> None:
        for part in self.parts:
            part.final_pose(rig)
