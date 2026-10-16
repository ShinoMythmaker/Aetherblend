import bpy

from .info_panel import AETHER_PT_InfoPanel

_REGISTERED = []


def _source_panels():
    # Imported lazily because the feature panels import from this package.
    from ..features.animation.panels import AETHER_PT_ExportPanel
    from ..features.model_import.panels import AETHER_PT_ImportPanel
    from ..features.rig_edit.panels import AETHER_PT_RigManipulation
    from ..features.rig_generator.panels import AETHER_PT_RigCreation
    from ..features.rig_ui.panels import (
        AETHER_PT_RigBakeSettingsPanel,
        AETHER_PT_RigLayersPanel,
        AETHER_PT_RigUIPanel,
    )

    return (
        AETHER_PT_InfoPanel,
        AETHER_PT_ImportPanel,
        AETHER_PT_ExportPanel,
        AETHER_PT_RigCreation,
        AETHER_PT_RigManipulation,
        AETHER_PT_RigLayersPanel,
        AETHER_PT_RigUIPanel,
        AETHER_PT_RigBakeSettingsPanel,
    )


def _build_panel(panel_cls):
    source_poll = getattr(panel_cls, "poll", None)
    source_draw = getattr(panel_cls, "draw", None)
    source_draw_header = getattr(panel_cls, "draw_header", None)

    @classmethod
    def poll(cls, context):
        if source_poll is None:
            return True
        try:
            return source_poll(context)
        except TypeError:
            return source_poll(panel_cls, context)

    def draw(self, context):
        if source_draw is not None:
            return source_draw(self, context)

    def draw_header(self, context):
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


def _mirrored_name(panel_cls):
    return f"{panel_cls.__name__}_Properties"


def _unregister_mirrored():
    for panel_cls in reversed(_source_panels()):
        cls = getattr(bpy.types, _mirrored_name(panel_cls), None)
        if cls is None:
            continue
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError:
            pass


def register():
    _unregister_mirrored()
    _REGISTERED.clear()
    for panel_cls in _source_panels():
        mirrored = _build_panel(panel_cls)
        bpy.utils.register_class(mirrored)
        _REGISTERED.append(mirrored)


def unregister():
    for panel_cls in reversed(_REGISTERED):
        try:
            bpy.utils.unregister_class(panel_cls)
        except RuntimeError:
            pass
    _REGISTERED.clear()
    _unregister_mirrored()
