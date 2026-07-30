import bpy
from bpy.types import Panel


def _build_host_description(scene: bpy.types.Scene) -> str:
    return f"Streaming to {scene.aether_bridge_scheme}://{scene.aether_bridge_host}:{scene.aether_bridge_port}{scene.aether_bridge_endpoint_path}"


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

        box = layout.box()
        box.label(text="UI subject to change", icon='URL')

        row = box.row(align=True)
        row.prop(scene, "aether_bridge_scheme", text="Protocol")
        row.prop(scene, "aether_bridge_host", text="Host")

        row = box.row(align=True)
        row.prop(scene, "aether_bridge_port", text="Port")
        row.prop(scene, "aether_bridge_endpoint_path", text="Path")

        box.label(text=_build_host_description(scene), icon='INFO')

        row = box.row(align=True)
        row.operator("aether.bridge_send_frame", text="Send Frame", icon='EXPORT')
        row.prop(scene, "aether_bridge_stream_enabled", text="Stream", toggle=True)

        if scene.aether_bridge_stream_enabled:
            row = box.row()
            row.prop(scene, "aether_bridge_stream_fps", text="FPS")

        box.separator()
        box.label(text="Select an armature to stream its pose.")
        box.label(text="Only the active armature is streamed.")


classes = (AETHER_PT_BridgePanel,)


def register() -> None:
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister() -> None:
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
