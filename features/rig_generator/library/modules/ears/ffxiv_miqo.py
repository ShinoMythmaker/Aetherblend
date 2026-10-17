"""Miqo'te ears: one controllable bone per ear."""

import bpy

from .... import definitions
from .... import instructions as abi


class Module(definitions.RigModule):
    name = "XIV-Miqo"

    # ------------------------------------------------------------------------

    def meta_edit(self, rig: bpy.types.Object) -> None:
        # Ear bones
        for side in definitions.SIDES:
            abi.extend(
                rig,
                f"Ear{side.suffix}",
                f"j_mimi_{side.source}",
                start_point="head",
                roll=-150 if side is definitions.LEFT else 150,
                parent=["Head", "j_kao"],
            )

    # ------------------------------------------------------------------------

    def meta_pose(self, rig: bpy.types.Object) -> None:
        # Ear controls
        for side in definitions.SIDES:
            abi.rigify.basic_super_copy(rig, f"Ear{side.suffix}", widget_type="bone")
            abi.collection(rig, [f"Ear{side.suffix}"], "Head")
            abi.link(rig, f"j_mimi_{side.source}", f"DEF-Ear{side.suffix}")
