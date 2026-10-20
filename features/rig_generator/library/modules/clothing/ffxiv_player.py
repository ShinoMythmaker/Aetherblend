"""Clothing module: a skirt whose segments swing with the thighs and shins."""

import bpy

from .... import definitions
from .... import instructions as abi


class Module(definitions.RigModule):
    """Build skirt automation when all source skirt segments are present."""

    name = "FFXIV Player Clothing"
    _enabled: bool = False
    _source_bones = [
        "j_sk_f_a_l",
        "j_sk_f_b_l",
        "j_sk_f_c_l",
        "j_sk_s_a_l",
        "j_sk_s_b_l",
        "j_sk_s_c_l",
        "j_sk_b_a_l",
        "j_sk_b_b_l",
        "j_sk_b_c_l",
        "j_sk_f_a_r",
        "j_sk_f_b_r",
        "j_sk_f_c_r",
        "j_sk_s_a_r",
        "j_sk_s_b_r",
        "j_sk_s_c_r",
        "j_sk_b_a_r",
        "j_sk_b_b_r",
        "j_sk_b_c_r",
    ]
    ui_flags = ("Skirt Automation",)

    # ------------------------------------------------------------------------

    def meta_edit(self, rig: bpy.types.Object) -> None:
        """Check skirt segments, update UI flags, and build skirt controls."""
        self._enabled = abi.require_bones(rig, self._source_bones, self.name)
        self.ui_flags = ("Skirt Automation",) if self._enabled else ()
        if not self._enabled:
            return
        for side in definitions.SIDES:
            # Leg tracking helpers
            abi.extend(
                rig,
                f"MCH-thigh_driv_tgt{side.suffix}",
                f"thigh{side.suffix}",
                start_point="head",
                size_factor=0.3,
                parent="Spine.001",
            )
            abi.extend(
                rig,
                f"MCH-shin_driv_tgt{side.suffix}",
                f"shin{side.suffix}",
                start_point="head",
                size_factor=0.3,
                parent=f"thigh{side.suffix}",
            )

            # Front skirt controls and automated helpers
            abi.connect(
                rig,
                f"Skirt_Front{side.suffix}",
                f"j_sk_f_a_{side.source}",
                f"j_sk_f_b_{side.source}",
                parent="Spine.001",
            )
            abi.connect(
                rig,
                f"Skirt_Front{side.suffix}.001",
                f"j_sk_f_b_{side.source}",
                f"j_sk_f_c_{side.source}",
                parent=f"Skirt_Front{side.suffix}",
                connected=True,
            )
            abi.extend(
                rig,
                f"Skirt_Front{side.suffix}.002",
                f"j_sk_f_c_{side.source}",
                start_point="head",
                parent=f"Skirt_Front{side.suffix}.001",
                connected=True,
            )
            abi.connect(
                rig,
                f"MCH-Skirt_Front{side.suffix}",
                f"j_sk_f_a_{side.source}",
                f"j_sk_f_b_{side.source}",
                parent="Spine.001",
                roll=0,
            )
            abi.connect(
                rig,
                f"MCH-Skirt_Front{side.suffix}.001",
                f"j_sk_f_b_{side.source}",
                f"j_sk_f_c_{side.source}",
                parent=f"MCH-Skirt_Front{side.suffix}",
                connected=True,
                roll=0,
            )
            abi.extend(
                rig,
                f"MCH-Skirt_Front{side.suffix}.002",
                f"j_sk_f_c_{side.source}",
                start_point="head",
                parent=f"MCH-Skirt_Front{side.suffix}.001",
                connected=True,
                roll=0,
            )

            # Side skirt controls and automated helpers
            abi.connect(
                rig,
                f"Skirt_Side{side.suffix}",
                f"j_sk_s_a_{side.source}",
                f"j_sk_s_b_{side.source}",
                parent="Spine.001",
            )
            abi.connect(
                rig,
                f"Skirt_Side{side.suffix}.001",
                f"j_sk_s_b_{side.source}",
                f"j_sk_s_c_{side.source}",
                parent=f"Skirt_Side{side.suffix}",
                connected=True,
            )
            abi.extend(
                rig,
                f"Skirt_Side{side.suffix}.002",
                f"j_sk_s_c_{side.source}",
                start_point="head",
                parent=f"Skirt_Side{side.suffix}.001",
                connected=True,
            )
            abi.connect(
                rig,
                f"MCH-Skirt_Middle{side.suffix}",
                f"j_sk_s_a_{side.source}",
                f"j_sk_s_b_{side.source}",
                parent="Spine.001",
                roll=-7 if side is definitions.LEFT else -173,
            )
            abi.connect(
                rig,
                f"MCH-Skirt_Middle{side.suffix}.001",
                f"j_sk_s_b_{side.source}",
                f"j_sk_s_c_{side.source}",
                parent=f"MCH-Skirt_Middle{side.suffix}",
                connected=True,
                roll=-7 if side is definitions.LEFT else -173,
            )
            abi.extend(
                rig,
                f"MCH-Skirt_Middle{side.suffix}.002",
                f"j_sk_s_c_{side.source}",
                start_point="head",
                parent=f"MCH-Skirt_Middle{side.suffix}.001",
                connected=True,
                roll=-7 if side is definitions.LEFT else -173,
            )

            # Back skirt controls and automated helpers
            abi.connect(
                rig,
                f"Skirt_Back{side.suffix}",
                f"j_sk_b_a_{side.source}",
                f"j_sk_b_b_{side.source}",
                parent="Spine.001",
            )
            abi.connect(
                rig,
                f"Skirt_Back{side.suffix}.001",
                f"j_sk_b_b_{side.source}",
                f"j_sk_b_c_{side.source}",
                parent=f"Skirt_Back{side.suffix}",
                connected=True,
            )
            abi.extend(
                rig,
                f"Skirt_Back{side.suffix}.002",
                f"j_sk_b_c_{side.source}",
                start_point="head",
                parent=f"Skirt_Back{side.suffix}.001",
                connected=True,
            )
            abi.connect(
                rig,
                f"MCH-Skirt_Back{side.suffix}",
                f"j_sk_b_a_{side.source}",
                f"j_sk_b_b_{side.source}",
                parent="Spine.001",
                roll=0,
            )
            abi.connect(
                rig,
                f"MCH-Skirt_Back{side.suffix}.001",
                f"j_sk_b_b_{side.source}",
                f"j_sk_b_c_{side.source}",
                parent=f"MCH-Skirt_Back{side.suffix}",
                connected=True,
                roll=0,
            )
            abi.extend(
                rig,
                f"MCH-Skirt_Back{side.suffix}.002",
                f"j_sk_b_c_{side.source}",
                start_point="head",
                parent=f"MCH-Skirt_Back{side.suffix}.001",
                connected=True,
                roll=0,
            )

    # ------------------------------------------------------------------------

    def meta_pose(self, rig: bpy.types.Object) -> None:
        """Configure skirt controls and source mappings."""
        if not self._enabled:
            return
        for side in definitions.SIDES:
            # Leg tracking helpers
            abi.rigify.basic_raw_copy(rig, f"MCH-thigh_driv_tgt{side.suffix}")
            abi.rigify.basic_raw_copy(rig, f"MCH-shin_driv_tgt{side.suffix}")

            # Front skirt controls and mappings
            abi.rigify.basic_copy_chain(rig, f"Skirt_Front{side.suffix}")
            abi.collection(
                rig,
                [
                    f"Skirt_Front{side.suffix}",
                    f"Skirt_Front{side.suffix}.001",
                    f"Skirt_Front{side.suffix}.002",
                ],
                "Skirt",
            )
            abi.rigify.basic_raw_copy(rig, f"MCH-Skirt_Front{side.suffix}")
            abi.rigify.basic_raw_copy(rig, f"MCH-Skirt_Front{side.suffix}.001")
            abi.rigify.basic_raw_copy(rig, f"MCH-Skirt_Front{side.suffix}.002")
            abi.link(rig, f"j_sk_f_a_{side.source}", f"DEF-Skirt_Front{side.suffix}")
            abi.link(rig, f"j_sk_f_b_{side.source}", f"DEF-Skirt_Front{side.suffix}.001")
            abi.link(rig, f"j_sk_f_c_{side.source}", f"DEF-Skirt_Front{side.suffix}.002")

            # Side skirt controls and mappings
            abi.rigify.basic_copy_chain(rig, f"Skirt_Side{side.suffix}")
            abi.collection(
                rig,
                [
                    f"Skirt_Side{side.suffix}",
                    f"Skirt_Side{side.suffix}.001",
                    f"Skirt_Side{side.suffix}.002",
                ],
                "Skirt",
            )
            abi.rigify.basic_raw_copy(rig, f"MCH-Skirt_Middle{side.suffix}")
            abi.rigify.basic_raw_copy(rig, f"MCH-Skirt_Middle{side.suffix}.001")
            abi.rigify.basic_raw_copy(rig, f"MCH-Skirt_Middle{side.suffix}.002")
            abi.link(rig, f"j_sk_s_a_{side.source}", f"DEF-Skirt_Side{side.suffix}")
            abi.link(rig, f"j_sk_s_b_{side.source}", f"DEF-Skirt_Side{side.suffix}.001")
            abi.link(rig, f"j_sk_s_c_{side.source}", f"DEF-Skirt_Side{side.suffix}.002")

            # Back skirt controls and mappings
            abi.rigify.basic_copy_chain(rig, f"Skirt_Back{side.suffix}")
            abi.collection(
                rig,
                [
                    f"Skirt_Back{side.suffix}",
                    f"Skirt_Back{side.suffix}.001",
                    f"Skirt_Back{side.suffix}.002",
                ],
                "Skirt",
            )
            abi.rigify.basic_raw_copy(rig, f"MCH-Skirt_Back{side.suffix}")
            abi.rigify.basic_raw_copy(rig, f"MCH-Skirt_Back{side.suffix}.001")
            abi.rigify.basic_raw_copy(rig, f"MCH-Skirt_Back{side.suffix}.002")
            abi.link(rig, f"j_sk_b_a_{side.source}", f"DEF-Skirt_Back{side.suffix}")
            abi.link(rig, f"j_sk_b_b_{side.source}", f"DEF-Skirt_Back{side.suffix}.001")
            abi.link(rig, f"j_sk_b_c_{side.source}", f"DEF-Skirt_Back{side.suffix}.002")

    # ------------------------------------------------------------------------

    def final_edit(self, rig: bpy.types.Object) -> None:
        """Parent the generated skirt automation helpers."""
        if not self._enabled:
            return
        # Skirt hierarchy
        for side in definitions.SIDES:
            abi.parent(rig, f"Skirt_Front{side.suffix}", f"MCH-Skirt_Front{side.suffix}")
            abi.parent(rig, f"Skirt_Side{side.suffix}", f"MCH-Skirt_Middle{side.suffix}")
            abi.parent(rig, f"Skirt_Back{side.suffix}", f"MCH-Skirt_Back{side.suffix}")

    # ------------------------------------------------------------------------

    def final_pose(self, rig: bpy.types.Object) -> None:
        """Configure skirt automation constraints and drivers."""
        if not self._enabled:
            return
        # Automation control
        abi.armature_prop(rig, "skirt_automation", 1.0, minimum=0.0, maximum=1.0)
        automation = abi.PropertyVariable("skirt_automation")

        for side in definitions.SIDES:
            sideways_comparison = "<" if side is definitions.LEFT else ">"
            middle_sign = "" if side is definitions.LEFT else "-"

            # Leg tracking and driver variables
            abi.collection(
                rig,
                [f"MCH-thigh_driv_tgt{side.suffix}", f"MCH-shin_driv_tgt{side.suffix}"],
                "MCH",
            )
            abi.constraints.damped_track(rig, f"MCH-thigh_driv_tgt{side.suffix}", f"ORG-shin{side.suffix}")
            abi.constraints.damped_track(rig, f"MCH-shin_driv_tgt{side.suffix}", f"ORG-foot{side.suffix}")
            thigh_forward = abi.TransformVariable(f"MCH-thigh_driv_tgt{side.suffix}", "ROT_X")
            thigh_sideways = abi.TransformVariable(f"MCH-thigh_driv_tgt{side.suffix}", "ROT_Z")
            shin_forward = abi.TransformVariable(f"MCH-shin_driv_tgt{side.suffix}", "ROT_X")

            # Front skirt swing
            abi.collection(
                rig,
                [
                    f"MCH-Skirt_Front{side.suffix}",
                    f"MCH-Skirt_Front{side.suffix}.001",
                    f"MCH-Skirt_Front{side.suffix}.002",
                ],
                "MCH",
            )
            abi.driver(
                rig,
                f"MCH-Skirt_Front{side.suffix}",
                "rotation_quaternion",
                index=1,
                expression="((RotX < 0) * (RotX * sk_auto) / (1 + (abs(RotX) - 0.8) * 0.1))",
                variables={"RotX": thigh_forward, "sk_auto": automation},
            )
            abi.driver(
                rig,
                f"MCH-Skirt_Front{side.suffix}",
                "rotation_quaternion",
                index=3,
                expression=f"((RotZ {sideways_comparison} 0) * (RotZ * sk_auto) / (2 + (abs(RotZ) - 0.5) * 0.5))",
                variables={"RotZ": thigh_sideways, "sk_auto": automation},
            )
            abi.driver(
                rig,
                f"MCH-Skirt_Front{side.suffix}.001",
                "rotation_quaternion",
                index=1,
                expression="((RotX > 0) * (RotX * sk_auto) / (2 + (abs(RotX) - 0.5) * 2)) * (abs(RotXThreshold) / (0.2 + abs(RotXThreshold))) if RotXThreshold < 0 else RotX * 0",  # noqa: E501
                variables={"RotX": shin_forward, "RotXThreshold": thigh_forward, "sk_auto": automation},
            )

            # Side skirt swing
            abi.collection(
                rig,
                [
                    f"MCH-Skirt_Middle{side.suffix}",
                    f"MCH-Skirt_Middle{side.suffix}.001",
                    f"MCH-Skirt_Middle{side.suffix}.002",
                ],
                "MCH",
            )
            abi.driver(
                rig,
                f"MCH-Skirt_Middle{side.suffix}",
                "rotation_quaternion",
                index=1,
                expression=f"((RotX < 0) * ({middle_sign}RotX * sk_auto) / (3 + (abs(RotX) - 0.5) * 2))",
                variables={"RotX": thigh_forward, "sk_auto": automation},
            )
            abi.driver(
                rig,
                f"MCH-Skirt_Middle{side.suffix}",
                "rotation_quaternion",
                index=3,
                expression=(
                    f"((RotZ {sideways_comparison} 0) * ({middle_sign}RotZ * sk_auto) / (1 + (abs(RotZ) - 0.1) * 1))"
                ),
                variables={"RotZ": thigh_sideways, "sk_auto": automation},
            )
            abi.driver(
                rig,
                f"MCH-Skirt_Middle{side.suffix}.001",
                "rotation_quaternion",
                index=1,
                expression=f"((RotX > 0) * ({middle_sign}RotX * sk_auto) / (3 + (abs(RotX) - 0.2) * 2)) * (abs(RotXThreshold) / (0.2 + abs(RotXThreshold))) if RotXThreshold < 0 else RotX * 0",  # noqa: E501
                variables={"RotX": shin_forward, "RotXThreshold": thigh_forward, "sk_auto": automation},
            )

            # Back skirt swing
            abi.collection(
                rig,
                [
                    f"MCH-Skirt_Back{side.suffix}",
                    f"MCH-Skirt_Back{side.suffix}.001",
                    f"MCH-Skirt_Back{side.suffix}.002",
                ],
                "MCH",
            )
            abi.driver(
                rig,
                f"MCH-Skirt_Back{side.suffix}",
                "rotation_quaternion",
                index=1,
                expression="((RotX < 0) * (RotX * sk_auto) / (5 + (abs(RotX) - 0.2) * 5)) + ((RotX > 0) * ((RotX * sk_auto) / (1 + (abs(RotX) + 0.1) * 0.2)))",  # noqa: E501
                variables={"RotX": thigh_forward, "sk_auto": automation},
            )
            abi.driver(
                rig,
                f"MCH-Skirt_Back{side.suffix}",
                "rotation_quaternion",
                index=3,
                expression=f"((RotZ {sideways_comparison} 0) * (RotZ * sk_auto) / (2 + (abs(RotZ) - 0.1) * 3))",
                variables={"RotZ": thigh_sideways, "sk_auto": automation},
            )
            abi.driver(
                rig,
                f"MCH-Skirt_Back{side.suffix}.001",
                "rotation_quaternion",
                index=1,
                expression="((RotX > 0) * (RotX * sk_auto) / (1 + (abs(RotX) + 0.5) * 0.3)) * (abs(RotXThreshold) / (0.5 + abs(RotXThreshold))) if RotXThreshold > 0 else RotX * 0",  # noqa: E501
                variables={"RotX": shin_forward, "RotXThreshold": thigh_forward, "sk_auto": automation},
            )
