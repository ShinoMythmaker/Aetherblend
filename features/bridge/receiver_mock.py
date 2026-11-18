"""Local mock receiver: GET /actors, POST /pose, and GET /data."""

import json
import threading
import time
from collections import deque
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ACTORS = ["0", "1", "2", "3"]
POSES: dict[str, dict] = {}
FRAME_COUNTS: dict[str, int] = {}
LAST_RECEIVED: dict[str, float] = {}
RECENT_FRAMES: dict[str, deque[float]] = {}
RECENT_PACKAGES: deque[float] = deque()
PACKAGE_COUNT = 0
FPS_WINDOW_SECONDS = 3.0
LOCK = threading.Lock()

_DASHBOARD = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>AetherBridge | Receiver</title>
<style>
:root { color-scheme: dark; font-family: system-ui, sans-serif; background: #10131b; color: #e7eaf3; }
* { box-sizing: border-box; }
body { margin: 0; }
main { max-width: 1280px; margin: auto; padding: 36px 24px 60px; }
header, .section-heading, .card-top, .details-heading { display: flex; justify-content: space-between; align-items: center; gap: 16px; }
header { margin-bottom: 30px; flex-wrap: wrap; }
.eyebrow { color: #a7a5ff; font-size: 12px; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; }
h1 { margin: 6px 0; font-size: 30px; letter-spacing: -.03em; }
h2 { font-size: 17px; margin: 0; } h3 { margin: 0; font-size: 16px; }
p { color: #929bb0; margin: 0; line-height: 1.5; }
.button, button { font: inherit; cursor: pointer; }
.button { display: inline-flex; align-items: center; text-decoration: none; background: #8c82ff; color: #111324;
  border-radius: 9px; padding: 11px 16px; font-weight: 700; }
.button:hover { background: #a49cff; }
.summary { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 32px; }
.stat, .actor, .details { background: #191e2a; border: 1px solid #2b3242; border-radius: 12px; }
.stat { padding: 16px 18px; } .stat span, .metric-label { display: block; color: #929bb0; font-size: 12px; }
.stat strong { display: block; font-size: 24px; margin-top: 5px; }
.stat .actor-ids { font-size: 16px; overflow-wrap: anywhere; }
.section-heading { margin-bottom: 14px; } .section-heading p { font-size: 13px; }
.actors { display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 12px; margin-bottom: 28px; }
.actor { color: inherit; text-align: left; padding: 16px; }
.actor:hover, .actor.selected { border-color: #8c82ff; }
.badge { border-radius: 20px; padding: 4px 8px; background: #2a303d; color: #aeb7c9; font-size: 11px; font-weight: 700; }
.badge.live { background: #153e35; color: #65e2b1; }
.metrics { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 20px; }
.metric-value { display: block; margin-top: 4px; font-size: 14px; font-weight: 600; }
.details { overflow: hidden; } .details-heading { padding: 18px; border-bottom: 1px solid #2b3242; flex-wrap: wrap; }
.details-heading p { margin-top: 4px; font-size: 13px; }
.download { color: #b7b0ff; font-size: 13px; text-decoration: none; }
.download:hover { text-decoration: underline; }
pre { margin: 0; padding: 18px; max-height: 540px; overflow: auto; color: #bec9dc; font-size: 12px; line-height: 1.6; }
.error { color: #ffa9a9; }
@media (max-width: 600px) { main { padding: 24px 16px; } .summary { grid-template-columns: 1fr; } }
</style></head>
<body><main>
<header><div><div class="eyebrow">AetherBlend / development</div><h1>Bridge receiver</h1>
<p>Monitor incoming actor poses in real time.</p></div>
<a class="button" href="/download">Download data package</a></header>
<section class="summary" aria-label="Receiver summary">
<div class="stat"><span>Available actor IDs</span><strong class="actor-ids" id="actor-ids">—</strong></div>
<div class="stat"><span>Package FPS · all actors (3s average)</span><strong id="receive-fps">—</strong></div>
<div class="stat"><span>Packages received</span><strong id="frame-count">—</strong></div></section>
<div class="section-heading"><h2>Available actors</h2><p id="connection" role="status">Connecting…</p></div>
<section class="actors" id="actors" aria-label="Available actors"></section>
<section class="details"><div class="details-heading"><div><h2 id="frame-title">Frame data</h2>
<p id="frame-description">Select an actor to inspect its latest frame.</p></div>
<a class="download" id="pose-download" hidden>Download pose</a></div>
<pre id="frame-data">Waiting for pose data…</pre></section>
</main>
<script>
let selectedActor = null;
let latest = null;
function element(tag, className, text) {
  const node = document.createElement(tag);
  node.className = className;
  node.textContent = text;
  return node;
}
function render() {
  const data = latest;
  const actors = document.getElementById('actors');
  document.getElementById('actor-ids').textContent = data.actors.join(', ') || 'None';
  document.getElementById('receive-fps').textContent = data.receive_fps.toFixed(1);
  document.getElementById('frame-count').textContent = data.package_count;
  if (!data.actors.includes(selectedActor)) selectedActor = data.actors[0] ?? null;
  const cards = new Map(Array.from(actors.children, card => [card.dataset.actor, card]));
  for (const [index, actor] of data.actors.entries()) {
    const pose = data.poses[actor];
    const metrics = data.frames[actor];
    const live = metrics && Date.now() / 1000 - metrics.last_received < 3;
    let card = cards.get(actor);
    if (!card) {
      card = element('button', 'actor', '');
      card.type = 'button';
      card.dataset.actor = actor;
      card.addEventListener('click', () => { selectedActor = actor; render(); });
    }
    cards.delete(actor);
    card.className = 'actor' + (actor === selectedActor ? ' selected' : '');
    card.setAttribute('aria-pressed', String(actor === selectedActor));
    const top = element('div', 'card-top', '');
    top.append(element('h3', '', 'Actor ' + actor), element('span', 'badge' + (live ? ' live' : ''), live ? 'LIVE' : 'IDLE'));
    const grid = element('div', 'metrics', '');
    const values = [['Frames', metrics ? metrics.count : 0], ['Receive FPS', metrics ? metrics.fps.toFixed(1) : '0.0'],
                    ['Bones', pose ? Object.keys(pose.Bones).length : 0]];
    for (const [label, value] of values) {
      const metric = element('div', '', '');
      metric.append(element('span', 'metric-label', label), element('span', 'metric-value', String(value)));
      grid.append(metric);
    }
    card.replaceChildren(top, grid);
    if (actors.children[index] !== card) actors.insertBefore(card, actors.children[index] ?? null);
  }
  for (const card of cards.values()) card.remove();
  const pose = data.poses[selectedActor];
  const metrics = data.frames[selectedActor];
  document.getElementById('frame-title').textContent = selectedActor === null ? 'Frame data' : 'Actor ' + selectedActor + ' · latest frame';
  document.getElementById('frame-description').textContent = metrics
    ? 'Received ' + new Date(metrics.last_received * 1000).toLocaleString() + ' · frame ' + metrics.count
    : 'No frames received for this actor yet.';
  document.getElementById('frame-data').textContent = pose ? JSON.stringify(pose, null, 2) : 'Waiting for pose data…';
  const download = document.getElementById('pose-download');
  download.hidden = !pose;
  if (pose) {
    download.href = 'data:application/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(pose, null, 2));
    download.download = 'actor-' + selectedActor + '.pose';
  }
}
async function refresh() {
  try {
    const response = await fetch('/data', {cache: 'no-store'});
    if (!response.ok) throw new Error('HTTP ' + response.status);
    latest = await response.json();
    render();
    const status = document.getElementById('connection');
    status.textContent = 'Connected · updates every second';
    status.className = '';
  } catch (error) {
    const status = document.getElementById('connection');
    status.textContent = 'Disconnected: ' + error;
    status.className = 'error';
  }
}
refresh(); setInterval(refresh, 1000);
</script></body></html>"""


def _snapshot() -> dict:
    with LOCK:
        cutoff = time.monotonic() - FPS_WINDOW_SECONDS
        for timestamps in RECENT_FRAMES.values():
            while timestamps and timestamps[0] <= cutoff:
                timestamps.popleft()
        while RECENT_PACKAGES and RECENT_PACKAGES[0] <= cutoff:
            RECENT_PACKAGES.popleft()
        rates = {actor: len(timestamps) / FPS_WINDOW_SECONDS for actor, timestamps in RECENT_FRAMES.items()}
        return {
            "actors": list(ACTORS),
            "frame_count": sum(FRAME_COUNTS.values()),
            "package_count": PACKAGE_COUNT,
            "receive_fps": len(RECENT_PACKAGES) / FPS_WINDOW_SECONDS,
            "frames": {
                actor: {"count": FRAME_COUNTS[actor], "last_received": timestamp, "fps": rates.get(actor, 0.0)}
                for actor, timestamp in LAST_RECEIVED.items()
                if actor in POSES
            },
            "poses": dict(POSES),
        }


class BridgeReceiverHandler(BaseHTTPRequestHandler):
    """Receive actor-tagged pose payloads and display the latest per actor."""

    def _respond(self, status: int, data: bytes, content_type: str, download: str | None = None) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        if download:
            self.send_header("Content-Disposition", f'attachment; filename="{download}"')
        self.end_headers()
        self.wfile.write(data)

    def _json(self, status: int, data: dict) -> None:
        self._respond(status, json.dumps(data).encode("utf-8"), "application/json")

    def do_GET(self) -> None:
        """Return actor IDs, the latest poses, or the monitor page."""
        if self.path == "/actors":
            self._json(200, {"actors": ACTORS})
        elif self.path == "/data":
            self._json(200, _snapshot())
        elif self.path == "/download":
            data = json.dumps(_snapshot(), indent=2).encode("utf-8")
            self._respond(200, data, "application/json", "aetherbridge-data.json")
        elif self.path == "/":
            self._respond(200, _DASHBOARD.encode("utf-8"), "text/html; charset=utf-8")
        else:
            self.send_error(404)

    def do_POST(self) -> None:
        """Store a complete package of actor poses."""
        global PACKAGE_COUNT
        if self.path != "/pose":
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 10_000_000:
                raise ValueError("Invalid content length")
            data = json.loads(self.rfile.read(length))
            if not isinstance(data, dict) or data.get("Type") != "poses":
                raise ValueError("Expected a poses package")
            poses = data.get("Poses")
            if not isinstance(poses, list) or not poses:
                raise ValueError("Expected a non-empty Poses array")
            actors = set()
            for pose in poses:
                if not isinstance(pose, dict) or pose.get("Type") != "pose":
                    raise ValueError("Expected a pose payload")
                actor = pose.get("ActorId")
                if not isinstance(actor, str) or actor not in ACTORS:
                    raise ValueError("Unknown actor ID")
                if actor in actors:
                    raise ValueError("Duplicate actor ID")
                actors.add(actor)
                if not isinstance(pose.get("Bones"), dict) or not pose["Bones"]:
                    raise ValueError("Expected a non-empty Bones object")
        except (ValueError, UnicodeDecodeError) as error:
            self._json(400, {"error": str(error)})
            return
        with LOCK:
            now = time.monotonic()
            timestamp = time.time()
            while RECENT_PACKAGES and RECENT_PACKAGES[0] <= now - FPS_WINDOW_SECONDS:
                RECENT_PACKAGES.popleft()
            RECENT_PACKAGES.append(now)
            PACKAGE_COUNT += 1
            POSES.clear()
            for pose in poses:
                actor = pose["ActorId"]
                recent = RECENT_FRAMES.setdefault(actor, deque())
                while recent and recent[0] <= now - FPS_WINDOW_SECONDS:
                    recent.popleft()
                recent.append(now)
                POSES[actor] = pose
                FRAME_COUNTS[actor] = FRAME_COUNTS.get(actor, 0) + 1
                LAST_RECEIVED[actor] = timestamp
        self._json(200, {"status": "ok"})

    def log_message(self, format: str, *args: object) -> None:
        """Keep the live stream from flooding the console."""


def run(port: int = 8080) -> None:
    """Run the local receiver until interrupted."""
    server = ThreadingHTTPServer(("127.0.0.1", port), BridgeReceiverHandler)
    print(f"AetherBridge mock: http://127.0.0.1:{port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    run()
