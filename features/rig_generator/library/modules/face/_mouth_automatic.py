"""Mouth module: jaw, lips, teeth and tongue."""

import bpy

from .... import definitions
from .... import instructions as abi


class Module(definitions.RigModule):
    """Build the automated jaw, lips, teeth, and tongue for the face module."""

    # ------------------------------------------------------------------------

    def meta_edit(self, rig: bpy.types.Object) -> None:
        """Build the automated mouth control chains."""
        # Jaw chain
        abi.center(rig, "jaw_master_ref", ["j_f_dlip_01_r", "j_f_dlip_01_l"], axis="Y", parent="Head")
        abi.connect(rig, "jaw_master", "j_f_ago", "jaw_master_ref", parent="Head")

        # Lip centers
        abi.center(rig, "Mouth.Center", ["j_f_ulip_02_r", "j_f_ulip_02_l"], axis="Z", parent="Head")
        abi.center(rig, "Mouth.Center.001", ["j_f_dlip_02_r", "j_f_dlip_02_l"], axis="Z", parent="Head")

        # Main and secondary lip chains
        for side in definitions.SIDES:
            abi.connect(
                rig,
                f"Lip.T{side.suffix}",
                "Mouth.Center",
                f"j_f_ulip_02_{side.source}",
                connected=False,
                parent="jaw_master",
            )
            abi.connect(
                rig,
                f"Lip.T{side.suffix}.001",
                f"j_f_ulip_02_{side.source}",
                f"j_f_umlip_02_{side.source}",
                parent=f"Lip.T{side.suffix}",
                connected=True,
            )
            abi.connect(
                rig,
                f"Lip.T{side.suffix}.002",
                f"j_f_umlip_02_{side.source}",
                f"j_f_uslip_{side.source}",
                parent=f"Lip.T{side.suffix}.001",
                connected=True,
            )
            abi.connect(
                rig,
                f"Lip.T{side.suffix}.003",
                f"j_f_uslip_{side.source}",
                f"Corner{side.suffix}",
                parent=f"Lip.T{side.suffix}.002",
                connected=True,
            )
            abi.connect(
                rig,
                f"Lip.B{side.suffix}",
                "Mouth.Center.001",
                f"j_f_dlip_02_{side.source}",
                connected=False,
                parent="jaw_master",
            )
            abi.connect(
                rig,
                f"Lip.B{side.suffix}.001",
                f"j_f_dlip_02_{side.source}",
                f"j_f_dmlip_02_{side.source}",
                parent=f"Lip.B{side.suffix}",
                connected=True,
            )
            abi.connect(
                rig,
                f"Lip.B{side.suffix}.002",
                f"j_f_dmlip_02_{side.source}",
                f"j_f_dslip_{side.source}",
                parent=f"Lip.B{side.suffix}.001",
                connected=True,
            )
            abi.connect(
                rig,
                f"Lip.B{side.suffix}.003",
                f"j_f_dslip_{side.source}",
                f"Corner{side.suffix}",
                parent=f"Lip.B{side.suffix}.002",
                connected=True,
            )

            abi.connect(
                rig,
                f"Lip.Sec.T{side.suffix}",
                f"j_f_ulip_01_{side.source}",
                f"j_f_umlip_01_{side.source}",
                parent="Head",
            )
            abi.connect(
                rig,
                f"Lip.Sec.T{side.suffix}.001",
                f"j_f_umlip_01_{side.source}",
                f"j_f_uslip_{side.source}",
                parent=f"Lip.Sec.T{side.suffix}",
                connected=True,
            )
            abi.connect(
                rig,
                f"Lip.Sec.B{side.suffix}",
                f"j_f_dlip_01_{side.source}",
                f"j_f_dmlip_01_{side.source}",
                parent="Head",
            )
            abi.connect(
                rig,
                f"Lip.Sec.B{side.suffix}.001",
                f"j_f_dmlip_01_{side.source}",
                f"j_f_dslip_{side.source}",
                parent=f"Lip.Sec.B{side.suffix}",
                connected=True,
            )

            # Upper lip glue
            abi.connect(
                rig,
                f"Lip.T{side.suffix}.001.glue",
                f"j_f_hana_{side.source}",
                f"j_f_ulip_01_{side.source}",
                parent="Head",
            )

        # Teeth and tongue chain
        abi.extend(rig, "Teeth.T", "j_f_hagukiup", axis="Y", start_point="head", parent="Head")
        abi.extend(rig, "Teeth.B", "j_f_hagukidn", axis="Y", start_point="head", parent="jaw_master")
        abi.connect(rig, "Tongue", "j_f_bero_01", "j_f_bero_02", parent="jaw_master")
        abi.connect(rig, "Tongue.001", "j_f_bero_02", "j_f_bero_03", parent="Tongue", connected=True)
        abi.extend(rig, "Tongue.002", "Tongue.001", axis="Y", parent="Tongue.001", connected=True)

    # ------------------------------------------------------------------------

    def meta_pose(self, rig: bpy.types.Object) -> None:
        """Configure automated jaw and lip behavior and deform mappings."""
        # Jaw controls
        abi.rigify.face_skin_jaw(rig, "jaw_master", jaw_mouth_influence=1)
        abi.collection(rig, ["jaw_master"], "Face (Primary)")
        abi.collection(rig, ["jaw_master_ref", "Mouth.Center", "Mouth.Center.001"], "MCH")
        abi.link(rig, "j_f_ago", "DEF-jaw_master")

        # Main and secondary lip controls
        for side in definitions.SIDES:
            abi.rigify.skin_stretchy_chain(
                rig,
                f"Lip.T{side.suffix}",
                control_orientation_bone="Mouth.Center",
                falloff_length=True,
                falloff=[0.0, 0.0, -1.0],
                primary_collection="Face (Primary)",
                use_scale=[True, True, True, True],
            )
            abi.collection(
                rig,
                [
                    f"Lip.T{side.suffix}",
                    f"Lip.T{side.suffix}.001",
                    f"Lip.T{side.suffix}.002",
                    f"Lip.T{side.suffix}.003",
                ],
                "Face (Secondary)",
            )
            abi.link(rig, f"j_f_ulip_02_{side.source}", f"DEF-Lip.T{side.suffix}.001")
            abi.link(rig, f"j_f_umlip_02_{side.source}", f"DEF-Lip.T{side.suffix}.002")
            abi.link(rig, f"j_f_uslip_{side.source}", f"DEF-Lip.T{side.suffix}.003")

            abi.rigify.skin_stretchy_chain(
                rig,
                f"Lip.B{side.suffix}",
                control_orientation_bone="Mouth.Center",
                falloff_length=True,
                falloff=[0.0, 0.0, -1.0],
                primary_collection="Face (Primary)",
                use_scale=[True, True, True, True],
            )
            abi.collection(
                rig,
                [
                    f"Lip.B{side.suffix}",
                    f"Lip.B{side.suffix}.001",
                    f"Lip.B{side.suffix}.002",
                    f"Lip.B{side.suffix}.003",
                ],
                "Face (Secondary)",
            )
            abi.link(rig, f"j_f_dlip_02_{side.source}", f"DEF-Lip.B{side.suffix}.001")
            abi.link(rig, f"j_f_dmlip_02_{side.source}", f"DEF-Lip.B{side.suffix}.002")
            abi.link(rig, f"j_f_dslip_{side.source}", f"DEF-Lip.B{side.suffix}.003")

            abi.rigify.skin_basic_chain(rig, f"Lip.Sec.T{side.suffix}", control_orientation_bone="Mouth.Center")
            abi.collection(
                rig,
                [f"Lip.Sec.T{side.suffix}", f"Lip.Sec.T{side.suffix}.001"],
                "Face (Secondary)",
            )
            abi.link(rig, f"j_f_ulip_01_{side.source}", f"DEF-Lip.Sec.T{side.suffix}")
            abi.link(rig, f"j_f_umlip_01_{side.source}", f"DEF-Lip.Sec.T{side.suffix}.001")
            abi.rigify.skin_basic_chain(rig, f"Lip.Sec.B{side.suffix}", control_orientation_bone="Mouth.Center")
            abi.collection(
                rig,
                [f"Lip.Sec.B{side.suffix}", f"Lip.Sec.B{side.suffix}.001"],
                "Face (Secondary)",
            )
            abi.link(rig, f"j_f_dlip_01_{side.source}", f"DEF-Lip.Sec.B{side.suffix}")
            abi.link(rig, f"j_f_dmlip_01_{side.source}", f"DEF-Lip.Sec.B{side.suffix}.001")

            # Upper lip glue
            abi.rigify.skin_glue(
                rig,
                f"Lip.T{side.suffix}.001.glue",
                relink_constraints=True,
                use_tail=True,
                reparent_tail=True,
                add_constraint="COPY_LOCATION_OWNER",
                add_constraint_influence=0.2,
            )
            abi.collection(rig, [f"Lip.T{side.suffix}.001.glue"], "MCH")

        # Teeth and tongue controls and source-to-deform mappings
        abi.rigify.basic_super_copy(rig, "Teeth.T", widget_type="teeth")
        abi.collection(rig, ["Teeth.T"], "Face (Misc)")
        abi.link(rig, "j_f_hagukiup", "DEF-Teeth.T")
        abi.rigify.basic_super_copy(rig, "Teeth.B", widget_type="teeth")
        abi.collection(rig, ["Teeth.B"], "Face (Misc)")
        abi.link(rig, "j_f_hagukidn", "DEF-Teeth.B")
        abi.rigify.skin_stretchy_chain(rig, "Tongue", control_orientation_bone="Mouth.Center")
        abi.collection(rig, ["Tongue", "Tongue.001", "Tongue.002"], "Face (Misc)")
        abi.link(rig, "j_f_bero_01", "DEF-Tongue")
        abi.link(rig, "j_f_bero_02", "DEF-Tongue.001")
        abi.link(rig, "j_f_bero_03", "DEF-Tongue.002")

    # ------------------------------------------------------------------------

    def final_edit(self, rig: bpy.types.Object) -> None:
        """Attach secondary lips to the generated primary lip offsets."""
        # Secondary lips follow the offset bones made for the main lip chains.
        for side in definitions.SIDES:
            abi.parent(rig, f"Lip.Sec.T{side.suffix}", f"MCH-Lip_offset.T{side.suffix}.001")
            abi.parent(rig, f"Lip.Sec.T{side.suffix}.001", f"MCH-Lip_offset.T{side.suffix}.002")
            abi.parent(rig, f"Lip.Sec.B{side.suffix}", f"MCH-Lip_offset.B{side.suffix}.001")
            abi.parent(rig, f"Lip.Sec.B{side.suffix}.001", f"MCH-Lip_offset.B{side.suffix}.002")

    # ------------------------------------------------------------------------

    def final_pose(self, rig: bpy.types.Object) -> None:
        """Configure teeth and automated mouth widgets."""
        # Teeth and mouth widgets
        abi.widget(rig, "Teeth.T", rotation_degrees=(0.0, 0.0, 180.0), scale_factor=1.7)
        abi.widget(rig, "Teeth.B", rotation_degrees=(0.0, 0.0, 180.0), scale_factor=1.7)
        abi.widget(rig, "jaw_master_mouth", scale=(0.6, 1.0, 0.3))
