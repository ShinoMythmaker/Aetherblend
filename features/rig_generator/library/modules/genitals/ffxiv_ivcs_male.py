"""Male IVCS genitals."""

import bpy

from .... import definitions
from .... import instructions as abi
from ....rigify import settings


class Module(definitions.RigModule):
    name = "XIV-IVCS Male"
    ui_collections = settings.UI_Collections(
        [
            settings.BoneCollection(
                name="Genitals (Male)",
                ui=True,
                color_set="IVCS",
                row_index=1,
                title="Genitals (Male)",
                visible=False,
            ),
        ]
    )

    # ------------------------------------------------------------------------

    def meta_edit(self, rig: bpy.types.Object) -> None:
        # Penis chain
        if abi.has_bone(rig, "iv_ochinko_a") and abi.has_bone(rig, "iv_ochinko_b"):
            abi.connect(rig, "Penis", "iv_ochinko_a", "iv_ochinko_b", parent=["Spine.001", "j_kosi"])
            abi.connect(
                rig,
                "Penis.001",
                "iv_ochinko_b",
                "iv_ochinko_c",
                parent="Penis",
                connected=True,
            )
            abi.connect(
                rig,
                "Penis.002",
                "iv_ochinko_c",
                "iv_ochinko_d",
                parent="Penis.001",
                connected=True,
            )
            abi.connect(
                rig,
                "Penis.003",
                "iv_ochinko_d",
                "iv_ochinko_e",
                parent="Penis.002",
                connected=True,
            )
            abi.connect(
                rig,
                "Penis.004",
                "iv_ochinko_e",
                "iv_ochinko_f",
                parent="Penis.003",
                connected=True,
            )
            abi.extend(rig, "Penis.005", "iv_ochinko_f", parent="Penis.004", connected=True)

        # Testicle bones
        for side in definitions.SIDES:
            if abi.has_bone(rig, f"iv_kougan_{side.source}"):
                abi.extend(
                    rig,
                    f"Testicle{side.suffix}",
                    f"iv_kougan_{side.source}",
                    start_point="head",
                    size_factor=0.5,
                    parent=["Spine.001", "j_kosi"],
                )

    # ------------------------------------------------------------------------

    def meta_pose(self, rig: bpy.types.Object) -> None:
        # Penis controls and source-to-deform mappings
        if "Penis" in rig.pose.bones:
            abi.rigify.limbs_spline_tentacle(rig, "Penis", sik_stretch_control="MANUAL_STRETCH")
            abi.collection(
                rig,
                ["Penis", "Penis.001", "Penis.002", "Penis.003", "Penis.004", "Penis.005"],
                "Genitals (Male)",
            )
            abi.link(rig, "iv_ochinko_a", "DEF-Penis")
            abi.link(rig, "iv_ochinko_b", "DEF-Penis.001")
            abi.link(rig, "iv_ochinko_c", "DEF-Penis.002")
            abi.link(rig, "iv_ochinko_d", "DEF-Penis.003")
            abi.link(rig, "iv_ochinko_e", "DEF-Penis.004")
            abi.link(rig, "iv_ochinko_f", "DEF-Penis.005")

        # Testicle controls and source-to-deform mappings
        for side in definitions.SIDES:
            if f"Testicle{side.suffix}" in rig.pose.bones:
                abi.rigify.skin_basic_chain(rig, f"Testicle{side.suffix}", control_orientation_bone="Spine.001")
                abi.collection(rig, [f"Testicle{side.suffix}"], "Genitals (Male)")
                abi.link(rig, f"iv_kougan_{side.source}", f"DEF-Testicle{side.suffix}")
