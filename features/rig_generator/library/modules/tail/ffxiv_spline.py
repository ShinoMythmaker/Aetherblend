"""Tail module: a spline-driven tail with stretch control."""
from ....instructions import *
from ....module import RigModule
from ....rigify.settings import BoneCollection, UI_Collections

TAIL_COLLECTION = "Tail"


class Module(RigModule):
    name = "XIV-Spline"
    requires = ["n_sippo_a", "n_sippo_b", "n_sippo_c", "n_sippo_d", "n_sippo_e"]
    ui_collections = UI_Collections([
        BoneCollection(name=TAIL_COLLECTION, ui=True, color_set="Torso_Tweak", row_index=1, title="Tail"),
    ])

    def meta_edit(self, rig):
        connect(rig, "Tail", "n_sippo_a", "n_sippo_b", parent=["Spine.001", "j_kosi"])
        connect(rig, "Tail.001", "n_sippo_b", "n_sippo_c", parent="Tail", connected=True)
        connect(rig, "Tail.002", "n_sippo_c", "n_sippo_d", parent="Tail.001", connected=True)
        connect(rig, "Tail.003", "n_sippo_d", "n_sippo_e", parent="Tail.002", connected=True)
        extend(rig, "Tail.004", "Tail.003", parent="Tail.003", connected=True)

    def meta_pose(self, rig):
        rigify.limbs_spline_tentacle(rig, "Tail", sik_stretch_control="MANUAL_STRETCH")
        collection(rig, ["Tail", "Tail.001", "Tail.002", "Tail.003", "Tail.004"], TAIL_COLLECTION)

        link(rig, "n_sippo_a", "DEF-Tail")
        link(rig, "n_sippo_b", "DEF-Tail.001")
        link(rig, "n_sippo_c", "DEF-Tail.002")
        link(rig, "n_sippo_d", "DEF-Tail.003")
        link(rig, "n_sippo_e", "DEF-Tail.004")

    def final_pose(self, rig):
        for control in ["Tail-end", "Tail-end01", "Tail-mid01", "Tail-start01", "Tail-master"]:
            widget(rig, control, scale_factor=0.5)
