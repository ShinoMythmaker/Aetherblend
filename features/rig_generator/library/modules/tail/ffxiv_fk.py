"""Tail module: a chain of FK controls following the tail bones."""

import bpy

from .... import definitions
from .... import instructions as abi
from ....rigify import settings


class Module(definitions.RigModule):
    name = "XIV-FK"
    requires = [
        "n_sippo_a",
        "n_sippo_b",
        "n_sippo_c",
        "n_sippo_d",
        "n_sippo_e",
    ]
    ui_collections = settings.UI_Collections(
        [
            settings.BoneCollection(name="Tail", ui=True, color_set="Torso_Tweak", row_index=1, title="Tail"),
        ]
    )

    # ------------------------------------------------------------------------

    def meta_edit(self, rig: bpy.types.Object) -> None:
        # Tail chain
        abi.connect(rig, "Tail", "n_sippo_a", "n_sippo_b", parent=["Spine.001", "j_kosi"])
        abi.connect(rig, "Tail.001", "n_sippo_b", "n_sippo_c", parent="Tail", connected=True)
        abi.connect(rig, "Tail.002", "n_sippo_c", "n_sippo_d", parent="Tail.001", connected=True)
        abi.connect(rig, "Tail.003", "n_sippo_d", "n_sippo_e", parent="Tail.002", connected=True)
        abi.extend(rig, "Tail.004", "Tail.003", parent="Tail.003", connected=True)

    # ------------------------------------------------------------------------

    def meta_pose(self, rig: bpy.types.Object) -> None:
        # Tail controls
        abi.rigify.basic_copy_chain(rig, "Tail")
        abi.collection(rig, ["Tail", "Tail.001", "Tail.002", "Tail.003", "Tail.004"], "Tail")

        # Source-to-deform mappings
        abi.link(rig, "n_sippo_a", "DEF-Tail")
        abi.link(rig, "n_sippo_b", "DEF-Tail.001")
        abi.link(rig, "n_sippo_c", "DEF-Tail.002")
        abi.link(rig, "n_sippo_d", "DEF-Tail.003")
        abi.link(rig, "n_sippo_e", "DEF-Tail.004")

    # ------------------------------------------------------------------------

    def final_pose(self, rig: bpy.types.Object) -> None:
        # Tail widgets
        abi.widget(rig, "Tail-end", scale_factor=0.5)
        abi.widget(rig, "Tail-end01", scale_factor=0.5)
        abi.widget(rig, "Tail-mid01", scale_factor=0.5)
        abi.widget(rig, "Tail-start01", scale_factor=0.5)
        abi.widget(rig, "Tail-master", scale_factor=0.5)
