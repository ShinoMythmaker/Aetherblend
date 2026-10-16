"""Rig modules and the templates that group them."""
import importlib
import pkgutil
from collections.abc import Container, Sequence
from dataclasses import dataclass

import bpy

from . import rigify


def discover_modules(package_name: str, package_path: list[str], namespace: dict) -> list[str]:
    """Load every file of a package and expose its RigModule class as an instance named after the file.

    Call it from a package `__init__` as `__all__ = discover_modules(__name__, __path__, globals())`.
    A file must define exactly one RigModule subclass.
    """
    exported_names: list[str] = []
    for module_info in pkgutil.iter_modules(package_path):
        file_module = importlib.import_module(f"{package_name}.{module_info.name}")
        rig_module_classes = [
            value for value in vars(file_module).values()
            if isinstance(value, type) and issubclass(value, RigModule) and value.__module__ == file_module.__name__
        ]
        if len(rig_module_classes) != 1:
            raise ImportError(f"{file_module.__name__} must define exactly one RigModule subclass, found {len(rig_module_classes)}.")

        namespace[module_info.name] = rig_module_classes[0]()
        exported_names.append(module_info.name)
    return exported_names


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
    modules: list[list[RigModule]]
