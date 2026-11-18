"""Bridge controls in the import/export tab."""

import bpy

from ...ui.tabs import get_active_tab
from ...ui.visibility import visible_in_current_area


class AETHER_PT_BridgePanel(bpy.types.Panel):
    """Configure actor assignments and pose streaming."""

    bl_label = "AetherBridge"
    bl_idname = "AETHER_PT_aetherbridge"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "AetherBlend"
    bl_order = 6

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        """Show the bridge alongside import and export tools."""
        return visible_in_current_area(context) and get_active_tab(context) == "IMPORT_EXPORT"

    def draw(self, context: bpy.types.Context) -> None:
        """Draw connection, actor, and stream controls."""
        layout = self.layout
        scene = context.scene
        row = layout.row(align=True)
        row.prop(scene, "aether_bridge_host")
        row.prop(scene, "aether_bridge_port")
        layout.operator("aether.bridge_refresh_actors", icon="FILE_REFRESH")
        armature = context.active_object
        if armature and armature.type == "ARMATURE":
            layout.prop(armature.aether_bridge, "actor")
            if armature.aether_bridge.actor_id:
                layout.label(text=f"Assigned actor: {armature.aether_bridge.actor_id}")
        else:
            layout.label(text="Select an armature to assign an actor", icon="INFO")
        layout.prop(scene, "aether_bridge_stream_enabled", toggle=True)
        if scene.aether_bridge_stream_enabled:
            layout.prop(scene, "aether_bridge_stream_fps")
        if scene.aether_bridge_status:
            layout.label(text=scene.aether_bridge_status, icon="ERROR")


def register() -> None:
    """Register the bridge panel."""
    bpy.utils.register_class(AETHER_PT_BridgePanel)


def unregister() -> None:
    """Unregister the bridge panel."""
    bpy.utils.unregister_class(AETHER_PT_BridgePanel)
