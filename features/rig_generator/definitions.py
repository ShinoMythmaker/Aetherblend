"""Definitions a rig is built from: modules, templates and UI links."""

from collections.abc import Container, Sequence
from dataclasses import dataclass
from typing import Literal, NamedTuple

import bpy

from . import rigify


class Side(NamedTuple):
    """Naming conventions for one body side."""

    suffix: str
    source: str
    name: str


LEFT = Side(".L", "l", "Left")
RIGHT = Side(".R", "r", "Right")
SIDES = (LEFT, RIGHT)


class RigModule:
    """A part of a rig. Subclass it, set the data, and override the steps the module needs.

    The generator runs the steps in this order: meta_edit and meta_pose on the meta rig,
    then, after rigify generated the rig, final_edit and final_pose on the final rig.
    """

    name: str = ""
    requires: Sequence[str] = ()
    ui_collections: rigify.settings.UI_Collections | None = None
    ui_flags: Sequence[str] = ()

    def missing_bones(self, available: Container[str]) -> list[str]:
        """Return the required bones that are not available."""
        return [bone for bone in self.requires if bone not in available]

    def meta_edit(self, rig: bpy.types.Object) -> None:
        """Edit the meta rig (edit mode)."""

    def meta_pose(self, rig: bpy.types.Object) -> None:
        """Configure the meta rig (pose mode)."""

    def final_edit(self, rig: bpy.types.Object) -> None:
        """Edit the generated rig (edit mode)."""

    def final_pose(self, rig: bpy.types.Object) -> None:
        """Configure the generated rig (pose mode)."""


@dataclass(frozen=True)
class Template:
    """A rig template: priority groups of modules where the first usable module of each group wins."""

    name: str
    modules: list[list[type[RigModule]]]


UI_Type = Literal["checkbox", "slider", "dropdown"]


@dataclass
class UILink:
    """Defines a link between a bone or armature property and a UI element."""

    title: str
    property_name: str | None = None
    bone_name: str | None = None
    constraint_name: str | None = None
    white_list: list[str] | None = None  # List of bone names that have to be selected for the UI to show.
    ui_type: UI_Type | None = "checkbox"
    ui_params: dict | None = None  # Additional parameters for the UI element
    override: Literal["EyeLidControl"] | None = (
        None  # Special cases where the link doesn't directly correspond to a property (e.g. custom UI behavior for eye lid controls)  # noqa: E501
    )

    def eye_lid_control_draw(self, context: bpy.types.Context, layout: bpy.types.UILayout) -> None:

        armature = context.active_object
        rig_props = armature.aether_rig
        if rig_props.eye_lid_edit_mode:
            layout.operator("aether.rig_ui_eyelid_edit_end", text="Exit Eye Lid Edit Mode", icon="CANCEL")
        else:
            layout.operator("aether.rig_ui_eyelid_edit_start", text="Enter Eye Lid Edit Mode", icon="EDITMODE_HLT")

        return

    def draw(self, context: bpy.types.Context, layout: bpy.types.UILayout) -> None:
        """Draws the UI element for this link."""
        armature = context.active_object
        if not armature or armature.type != "ARMATURE":
            return

        # Collect selected pose bones (only available in POSE mode).
        selected_bones: set[str] = set()
        if context.mode == "POSE":
            try:
                selected_bones = set(bone.name for bone in (context.selected_pose_bones or []))
                if context.active_pose_bone:
                    selected_bones.add(context.active_pose_bone.name)
            except (AttributeError, TypeError):
                pass

        # Apply whitelist: skip drawing unless a whitelisted bone is selected.
        if self.white_list:
            if not selected_bones.intersection(self.white_list):
                return

        if self.override == "EyeLidControl":
            self.eye_lid_control_draw(context, layout)
            return

        target = armature.data
        if self.bone_name:
            target = armature.pose.bones.get(self.bone_name)
            if not target:
                return
            if self.constraint_name:
                target = target.constraints.get(self.constraint_name)
                if not target:
                    return

        col = layout.column(align=True)
        if self.ui_type == "checkbox":
            col.prop(target, "mute", text=self.title)
        elif self.ui_type == "slider":
            col.prop(target, self.property_name, text=self.title, slider=True, **(self.ui_params or {}))
        elif self.ui_type == "dropdown":
            col.prop(target, self.property_name, text=self.title, **(self.ui_params or {}))
        else:
            print(f"[AetherBlend] Unknown UI element type '{self.ui_type}' for UILink '{self.title}'")
