"""Leg module: IK/FK legs with knee and heel helpers."""
from typing import NamedTuple

import bpy

from ....instructions import *
from ....module import RigModule
from ....rigify.settings import BoneCollection, UI_Collections


class Side(NamedTuple):
    """Naming of one body side."""

    suffix: str
    source: str
    name: str


LEFT = Side(".L", "l", "Left")
RIGHT = Side(".R", "r", "Right")
SIDES = (LEFT, RIGHT)


def _ui_collections() -> UI_Collections:
    collections: list[BoneCollection] = []
    for side in SIDES:
        collections += [
            BoneCollection(name=f"Leg{side.suffix} (IK)", ui=True, color_set=f"IK_{side.name}", row_index=1, title=f"Leg IK{side.suffix}"),
            BoneCollection(name=f"Leg{side.suffix} (FK)", ui=True, color_set=f"FK_{side.name}", row_index=2, title=f"Leg FK{side.suffix}", visible=False),
            BoneCollection(name=f"Leg{side.suffix} (Tweak)", ui=True, color_set=f"Tweak_{side.name}", row_index=3, title=f"Tweak{side.suffix}", visible=False),
        ]
    return UI_Collections(collections)


class Module(RigModule):
    name = "XIV-Default"
    requires = tuple(f"j_asi_{part}_{side.source}" for side in SIDES for part in "abcde")
    ui_collections = _ui_collections()

    def meta_edit(self, rig: bpy.types.Object) -> None:
        for side in SIDES:
            suffix = side.suffix
            source_thigh = f"j_asi_a_{side.source}"
            source_knee = f"j_asi_b_{side.source}"
            source_shin = f"j_asi_c_{side.source}"
            source_ankle = f"j_asi_d_{side.source}"
            source_toe = f"j_asi_e_{side.source}"

            connect(rig, f"thigh{suffix}", source_thigh, source_knee, end_point="tail", parent=["Spine.001", "j_kosi"], roll=-90)
            connect(rig, f"shin{suffix}", source_knee, source_ankle, start_point="tail", parent=f"thigh{suffix}", connected=True, roll=-90)
            # The left foot has never had a roll; kept so the rig stays identical.
            foot_roll = -90 if side is RIGHT else 0
            connect(rig, f"foot{suffix}", source_ankle, source_toe, parent=f"shin{suffix}", connected=True, roll=foot_roll)
            extend(rig, f"toe{suffix}", source_toe, start_point="head", parent=f"foot{suffix}", connected=True)

            parallel(
                rig, f"heel_pivot{suffix}.helper", f"toe{suffix}", f"shin{suffix}",
                start_point="head", end_point="tail", coordinate="Y", parent=f"shin{suffix}",
            )
            extend(rig, f"heel_pivot{suffix}", f"heel_pivot{suffix}.helper", parent=f"foot{suffix}")

            extend(rig, f"MCH-knee{suffix}", source_knee, start_point="head", size_factor=1.5, parent="spine.001")
            extend(rig, f"knee{suffix}", source_knee, start_point="head", size_factor=1.5, parent="spine.001")
            extend(rig, f"MCH-knee_target{suffix}", source_shin, start_point="head", size_factor=0.2, parent="spine.001")

    def meta_pose(self, rig: bpy.types.Object) -> None:
        for side in SIDES:
            suffix = side.suffix

            rigify.limbs_leg(rig, f"thigh{suffix}", fk_collection=f"Leg{suffix} (FK)", tweak_collection=f"Leg{suffix} (Tweak)")
            rigify.basic_raw_copy(rig, f"MCH-knee{suffix}")
            rigify.basic_super_copy(rig, f"knee{suffix}")
            rigify.basic_raw_copy(rig, f"MCH-knee_target{suffix}")

            collection(
                rig,
                [f"thigh{suffix}", f"shin{suffix}", f"foot{suffix}", f"toe{suffix}", f"heel_pivot{suffix}.helper", f"heel_pivot{suffix}"],
                f"Leg{suffix} (IK)",
            )
            collection(rig, [f"MCH-knee{suffix}", f"knee{suffix}", f"MCH-knee_target{suffix}"], "MCH")

            link(rig, f"j_asi_a_{side.source}", f"DEF-thigh{suffix}.001")
            link(rig, f"j_asi_c_{side.source}", f"DEF-shin{suffix}.001")
            link(rig, f"j_asi_d_{side.source}", f"DEF-foot{suffix}")
            link(rig, f"j_asi_e_{side.source}", f"DEF-toe{suffix}")
            link(rig, f"j_asi_b_{side.source}", f"DEF-knee{suffix}")

    def final_edit(self, rig: bpy.types.Object) -> None:
        # Rigify's leg rejects its own bones as parents, so these are reparented after generation.
        for side in SIDES:
            suffix = side.suffix
            parent(rig, f"MCH-knee{suffix}", f"DEF-thigh{suffix}.001")
            parent(rig, f"knee{suffix}", f"MCH-knee{suffix}")
            parent(rig, f"MCH-knee_target{suffix}", f"DEF-shin{suffix}")

    def final_pose(self, rig: bpy.types.Object) -> None:
        for side in SIDES:
            suffix = side.suffix
            constraints.damped_track(rig, f"MCH-knee{suffix}", target=f"MCH-knee_target{suffix}")
            prop(rig, f"thigh_parent{suffix}", "IK_Stretch", 0)
