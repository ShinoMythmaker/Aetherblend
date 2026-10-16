"""Instructions a rig module uses to build a rig in Blender."""

from . import constraints, rigify
from .edit_bone import connect, extend, parallel, parent, resolve_pending_parents
from .pose_bone import collection, link, prop

__all__ = [
    "collection",
    "connect",
    "constraints",
    "extend",
    "link",
    "parallel",
    "parent",
    "prop",
    "rigify",
]
