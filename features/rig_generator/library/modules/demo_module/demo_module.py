"""Demonstrate direct rig instructions; collection display belongs in a UI layout."""

import bpy

from .... import definitions
from .... import instructions as abi


class Module(definitions.RigModule):
    # Shown in the log when the module is skipped.
    name = "Demo"

    # Bones that must exist in the source armature. If one is missing, the module is skipped.
    requires = [
        "j_example_bone",
    ]

    # ------------------------------------------------------------------------

    def meta_edit(self, rig: bpy.types.Object) -> None:
        # Demo chain
        abi.connect(rig, "demo_bone", "j_example_bone", "j_example_bone", end_point="tail", parent="Spine.001")
        abi.extend(rig, "demo_bone_tip", "j_example_bone", parent="demo_bone", connected=True)

    # ------------------------------------------------------------------------

    def meta_pose(self, rig: bpy.types.Object) -> None:
        # Demo controls
        abi.rigify.basic_super_copy(rig, "demo_bone")
        abi.collection(rig, ["demo_bone", "demo_bone_tip"], "Demo (IK)")
        # Source-to-deform mapping
        abi.link(rig, "j_example_bone", "DEF-demo_bone")

    # ------------------------------------------------------------------------

    def final_edit(self, rig: bpy.types.Object) -> None:
        # Demo hierarchy
        abi.parent(rig, "demo_bone_tip", "DEF-demo_bone")

    # ------------------------------------------------------------------------

    def final_pose(self, rig: bpy.types.Object) -> None:
        # Demo tracking and property
        abi.constraints.damped_track(rig, "demo_bone", target="demo_bone_tip")
        abi.prop(rig, "demo_bone", "Demo_Property", 0)
