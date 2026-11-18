"""Properties and actor choices for the bridge."""

import bpy

from .stream import update_stream

ACTOR_ITEMS: list[tuple[str, str, str, int]] = [("__NONE__", "No actor", "", 0)]


def _actor_items(_self: bpy.types.PropertyGroup, _context: bpy.types.Context) -> list[tuple[str, str, str, int]]:
    return ACTOR_ITEMS


def _get_actor(self: bpy.types.PropertyGroup) -> int:
    return next((number for actor, _, _, number in ACTOR_ITEMS if actor == self.actor_id), 0)


def _set_actor(self: bpy.types.PropertyGroup, value: int) -> None:
    self.actor_id = next((actor for actor, _, _, number in ACTOR_ITEMS if number == value and number != 0), "")


def _update_stream(self: bpy.types.Scene, context: bpy.types.Context) -> None:
    update_stream(self, context)


class AetherBridgeArmatureProperties(bpy.types.PropertyGroup):
    """Store the actor assigned to an armature."""

    actor_id: bpy.props.StringProperty(name="Actor ID")  # type: ignore
    actor: bpy.props.EnumProperty(name="Actor", items=_actor_items, get=_get_actor, set=_set_actor)  # type: ignore


def register() -> None:
    """Register bridge properties."""
    bpy.utils.register_class(AetherBridgeArmatureProperties)
    bpy.types.Object.aether_bridge = bpy.props.PointerProperty(type=AetherBridgeArmatureProperties)
    bpy.types.Scene.aether_bridge_host = bpy.props.StringProperty(name="Host", default="127.0.0.1")
    bpy.types.Scene.aether_bridge_port = bpy.props.IntProperty(name="Port", default=8080, min=1, max=65535)
    bpy.types.Scene.aether_bridge_stream_enabled = bpy.props.BoolProperty(name="Stream", update=_update_stream)
    bpy.types.Scene.aether_bridge_stream_fps = bpy.props.IntProperty(name="FPS", default=30, min=1, max=60)
    bpy.types.Scene.aether_bridge_status = bpy.props.StringProperty(name="Bridge status", options={"SKIP_SAVE"})


def unregister() -> None:
    """Remove bridge properties."""
    del bpy.types.Scene.aether_bridge_status
    del bpy.types.Scene.aether_bridge_stream_fps
    del bpy.types.Scene.aether_bridge_stream_enabled
    del bpy.types.Scene.aether_bridge_port
    del bpy.types.Scene.aether_bridge_host
    del bpy.types.Object.aether_bridge
    bpy.utils.unregister_class(AetherBridgeArmatureProperties)
