"""Demonstrate direct rig instructions; collection display belongs in a UI layout."""

import bpy

from .... import definitions
from .... import instructions as abi


class Module(definitions.RigModule):
    """Demonstrate module-owned validation and generation stages."""

    name = "Demo"
    _enabled: bool = False

    # ------------------------------------------------------------------------

    def meta_edit(self, rig: bpy.types.Object) -> None:
        """Check the demo source bone before creating its controls."""
        self._enabled = abi.require_bones(rig, ["j_example_bone"], self.name)
        if not self._enabled:
            return
        # Demo chain
        abi.connect(rig, "demo_bone", "j_example_bone", "j_example_bone", end_point="tail", parent="Spine.001")
        abi.extend(rig, "demo_bone_tip", "j_example_bone", parent="demo_bone", connected=True)

    # ------------------------------------------------------------------------

    def meta_pose(self, rig: bpy.types.Object) -> None:
        """Configure the demo controls and source mapping."""
        if not self._enabled:
            return
        # Demo controls
        abi.rigify.basic_super_copy(rig, "demo_bone")
        abi.collection(rig, ["demo_bone", "demo_bone_tip"], "Demo (IK)")
        # Source-to-deform mapping
        abi.link(rig, "j_example_bone", "DEF-demo_bone")

    # ------------------------------------------------------------------------

    def final_edit(self, rig: bpy.types.Object) -> None:
        """Parent the demo tip to its generated deform bone."""
        if not self._enabled:
            return
        # Demo hierarchy
        abi.parent(rig, "demo_bone_tip", "DEF-demo_bone")

    # ------------------------------------------------------------------------

    def final_pose(self, rig: bpy.types.Object) -> None:
        """Add the demo tracking constraint and custom property."""
        if not self._enabled:
            return
        # Demo tracking and property
        abi.constraints.damped_track(rig, "demo_bone", target="demo_bone_tip")
        abi.prop(rig, "demo_bone", "Demo_Property", 0)
