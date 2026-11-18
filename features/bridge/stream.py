"""Fetch actors and stream original FFXIV bone poses."""

import json
import math
import re
import time
import urllib.error
import urllib.request
from concurrent.futures import Future, ThreadPoolExecutor

import bpy
from mathutils import Matrix

from ...utils.axis_conversion import DEFAULT_PRIMARY_BONE_AXIS, DEFAULT_SECONDARY_BONE_AXIS, get_export_correction_matrix

_executor: ThreadPoolExecutor | None = None
_future: Future | None = None
_scene: bpy.types.Scene | None = None
_next_frame = 0.0
_actor_item_history: list[list[tuple[str, str, str, int]]] = []


def _url(scene: bpy.types.Scene, path: str) -> str:
    return f"http://{scene.aether_bridge_host.strip()}:{scene.aether_bridge_port}{path}"


def _assigned_rigs(scene: bpy.types.Scene) -> list[bpy.types.Object]:
    return [obj for obj in scene.objects if obj.type == "ARMATURE" and obj.aether_bridge.actor_id]


def _validate_rigs(scene: bpy.types.Scene) -> str | None:
    rigs = _assigned_rigs(scene)
    if not rigs:
        return "Assign an actor to at least one armature before streaming"
    actors = set()
    for rig in rigs:
        if rig.aether_bridge.actor_id in actors:
            return f"Actor {rig.aether_bridge.actor_id} is assigned to multiple armatures"
        actors.add(rig.aether_bridge.actor_id)
        if rig.data.collections.get("Original") is None:
            return f"{rig.name} has no Original bone collection"
    return None


def _pose_payload(rig: bpy.types.Object) -> dict:
    collection = rig.data.collections.get("Original")
    if collection is None:
        raise ValueError(f"{rig.name} has no Original bone collection")
    correction = get_export_correction_matrix(DEFAULT_PRIMARY_BONE_AXIS, DEFAULT_SECONDARY_BONE_AXIS)
    rotation = Matrix.Rotation(math.radians(-90), 4, "X")
    world = rotation @ rig.matrix_world
    bones = {}
    for original in collection.bones:
        bone = rig.pose.bones.get(original.name)
        if bone is None:
            continue
        matrix = world @ bone.matrix @ correction
        position, quaternion, scale = matrix.translation, matrix.to_quaternion(), matrix.to_scale()
        name = re.sub(r"\.\d+$", "", bone.name)
        if name in bones:
            raise ValueError(f"{rig.name} has duplicate original bone name {name}")
        bones[name] = {
            "Position": f"{position.x:.6f}, {position.y:.6f}, {position.z:.6f}",
            "Rotation": f"{quaternion.x:.6f}, {quaternion.y:.6f}, {quaternion.z:.6f}, {quaternion.w:.6f}",
            "Scale": f"{scale.x:.8f}, {scale.y:.8f}, {scale.z:.8f}",
        }
    if not bones:
        raise ValueError(f"{rig.name} has no bones in its Original collection")
    return {"Type": "pose", "ActorId": rig.aether_bridge.actor_id, "Bones": bones}


def _send_poses(url: str, payloads: list[dict]) -> None:
    request = urllib.request.Request(
        url,
        data=json.dumps({"Type": "poses", "Poses": payloads}, separators=(",", ":")).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=2) as response:
        response.read()


def _stop() -> None:
    global _executor, _future, _scene, _next_frame
    if bpy.app.timers.is_registered(_tick):
        bpy.app.timers.unregister(_tick)
    if _executor is not None:
        _executor.shutdown(wait=False, cancel_futures=True)
    _executor = None
    _future = None
    _scene = None
    _next_frame = 0.0


def _tick() -> float | None:
    global _future, _next_frame
    started = time.monotonic()
    scene = _scene
    if scene is None or not scene.aether_bridge_stream_enabled:
        return None
    try:
        if _future is not None:
            if not _future.done():
                return 0.005
            _future.result()
            _future = None
        if started < _next_frame:
            return _next_frame - started
        error = _validate_rigs(scene)
        if error:
            raise ValueError(error)
        payloads = [_pose_payload(rig) for rig in _assigned_rigs(scene)]
        if _executor is None:
            raise RuntimeError("Bridge streaming executor is not running")
        _future = _executor.submit(_send_poses, _url(scene, "/pose"), payloads)
        interval = 1.0 / scene.aether_bridge_stream_fps
        if not _next_frame:
            _next_frame = started
        _next_frame = max(_next_frame, started - interval) + interval
    except (ValueError, RuntimeError, OSError) as error:
        print(f"[AetherBridge] Streaming stopped: {error}")
        scene.aether_bridge_stream_enabled = False
        scene.aether_bridge_status = str(error)
        return None
    return max(0.001, _next_frame - time.monotonic())


def update_stream(scene: bpy.types.Scene, _context: bpy.types.Context) -> None:
    """Start or stop streaming assigned armatures from this scene."""
    global _executor, _scene
    if not scene.aether_bridge_stream_enabled:
        if _scene == scene:
            _stop()
        scene.aether_bridge_status = ""
        return
    error = _validate_rigs(scene)
    if _scene is not None:
        error = "Streaming is already active in another scene"
    if not scene.aether_bridge_host.strip():
        error = "Bridge host cannot be empty"
    if error:
        print(f"[AetherBridge] {error}")
        scene.aether_bridge_stream_enabled = False
        scene.aether_bridge_status = error
        return
    scene.aether_bridge_status = ""
    _scene = scene
    _executor = ThreadPoolExecutor(max_workers=1)
    bpy.app.timers.register(_tick)


class AETHER_OT_BridgeRefreshActors(bpy.types.Operator):
    """Fetch available actor IDs from the bridge receiver."""

    bl_idname = "aether.bridge_refresh_actors"
    bl_label = "Fetch Actors"

    def execute(self, context: bpy.types.Context) -> set[str]:
        """Replace the actor choices with the receiver's current list."""
        from .properties import ACTOR_ITEMS

        try:
            with urllib.request.urlopen(_url(context.scene, "/actors"), timeout=2) as response:
                data = json.load(response)
            actors = data["actors"]
            if not isinstance(actors, list) or any(not isinstance(actor, str) or not actor or actor == "__NONE__" for actor in actors):
                raise ValueError("Expected a list of non-empty actor IDs")
            if len(set(actors)) != len(actors):
                raise ValueError("Receiver returned duplicate actor IDs")
        except (OSError, ValueError, KeyError, TypeError) as error:
            self.report({"ERROR"}, f"Could not fetch actors: {error}")
            return {"CANCELLED"}
        items = [("__NONE__", "No actor", "", 0)]
        items.extend((actor, f"Actor {actor}", "", index) for index, actor in enumerate(actors, 1))
        _actor_item_history.append(list(ACTOR_ITEMS))
        ACTOR_ITEMS[:] = items
        self.report({"INFO"}, f"Loaded {len(actors)} actors")
        return {"FINISHED"}


def register() -> None:
    """Register the actor-fetch operator."""
    bpy.utils.register_class(AETHER_OT_BridgeRefreshActors)


def unregister() -> None:
    """Stop streaming and unregister the actor-fetch operator."""
    _stop()
    bpy.utils.unregister_class(AETHER_OT_BridgeRefreshActors)
