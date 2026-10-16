"""Female IVCS genitals."""

import bpy

from .... import definitions
from .... import instructions as abi
from ....rigify import settings


class Module(definitions.RigModule):
    name = "XIV-IVCS Female"
    ui_collections = settings.UI_Collections(
        [
            settings.BoneCollection(
                name="Genitals (Female)",
                ui=True,
                color_set="IVCS",
                row_index=1,
                title="Genitals (Female)",
                visible=False,
            ),
        ]
    )

    # ------------------------------------------------------------------------

    def meta_edit(self, rig: bpy.types.Object) -> None:
        # Optional control bones
        if abi.has_bone(rig, "iv_kuritto") and abi.has_bone(rig, "j_kosi"):
            abi.connect(rig, "Clitoris", "iv_kuritto", "j_kosi", parent=["Spine.001", "j_kosi"])
        if abi.has_bone(rig, "iv_inshin_r") and abi.has_bone(rig, "j_kosi"):
            abi.connect(rig, "Vulva.R", "iv_inshin_r", "j_kosi", parent="Spine.001")
        if abi.has_bone(rig, "iv_inshin_l") and abi.has_bone(rig, "j_kosi"):
            abi.connect(rig, "Vulva.L", "iv_inshin_l", "j_kosi", parent="Spine.001")
        if abi.has_bone(rig, "iv_omanko") and abi.has_bone(rig, "j_kosi"):
            abi.connect(rig, "Vulva", "iv_omanko", "j_kosi", parent="Spine.001")

        # Anchor helper
        if abi.has_bone(rig, "Clitoris"):
            abi.extend(rig, "Anchor_V", "Clitoris", parent="Spine.001")

    # ------------------------------------------------------------------------

    def meta_pose(self, rig: bpy.types.Object) -> None:
        # Controls and source-to-deform mappings
        if "Clitoris" in rig.pose.bones:
            abi.rigify.skin_basic_chain(rig, "Clitoris", control_orientation_bone="Spine.001")
            abi.collection(rig, ["Clitoris"], "Genitals (Female)")
            abi.link(rig, "iv_kuritto", "DEF-Clitoris")
        if "Vulva.R" in rig.pose.bones:
            abi.rigify.skin_basic_chain(rig, "Vulva.R", control_orientation_bone="Spine.001")
            abi.collection(rig, ["Vulva.R"], "Genitals (Female)")
            abi.link(rig, "iv_inshin_r", "DEF-Vulva.R")
        if "Vulva.L" in rig.pose.bones:
            abi.rigify.skin_basic_chain(rig, "Vulva.L", control_orientation_bone="Spine.001")
            abi.collection(rig, ["Vulva.L"], "Genitals (Female)")
            abi.link(rig, "iv_inshin_l", "DEF-Vulva.L")
        if "Vulva" in rig.pose.bones:
            abi.rigify.skin_basic_chain(rig, "Vulva", control_orientation_bone="Spine.001")
            abi.collection(rig, ["Vulva"], "Genitals (Female)")
            abi.link(rig, "iv_omanko", "DEF-Vulva")

        if "Anchor_V" in rig.pose.bones:
            abi.rigify.skin_anchor(rig, "Anchor_V", hide=True)
            abi.collection(rig, ["Anchor_V"], "Genitals (Female)")

    # ------------------------------------------------------------------------

    def final_pose(self, rig: bpy.types.Object) -> None:
        # Control widgets
        abi.widget(rig, "Clitoris", scale_factor=0.2)
        abi.widget(rig, "Vulva.R", scale_factor=0.2)
        abi.widget(rig, "Vulva.L", scale_factor=0.2)
        abi.widget(rig, "Vulva", scale_factor=0.2)
