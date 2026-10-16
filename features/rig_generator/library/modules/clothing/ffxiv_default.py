"""Clothing module: a skirt whose segments swing with the thighs and shins."""
from typing import NamedTuple

from ....definitions import RigModule
from ....instructions import *
from ....rigify.settings import BoneCollection, UI_Collections

SKIRT_COLLECTION = "Skirt"
AUTOMATION_PROPERTY = "skirt_automation"
ROTATION_X_INDEX = 1
ROTATION_Z_INDEX = 3


class Side(NamedTuple):
    """One body side: its naming, the middle segment roll and the signs that mirror the swing expressions."""

    suffix: str
    source: str
    middle_roll: float
    middle_sign: str
    sideways_comparison: str


LEFT = Side(".L", "l", middle_roll=-7, middle_sign="", sideways_comparison="<")
RIGHT = Side(".R", "r", middle_roll=-173, middle_sign="-", sideways_comparison=">")
SIDES = (LEFT, RIGHT)


class Section(NamedTuple):
    """A skirt segment: the control chain, the driven helper chain and the expressions that move the helper."""

    control: str
    driven: str
    source: str
    roll: float
    first_forward_expression: str
    first_sideways_expression: str
    second_forward_expression: str


def _sections(side: Side) -> tuple[Section, ...]:
    sideways = side.sideways_comparison
    sign = side.middle_sign
    return (
        Section(
            control="Skirt_Front",
            driven="MCH-Skirt_Front",
            source="j_sk_f",
            roll=0,
            first_forward_expression="((RotX < 0) * (RotX * sk_auto) / (1 + (abs(RotX) - 0.8) * 0.1))",
            first_sideways_expression=f"((RotZ {sideways} 0) * (RotZ * sk_auto) / (2 + (abs(RotZ) - 0.5) * 0.5))",
            second_forward_expression="((RotX > 0) * (RotX * sk_auto) / (2 + (abs(RotX) - 0.5) * 2)) * (abs(RotXThreshold) / (0.2 + abs(RotXThreshold))) if RotXThreshold < 0 else RotX * 0",
        ),
        Section(
            control="Skirt_Side",
            driven="MCH-Skirt_Middle",
            source="j_sk_s",
            roll=side.middle_roll,
            first_forward_expression=f"((RotX < 0) * ({sign}RotX * sk_auto) / (3 + (abs(RotX) - 0.5) * 2))",
            first_sideways_expression=f"((RotZ {sideways} 0) * ({sign}RotZ * sk_auto) / (1 + (abs(RotZ) - 0.1) * 1))",
            second_forward_expression=f"((RotX > 0) * ({sign}RotX * sk_auto) / (3 + (abs(RotX) - 0.2) * 2)) * (abs(RotXThreshold) / (0.2 + abs(RotXThreshold))) if RotXThreshold < 0 else RotX * 0",
        ),
        Section(
            control="Skirt_Back",
            driven="MCH-Skirt_Back",
            source="j_sk_b",
            roll=0,
            first_forward_expression="((RotX < 0) * (RotX * sk_auto) / (5 + (abs(RotX) - 0.2) * 5)) + ((RotX > 0) * ((RotX * sk_auto) / (1 + (abs(RotX) + 0.1) * 0.2)))",
            first_sideways_expression=f"((RotZ {sideways} 0) * (RotZ * sk_auto) / (2 + (abs(RotZ) - 0.1) * 3))",
            second_forward_expression="((RotX > 0) * (RotX * sk_auto) / (1 + (abs(RotX) + 0.5) * 0.3)) * (abs(RotXThreshold) / (0.5 + abs(RotXThreshold))) if RotXThreshold > 0 else RotX * 0",
        ),
    )


def _chain(name: str) -> list[str]:
    return [name, f"{name}.001", f"{name}.002"]


