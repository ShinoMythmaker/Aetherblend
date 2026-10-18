"""Spine module: torso, chest, neck and head with the pivot and hara links."""

import bpy

from .... import definitions
from .... import instructions as abi


class Module(definitions.RigModule):
    name = "XIV-Default"
    requires = [
        "j_kosi",
        "j_sebo_a",
        "j_sebo_b",
        "j_sebo_c",
        "j_kubi",
        "j_kao",
        "n_hara",
    ]

    # ------------------------------------------------------------------------

    def meta_edit(self, rig: bpy.types.Object) -> None:
        # Spine chain
        abi.connect(rig, "Spine.001", "j_kosi", "j_kosi", start_point="tail", end_point="head")
        abi.connect(rig, "Spine.002", "j_sebo_a", "j_sebo_b", parent="Spine.001", connected=True)
        abi.connect(rig, "Spine.003", "j_sebo_b", "j_sebo_c", parent="Spine.002", connected=True)
        abi.connect(rig, "Spine.004", "j_sebo_c", "j_kubi", parent="Spine.003", connected=True)

        # Chest bones
        for side in definitions.SIDES:
            if abi.has_bone(rig, f"j_mune_{side.source}"):
                abi.extend(
                    rig,
                    f"Chest{side.suffix}",
                    f"j_mune_{side.source}",
                    start_point="head",
                    roll=-132 if side is definitions.LEFT else 132,
                    parent="Spine.003",
                )

        # Neck, head and retarget helper
        abi.connect(rig, "Neck", "j_kubi", "j_kao", parent=["Spine.004", "j_sebo_c"])
        abi.extend(
            rig, "Head", "j_kao", axis="Z", axis_space="armature", size_factor=20.0, parent="Neck", connected=True
        )
        abi.extend(rig, "n_hara_retarget", "n_hara", start_point="head", size_factor=0.5)

    # ------------------------------------------------------------------------

    def meta_pose(self, rig: bpy.types.Object) -> None:
        # Torso and head controls
        abi.rigify.spines_basic_spine(
            rig,
            "Spine.001",
            fk_collection="Torso (Tweak)",
            tweak_collection="Torso (Tweak)",
            pivot_position=1,
        )
        abi.rigify.spines_super_head(rig, "Neck")
        abi.rigify.basic_raw_copy(rig, "n_hara_retarget")
        for side in definitions.SIDES:
            abi.rigify.basic_super_copy(rig, f"Chest{side.suffix}", widget_type="bone")

        # Control collections
        abi.collection(rig, ["Spine.001", "Spine.002", "Spine.003", "Spine.004", "Chest.R", "Chest.L"], "Torso")
        abi.collection(rig, ["Neck", "Head"], "Head")
        abi.collection(rig, ["n_hara_retarget"], "MCH")

        # Source-to-deform mappings
        abi.link(rig, "n_hara", "MCH-pivot", location_only=True)
        abi.link(rig, "j_kosi", "DEF-Spine.001")
        abi.link(rig, "j_sebo_a", "DEF-Spine.002")
        abi.link(rig, "j_sebo_b", "DEF-Spine.003")
        abi.link(rig, "j_sebo_c", "DEF-Spine.004")
        for side in definitions.SIDES:
            abi.link(rig, f"j_mune_{side.source}", f"DEF-Chest{side.suffix}")
        abi.link(rig, "j_kubi", "DEF-Neck")
        abi.link(rig, "j_kao", "DEF-Head")

    # ------------------------------------------------------------------------

    def final_edit(self, rig: bpy.types.Object) -> None:
        # Retarget hierarchy
        abi.parent(rig, "MCH-Spine.001", "n_hara_retarget")
        abi.parent(rig, "MCH-Spine.002", "n_hara_retarget")
        abi.parent(rig, "n_hara_retarget", "torso")

    # ------------------------------------------------------------------------

    def final_pose(self, rig: bpy.types.Object) -> None:
        # Chest widgets and root tracking
        for side in definitions.SIDES:
            abi.widget(rig, f"Chest{side.suffix}", translation=[0, 0.05, 0])
        abi.constraints.copy_transforms(rig, "n_root", "root", name="AetherBlend_CopyTransform", mix_mode="BEFORE_FULL")
