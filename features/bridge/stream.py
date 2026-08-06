import json
import math
import re
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

import bpy
from mathutils import Matrix

from ...utils.axis_conversion import get_export_correction_matrix
from .properties import BRIDGE_ACTOR_ITEMS

_STREAM_TIMER = None
_STREAM_EXECUTOR = None
_STREAM_FUTURE = None


def _get_bridge_props(armature: bpy.types.Object) -> bpy.types.PropertyGroup:
    return armature.aether_bridge if hasattr(armature, "aether_bridge") else None


def _build_endpoint(armature: bpy.types.Object) -> str:
    props = _get_bridge_props(armature)
    if props is None:
        return ""
    scene = bpy.context.scene
    host = scene.aether_bridge_host.strip() or "127.0.0.1"
    port = scene.aether_bridge_port
    actor_id = props.actor_id.strip() if getattr(props, "actor_id", "") else ""
    if actor_id:
        return f"http://{host}:{port}/bridge/{actor_id}"
    return f"http://{host}:{port}/pose"


def _build_state_endpoint(armature: bpy.types.Object, state: str) -> str:
    props = _get_bridge_props(armature)
    if props is None:
        return ""
    scene = bpy.context.scene
    host = scene.aether_bridge_host.strip() or "127.0.0.1"
    port = scene.aether_bridge_port
    actor_id = props.actor_id.strip() if getattr(props, "actor_id", "") else ""
    if actor_id:
        return f"http://{host}:{port}/bridge/{actor_id}/stream/{state}"
    return f"http://{host}:{port}/stream/{state}"


def _collect_pose_payload(armature: bpy.types.Object) -> dict:
    props = _get_bridge_props(armature)
    pose_correction_matrix = Matrix.Identity(4)
    if props is not None and props.use_axis_conversion:
        pose_correction_matrix = get_export_correction_matrix(
            bpy.context.scene.aether_bridge_pose_primary_axis,
            bpy.context.scene.aether_bridge_pose_secondary_axis,
        )

    x_rotation = Matrix.Rotation(math.radians(-90), 4, 'X')

    bones = {}
    for pose_bone in armature.pose.bones:
        bone_data = armature.data.bones.get(pose_bone.name)
        if not bone_data or not bone_data.use_deform:
            continue

        clean_bone_name = re.sub(r"\.\d+$", "", pose_bone.name)
        bone_matrix_world = armature.matrix_world @ pose_bone.matrix
        if props is not None and props.use_axis_conversion:
            bone_matrix_world = bone_matrix_world @ pose_correction_matrix
        bone_matrix_world = x_rotation @ bone_matrix_world

        bones[clean_bone_name] = {
            "Position": f"{bone_matrix_world.translation.x:.6f}, {bone_matrix_world.translation.y:.6f}, {bone_matrix_world.translation.z:.6f}",
            "Rotation": f"{bone_matrix_world.to_quaternion().x:.6f}, {bone_matrix_world.to_quaternion().y:.6f}, {bone_matrix_world.to_quaternion().z:.6f}, {bone_matrix_world.to_quaternion().w:.6f}",
            "Scale": f"{bone_matrix_world.to_scale().x:.8f}, {bone_matrix_world.to_scale().y:.8f}, {bone_matrix_world.to_scale().z:.8f}",
        }

    return {
        "FileExtension": ".pose",
        "TypeName": "Aetherblend Pose",
        "FileVersion": 2,
        "Bones": bones,
    }


def _send_frame(endpoint: str, payload: dict) -> int:
    encoded = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    request = urllib.request.Request(
        endpoint,
        data=encoded,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=1.0) as response:
        return response.getcode()


def _notify_stream_state(armature: bpy.types.Object, state: str) -> None:
    endpoint = _build_state_endpoint(armature, state)
    try:
        status = _send_frame(endpoint, {"event": state})
        if not 200 <= status < 300:
            print(f"[AetherBridge] stream {state} notification failed: HTTP {status}")
    except Exception as error:
        print(f"[AetherBridge] stream {state} notification failed: {error}")


def _bridge_stream_worker(endpoint: str, payload: dict) -> None:
    global _STREAM_FUTURE
    try:
        status = _send_frame(endpoint, payload)
        if not 200 <= status < 300:
            print(f"[AetherBridge] streaming failed: HTTP {status}")
    except urllib.error.URLError as error:
        print(f"[AetherBridge] streaming error: {error}")
    except Exception as error:
        print(f"[AetherBridge] streaming error: {error}")
    finally:
        _STREAM_FUTURE = None


def _get_active_armature() -> bpy.types.Object | None:
    active = bpy.context.active_object
    return active if active and active.type == "ARMATURE" else None


def _shutdown_stream() -> None:
    global _STREAM_TIMER, _STREAM_EXECUTOR, _STREAM_FUTURE
    if _STREAM_TIMER is not None:
        try:
            bpy.app.timers.unregister(_STREAM_TIMER)
        except Exception:
            pass
        _STREAM_TIMER = None

    if _STREAM_FUTURE is not None:
        try:
            _STREAM_FUTURE.cancel()
        except Exception:
            pass
        _STREAM_FUTURE = None

    if _STREAM_EXECUTOR is not None:
        _STREAM_EXECUTOR.shutdown(wait=False)
        _STREAM_EXECUTOR = None


