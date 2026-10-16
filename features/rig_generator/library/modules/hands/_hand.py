"""Hands shared by every hand variant; a variant only decides whether the fingers have IVCS tip bones."""

from typing import NamedTuple

import bpy

from ....definitions import RigModule
from ....instructions import *
from ....rigify.settings import BoneCollection, UI_Collections


class Side(NamedTuple):
    suffix: str
    letter: str
    palm_roll: float
    color_set: str


class Finger(NamedTuple):
    """A finger's rigify name, the name used for it in the source bones and the number of its palm bone."""

    name: str
    source: str
    palm: str | None


SIDES = (
    Side(".R", "r", 135, "Fingers_Right"),
    Side(".L", "l", -135, "Fingers_Left"),
)
THUMB = Finger("thumb", "oya", None)
LONG_FINGERS = (
    Finger("index", "hito", "palm.01"),
    Finger("middle", "naka", "palm.02"),
    Finger("ring", "kusu", "palm.03"),
    Finger("pinky", "ko", "palm.04"),
)
THUMB_ROLL = -15


def required_bones(has_tip_bones: bool) -> list[str]:
    bones = []
    for side in SIDES:
        for finger in (THUMB, *LONG_FINGERS):
            bones += [f"j_{finger.source}_a_{side.letter}", f"j_{finger.source}_b_{side.letter}"]
            if has_tip_bones and finger is not THUMB:
                bones.append(f"iv_{finger.source}_c_{side.letter}")
    return bones


def ui_collections() -> UI_Collections:
    return UI_Collections(
        [
            BoneCollection(
                name=f"Fingers{side.suffix}",
                ui=True,
                color_set=side.color_set,
                row_index=1,
                title=f"Fingers{side.suffix}",
                visible=False,
            )
            for side in SIDES
        ]
    )


class Hands(RigModule):
    has_tip_bones = False

    def meta_edit(self, rig: bpy.types.Object) -> None:
        for side in SIDES:
            hand_parents = [f"hand{side.suffix}", f"j_te_{side.letter}"]

            for finger in LONG_FINGERS:
                extend(
                    rig,
                    f"{finger.palm}{side.suffix}",
                    f"j_{finger.source}_a_{side.letter}",
                    start_point="head",
                    parent=f"hand{side.suffix}",
                    roll=side.palm_roll,
                )

            thumb_master = f"DEF-thumb_master{side.suffix}"
            copy(rig, thumb_master, f"j_oya_a_{side.letter}", parent=hand_parents)
            connect(
                rig,
                f"thumb{side.suffix}",
                f"j_oya_a_{side.letter}",
                f"j_oya_b_{side.letter}",
                parent=thumb_master,
                roll=THUMB_ROLL,
            )
            extend(
                rig,
                f"thumb{side.suffix}.001",
                f"j_oya_b_{side.letter}",
                size_factor=0.2,
                start_point="head",
                parent=f"thumb{side.suffix}",
                connected=True,
            )

            for finger in LONG_FINGERS:
                base = f"{finger.name}{side.suffix}"
                lower, upper = f"j_{finger.source}_a_{side.letter}", f"j_{finger.source}_b_{side.letter}"
                connect(rig, base, lower, upper, parent=f"{finger.palm}{side.suffix}", roll=side.palm_roll)

                if self.has_tip_bones:
                    tip = f"iv_{finger.source}_c_{side.letter}"
                    connect(rig, f"{base}.001", upper, tip, parent=base, connected=True)
                    extend(rig, f"{base}.002", tip, start_point="head", parent=f"{base}.001", connected=True)
                else:
                    extend(rig, f"{base}.001", upper, start_point="head", parent=base, connected=True)

    def meta_pose(self, rig: bpy.types.Object) -> None:
        for side in SIDES:
            fingers_collection = f"Fingers{side.suffix}"
            thumb_master = f"DEF-thumb_master{side.suffix}"

            rigify.limbs_super_palm(rig, f"palm.01{side.suffix}", palm_both_sides=True)
            collection(rig, [f"{finger.palm}{side.suffix}" for finger in LONG_FINGERS], fingers_collection)

            rigify.basic_raw_copy(rig, thumb_master, relink_constraints=True, parent="DEF")
            collection(rig, [thumb_master], "DEF")

            tip_count = 2 if self.has_tip_bones else 1
            for finger in (THUMB, *LONG_FINGERS):
                base = f"{finger.name}{side.suffix}"
                rigify.limbs_super_finger(
                    rig, base, extra_ik_control=True, extra_ik_collection=f"{fingers_collection} (IK)"
                )

                segment_count = 1 if finger is THUMB else tip_count
                segments = [base] + [f"{base}.{number:03}" for number in range(1, segment_count + 1)]
                collection(rig, segments, fingers_collection)

                link(rig, f"j_{finger.source}_a_{side.letter}", f"DEF-{base}")
                link(rig, f"j_{finger.source}_b_{side.letter}", f"DEF-{base}.001")
                if self.has_tip_bones and finger is not THUMB:
                    link(rig, f"iv_{finger.source}_c_{side.letter}", f"DEF-{base}.002")

    def final_edit(self, rig: bpy.types.Object) -> None:
        for side in SIDES:
            for finger in LONG_FINGERS:
                parent(rig, f"{finger.palm}{side.suffix}", [f"hand{side.suffix}", f"j_te_{side.letter}"])
