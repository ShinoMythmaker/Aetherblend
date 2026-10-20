"""Arm module: IK/FK arms with clavicle, elbow and pauldron helpers."""

import bpy

from .... import definitions
from .... import instructions as abi


class Module(definitions.RigModule):
    """Build arms only when their source chains and helpers are available."""

    name = "FFXIV Player Arms"
    _enabled: bool = False
    _source_bones = [
        "j_sako_l",
        "j_ude_a_l",
        "j_ude_b_l",
        "j_te_l",
        "n_kataarmor_l",
        "n_hhiji_l",
        "j_sako_r",
        "j_ude_a_r",
        "j_ude_b_r",
        "j_te_r",
        "n_kataarmor_r",
        "n_hhiji_r",
    ]

    # ------------------------------------------------------------------------

    def meta_edit(self, rig: bpy.types.Object) -> None:
        """Check the source bones and create both arm chains and helpers."""
        self._enabled = abi.require_bones(rig, self._source_bones, self.name)
        if not self._enabled:
            return
        for side in definitions.SIDES:
            # Pauldron helpers
            abi.extend(
                rig, f"MCH-pauldron{side.suffix}", f"n_kataarmor_{side.source}", start_point="head", parent="Spine.004"
            )
            abi.extend(
                rig,
                f"pauldron{side.suffix}",
                f"n_kataarmor_{side.source}",
                start_point="head",
                parent=f"MCH-pauldron{side.suffix}",
            )

            # Arm chain
            abi.connect(
                rig,
                f"clavicle{side.suffix}",
                f"j_sako_{side.source}",
                f"j_ude_a_{side.source}",
                parent=["Spine.004", "j_sebo_c"],
            )
            abi.connect(
                rig,
                f"upper_arm{side.suffix}",
                f"j_ude_a_{side.source}",
                f"j_ude_b_{side.source}",
                parent=f"clavicle{side.suffix}",
            )
            abi.connect(
                rig,
                f"forearm{side.suffix}",
                f"j_ude_b_{side.source}",
                f"j_te_{side.source}",
                parent=f"upper_arm{side.suffix}",
                connected=True,
            )
            abi.extend(
                rig,
                f"hand{side.suffix}",
                f"j_te_{side.source}",
                size_factor=0.6,
                parent=f"forearm{side.suffix}",
                connected=True,
            )
            # Elbow helper
            abi.extend(
                rig,
                f"elbow{side.suffix}",
                f"n_hhiji_{side.source}",
                start_point="head",
                size_factor=0.5,
                parent=f"forearm{side.suffix}",
            )

    # ------------------------------------------------------------------------

    def meta_pose(self, rig: bpy.types.Object) -> None:
        """Configure arm controls, collections, and deform mappings."""
        if not self._enabled:
            return
        for side in definitions.SIDES:
            # Arm and helper controls
            abi.rigify.basic_raw_copy(rig, f"MCH-pauldron{side.suffix}")
            abi.rigify.basic_super_copy(rig, f"pauldron{side.suffix}", widget_type="shoulder")
            abi.rigify.basic_super_copy(rig, f"clavicle{side.suffix}", widget_type="shoulder")
            abi.rigify.limbs_arm(
                rig,
                f"upper_arm{side.suffix}",
                fk_collection=f"Arm{side.suffix} (FK)",
                tweak_collection=f"Arm{side.suffix} (Tweak)",
            )
            abi.rigify.basic_super_copy(rig, f"elbow{side.suffix}", widget_type="pivot_cross")

            # Control collections
            abi.collection(rig, [f"pauldron{side.suffix}", f"elbow{side.suffix}"], f"Arm{side.suffix} (Tweak)")
            abi.collection(
                rig,
                [f"upper_arm{side.suffix}", f"forearm{side.suffix}", f"hand{side.suffix}"],
                f"Arm{side.suffix} (IK)",
            )
            abi.collection(rig, [f"clavicle{side.suffix}"], "Torso")

            # Source-to-deform mappings
            abi.link(rig, f"j_ude_a_{side.source}", f"DEF-upper_arm{side.suffix}.001")
            abi.link(rig, f"j_ude_b_{side.source}", f"DEF-forearm{side.suffix}")
            abi.link(rig, f"j_te_{side.source}", f"DEF-hand{side.suffix}")
            abi.link(rig, f"j_sako_{side.source}", f"DEF-clavicle{side.suffix}")
            abi.link(rig, f"n_hte_{side.source}", f"DEF-forearm{side.suffix}.001")
            abi.link(rig, f"n_hhiji_{side.source}", f"DEF-elbow{side.suffix}")
            abi.link(rig, f"n_kataarmor_{side.source}", f"DEF-pauldron{side.suffix}")

    # ------------------------------------------------------------------------

    def final_pose(self, rig: bpy.types.Object) -> None:
        """Apply pauldron follow behavior and control settings."""
        if not self._enabled:
            return
        for side in definitions.SIDES:
            # Pauldron follow
            abi.collection(rig, [f"MCH-pauldron{side.suffix}"], "MCH")
            abi.driver(
                rig,
                f"MCH-pauldron{side.suffix}",
                "rotation_quaternion",
                index=3,
                expression="-RotX" if side is definitions.LEFT else "RotX",
                variables={"RotX": abi.TransformVariable(f"DEF-upper_arm{side.suffix}", "ROT_X")},
            )
            abi.driver(
                rig,
                f"MCH-pauldron{side.suffix}",
                "rotation_quaternion",
                index=1,
                expression="RotZ" if side is definitions.LEFT else "-RotZ",
                variables={"RotZ": abi.TransformVariable(f"DEF-upper_arm{side.suffix}", "ROT_Z")},
            )
            # Pauldron widget and arm stretch
            abi.widget(rig, f"pauldron{side.suffix}", widget_name="Pauldron", scale_to_bone_length=True, wire_width=1)
            abi.prop(rig, f"upper_arm_parent{side.suffix}", "IK_Stretch", 0)