def _bridge_stream_timer() -> float | None:
    global _STREAM_FUTURE, _STREAM_EXECUTOR
    scene = bpy.context.scene
    armature = _get_active_armature()
    if armature is None:
        return None

    props = _get_bridge_props(armature)
    if props is None or not bpy.context.scene.aether_bridge_stream_enabled:
        _shutdown_stream()
        return None

    if _STREAM_FUTURE is not None and not _STREAM_FUTURE.done():
        return 1.0 / max(bpy.context.scene.aether_bridge_stream_fps, 1)

    payload = _collect_pose_payload(armature)
    if not payload["Bones"]:
        return 1.0 / max(bpy.context.scene.aether_bridge_stream_fps, 1)

    endpoint = _build_endpoint(armature)
    if _STREAM_EXECUTOR is None:
        _STREAM_EXECUTOR = ThreadPoolExecutor(max_workers=1)

    _STREAM_FUTURE = _STREAM_EXECUTOR.submit(_bridge_stream_worker, endpoint, payload)
    return 1.0 / max(bpy.context.scene.aether_bridge_stream_fps, 1)


def on_stream_enabled_update(self: bpy.types.PropertyGroup, context: bpy.types.Context) -> None:
    armature = context.active_object
    global _STREAM_TIMER
    if armature is None or not hasattr(armature, "aether_bridge"):
        return
    props = armature.aether_bridge
    if bpy.context.scene.aether_bridge_stream_enabled:
        if _STREAM_TIMER is None:
            print("[AetherBridge] streaming enabled")
            _notify_stream_state(armature, "start")
            _STREAM_TIMER = bpy.app.timers.register(_bridge_stream_timer)
    else:
        _shutdown_stream()
        _notify_stream_state(armature, "stop")
        print("[AetherBridge] streaming disabled")


class AETHER_OT_BridgeRefreshActors(bpy.types.Operator):
    bl_idname = "aether.bridge_refresh_actors"
    bl_label = "Fetch Actors"
    bl_description = "Fetch the actor list from the bridge mock server"

    def execute(self, context: bpy.types.Context) -> set[str]:
        scene = context.scene
        armature = context.active_object
        if armature is None or not hasattr(armature, "aether_bridge"):
            self.report({'ERROR'}, "Select an armature first")
            return {'CANCELLED'}
        props = armature.aether_bridge
        host = scene.aether_bridge_host.strip() or "127.0.0.1"
        port = scene.aether_bridge_port
        endpoint = f"http://{host}:{port}/bridge/actors"
        try:
            request = urllib.request.Request(endpoint, headers={"Accept": "application/json"}, method="GET")
            with urllib.request.urlopen(request, timeout=2.0) as response:
                payload = json.load(response)
        except Exception as error:
            self.report({'ERROR'}, f"Could not load actors: {error}")
            return {'CANCELLED'}

        actors = payload.get("actors", [])
        global BRIDGE_ACTOR_ITEMS
        BRIDGE_ACTOR_ITEMS = [
            (str(actor.get("id", "")), f"{actor.get('id', '')} - {actor.get('name', '')}", "")
            for actor in actors
            if actor.get("id")
        ]

        if BRIDGE_ACTOR_ITEMS:
            current_values = [item[0] for item in BRIDGE_ACTOR_ITEMS]
            if props.actor_id not in current_values:
                props.actor_id = BRIDGE_ACTOR_ITEMS[0][0]
        else:
            props.actor_id = ""

        if context.area is not None:
            context.area.tag_redraw()
        if context.region is not None:
            context.region.tag_redraw()
        self.report({'INFO'}, f"Loaded {len(BRIDGE_ACTOR_ITEMS)} actors")
        return {'FINISHED'}


class AETHER_OT_BridgeClearActor(bpy.types.Operator):
    bl_idname = "aether.bridge_clear_actor"
    bl_label = "Clear Actor"
    bl_description = "Remove the assigned actor and stop streaming"

    def execute(self, context: bpy.types.Context) -> set[str]:
        armature = context.active_object
        if armature is None or not hasattr(armature, "aether_bridge"):
            self.report({'ERROR'}, "Select an armature first")
            return {'CANCELLED'}

        props = armature.aether_bridge
        props.actor_id = ""
        if context.scene.aether_bridge_stream_enabled:
            context.scene.aether_bridge_stream_enabled = False

        if context.area is not None:
            context.area.tag_redraw()
        self.report({'INFO'}, "Actor cleared")
        return {'FINISHED'}


classes = (AETHER_OT_BridgeRefreshActors, AETHER_OT_BridgeClearActor)


def register() -> None:
    from .properties import register as register_properties

    register_properties()

    if not hasattr(bpy.types.Scene, "aether_bridge_pose_primary_axis"):
        bpy.types.Scene.aether_bridge_pose_primary_axis = bpy.props.EnumProperty(
            name="Primary Axis",
            description="Primary axis for bridge pose export orientation",
            items=[('X', 'X Axis', ''), ('Y', 'Y Axis', ''), ('Z', 'Z Axis', ''), ('-X', '-X Axis', ''), ('-Y', '-Y Axis', ''), ('-Z', '-Z Axis', '')],
            default='X',
        )
    if not hasattr(bpy.types.Scene, "aether_bridge_pose_secondary_axis"):
        bpy.types.Scene.aether_bridge_pose_secondary_axis = bpy.props.EnumProperty(
            name="Secondary Axis",
            description="Secondary axis for bridge pose export orientation",
            items=[('X', 'X Axis', ''), ('Y', 'Y Axis', ''), ('Z', 'Z Axis', ''), ('-X', '-X Axis', ''), ('-Y', '-Y Axis', ''), ('-Z', '-Z Axis', '')],
            default='Y',
        )


def unregister() -> None:
    global _STREAM_TIMER
    _shutdown_stream()

    from .properties import unregister as unregister_properties

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    unregister_properties()

    if hasattr(bpy.types.Scene, "aether_bridge_pose_primary_axis"):
        del bpy.types.Scene.aether_bridge_pose_primary_axis
    if hasattr(bpy.types.Scene, "aether_bridge_pose_secondary_axis"):
        del bpy.types.Scene.aether_bridge_pose_secondary_axis
