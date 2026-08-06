import bpy
from bpy.types import Panel


def _build_host_description(armature: bpy.types.Object | None, scene: bpy.types.Scene) -> str:
    if armature is None or not hasattr(armature, "aether_bridge"):
        return "Select an armature to configure bridge streaming"
    props = armature.aether_bridge
    actor_id = props.actor_id.strip() if getattr(props, "actor_id", "") else ""
    target = f"/bridge/{actor_id}" if actor_id else "/pose"
    return f"Streaming to http://{scene.aether_bridge_host}:{scene.aether_bridge_port}{target}"


class AETHER_PT_BridgePanel(Panel):
    bl_label = "AetherBridge"
    bl_idname = "AETHER_PT_aetherbridge"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AetherBlend'
    bl_order = 6

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        return True

    def draw(self, context: bpy.types.Context) -> None:
        layout = self.layout
        scene = context.scene
        armature = context.active_object
        if armature is None or not hasattr(armature, "aether_bridge"):
            layout.label(text="Select an armature to configure bridge streaming")
            return

        props = armature.aether_bridge

        box = layout.box()
        box.label(text="Bridge stream settings", icon='URL')

        row = box.row(align=True)
        row.prop(scene, "aether_bridge_host", text="Host")
        row.prop(scene, "aether_bridge_port", text="Port")

        box.label(text=_build_host_description(armature, scene), icon='INFO')

        row = box.row(align=True)
        row.prop(props, "actor_id", text="Actor")

        row = box.row(align=True)
        row.operator("aether.bridge_refresh_actors", text="Fetch Actors", icon='FILE_REFRESH')
        row.operator("aether.bridge_clear_actor", text="Clear Actor", icon='X')

        row = box.row(align=True)
        row.prop(scene, "aether_bridge_stream_enabled", text="Stream", toggle=True)

        if scene.aether_bridge_stream_enabled:
            row = box.row()
            row.prop(scene, "aether_bridge_stream_fps", text="FPS")

        box.separator()
        box.label(text="Host/port/stream toggles are shared for all armatures.")
        box.label(text="Actor assignment is stored per armature.")


classes = (AETHER_PT_BridgePanel,)


def register() -> None:
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister() -> None:
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
