"""Leg module: IK/FK legs with knee and heel helpers."""

import bpy

from .... import definitions
from .... import instructions as abi


class Module(definitions.RigModule):
    name = "XIV-Default"
    requires = [
        "j_asi_a_l",
        "j_asi_b_l",
        "j_asi_c_l",
        "j_asi_d_l",
        "j_asi_e_l",
        "j_asi_a_r",
        "j_asi_b_r",
        "j_asi_c_r",
        "j_asi_d_r",
        "j_asi_e_r",
    ]

    # ------------------------------------------------------------------------

    def meta_edit(self, rig: bpy.types.Object) -> None:
        for side in definitions.SIDES:
            # Leg chain
            abi.connect(
                rig,
                f"thigh{side.suffix}",
                f"j_asi_a_{side.source}",
                f"j_asi_b_{side.source}",
                end_point="tail",
                parent=["Spine.001", "j_kosi"],
                roll=-90,
            )
            abi.connect(
                rig,
                f"shin{side.suffix}",
                f"j_asi_b_{side.source}",
                f"j_asi_d_{side.source}",
                start_point="tail",
                parent=f"thigh{side.suffix}",
                connected=True,
                roll=-90,
            )
            # The left foot has never had a roll; keep it to preserve the existing rig.
            abi.connect(
                rig,
                f"foot{side.suffix}",
                f"j_asi_d_{side.source}",
                f"j_asi_e_{side.source}",
                parent=f"shin{side.suffix}",
                connected=True,
                roll=0 if side is definitions.LEFT else -90,
            )
            abi.extend(
                rig,
                f"toe{side.suffix}",
                f"j_asi_e_{side.source}",
                start_point="head",
                parent=f"foot{side.suffix}",
                connected=True,
            )

            # Heel pivot
            abi.parallel(
                rig,
                f"heel_pivot{side.suffix}.helper",
                f"toe{side.suffix}",
                f"shin{side.suffix}",
                start_point="head",
                end_point="tail",
                coordinate="Y",
                parent=f"shin{side.suffix}",
            )
            abi.extend(rig, f"heel_pivot{side.suffix}", f"heel_pivot{side.suffix}.helper", parent=f"foot{side.suffix}")

            # Knee helpers
            abi.extend(
                rig,
                f"MCH-knee{side.suffix}",
                f"j_asi_b_{side.source}",
                start_point="head",
                size_factor=1.5,
                parent="spine.001",
            )
            abi.extend(
                rig,
                f"knee{side.suffix}",
                f"j_asi_b_{side.source}",
                start_point="head",
                size_factor=1.5,
                parent="spine.001",
            )
            abi.extend(
                rig,
                f"MCH-knee_target{side.suffix}",
                f"j_asi_c_{side.source}",
                start_point="head",
                size_factor=0.2,
                parent="spine.001",
            )

    # ------------------------------------------------------------------------

    def meta_pose(self, rig: bpy.types.Object) -> None:
        for side in definitions.SIDES:
            # Leg and knee rig types
            abi.rigify.limbs_leg(
                rig,
                f"thigh{side.suffix}",
                fk_collection=f"Leg{side.suffix} (FK)",
                tweak_collection=f"Leg{side.suffix} (Tweak)",
            )
            abi.rigify.basic_raw_copy(rig, f"MCH-knee{side.suffix}")
            abi.rigify.basic_super_copy(rig, f"knee{side.suffix}")
            abi.rigify.basic_raw_copy(rig, f"MCH-knee_target{side.suffix}")

            # Control and mechanism collections
            abi.collection(
                rig,
                [
                    f"thigh{side.suffix}",
                    f"shin{side.suffix}",
                    f"foot{side.suffix}",
                    f"toe{side.suffix}",
                    f"heel_pivot{side.suffix}.helper",
                    f"heel_pivot{side.suffix}",
                ],
                f"Leg{side.suffix} (IK)",
            )
            abi.collection(
                rig, [f"MCH-knee{side.suffix}", f"knee{side.suffix}", f"MCH-knee_target{side.suffix}"], "MCH"
            )

            # Source-to-deform mappings
            abi.link(rig, f"j_asi_a_{side.source}", f"DEF-thigh{side.suffix}.001")
            abi.link(rig, f"j_asi_c_{side.source}", f"DEF-shin{side.suffix}.001")
            abi.link(rig, f"j_asi_d_{side.source}", f"DEF-foot{side.suffix}")
            abi.link(rig, f"j_asi_e_{side.source}", f"DEF-toe{side.suffix}")
            abi.link(rig, f"j_asi_b_{side.source}", f"DEF-knee{side.suffix}")

    # ------------------------------------------------------------------------

    def final_edit(self, rig: bpy.types.Object) -> None:
        for side in definitions.SIDES:
            # Knee hierarchy
            abi.parent(rig, f"MCH-knee{side.suffix}", f"DEF-thigh{side.suffix}.001")
            abi.parent(rig, f"knee{side.suffix}", f"MCH-knee{side.suffix}")
            abi.parent(rig, f"MCH-knee_target{side.suffix}", f"DEF-shin{side.suffix}")

    # ------------------------------------------------------------------------

    def final_pose(self, rig: bpy.types.Object) -> None:
        for side in definitions.SIDES:
            # Knee tracking and leg stretch
            abi.constraints.damped_track(rig, f"MCH-knee{side.suffix}", target=f"MCH-knee_target{side.suffix}")
            abi.prop(rig, f"thigh_parent{side.suffix}", "IK_Stretch", 0)
