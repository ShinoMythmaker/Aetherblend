"""Backend template lookup and rig generator construction."""

import bpy

from .definitions import Template
from .generator import AetherRigGenerator
from .library import CS_COLORSETS, DEFAULT_TEMPLATE_NAME, TEMPLATES

DEFAULT_COLORSET_NAME = "AetherBlend"


def get_template(aether_rig: bpy.types.PropertyGroup) -> Template:
    """Resolve the armature's template, including the default for older rigs."""
    return TEMPLATES.get(getattr(aether_rig, "template", DEFAULT_TEMPLATE_NAME)) or TEMPLATES[DEFAULT_TEMPLATE_NAME]


def get_template_toggles(aether_rig: bpy.types.PropertyGroup) -> bpy.types.PropertyGroup | None:
    """Return this armature's persistent settings for its selected template."""
    template = get_template(aether_rig)
    return getattr(aether_rig, template.toggles.__name__) if template.toggles else None


def get_template_items(self: bpy.types.PropertyGroup, context: bpy.types.Context) -> list[tuple[str, str, str]]:
    """Dropdown items for the per-rig template property."""
    return [(name, name, "") for name in TEMPLATES]


def get_colorset_items(self: bpy.types.PropertyGroup, context: bpy.types.Context) -> list[tuple[str, str, str]]:
    """Dropdown items for the colorset override."""
    return [(key, key, "") for key in CS_COLORSETS]


def get_rig_generator(aether_rig: bpy.types.PropertyGroup) -> AetherRigGenerator | None:
    """Build a generator using the selected template's modules, toggles, and layout."""
    template = get_template(aether_rig)
    color_sets = CS_COLORSETS.get(getattr(aether_rig, "selected_colorset", DEFAULT_COLORSET_NAME))

    if not color_sets:
        print("[AetherBlend] Select an available colorset before generating the rig.")
        return None

    toggles = get_template_toggles(aether_rig)
    ui_layout = template.ui_layout(toggles) if callable(template.ui_layout) else template.ui_layout

    return AetherRigGenerator(
        name=template.name,
        color_sets=color_sets,
        ui_layout=ui_layout,
        modules=template.modules,
        toggles=toggles,
    )


def register() -> None:
    """Register this module's classes."""
    pass


def unregister() -> None:
    """Unregister this module's classes."""
    pass
