"""Widget instruction: set the custom shape of a bone."""
import math

import bpy
import mathutils

from .... import utils
from ._bones import get_pose_bone

_WIDGET_COLLECTION_PREFIX = "WGTS"
_WIDGET_OBJECT_PREFIX = "AB_WGT_"


def _find_widget_name(rig: bpy.types.Object, widget_name: str) -> str | None:
    """Find a widget object by name in the rig's WGTS collections, falling back to the whole blend file."""
    expected_name = widget_name if widget_name.startswith(_WIDGET_OBJECT_PREFIX) else f"{_WIDGET_OBJECT_PREFIX}{widget_name}"

    def matches(object_name: str) -> bool:
        return object_name == expected_name

    rig_collections: list[bpy.types.Collection] = []
    for rig_collection in rig.users_collection:
        rig_collections.extend(utils.collection.collection_tree(rig_collection))
    found_name = utils.collection.find_object_name_in_prefixed_collections(rig_collections, _WIDGET_COLLECTION_PREFIX, matches)
    if found_name:
        return found_name

    blend_file_collections = [
        collection for collection in bpy.data.collections if collection.name.upper().startswith(_WIDGET_COLLECTION_PREFIX)
    ]
    found_name = utils.collection.find_object_name_in_prefixed_collections(blend_file_collections, _WIDGET_COLLECTION_PREFIX, matches)
    if not found_name:
        print(f"[AetherBlend] No widget '{expected_name}' found for '{rig.name}'.")
    return found_name


def widget(
    rig: bpy.types.Object,
    bone: str,
    *,
    widget_name: str | None = None,
    color_set: str | None = None,
    custom_color_normal: tuple[float, float, float] | None = None,
    custom_color_select: tuple[float, float, float] | None = None,
    custom_color_active: tuple[float, float, float] | None = None,
    translation: tuple[float, float, float] = (0.0, 0.0, 0.0),
    rotation_degrees: tuple[float, float, float] = (0.0, 0.0, 0.0),
    scale: tuple[float, float, float] = (1.0, 1.0, 1.0),
    scale_factor: float = 1.0,
    override_transform: str | None = None,
    affect_gizmo: bool = False,
    use_as_pivot: bool = False,
    scale_to_bone_length: bool = True,
    wire_width: float = 1.0,
) -> None:
    """Set the widget shape and its transform for a bone."""
    pose_bone = get_pose_bone(rig, bone)
    if not pose_bone:
        return

    if color_set:
        pose_bone.color.palette = color_set
        if color_set == "CUSTOM":
            if custom_color_normal:
                pose_bone.color.custom.normal = mathutils.Color(custom_color_normal)
            if custom_color_select:
                pose_bone.color.custom.select = mathutils.Color(custom_color_select)
            if custom_color_active:
                pose_bone.color.custom.active = mathutils.Color(custom_color_active)
    if widget_name:
        found_name = _find_widget_name(rig, widget_name)
        pose_bone.custom_shape = bpy.data.objects.get(found_name) if found_name else None

    pose_bone.custom_shape_translation = translation
    pose_bone.custom_shape_rotation_euler = [math.radians(angle) for angle in rotation_degrees]
    pose_bone.custom_shape_scale_xyz = tuple(axis_scale * scale_factor for axis_scale in scale)
    pose_bone.custom_shape_transform = override_transform
    pose_bone.use_transform_at_custom_shape = affect_gizmo
    pose_bone.use_transform_around_custom_shape = use_as_pivot
    pose_bone.use_custom_shape_bone_size = scale_to_bone_length
    pose_bone.custom_shape_wire_width = wire_width
