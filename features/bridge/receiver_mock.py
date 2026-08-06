"""Mock receiving endpoint for AetherBlend bridge pose streaming.

This mock server accepts pose frames at POST /pose and provides a minimal
monitor dashboard with live metrics for partner testing.

Endpoints:
- POST /pose: send JSON payload with bone transforms
- GET /: browser dashboard
- GET /data: JSON metrics and last frame details
"""

import time
import html
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

STORED_FRAMES: list[dict] = []
MAX_STORED_FRAMES = 50
TOTAL_FRAMES_RECEIVED = 0
STREAM_ACTIVE = False
MAX_DISPLAY_BONES = 20
ACTORS: list[dict] = [
    {"id": "1", "name": "Actor 1"},
    {"id": "2", "name": "Actor 2"},
    {"id": "3", "name": "Actor 3"},
]
ACTOR_FRAMES: dict[str, list[dict]] = {}


def _reset_stream_state(active: bool = False) -> None:
    global STORED_FRAMES, TOTAL_FRAMES_RECEIVED, STREAM_ACTIVE
    STORED_FRAMES.clear()
    TOTAL_FRAMES_RECEIVED = 0
    STREAM_ACTIVE = active
    ACTOR_FRAMES.clear()


def _store_frame(actor_id: str | None, frame_data: dict) -> None:
    global STORED_FRAMES, TOTAL_FRAMES_RECEIVED
    STORED_FRAMES.insert(0, frame_data)
    STORED_FRAMES[:] = STORED_FRAMES[:MAX_STORED_FRAMES]
    TOTAL_FRAMES_RECEIVED += 1
    if actor_id:
        actor_frames = ACTOR_FRAMES.setdefault(actor_id, [])
        actor_frames.insert(0, frame_data)
        ACTOR_FRAMES[actor_id] = actor_frames[:MAX_STORED_FRAMES]


def _calculate_fps() -> float:
    if len(STORED_FRAMES) < 2:
        return 0.0
    recent = STORED_FRAMES[:min(len(STORED_FRAMES), 20)]
    timestamps = [frame["timestamp"] for frame in recent]
    duration = timestamps[0] - timestamps[-1]
    return (len(timestamps) - 1) / duration if duration > 0 else 0.0


def _get_bone_display_values(bone: object) -> tuple[object, object, object]:
    if isinstance(bone, dict):
        position = bone.get("position")
        if position is None:
            position = bone.get("Position")
        rotation = bone.get("rotation")
        if rotation is None:
            rotation = bone.get("Rotation")
        scale = bone.get("scale")
        if scale is None:
            scale = bone.get("Scale")
        return position, rotation, scale
    if isinstance(bone, str):
        return bone, None, None
    return None, None, None


def _build_response_data(actor_id: str | None = None) -> dict:
    global TOTAL_FRAMES_RECEIVED, STREAM_ACTIVE
    frame_count = TOTAL_FRAMES_RECEIVED
    fps = _calculate_fps()
    frames = ACTOR_FRAMES.get(actor_id, STORED_FRAMES) if actor_id else STORED_FRAMES
    last_frame = frames[0] if frames else None
    if last_frame and isinstance(last_frame.get("bones"), dict):
        bones = last_frame["bones"]
        normalized_bones = {}
        for name, bone in list(bones.items())[:MAX_DISPLAY_BONES]:
            position, rotation, scale = _get_bone_display_values(bone)
            normalized_bones[name] = {
                "position": position,
                "rotation": rotation,
                "scale": scale,
            }
        last_frame_info = {
            "frame_number": last_frame.get("frame_number"),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(last_frame.get("timestamp", time.time()))),
            "bone_count": len(bones),
            "bones": normalized_bones,
            "has_more_bones": len(bones) > MAX_DISPLAY_BONES,
            "total_bones": len(bones),
            "actor_id": actor_id,
        }
    else:
        last_frame_info = None
    return {
        "frame_count": frame_count,
        "fps": fps,
        "stream_active": STREAM_ACTIVE,
        "last_frame": last_frame_info,
        "download_url": f"/download-last-pose{'/' + actor_id if actor_id else ''}",
    }


