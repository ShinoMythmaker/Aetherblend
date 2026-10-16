"""Arm module: IK/FK arms with clavicle, elbow and pauldron helpers."""
from typing import NamedTuple

import bpy

from ....definitions import RigModule
from ....instructions import *
from ....rigify.settings import BoneCollection, UI_Collections


class Side(NamedTuple):
    """Naming of one body side and how the pauldron follows the upper arm on it."""

    suffix: str
    source: str
    name: str
    pauldron_twist_expression: str
    pauldron_swing_expression: str


LEFT = Side(".L", "l", "Left", pauldron_twist_expression="-RotX", pauldron_swing_expression="RotZ")
RIGHT = Side(".R", "r", "Right", pauldron_twist_expression="RotX", pauldron_swing_expression="-RotZ")
SIDES = (LEFT, RIGHT)


def _ui_collections() -> UI_Collections:
    collections: list[BoneCollection] = []
    for side in SIDES:
        collections += [
            BoneCollection(name=f"Arm{side.suffix} (IK)", ui=True, color_set=f"IK_{side.name}", row_index=1, title=f"Arm IK{side.suffix}"),
            BoneCollection(name=f"Arm{side.suffix} (FK)", ui=True, color_set=f"FK_{side.name}", row_index=2, title=f"Arm FK{side.suffix}", visible=False),
            BoneCollection(name=f"Arm{side.suffix} (Tweak)", ui=True, color_set=f"Tweak_{side.name}", row_index=3, title=f"Tweak{side.suffix}", visible=False),
        ]
    return UI_Collections(collections)


class Module(RigModule):
    name = "XIV-Default"
    requires = tuple(
        f"{part}_{side.source}"
        for side in SIDES
        for part in ("j_sako", "j_ude_a", "j_ude_b", "j_te", "n_kataarmor", "n_hhiji")
    )
    ui_collections = _ui_collections()

    def meta_edit(self, rig: bpy.types.Object) -> None:
        for side in SIDES:
            suffix = side.suffix
            source_clavicle = f"j_sako_{side.source}"
            source_upper_arm = f"j_ude_a_{side.source}"
            source_forearm = f"j_ude_b_{side.source}"
            source_hand = f"j_te_{side.source}"
            source_elbow = f"n_hhiji_{side.source}"
            source_pauldron = f"n_kataarmor_{side.source}"

            extend(rig, f"MCH-pauldron{suffix}", source_pauldron, start_point="head", parent="Spine.004")
            extend(rig, f"pauldron{suffix}", source_pauldron, start_point="head", parent=f"MCH-pauldron{suffix}")

            connect(rig, f"clavicle{suffix}", source_clavicle, source_upper_arm, parent=["Spine.004", "j_sebo_c"])
            connect(rig, f"upper_arm{suffix}", source_upper_arm, source_forearm, parent=f"clavicle{suffix}")
            connect(rig, f"forearm{suffix}", source_forearm, source_hand, parent=f"upper_arm{suffix}", connected=True)
            extend(rig, f"hand{suffix}", source_hand, size_factor=0.6, parent=f"forearm{suffix}", connected=True)
            extend(rig, f"elbow{suffix}", source_elbow, start_point="head", size_factor=0.5, parent=f"forearm{suffix}")

    def meta_pose(self, rig: bpy.types.Object) -> None:
        for side in SIDES:
            suffix = side.suffix

            rigify.basic_raw_copy(rig, f"MCH-pauldron{suffix}")
            rigify.basic_super_copy(rig, f"pauldron{suffix}", widget_type="shoulder")
            rigify.basic_super_copy(rig, f"clavicle{suffix}", widget_type="shoulder")
            rigify.limbs_arm(rig, f"upper_arm{suffix}", fk_collection=f"Arm{suffix} (FK)", tweak_collection=f"Arm{suffix} (Tweak)")
            rigify.basic_super_copy(rig, f"elbow{suffix}", widget_type="pivot_cross")

            collection(rig, [f"pauldron{suffix}", f"elbow{suffix}"], f"Arm{suffix} (Tweak)")
            collection(rig, [f"upper_arm{suffix}", f"forearm{suffix}", f"hand{suffix}"], f"Arm{suffix} (IK)")
            collection(rig, [f"clavicle{suffix}"], "Torso")

            link(rig, f"j_ude_a_{side.source}", f"DEF-upper_arm{suffix}.001")
            link(rig, f"j_ude_b_{side.source}", f"DEF-forearm{suffix}")
            link(rig, f"j_te_{side.source}", f"DEF-hand{suffix}")
            link(rig, f"j_sako_{side.source}", f"DEF-clavicle{suffix}")
            link(rig, f"n_hte_{side.source}", f"DEF-forearm{suffix}.001")
            link(rig, f"n_hhiji_{side.source}", f"DEF-elbow{suffix}")
            link(rig, f"n_kataarmor_{side.source}", f"DEF-pauldron{suffix}")

    def final_pose(self, rig: bpy.types.Object) -> None:
        for side in SIDES:
            suffix = side.suffix
            deform_upper_arm = f"DEF-upper_arm{suffix}"

            collection(rig, [f"MCH-pauldron{suffix}"], "MCH")
            driver(
                rig, f"MCH-pauldron{suffix}", "rotation_quaternion", index=3,
                expression=side.pauldron_twist_expression,
                variables={"RotX": TransformVariable(deform_upper_arm, "ROT_X")},
            )
            driver(
                rig, f"MCH-pauldron{suffix}", "rotation_quaternion", index=1,
                expression=side.pauldron_swing_expression,
                variables={"RotZ": TransformVariable(deform_upper_arm, "ROT_Z")},
            )
            widget(rig, f"pauldron{suffix}", widget_name="Pauldron", scale_to_bone_length=True, wire_width=1)
            prop(rig, f"upper_arm_parent{suffix}", "IK_Stretch", 0)
