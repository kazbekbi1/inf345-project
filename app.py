"""A tiny notes API using only the Python standard library."""
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

NOTES = []


class Handler(BaseHTTPRequestHandler):
    def _send(self, status, data):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/healthz":
            self._send(200, {"status": "ok"})
        elif self.path == "/notes":
            self._send(200, NOTES)
        elif self.path == "/":
            self._send(200, {"service": "notes-api", "endpoints": ["/healthz", "/notes"]})
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/notes":
            self._send(404, {"error": "not found"})
            return
        length = int(self.headers.get("Content-Length", 0))
        try:
            data = json.loads(self.rfile.read(length) or b"{}")
        except ValueError:
            self._send(400, {"error": "invalid json"})
            return
        text = data.get("text") if isinstance(data, dict) else None
        if not text:
            self._send(400, {"error": "text is required"})
            return
        note = {"id": len(NOTES) + 1, "text": text}
        NOTES.append(note)
        self._send(201, note)

    def log_message(self, *args):
        pass


def make_server(port):
    return HTTPServer(("0.0.0.0", port), Handler)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    print(f"Listening on port {port}", flush=True)
    make_server(port).serve_forever()
