"""Mouth module: manual controls, one plain control per lip, teeth and tongue bone."""

import bpy

from .... import definitions
from .... import instructions as abi


class Module(definitions.RigModule):
    name = "XIV-Manual"

    # ------------------------------------------------------------------------

    def meta_edit(self, rig: bpy.types.Object) -> None:
        # Jaw bones
        abi.center(rig, "jaw_ref", ["j_f_dlip_01_r", "j_f_dlip_01_l"], axis="Y", parent="Head")
        abi.connect(rig, "Jaw", "j_f_ago", "jaw_ref", parent="Head")

        # Lip controls
        for side in definitions.SIDES:
            abi.extend(
                rig,
                f"Lip.T{side.suffix}",
                f"j_f_ulip_01_{side.source}",
                axis="Y",
                start_point="head",
                size_factor=0.3,
                parent="Head",
            )
            abi.extend(
                rig,
                f"Lip.T{side.suffix}.001",
                f"j_f_umlip_01_{side.source}",
                axis="Y",
                start_point="head",
                size_factor=0.3,
                parent="Head",
            )
            abi.extend(
                rig,
                f"Lip.T{side.suffix}.002",
                f"j_f_uslip_{side.source}",
                axis="Y",
                start_point="head",
                size_factor=0.3,
                parent="Head",
            )
            abi.extend(
                rig,
                f"Lip.T{side.suffix}.003",
                f"j_f_ulip_02_{side.source}",
                axis="Y",
                start_point="head",
                size_factor=0.3,
                parent=f"Lip.T{side.suffix}",
            )
            abi.extend(
                rig,
                f"Lip.T{side.suffix}.004",
                f"j_f_umlip_02_{side.source}",
                axis="Y",
                start_point="head",
                size_factor=0.3,
                parent=f"Lip.T{side.suffix}.001",
            )
            abi.extend(
                rig,
                f"Lip.B{side.suffix}",
                f"j_f_dlip_01_{side.source}",
                axis="Y",
                start_point="head",
                size_factor=0.3,
                parent="Jaw",
            )
            abi.extend(
                rig,
                f"Lip.B{side.suffix}.001",
                f"j_f_dmlip_01_{side.source}",
                axis="Y",
                start_point="head",
                size_factor=0.3,
                parent="Jaw",
            )
            abi.extend(
                rig,
                f"Lip.B{side.suffix}.002",
                f"j_f_dslip_{side.source}",
                axis="Y",
                start_point="head",
                size_factor=0.3,
                parent="Jaw",
            )
            abi.extend(
                rig,
                f"Lip.B{side.suffix}.003",
                f"j_f_dlip_02_{side.source}",
                axis="Y",
                start_point="head",
                size_factor=0.3,
                parent=f"Lip.B{side.suffix}",
            )
            abi.extend(
                rig,
                f"Lip.B{side.suffix}.004",
                f"j_f_dmlip_02_{side.source}",
                axis="Y",
                start_point="head",
                size_factor=0.3,
                parent=f"Lip.B{side.suffix}.001",
            )

        # Teeth and tongue
        abi.extend(rig, "Teeth.T", "j_f_hagukiup", axis="Y", start_point="head", parent="Head")
        abi.extend(rig, "Teeth.B", "j_f_hagukidn", axis="Y", start_point="head", parent="Jaw")
        abi.extend(
            rig,
            "Tongue",
            "j_f_bero_01",
            axis="Y",
            start_point="head",
            size_factor=0.3,
            parent="Jaw",
        )
        abi.extend(
            rig,
            "Tongue.001",
            "j_f_bero_02",
            axis="Y",
            start_point="head",
            size_factor=0.3,
            parent="Tongue",
        )
        abi.extend(
            rig,
            "Tongue.002",
            "j_f_bero_03",
            axis="Y",
            start_point="head",
            size_factor=0.3,
            parent="Tongue.001",
        )

    # ------------------------------------------------------------------------

    def meta_pose(self, rig: bpy.types.Object) -> None:
        # Jaw controls
        abi.collection(rig, ["jaw_ref"], "MCH")
        abi.rigify.basic_super_copy(rig, "Jaw", widget_type="jaw")
        abi.collection(rig, ["Jaw"], "Face (Primary)")
        abi.link(rig, "j_f_ago", "DEF-Jaw")

        # Lip controls
        for side in definitions.SIDES:
            abi.rigify.basic_super_copy(rig, f"Lip.T{side.suffix}", widget_type="circle")
            abi.collection(rig, [f"Lip.T{side.suffix}"], "Face (Primary)")
            abi.link(rig, f"j_f_ulip_01_{side.source}", f"DEF-Lip.T{side.suffix}")
            abi.rigify.basic_super_copy(rig, f"Lip.T{side.suffix}.001", widget_type="circle")
            abi.collection(rig, [f"Lip.T{side.suffix}.001"], "Face (Primary)")
            abi.link(rig, f"j_f_umlip_01_{side.source}", f"DEF-Lip.T{side.suffix}.001")
            abi.rigify.basic_super_copy(rig, f"Lip.T{side.suffix}.002", widget_type="circle")
            abi.collection(rig, [f"Lip.T{side.suffix}.002"], "Face (Primary)")
            abi.link(rig, f"j_f_uslip_{side.source}", f"DEF-Lip.T{side.suffix}.002")
            abi.rigify.basic_super_copy(rig, f"Lip.T{side.suffix}.003", widget_type="circle")
            abi.collection(rig, [f"Lip.T{side.suffix}.003"], "Face (Secondary)")
            abi.link(rig, f"j_f_ulip_02_{side.source}", f"DEF-Lip.T{side.suffix}.003")
            abi.rigify.basic_super_copy(rig, f"Lip.T{side.suffix}.004", widget_type="circle")
            abi.collection(rig, [f"Lip.T{side.suffix}.004"], "Face (Secondary)")
            abi.link(rig, f"j_f_umlip_02_{side.source}", f"DEF-Lip.T{side.suffix}.004")

            abi.rigify.basic_super_copy(rig, f"Lip.B{side.suffix}", widget_type="circle")
            abi.collection(rig, [f"Lip.B{side.suffix}"], "Face (Primary)")
            abi.link(rig, f"j_f_dlip_01_{side.source}", f"DEF-Lip.B{side.suffix}")
            abi.rigify.basic_super_copy(rig, f"Lip.B{side.suffix}.001", widget_type="circle")
            abi.collection(rig, [f"Lip.B{side.suffix}.001"], "Face (Primary)")
            abi.link(rig, f"j_f_dmlip_01_{side.source}", f"DEF-Lip.B{side.suffix}.001")
            abi.rigify.basic_super_copy(rig, f"Lip.B{side.suffix}.002", widget_type="circle")
            abi.collection(rig, [f"Lip.B{side.suffix}.002"], "Face (Primary)")
            abi.link(rig, f"j_f_dslip_{side.source}", f"DEF-Lip.B{side.suffix}.002")
            abi.rigify.basic_super_copy(rig, f"Lip.B{side.suffix}.003", widget_type="circle")
            abi.collection(rig, [f"Lip.B{side.suffix}.003"], "Face (Secondary)")
            abi.link(rig, f"j_f_dlip_02_{side.source}", f"DEF-Lip.B{side.suffix}.003")
            abi.rigify.basic_super_copy(rig, f"Lip.B{side.suffix}.004", widget_type="circle")
            abi.collection(rig, [f"Lip.B{side.suffix}.004"], "Face (Secondary)")
            abi.link(rig, f"j_f_dmlip_02_{side.source}", f"DEF-Lip.B{side.suffix}.004")

        # Teeth and tongue controls and mappings
        abi.rigify.basic_super_copy(rig, "Teeth.T", widget_type="teeth")
        abi.collection(rig, ["Teeth.T"], "Face (Misc)")
        abi.link(rig, "j_f_hagukiup", "DEF-Teeth.T")
        abi.rigify.basic_super_copy(rig, "Teeth.B", widget_type="teeth")
        abi.collection(rig, ["Teeth.B"], "Face (Misc)")
        abi.link(rig, "j_f_hagukidn", "DEF-Teeth.B")
        abi.rigify.basic_super_copy(rig, "Tongue", widget_type="circle")
        abi.collection(rig, ["Tongue"], "Face (Misc)")
        abi.link(rig, "j_f_bero_01", "DEF-Tongue")
        abi.rigify.basic_super_copy(rig, "Tongue.001", widget_type="circle")
        abi.collection(rig, ["Tongue.001"], "Face (Misc)")
        abi.link(rig, "j_f_bero_02", "DEF-Tongue.001")
        abi.rigify.basic_super_copy(rig, "Tongue.002", widget_type="circle")
        abi.collection(rig, ["Tongue.002"], "Face (Misc)")
        abi.link(rig, "j_f_bero_03", "DEF-Tongue.002")

    # ------------------------------------------------------------------------

    def final_pose(self, rig: bpy.types.Object) -> None:
        # Teeth widgets
        abi.widget(rig, "Teeth.T", rotation_degrees=(0.0, 0.0, 180.0), scale_factor=1.7)
        abi.widget(rig, "Teeth.B", rotation_degrees=(0.0, 0.0, 180.0), scale_factor=1.7)
