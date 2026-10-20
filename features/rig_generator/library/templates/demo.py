"""Demonstrate template toggles, dependent UI, and collection layout.

This example is not registered in TEMPLATES, just like the demo module is not
part of the production rig. To try it, import DEMO in templates/__init__.py and
include it in the TEMPLATES tuple before registering the add-on.

The demo module expects j_example_bone and a Spine.001 parent on the source rig.
"""

import bpy

from ...definitions import Template
from ...rigify.settings import BoneCollection
from ..modules.demo_module.demo_module import Module as DemoModule

# ------------------------------
# Persistent per-armature settings
# ------------------------------


class AETHER_PG_demo_toggles(bpy.types.PropertyGroup):
    """Store the demo template's persistent generation settings."""

    mode: bpy.props.EnumProperty(
        name="Mode",
        description="Show basic settings or additional collection settings",
        items=[
            ("BASIC", "Basic", "Use the default collection visibility"),
            ("ADVANCED", "Advanced", "Customize the initial collection visibility"),
        ],
        default="BASIC",
    )  # type: ignore
    show_controls: bpy.props.BoolProperty(
        name="Show Controls",
        description="Initially show the demo controls in advanced mode",
        default=True,
    )  # type: ignore


# ------------------------------
# Collection layout
# ------------------------------


def get_ui_layout(toggles: bpy.types.PropertyGroup | None) -> list[BoneCollection]:
    """Build collection display settings from the selected demo mode."""
    if toggles is None:
        raise ValueError("The demo UI layout requires template toggles")
    if toggles.mode not in {"BASIC", "ADVANCED"}:
        raise ValueError(f"Unknown demo mode: {toggles.mode}")
    return [
        BoneCollection(
            "Demo (IK)",
            ui=True,
            row_index=1,
            title="Demo Controls",
            visible=toggles.mode == "BASIC" or toggles.show_controls,
        ),
        BoneCollection("Original", ui=True, row_index=3, visible=False),
        BoneCollection("Root", ui=True, row_index=5),
    ]


# ------------------------------
# Template assembly
# ------------------------------

DEMO = Template(
    name="Demo",
    toggles=AETHER_PG_demo_toggles,
    # Visibility only hides the UI field; generation must handle its stored value.
    toggle_visibility={
        "show_controls": lambda toggles: toggles.mode == "ADVANCED",
    },
    # A fixed list of BoneCollection entries can replace this callable.
    ui_layout=get_ui_layout,
    # Modules run in this order and receive the settings through self.toggles.
    modules=[DemoModule],
)