class BridgeReceiverHandler(BaseHTTPRequestHandler):
    def _send_json(self, data: dict, status: int = 200) -> None:
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, html_content: str, status: int = 200) -> None:
        body = html_content.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        if length == 0:
            return {}
        payload = self.rfile.read(length).decode("utf-8")
        return json.loads(payload)

    def do_POST(self):
        if self.path == "/pose":
            self._handle_pose_post(None)
        elif self.path.startswith("/bridge/"):
            parts = [part for part in self.path.split("/") if part]
            if len(parts) >= 2 and parts[0] == "bridge" and parts[1] == "actors":
                self._send_json({"status": "ok", "actors": ACTORS})
                return
            if len(parts) >= 4 and parts[0] == "bridge" and parts[2] == "stream":
                actor_id = parts[1]
                if actor_id not in {actor["id"] for actor in ACTORS}:
                    self._send_json({"status": "error", "message": "Unknown actor"}, status=404)
                    return
                state = parts[3]
                if state == "start":
                    _reset_stream_state(active=True)
                elif state == "stop":
                    _reset_stream_state(active=False)
                else:
                    self._send_json({"status": "error", "message": "Unsupported stream state"}, status=400)
                    return
                self._send_json({"status": "ok", "stream_active": state == "start", "actor_id": actor_id})
                return
            actor_id = parts[1] if len(parts) >= 2 and parts[0] == "bridge" else None
            if actor_id and actor_id not in {actor["id"] for actor in ACTORS}:
                self._send_json({"status": "error", "message": "Unknown actor"}, status=404)
                return
            self._handle_pose_post(actor_id)
        elif self.path == "/stream/start":
            _reset_stream_state(active=True)
            self._send_json({"status": "ok", "stream_active": True})
        elif self.path == "/stream/stop":
            _reset_stream_state(active=False)
            self._send_json({"status": "ok", "stream_active": False})
        else:
            self.send_error(404, "Not Found")

    def _handle_pose_post(self, actor_id: str | None) -> None:
        try:
            data = self._read_json()
            bones = data.get("Bones") or data.get("bones", {})
            bone_count = len(bones) if isinstance(bones, dict) else 0
            print(f"Received pose frame for actor {actor_id or 'default'} with {bone_count} bones")

            global STREAM_ACTIVE
            STREAM_ACTIVE = True
            frame_data = {
                "frame_number": TOTAL_FRAMES_RECEIVED + 1,
                "timestamp": time.time(),
                "bones": bones,
                "actor_id": actor_id,
            }
            _store_frame(actor_id, frame_data)
            self._send_json({"status": "ok", "stream_active": STREAM_ACTIVE, "actor_id": actor_id})
        except Exception as exc:
            print(f"Error receiving pose: {exc}")
            self._send_json({"status": "error", "message": str(exc)}, status=400)

    def do_GET(self):
        if self.path == "/data":
            self._send_json(_build_response_data())
        elif self.path == "/bridge/actors":
            self._send_json({"actors": ACTORS})
        elif self.path.startswith("/download-last-pose"):
            actor_id = self.path.removeprefix("/download-last-pose/") if self.path.startswith("/download-last-pose/") else None
            self._download_last_pose(actor_id)
        elif self.path.startswith("/bridge/"):
            parts = [part for part in self.path.split("/") if part]
            actor_id = parts[1] if len(parts) >= 2 and parts[0] == "bridge" and parts[1] != "actors" else None
            if actor_id and actor_id not in {actor["id"] for actor in ACTORS}:
                self._send_json({"status": "error", "message": "Unknown actor"}, status=404)
                return
            self._send_json(_build_response_data(actor_id))
        elif self.path == "/":
            self._send_html(self._build_dashboard())
        else:
            self.send_error(404, "Not Found")

    def _download_last_pose(self, actor_id: str | None = None) -> None:
        frames = ACTOR_FRAMES.get(actor_id, STORED_FRAMES) if actor_id else STORED_FRAMES
        last_frame = frames[0] if frames else None
        if not last_frame or not isinstance(last_frame.get("bones"), dict):
            self._send_json({"status": "error", "message": "No pose frame available"}, status=404)
            return

        payload = {
            "Author": "AetherBridge Mock",
            "Description": "Latest streamed frame",
            "Version": "1.0.0",
            "Tags": ["bridge", "mock"],
            "FileExtension": ".pose",
            "TypeName": "Aetherblend Pose",
            "FileVersion": 2,
            "Bones": last_frame["bones"],
        }
        body = json.dumps(payload, indent=4).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Disposition", "attachment; filename=last_frame.pose")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _build_dashboard(self) -> str:
        global TOTAL_FRAMES_RECEIVED, STREAM_ACTIVE
        frame_count = TOTAL_FRAMES_RECEIVED
        fps = _calculate_fps()
        last_frame = STORED_FRAMES[0] if STORED_FRAMES else None

        if last_frame and isinstance(last_frame.get("bones"), dict):
            bones = last_frame["bones"]
            last_frame_title = f"Last Frame #{last_frame.get('frame_number')}"
            last_frame_meta = f"{len(bones)} bones · {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_frame.get('timestamp', time.time())))}"
            lines = [
                f"Frame: {last_frame.get('frame_number')}",
                f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_frame.get('timestamp', time.time())))}",
                f"Bone count: {len(bones)}",
            ]
            for name, bone in list(bones.items())[:MAX_DISPLAY_BONES]:
                position, rotation, scale = _get_bone_display_values(bone)
                lines.append(
                    f"{html.escape(name)}: position={html.escape(str(position))} rotation={html.escape(str(rotation))} scale={html.escape(str(scale))}"
                )
            if len(bones) > MAX_DISPLAY_BONES:
                lines.append(f"...and {len(bones) - MAX_DISPLAY_BONES} more bones...")
            last_frame_text = "\n\n".join(lines)
        else:
            last_frame_title = "No frame received yet"
            last_frame_meta = ""
            last_frame_text = "Waiting for first pose frame..."

        return f"""
<html>
<head>
<title>AetherBridge Receiver Mock</title>
<style>
body {{ margin: 0; min-height: 100vh; background: #090b10; color: #e7eefc; font-family: Inter, Arial, sans-serif; }}
.container {{ max-width: 960px; margin: 0 auto; padding: 30px; }}
.header {{ margin-bottom: 24px; }}
.header h1 {{ margin: 0 0 8px; font-size: 2.2rem; }}
.header p {{ margin: 0; color: #a5b3d0; }}
.stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; margin-bottom: 24px; }}
.stat {{ padding: 22px; border-radius: 20px; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); box-shadow: 0 24px 50px rgba(0,0,0,0.18); }}
.stat strong {{ display: block; font-size: 2.6rem; color: #ffffff; margin-bottom: 8px; }}
.card {{ padding: 24px; border-radius: 22px; background: #0f1728; border: 1px solid rgba(255,255,255,0.08); box-shadow: 0 24px 55px rgba(0,0,0,0.2); }}
.card h2 {{ margin-top: 0; font-size: 1.3rem; }}
.code-block {{ white-space: pre-wrap; word-break: break-word; margin: 0; padding: 18px; background: #08101f; border: 1px solid rgba(255,255,255,0.06); border-radius: 16px; color: #d7e3ff; line-height: 1.6; max-height: 520px; overflow: auto; }}
.small {{ color: #8fa3c4; margin-top: 8px; }}
</style>
<script>
async function refreshDashboard() {{
  try {{
    const res = await fetch('/data', {{ cache: 'no-store' }});
    const data = await res.json();
    document.getElementById('frame-count').textContent = data.frame_count;
    document.getElementById('frame-fps').textContent = data.fps.toFixed(2);
    document.getElementById('stream-status').textContent = data.stream_active ? 'Active' : 'Idle';
    if (data.last_frame) {{
      document.getElementById('last-title').textContent = `Last Frame #${{data.last_frame.frame_number}}`;
      document.getElementById('last-meta').textContent = `${{data.last_frame.bone_count}} bones · ${{data.last_frame.timestamp}}`;
      const lines = [];
      for (const [name, bone] of Object.entries(data.last_frame.bones)) {{
        const position = bone.position ?? null;
        const rotation = bone.rotation ?? null;
        const scale = bone.scale ?? null;
        lines.push(`${{name}}: position=${{JSON.stringify(position)}} rotation=${{JSON.stringify(rotation)}} scale=${{JSON.stringify(scale)}}`);
      }}
      if (data.last_frame.has_more_bones) {{
        lines.push(`...and ${{data.last_frame.total_bones - Object.keys(data.last_frame.bones).length}} more bones...`);
      }}
      document.getElementById('last-data').textContent = lines.join('\n\n');
    }} else {{
      document.getElementById('last-title').textContent = 'No frame received yet';
      document.getElementById('last-meta').textContent = '';
      document.getElementById('last-data').textContent = 'Waiting for first pose frame...';
    }}
  }} catch (error) {{
    console.warn('Dashboard refresh failed', error);
  }}
}}
window.addEventListener('load', () => {{
  refreshDashboard();
  setInterval(refreshDashboard, 1000);
}});
</script>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>AetherBridge Receiver Mock</h1>
    <p>Live receive monitor for pose frames sent from Blender. Refreshes automatically.</p>
  </div>
  <div class="stats">
    <div class="stat">
      <strong id="frame-count">{frame_count}</strong>
      Total frames received
    </div>
    <div class="stat">
      <strong id="frame-fps">{fps:.2f}</strong>
      Receive FPS
    </div>
    <div class="stat">
      <strong id="stream-status">{'Active' if STREAM_ACTIVE else 'Idle'}</strong>
      Stream status
    </div>
  </div>
  <div class="card">
    <h2 id="last-title">{last_frame_title}</h2>
    <div class="small" id="last-meta">{last_frame_meta}</div>
    <div class="small" style="margin-bottom: 12px;"><a href="/download-last-pose" style="color: #7dd3fc;">Download last frame as .pose</a></div>
    <pre class="code-block" id="last-data">{last_frame_text}</pre>
  </div>
</div>
</body>
</html>
"""

    def log_message(self, format: str, *args) -> None:
        return


def run(port: int = 8080) -> None:
    server = ThreadingHTTPServer(("0.0.0.0", port), BridgeReceiverHandler)
    print(f"AetherBridge receiver mock running on http://127.0.0.1:{port}")
    print("POST /pose to send frames")
    print("GET /data for JSON metrics")
    print(f"Open http://127.0.0.1:{port}/ in a browser to inspect received frames")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Receiver mock stopped")
        server.server_close()


if __name__ == "__main__":
    run()
