"""Small dependency-free local server for the EFSAT prototype."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json
import urllib.parse

ROOT = Path(__file__).parent
WEB = ROOT / "web"
EVENTS = json.loads((ROOT / "data" / "demo_events.json").read_text(encoding="utf-8"))

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB), **kwargs)

    def _json(self, payload, status=200):
        raw = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/events":
            query = urllib.parse.parse_qs(parsed.query).get("q", [""])[0].lower()
            event_type = urllib.parse.parse_qs(parsed.query).get("type", [""])[0]
            filtered = [e for e in EVENTS if (not query or query in (e["label"] + e["description"] + e["location"]).lower()) and (not event_type or e["type"] == event_type)]
            return self._json({"events": filtered, "count": len(filtered)})
        if parsed.path == "/api/stats":
            return self._json({"indexedScenes": 1248, "events": len(EVENTS), "avgLatencyMs": 184, "packetReduction": 91.7})
        return super().do_GET()

    def do_POST(self):
        if self.path != "/api/ingest":
            return self._json({"error": "not found"}, 404)
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        return self._json({"accepted": True, "fileBytes": len(body), "jobId": "ING-" + str(len(body)), "message": "Scene queued for local quality masking and semantic indexing."}, 202)

if __name__ == "__main__":
    print("EFSAT running at http://localhost:8080")
    ThreadingHTTPServer(("127.0.0.1", 8080), Handler).serve_forever()
