"""Male and female IVCS genitals together."""

import bpy

from ....definitions import RigModule
from ....rigify.settings import UI_Collections
from .ffxiv_ivcs_female import Module as FemaleGenitals
from .ffxiv_ivcs_male import Module as MaleGenitals


class Module(RigModule):
    name = "XIV-IVCS Both"
    ui_collections = UI_Collections(
        [
            *MaleGenitals.ui_collections.collections,
            *FemaleGenitals.ui_collections.collections,
        ]
    )

    def __init__(self) -> None:
        self.parts = [FemaleGenitals(), MaleGenitals()]

    def meta_edit(self, rig: bpy.types.Object) -> None:
        for part in self.parts:
            part.meta_edit(rig)

    def meta_pose(self, rig: bpy.types.Object) -> None:
        for part in self.parts:
            part.meta_pose(rig)

    def final_edit(self, rig: bpy.types.Object) -> None:
        for part in self.parts:
            part.final_edit(rig)

    def final_pose(self, rig: bpy.types.Object) -> None:
        for part in self.parts:
            part.final_pose(rig)
