"""IVCS toes: five toes per foot with finger-style Rigify controls."""

import bpy

from .... import definitions
from .... import instructions as abi


class Module(definitions.RigModule):
    """Build IVCS toe controls only for complete source toe chains."""

    name = "FFXIV Player Toes"
    _enabled: bool = False
    _source_bones = [
        "iv_asi_oya_a_l",
        "iv_asi_oya_a_r",
        "iv_asi_oya_b_l",
        "iv_asi_oya_b_r",
        "iv_asi_hito_a_l",
        "iv_asi_hito_a_r",
        "iv_asi_hito_b_l",
        "iv_asi_hito_b_r",
        "iv_asi_naka_a_l",
        "iv_asi_naka_a_r",
        "iv_asi_naka_b_l",
        "iv_asi_naka_b_r",
        "iv_asi_kusu_a_l",
        "iv_asi_kusu_a_r",
        "iv_asi_kusu_b_l",
        "iv_asi_kusu_b_r",
        "iv_asi_ko_a_l",
        "iv_asi_ko_a_r",
        "iv_asi_ko_b_l",
        "iv_asi_ko_b_r",
    ]

    # ------------------------------------------------------------------------

    def meta_edit(self, rig: bpy.types.Object) -> None:
        """Check the source toe bones and create the control chains."""
        if self.toggles is None:
            raise ValueError(f"{self.name} requires template toggles")
        mode = self.toggles.ivcs
        if mode not in {"AUTO", "ON", "OFF"}:
            raise ValueError(f"Unknown IVCS mode: {mode}")
        self._enabled = False
        if mode == "OFF":
            return
        if mode == "AUTO" and not all(abi.has_bone(rig, bone) for bone in self._source_bones):
            return
        self._enabled = abi.require_bones(rig, self._source_bones, self.name)
        if not self._enabled:
            return
        for side in definitions.SIDES:
            # Toe chains
            abi.connect(
                rig,
                f"Hallux_Toe{side.suffix}",
                f"iv_asi_oya_a_{side.source}",
                f"iv_asi_oya_b_{side.source}",
                parent=[f"toe{side.suffix}", f"j_asi_e_{side.source}"],
            )
            abi.extend(
                rig,
                f"Hallux_Toe{side.suffix}.001",
                f"iv_asi_oya_b_{side.source}",
                parent=f"Hallux_Toe{side.suffix}",
                connected=True,
            )
            abi.connect(
                rig,
                f"Index_Toe{side.suffix}",
                f"iv_asi_hito_a_{side.source}",
                f"iv_asi_hito_b_{side.source}",
                parent=[f"toe{side.suffix}", f"j_asi_e_{side.source}"],
            )
            abi.extend(
                rig,
                f"Index_Toe{side.suffix}.001",
                f"iv_asi_hito_b_{side.source}",
                parent=f"Index_Toe{side.suffix}",
                connected=True,
            )
            abi.connect(
                rig,
                f"Middle_Toe{side.suffix}",
                f"iv_asi_naka_a_{side.source}",
                f"iv_asi_naka_b_{side.source}",
                parent=[f"toe{side.suffix}", f"j_asi_e_{side.source}"],
            )
            abi.extend(
                rig,
                f"Middle_Toe{side.suffix}.001",
                f"iv_asi_naka_b_{side.source}",
                parent=f"Middle_Toe{side.suffix}",
                connected=True,
            )
            abi.connect(
                rig,
                f"Ring_Toe{side.suffix}",
                f"iv_asi_kusu_a_{side.source}",
                f"iv_asi_kusu_b_{side.source}",
                parent=[f"toe{side.suffix}", f"j_asi_e_{side.source}"],
            )
            abi.extend(
                rig,
                f"Ring_Toe{side.suffix}.001",
                f"iv_asi_kusu_b_{side.source}",
                parent=f"Ring_Toe{side.suffix}",
                connected=True,
            )
            abi.connect(
                rig,
                f"Pinky_Toe{side.suffix}",
                f"iv_asi_ko_a_{side.source}",
                f"iv_asi_ko_b_{side.source}",
                parent=[f"toe{side.suffix}", f"j_asi_e_{side.source}"],
            )
            abi.extend(
                rig,
                f"Pinky_Toe{side.suffix}.001",
                f"iv_asi_ko_b_{side.source}",
                parent=f"Pinky_Toe{side.suffix}",
                connected=True,
            )

    # ------------------------------------------------------------------------

    def meta_pose(self, rig: bpy.types.Object) -> None:
        """Configure toe controls and source mappings."""
        if not self._enabled:
            return
        for side in definitions.SIDES:
            # Toe controls and source-to-deform mappings
            abi.rigify.limbs_super_finger(rig, f"Hallux_Toe{side.suffix}")
            abi.collection(
                rig,
                [f"Hallux_Toe{side.suffix}", f"Hallux_Toe{side.suffix}.001"],
                f"Toes{side.suffix}",
            )
            abi.link(rig, f"iv_asi_oya_a_{side.source}", f"DEF-Hallux_Toe{side.suffix}")
            abi.link(rig, f"iv_asi_oya_b_{side.source}", f"DEF-Hallux_Toe{side.suffix}.001")
            abi.rigify.limbs_super_finger(rig, f"Index_Toe{side.suffix}")
            abi.collection(
                rig,
                [f"Index_Toe{side.suffix}", f"Index_Toe{side.suffix}.001"],
                f"Toes{side.suffix}",
            )
            abi.link(rig, f"iv_asi_hito_a_{side.source}", f"DEF-Index_Toe{side.suffix}")
            abi.link(rig, f"iv_asi_hito_b_{side.source}", f"DEF-Index_Toe{side.suffix}.001")
            abi.rigify.limbs_super_finger(rig, f"Middle_Toe{side.suffix}")
            abi.collection(
                rig,
                [f"Middle_Toe{side.suffix}", f"Middle_Toe{side.suffix}.001"],
                f"Toes{side.suffix}",
            )
            abi.link(rig, f"iv_asi_naka_a_{side.source}", f"DEF-Middle_Toe{side.suffix}")
            abi.link(rig, f"iv_asi_naka_b_{side.source}", f"DEF-Middle_Toe{side.suffix}.001")
            abi.rigify.limbs_super_finger(rig, f"Ring_Toe{side.suffix}")
            abi.collection(
                rig,
                [f"Ring_Toe{side.suffix}", f"Ring_Toe{side.suffix}.001"],
                f"Toes{side.suffix}",
            )
            abi.link(rig, f"iv_asi_kusu_a_{side.source}", f"DEF-Ring_Toe{side.suffix}")
            abi.link(rig, f"iv_asi_kusu_b_{side.source}", f"DEF-Ring_Toe{side.suffix}.001")
            abi.rigify.limbs_super_finger(rig, f"Pinky_Toe{side.suffix}")
            abi.collection(
                rig,
                [f"Pinky_Toe{side.suffix}", f"Pinky_Toe{side.suffix}.001"],
                f"Toes{side.suffix}",
            )
            abi.link(rig, f"iv_asi_ko_a_{side.source}", f"DEF-Pinky_Toe{side.suffix}")
            abi.link(rig, f"iv_asi_ko_b_{side.source}", f"DEF-Pinky_Toe{side.suffix}.001")
