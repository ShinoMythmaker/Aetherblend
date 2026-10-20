"""Instructions a rig module uses to build a rig in Blender."""

from . import constraints, rigify
from .driver import PropertyVariable, TransformVariable, driver, object_driver
from .edit_bone import (
    bridge,
    center,
    connect,
    copy,
    extend,
    find_chains,
    has_bone,
    heaviest_vertex,
    offset,
    parallel,
    parent,
    require_bones,
)
from .edit_bone import resolve_pending_parents as resolve_pending_parents
from .pose_bone import armature_prop, collection, link, pose, prop, restrict
from .widget import widget

__all__ = [
    "PropertyVariable",
    "TransformVariable",
    "armature_prop",
    "bridge",
    "center",
    "collection",
    "connect",
    "constraints",
    "copy",
    "driver",
    "extend",
    "find_chains",
    "has_bone",
    "heaviest_vertex",
    "link",
    "object_driver",
    "offset",
    "parallel",
    "parent",
    "pose",
    "prop",
    "restrict",
    "require_bones",
    "rigify",
    "widget",
]
