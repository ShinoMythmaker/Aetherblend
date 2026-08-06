import bpy

from ...utils.axis_conversion import AXIS_ITEMS

BRIDGE_ACTOR_ITEMS: list[tuple[str, str, str]] = []


def _get_actor_items(self: bpy.types.PropertyGroup, context: bpy.types.Context) -> list[tuple[str, str, str]]:
    return BRIDGE_ACTOR_ITEMS or [("", "No actors loaded", "")]


def _on_stream_enabled_update(self: bpy.types.PropertyGroup, context: bpy.types.Context) -> None:
    from . import stream

    stream.on_stream_enabled_update(self, context)


class AetherBridgeArmatureProperties(bpy.types.PropertyGroup):
    actor_id: bpy.props.EnumProperty(
        name="Actor",
        description="Select the actor to stream to",
        items=_get_actor_items,
    )  # type: ignore

    use_axis_conversion: bpy.props.BoolProperty(
        name="Use Axis Conversion",
        description="Apply bridge pose axis conversion before sending",
        default=True,
    )  # type: ignore


def register() -> None:
    bpy.utils.register_class(AetherBridgeArmatureProperties)
    bpy.types.Object.aether_bridge = bpy.props.PointerProperty(type=AetherBridgeArmatureProperties)

    bpy.types.Scene.aether_bridge_host = bpy.props.StringProperty(
        name="Host",
        description="Hostname or IP address for bridge streaming",
        default="127.0.0.1",
    )
    bpy.types.Scene.aether_bridge_port = bpy.props.IntProperty(
        name="Port",
        description="Port used by the bridge target server",
        default=8080,
        min=1,
        max=65535,
    )
    bpy.types.Scene.aether_bridge_stream_enabled = bpy.props.BoolProperty(
        name="Stream Pose",
        description="Enable continuous pose streaming",
        default=False,
        update=_on_stream_enabled_update,
    )
    bpy.types.Scene.aether_bridge_stream_fps = bpy.props.IntProperty(
        name="Stream FPS",
        description="Target frames per second for bridge streaming",
        default=15,
        min=1,
        max=60,
    )


def unregister() -> None:
    if hasattr(bpy.types.Object, "aether_bridge"):
        del bpy.types.Object.aether_bridge
    if hasattr(bpy.types.Scene, "aether_bridge_host"):
        del bpy.types.Scene.aether_bridge_host
    if hasattr(bpy.types.Scene, "aether_bridge_port"):
        del bpy.types.Scene.aether_bridge_port
    if hasattr(bpy.types.Scene, "aether_bridge_stream_enabled"):
        del bpy.types.Scene.aether_bridge_stream_enabled
    if hasattr(bpy.types.Scene, "aether_bridge_stream_fps"):
        del bpy.types.Scene.aether_bridge_stream_fps
    bpy.utils.unregister_class(AetherBridgeArmatureProperties)
