"""FFXIV player hands with optional IVCS finger tips."""

import typing

import bpy

from .... import definitions
from .... import instructions as abi


class Finger(typing.NamedTuple):
    """A finger's rigify name, the name used for it in the source bones and the number of its palm bone."""

    name: str
    source: str
    palm: str | None


THUMB = Finger("thumb", "oya", None)
LONG_FINGERS = (
    Finger("index", "hito", "palm.01"),
    Finger("middle", "naka", "palm.02"),
    Finger("ring", "kusu", "palm.03"),
    Finger("pinky", "ko", "palm.04"),
)


def required_bones(has_tip_bones: bool) -> list[str]:
    """Return the source bones used by the requested hand style."""
    bones = []
    for side in definitions.SIDES:
        for finger in (THUMB, *LONG_FINGERS):
            bones += [f"j_{finger.source}_a_{side.source}", f"j_{finger.source}_b_{side.source}"]
            if has_tip_bones and finger is not THUMB:
                bones.append(f"iv_{finger.source}_c_{side.source}")
    return bones


class Module(definitions.RigModule):
    """Choose standard or IVCS fingers from template toggles and available bones."""

    name = "FFXIV Player Hands"
    has_tip_bones: bool = False
    _enabled: bool = False

    # ------------------------------------------------------------------------

    def meta_edit(self, rig: bpy.types.Object) -> None:
        """Check the selected source bones and create palm and finger chains."""
        if self.toggles is None:
            raise ValueError(f"{self.name} requires template toggles")
        mode = self.toggles.ivcs
        if mode not in {"AUTO", "ON", "OFF"}:
            raise ValueError(f"Unknown IVCS mode: {mode}")
        self.has_tip_bones = mode != "OFF" and all(abi.has_bone(rig, bone) for bone in required_bones(True))
        self._enabled = abi.require_bones(rig, required_bones(self.has_tip_bones), self.name)
        if not self._enabled:
            return
        if mode == "ON" and not self.has_tip_bones:
            print(f"[AetherBlend] {self.name}: IVCS tip bones are incomplete; generating standard fingers.")
        for side in definitions.SIDES:
            # Palm bones
            abi.extend(
                rig,
                f"palm.01{side.suffix}",
                f"j_hito_a_{side.source}",
                start_point="head",
                parent=f"hand{side.suffix}",
                roll=-135 if side is definitions.LEFT else 135,
            )
            abi.extend(
                rig,
                f"palm.02{side.suffix}",
                f"j_naka_a_{side.source}",
                start_point="head",
                parent=f"hand{side.suffix}",
                roll=-135 if side is definitions.LEFT else 135,
            )
            abi.extend(
                rig,
                f"palm.03{side.suffix}",
                f"j_kusu_a_{side.source}",
                start_point="head",
                parent=f"hand{side.suffix}",
                roll=-135 if side is definitions.LEFT else 135,
            )
            abi.extend(
                rig,
                f"palm.04{side.suffix}",
                f"j_ko_a_{side.source}",
                start_point="head",
                parent=f"hand{side.suffix}",
                roll=-135 if side is definitions.LEFT else 135,
            )

            # Thumb chain
            abi.copy(
                rig,
                f"DEF-thumb_master{side.suffix}",
                f"j_oya_a_{side.source}",
                parent=[f"hand{side.suffix}", f"j_te_{side.source}"],
            )
            abi.connect(
                rig,
                f"thumb{side.suffix}",
                f"j_oya_a_{side.source}",
                f"j_oya_b_{side.source}",
                parent=f"DEF-thumb_master{side.suffix}",
                roll=-15,
            )
            abi.extend(
                rig,
                f"thumb{side.suffix}.001",
                f"j_oya_b_{side.source}",
                size_factor=0.2,
                start_point="head",
                parent=f"thumb{side.suffix}",
                connected=True,
            )

            # Finger chains
            abi.connect(
                rig,
                f"index{side.suffix}",
                f"j_hito_a_{side.source}",
                f"j_hito_b_{side.source}",
                parent=f"palm.01{side.suffix}",
                roll=-135 if side is definitions.LEFT else 135,
            )
            if self.has_tip_bones:
                abi.connect(
                    rig,
                    f"index{side.suffix}.001",
                    f"j_hito_b_{side.source}",
                    f"iv_hito_c_{side.source}",
                    parent=f"index{side.suffix}",
                    connected=True,
                )
                abi.extend(
                    rig,
                    f"index{side.suffix}.002",
                    f"iv_hito_c_{side.source}",
                    start_point="head",
                    parent=f"index{side.suffix}.001",
                    connected=True,
                )
            else:
                abi.extend(
                    rig,
                    f"index{side.suffix}.001",
                    f"j_hito_b_{side.source}",
                    start_point="head",
                    parent=f"index{side.suffix}",
                    connected=True,
                )

            abi.connect(
                rig,
                f"middle{side.suffix}",
                f"j_naka_a_{side.source}",
                f"j_naka_b_{side.source}",
                parent=f"palm.02{side.suffix}",
                roll=-135 if side is definitions.LEFT else 135,
            )
            if self.has_tip_bones:
                abi.connect(
                    rig,
                    f"middle{side.suffix}.001",
                    f"j_naka_b_{side.source}",
                    f"iv_naka_c_{side.source}",
                    parent=f"middle{side.suffix}",
                    connected=True,
                )
                abi.extend(
                    rig,
                    f"middle{side.suffix}.002",
                    f"iv_naka_c_{side.source}",
                    start_point="head",
                    parent=f"middle{side.suffix}.001",
                    connected=True,
                )
            else:
                abi.extend(
                    rig,
                    f"middle{side.suffix}.001",
                    f"j_naka_b_{side.source}",
                    start_point="head",
                    parent=f"middle{side.suffix}",
                    connected=True,
                )

            abi.connect(
                rig,
                f"ring{side.suffix}",
                f"j_kusu_a_{side.source}",
                f"j_kusu_b_{side.source}",
                parent=f"palm.03{side.suffix}",
                roll=-135 if side is definitions.LEFT else 135,
            )
            if self.has_tip_bones:
                abi.connect(
                    rig,
                    f"ring{side.suffix}.001",
                    f"j_kusu_b_{side.source}",
                    f"iv_kusu_c_{side.source}",
                    parent=f"ring{side.suffix}",
                    connected=True,
                )
                abi.extend(
                    rig,
                    f"ring{side.suffix}.002",
                    f"iv_kusu_c_{side.source}",
                    start_point="head",
                    parent=f"ring{side.suffix}.001",
                    connected=True,
                )
            else:
                abi.extend(
                    rig,
                    f"ring{side.suffix}.001",
                    f"j_kusu_b_{side.source}",
                    start_point="head",
                    parent=f"ring{side.suffix}",
                    connected=True,
                )

            abi.connect(
                rig,
                f"pinky{side.suffix}",
                f"j_ko_a_{side.source}",
                f"j_ko_b_{side.source}",
                parent=f"palm.04{side.suffix}",
                roll=-135 if side is definitions.LEFT else 135,
            )
            if self.has_tip_bones:
                abi.connect(
                    rig,
                    f"pinky{side.suffix}.001",
                    f"j_ko_b_{side.source}",
                    f"iv_ko_c_{side.source}",
                    parent=f"pinky{side.suffix}",
                    connected=True,
                )
                abi.extend(
                    rig,
                    f"pinky{side.suffix}.002",
                    f"iv_ko_c_{side.source}",
                    start_point="head",
                    parent=f"pinky{side.suffix}.001",
                    connected=True,
                )
            else:
                abi.extend(
                    rig,
                    f"pinky{side.suffix}.001",
                    f"j_ko_b_{side.source}",
                    start_point="head",
                    parent=f"pinky{side.suffix}",
                    connected=True,
                )

    # ------------------------------------------------------------------------

    def meta_pose(self, rig: bpy.types.Object) -> None:
        """Configure finger controls, collections, and source mappings."""
        if not self._enabled:
            return
        for side in definitions.SIDES:
            fingers_collection = f"Fingers{side.suffix}"

            # Palm controls
            abi.rigify.limbs_super_palm(rig, f"palm.01{side.suffix}", palm_both_sides=True)
            abi.collection(
                rig,
                [
                    f"palm.01{side.suffix}",
                    f"palm.02{side.suffix}",
                    f"palm.03{side.suffix}",
                    f"palm.04{side.suffix}",
                ],
                fingers_collection,
            )

            # Thumb master
            abi.rigify.basic_raw_copy(rig, f"DEF-thumb_master{side.suffix}", relink_constraints=True, parent="DEF")
            abi.collection(rig, [f"DEF-thumb_master{side.suffix}"], "DEF")

            # Finger controls and source-to-deform mappings
            abi.rigify.limbs_super_finger(
                rig,
                f"thumb{side.suffix}",
                extra_ik_control=True,
                extra_ik_collection=f"{fingers_collection} (IK)",
            )
            abi.collection(rig, [f"thumb{side.suffix}", f"thumb{side.suffix}.001"], fingers_collection)
            abi.link(rig, f"j_oya_a_{side.source}", f"DEF-thumb{side.suffix}")
            abi.link(rig, f"j_oya_b_{side.source}", f"DEF-thumb{side.suffix}.001")

            abi.rigify.limbs_super_finger(
                rig,
                f"index{side.suffix}",
                extra_ik_control=True,
                extra_ik_collection=f"{fingers_collection} (IK)",
            )
            if self.has_tip_bones:
                abi.collection(
                    rig,
                    [f"index{side.suffix}", f"index{side.suffix}.001", f"index{side.suffix}.002"],
                    fingers_collection,
                )
            else:
                abi.collection(rig, [f"index{side.suffix}", f"index{side.suffix}.001"], fingers_collection)
            abi.link(rig, f"j_hito_a_{side.source}", f"DEF-index{side.suffix}")
            abi.link(rig, f"j_hito_b_{side.source}", f"DEF-index{side.suffix}.001")
            if self.has_tip_bones:
                abi.link(rig, f"iv_hito_c_{side.source}", f"DEF-index{side.suffix}.002")

            abi.rigify.limbs_super_finger(
                rig,
                f"middle{side.suffix}",
                extra_ik_control=True,
                extra_ik_collection=f"{fingers_collection} (IK)",
            )
            if self.has_tip_bones:
                abi.collection(
                    rig,
                    [f"middle{side.suffix}", f"middle{side.suffix}.001", f"middle{side.suffix}.002"],
                    fingers_collection,
                )
            else:
                abi.collection(rig, [f"middle{side.suffix}", f"middle{side.suffix}.001"], fingers_collection)
            abi.link(rig, f"j_naka_a_{side.source}", f"DEF-middle{side.suffix}")
            abi.link(rig, f"j_naka_b_{side.source}", f"DEF-middle{side.suffix}.001")
            if self.has_tip_bones:
                abi.link(rig, f"iv_naka_c_{side.source}", f"DEF-middle{side.suffix}.002")

            abi.rigify.limbs_super_finger(
                rig,
                f"ring{side.suffix}",
                extra_ik_control=True,
                extra_ik_collection=f"{fingers_collection} (IK)",
            )
            if self.has_tip_bones:
                abi.collection(
                    rig,
                    [f"ring{side.suffix}", f"ring{side.suffix}.001", f"ring{side.suffix}.002"],
                    fingers_collection,
                )
            else:
                abi.collection(rig, [f"ring{side.suffix}", f"ring{side.suffix}.001"], fingers_collection)
            abi.link(rig, f"j_kusu_a_{side.source}", f"DEF-ring{side.suffix}")
            abi.link(rig, f"j_kusu_b_{side.source}", f"DEF-ring{side.suffix}.001")
            if self.has_tip_bones:
                abi.link(rig, f"iv_kusu_c_{side.source}", f"DEF-ring{side.suffix}.002")

            abi.rigify.limbs_super_finger(
                rig,
                f"pinky{side.suffix}",
                extra_ik_control=True,
                extra_ik_collection=f"{fingers_collection} (IK)",
            )
            if self.has_tip_bones:
                abi.collection(
                    rig,
                    [f"pinky{side.suffix}", f"pinky{side.suffix}.001", f"pinky{side.suffix}.002"],
                    fingers_collection,
                )
            else:
                abi.collection(rig, [f"pinky{side.suffix}", f"pinky{side.suffix}.001"], fingers_collection)
            abi.link(rig, f"j_ko_a_{side.source}", f"DEF-pinky{side.suffix}")
            abi.link(rig, f"j_ko_b_{side.source}", f"DEF-pinky{side.suffix}.001")
            if self.has_tip_bones:
                abi.link(rig, f"iv_ko_c_{side.source}", f"DEF-pinky{side.suffix}.002")

    # ------------------------------------------------------------------------

    def final_edit(self, rig: bpy.types.Object) -> None:
        """Parent the two generated palm controls on each side."""
        if not self._enabled:
            return
        # Palm hierarchy
        for side in definitions.SIDES:
            abi.parent(rig, f"palm.01{side.suffix}", [f"hand{side.suffix}", f"j_te_{side.source}"])
            abi.parent(rig, f"palm{side.suffix}", [f"hand{side.suffix}", f"j_te_{side.source}"])
