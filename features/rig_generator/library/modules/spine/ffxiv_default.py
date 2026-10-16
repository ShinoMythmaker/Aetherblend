"""Spine module: torso, chest, neck and head with the pivot and hara links."""
from ....instructions import *
from ....module import RigModule
from ....rigify.settings import BoneCollection, UI_Collections

TORSO_COLLECTION = "Torso"
TORSO_TWEAK_COLLECTION = "Torso (Tweak)"
HEAD_COLLECTION = "Head"


class Module(RigModule):
    name = "XIV-Default"
    requires = ["j_kosi", "j_sebo_a", "j_sebo_b", "j_sebo_c", "j_kubi", "j_kao", "n_hara"]
    ui_collections = UI_Collections([
        BoneCollection(name=TORSO_COLLECTION, ui=True, color_set="Torso", row_index=2, title="Torso"),
        BoneCollection(name=TORSO_TWEAK_COLLECTION, ui=True, color_set="Torso_Tweak", row_index=3, title="Tweak", visible=False),
        BoneCollection(name=HEAD_COLLECTION, ui=True, color_set="Head", row_index=1, title="Head"),
    ])

    def meta_edit(self, rig):
        connect(rig, "Spine.001", "j_kosi", "j_kosi", start_point="tail", end_point="head")
        connect(rig, "Spine.002", "j_sebo_a", "j_sebo_b", parent="Spine.001", connected=True)
        connect(rig, "Spine.003", "j_sebo_b", "j_sebo_c", parent="Spine.002", connected=True)
        connect(rig, "Spine.004", "j_sebo_c", "j_kubi", parent="Spine.003", connected=True)

        if has_bone(rig, "j_mune_r"):
            extend(rig, "Chest.R", "j_mune_r", start_point="head", roll=132, parent="Spine.003")
        if has_bone(rig, "j_mune_l"):
            extend(rig, "Chest.L", "j_mune_l", start_point="head", roll=-132, parent="Spine.003")

        connect(rig, "Neck", "j_kubi", "j_kao", parent=["Spine.004", "j_sebo_c"])
        extend(rig, "Head", "j_kao", axis="Z", axis_space="armature", size_factor=20.0, parent="Neck", connected=True)
        extend(rig, "n_hara_retarget", "n_hara", start_point="head", size_factor=0.5)

    def meta_pose(self, rig):
        rigify.spines_basic_spine(rig, "Spine.001", fk_collection=TORSO_TWEAK_COLLECTION, tweak_collection=TORSO_TWEAK_COLLECTION, pivot_position=1)
        rigify.spines_super_head(rig, "Neck")
        rigify.basic_raw_copy(rig, "n_hara_retarget")
        for chest in ["Chest.R", "Chest.L"]:
            rigify.basic_super_copy(rig, chest, widget_type="bone")

        collection(rig, ["Spine.001", "Spine.002", "Spine.003", "Spine.004", "Chest.R", "Chest.L"], TORSO_COLLECTION)
        collection(rig, ["Neck", "Head"], HEAD_COLLECTION)
        collection(rig, ["n_hara_retarget"], "MCH")

        link(rig, "n_hara", "MCH-pivot", location_only=True)
        link(rig, "j_kosi", "DEF-Spine.001")
        link(rig, "j_sebo_a", "DEF-Spine.002")
        link(rig, "j_sebo_b", "DEF-Spine.003")
        link(rig, "j_sebo_c", "DEF-Spine.004")
        link(rig, "j_mune_r", "DEF-Chest.R")
        link(rig, "j_mune_l", "DEF-Chest.L")
        link(rig, "j_kubi", "DEF-Neck")
        link(rig, "j_kao", "DEF-Head")

    def final_edit(self, rig):
        parent(rig, "MCH-Spine.001", "n_hara_retarget")
        parent(rig, "MCH-Spine.002", "n_hara_retarget")
        parent(rig, "n_hara_retarget", "torso")

    def final_pose(self, rig):
        for chest in ["Chest.R", "Chest.L"]:
            widget(rig, chest, translation=[0, 0.05, 0])
        constraints.copy_transforms(rig, "n_root", "root", name="AetherBlend_CopyTransform", mix_mode="BEFORE_FULL")
