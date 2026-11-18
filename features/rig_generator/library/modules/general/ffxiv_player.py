"""General adjustments for FFXIV player rigs."""

import bpy

from .... import definitions
from .... import instructions as abi


class Module(definitions.RigModule):
    """Apply whole-rig FFXIV player customizations."""

    name = "FFXIV Player General"

    def final_pose(self, rig: bpy.types.Object) -> None:
        """Set the generated root control's widget scale."""
        abi.widget(rig, "root",widget_name="AB_WGT_logo_ffxiv")
