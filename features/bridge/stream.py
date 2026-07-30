import json
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

import bpy

_STREAM_TIMER = None
_STREAM_EXECUTOR = None
_STREAM_FUTURE = None


def _clean_path(path: str) -> str:
    path = path.strip()
    if not path:
        return "/pose"
    return path if path.startswith("/") else f"/{path}"


def _build_endpoint(scene: bpy.types.Scene) -> str:
    host = scene.aether_bridge_host.strip() or "127.0.0.1"
    port = scene.aether_bridge_port
    scheme = scene.aether_bridge_scheme
    path = _clean_path(scene.aether_bridge_endpoint_path)
    return f"{scheme}://{host}:{port}{path}"


def _collect_pose_payload(armature: bpy.types.Object) -> dict:
    bones = {}
    for pose_bone in armature.pose.bones:
        matrix = pose_bone.matrix.copy()
        translation = matrix.to_translation()
        rotation = matrix.to_quaternion()
        scale = matrix.to_scale()

        bones[pose_bone.name] = {
            "position": {"x": translation.x, "y": translation.y, "z": translation.z},
            "rotation": {"x": rotation.x, "y": rotation.y, "z": rotation.z, "w": rotation.w},
            "scale": {"x": scale.x, "y": scale.y, "z": scale.z},
        }

    return {"bones": bones}


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

    if not scene.aether_bridge_stream_enabled:
        _shutdown_stream()
        return None

    if _STREAM_FUTURE is not None and not _STREAM_FUTURE.done():
        return 1.0 / max(scene.aether_bridge_stream_fps, 1)

    armature = _get_active_armature()
    if armature is None:
        return 1.0 / max(scene.aether_bridge_stream_fps, 1)

    payload = _collect_pose_payload(armature)
    if not payload["bones"]:
        return 1.0 / max(scene.aether_bridge_stream_fps, 1)

    endpoint = _build_endpoint(scene)
    if _STREAM_EXECUTOR is None:
        _STREAM_EXECUTOR = ThreadPoolExecutor(max_workers=1)

    _STREAM_FUTURE = _STREAM_EXECUTOR.submit(_bridge_stream_worker, endpoint, payload)
    return 1.0 / max(scene.aether_bridge_stream_fps, 1)


def on_stream_enabled_update(self: bpy.types.PropertyGroup, context: bpy.types.Context) -> None:
    scene = context.scene
    global _STREAM_TIMER
    if scene.aether_bridge_stream_enabled:
        if _STREAM_TIMER is None:
            print("[AetherBridge] streaming enabled")
            _STREAM_TIMER = bpy.app.timers.register(_bridge_stream_timer)
    else:
        _shutdown_stream()
        print("[AetherBridge] streaming disabled")


class AETHER_OT_BridgeSendFrame(bpy.types.Operator):
    bl_idname = "aether.bridge_send_frame"
    bl_label = "Send Current Frame"
    bl_description = "Send the current armature pose once to the bridge server"

    def execute(self, context: bpy.types.Context) -> set[str]:
        scene = context.scene
        armature = _get_active_armature()
        if armature is None:
            self.report({'ERROR'}, "Select an armature before sending")
            return {'CANCELLED'}

        payload = _collect_pose_payload(armature)
        if not payload["bones"]:
            self.report({'ERROR'}, "No pose bones found to stream")
            return {'CANCELLED'}

        endpoint = _build_endpoint(scene)
        try:
            status = _send_frame(endpoint, payload)
            if 200 <= status < 300:
                self.report({'INFO'}, f"Frame streamed to {endpoint}")
                return {'FINISHED'}
            self.report({'ERROR'}, f"Server returned HTTP {status}")
            return {'CANCELLED'}
        except Exception as error:
            self.report({'ERROR'}, f"Streaming failed: {error}")
            return {'CANCELLED'}


classes = (
    AETHER_OT_BridgeSendFrame,
)


def register() -> None:
    for cls in classes:
        bpy.utils.register_class(cls)

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

    bpy.types.Scene.aether_bridge_scheme = bpy.props.EnumProperty(
        name="Protocol",
        description="HTTP protocol for bridge streaming",
        items=(
            ('http', "HTTP", "Use HTTP"),
            ('https', "HTTPS", "Use HTTPS"),
        ),
        default='http',
    )

    bpy.types.Scene.aether_bridge_endpoint_path = bpy.props.StringProperty(
        name="Path",
        description="Endpoint path for bridge streaming",
        default="/pose",
    )

    bpy.types.Scene.aether_bridge_stream_enabled = bpy.props.BoolProperty(
        name="Stream Pose",
        description="Enable continuous pose streaming",
        default=False,
        update=on_stream_enabled_update,
    )

    bpy.types.Scene.aether_bridge_stream_fps = bpy.props.IntProperty(
        name="Stream FPS",
        description="Target frames per second for bridge streaming",
        default=15,
        min=1,
        max=60,
    )


def unregister() -> None:
    global _STREAM_TIMER
    _shutdown_stream()

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.aether_bridge_host
    del bpy.types.Scene.aether_bridge_port
    del bpy.types.Scene.aether_bridge_scheme
    del bpy.types.Scene.aether_bridge_endpoint_path
    del bpy.types.Scene.aether_bridge_stream_enabled
    del bpy.types.Scene.aether_bridge_stream_fps
