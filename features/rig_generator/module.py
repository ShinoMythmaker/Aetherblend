"""Rig modules and the templates that group them."""
from collections.abc import Container, Sequence
from dataclasses import dataclass

import bpy

from . import rigify


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
