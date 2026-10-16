"""Miqo'te ears: one controllable bone per ear."""

import bpy

from ....definitions import RigModule
from ....instructions import *
from ....rigify.settings import BoneCollection, UI_Collections

HEAD_COLLECTION = "Head"


class Module(RigModule):
    name = "XIV-Miqo"
    ui_collections = UI_Collections(
        [
            BoneCollection(name=HEAD_COLLECTION, ui=True, color_set="Head", row_index=0, title="Head", visible=True),
        ]
    )

    def meta_edit(self, rig: bpy.types.Object) -> None:
        extend(rig, "Ear.R", "j_mimi_r", start_point="head", roll=150, parent=["Head", "j_kao"])
        extend(rig, "Ear.L", "j_mimi_l", start_point="head", roll=-150, parent=["Head", "j_kao"])

    def meta_pose(self, rig: bpy.types.Object) -> None:
        for ear in ["Ear.R", "Ear.L"]:
            rigify.basic_super_copy(rig, ear, widget_type="bone")
            collection(rig, [ear], HEAD_COLLECTION)

        link(rig, "j_mimi_r", "DEF-Ear.R")
        link(rig, "j_mimi_l", "DEF-Ear.L")