class Module(RigModule):
    name = "XIV-Default"
    requires = [f"{section.source}_{part}_{side.source}" for side in SIDES for section in _sections(side) for part in ("a", "b", "c")]
    ui_collections = UI_Collections([
        BoneCollection(name=SKIRT_COLLECTION, ui=True, color_set="Head", row_index=1, title="Skirt", visible=False),
    ])
    ui_flags = ("Skirt Automation",)

    def meta_edit(self, rig):
        for side in SIDES:
            suffix = side.suffix
            extend(rig, f"MCH-thigh_driv_tgt{suffix}", f"thigh{suffix}", start_point="head", size_factor=0.3, parent="Spine.001")
            extend(rig, f"MCH-shin_driv_tgt{suffix}", f"shin{suffix}", start_point="head", size_factor=0.3, parent=f"thigh{suffix}")

            for section in _sections(side):
                upper, middle, lower = (f"{section.source}_{part}_{side.source}" for part in ("a", "b", "c"))

                control = f"{section.control}{suffix}"
                connect(rig, control, upper, middle, parent="Spine.001")
                connect(rig, f"{control}.001", middle, lower, parent=control, connected=True)
                extend(rig, f"{control}.002", lower, start_point="head", parent=f"{control}.001", connected=True)

                driven = f"{section.driven}{suffix}"
                connect(rig, driven, upper, middle, parent="Spine.001", roll=section.roll)
                connect(rig, f"{driven}.001", middle, lower, parent=driven, connected=True, roll=section.roll)
                extend(rig, f"{driven}.002", lower, start_point="head", parent=f"{driven}.001", connected=True, roll=section.roll)

    def meta_pose(self, rig):
        for side in SIDES:
            suffix = side.suffix
            rigify.basic_raw_copy(rig, f"MCH-thigh_driv_tgt{suffix}")
            rigify.basic_raw_copy(rig, f"MCH-shin_driv_tgt{suffix}")

            for section in _sections(side):
                control_bones = _chain(f"{section.control}{suffix}")
                rigify.basic_copy_chain(rig, control_bones[0])
                collection(rig, control_bones, SKIRT_COLLECTION)

                for driven_bone in _chain(f"{section.driven}{suffix}"):
                    rigify.basic_raw_copy(rig, driven_bone)

                for part, control_bone in zip(("a", "b", "c"), control_bones):
                    link(rig, f"{section.source}_{part}_{side.source}", f"DEF-{control_bone}")

    def final_edit(self, rig):
        for side in SIDES:
            for section in _sections(side):
                parent(rig, f"{section.control}{side.suffix}", f"{section.driven}{side.suffix}")

    def final_pose(self, rig):
        armature_prop(rig, AUTOMATION_PROPERTY, 1.0, minimum=0.0, maximum=1.0)
        automation = PropertyVariable(AUTOMATION_PROPERTY)

        for side in SIDES:
            suffix = side.suffix
            thigh_target = f"MCH-thigh_driv_tgt{suffix}"
            shin_target = f"MCH-shin_driv_tgt{suffix}"
            collection(rig, [thigh_target, shin_target], "MCH")
            constraints.damped_track(rig, thigh_target, f"ORG-shin{suffix}")
            constraints.damped_track(rig, shin_target, f"ORG-foot{suffix}")

            thigh_forward = TransformVariable(thigh_target, "ROT_X")
            thigh_sideways = TransformVariable(thigh_target, "ROT_Z")
            shin_forward = TransformVariable(shin_target, "ROT_X")

            for section in _sections(side):
                driven_bones = _chain(f"{section.driven}{suffix}")
                collection(rig, driven_bones, "MCH")

                driver(
                    rig, driven_bones[0], "rotation_quaternion", index=ROTATION_X_INDEX,
                    expression=section.first_forward_expression,
                    variables={"RotX": thigh_forward, "sk_auto": automation},
                )
                driver(
                    rig, driven_bones[0], "rotation_quaternion", index=ROTATION_Z_INDEX,
                    expression=section.first_sideways_expression,
                    variables={"RotZ": thigh_sideways, "sk_auto": automation},
                )
                driver(
                    rig, driven_bones[1], "rotation_quaternion", index=ROTATION_X_INDEX,
                    expression=section.second_forward_expression,
                    variables={"RotX": shin_forward, "RotXThreshold": thigh_forward, "sk_auto": automation},
                )
