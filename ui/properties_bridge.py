"""Mirrors the add-on panels into the Properties editor Tool tab."""

import bpy

from .info_panel import AETHER_PT_ui_info

_REGISTERED = []


def _source_panels() -> tuple[type[bpy.types.Panel], ...]:
    # Imported lazily because the feature panels import from this package.
    from ..features.import_export.panels import AETHER_PT_import_export_export, AETHER_PT_import_export_import
    from ..features.rig_edit.panels import AETHER_PT_rig_edit_manipulation
    from ..features.rig_generator.panels import AETHER_PT_rig_generator_creation
    from ..features.rig_ui.panels import (
        AETHER_PT_rig_ui_bake_settings,
        AETHER_PT_rig_ui_layers,
        AETHER_PT_rig_ui_main,
    )

    return (
        AETHER_PT_ui_info,
        AETHER_PT_import_export_import,
        AETHER_PT_import_export_export,
        AETHER_PT_rig_generator_creation,
        AETHER_PT_rig_edit_manipulation,
        AETHER_PT_rig_ui_layers,
        AETHER_PT_rig_ui_main,
        AETHER_PT_rig_ui_bake_settings,
    )


def _build_panel(panel_cls: type[bpy.types.Panel]) -> type[bpy.types.Panel]:
    source_poll = getattr(panel_cls, "poll", None)
    source_draw = getattr(panel_cls, "draw", None)
    source_draw_header = getattr(panel_cls, "draw_header", None)

    @classmethod
    def poll(cls: type[bpy.types.Panel], context: bpy.types.Context) -> bool:
        if source_poll is None:
            return True
        try:
            return source_poll(context)
        except TypeError:
            return source_poll(panel_cls, context)

    def draw(self: bpy.types.Panel, context: bpy.types.Context) -> None:
        if source_draw is not None:
            return source_draw(self, context)

    def draw_header(self: bpy.types.Panel, context: bpy.types.Context) -> None:
        if source_draw_header is not None:
            return source_draw_header(self, context)

    return type(
        f"{panel_cls.__name__}_Properties",
        (bpy.types.Panel,),
        {
            "bl_label": panel_cls.bl_label,
            "bl_idname": f"{panel_cls.bl_idname}_properties",
            "bl_space_type": "VIEW_3D",
            "bl_region_type": "UI",
            "bl_category": "Tool",
            "bl_order": getattr(panel_cls, "bl_order", 0),
            "poll": poll,
            "draw": draw,
            "draw_header": draw_header,
        },
    )


def _mirrored_name(panel_cls: type[bpy.types.Panel]) -> str:
    return f"{panel_cls.__name__}_Properties"


def _unregister_mirrored() -> None:
    for panel_cls in reversed(_source_panels()):
        cls = getattr(bpy.types, _mirrored_name(panel_cls), None)
        if cls is None:
            continue
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError:
            pass


def register() -> None:
    """Register this module's classes."""
    _unregister_mirrored()
    _REGISTERED.clear()
    for panel_cls in _source_panels():
        mirrored = _build_panel(panel_cls)
        bpy.utils.register_class(mirrored)
        _REGISTERED.append(mirrored)


def unregister() -> None:
    """Unregister this module's classes."""
    for panel_cls in reversed(_REGISTERED):
        try:
            bpy.utils.unregister_class(panel_cls)
        except RuntimeError:
            pass
    _REGISTERED.clear()
    _unregister_mirrored()
