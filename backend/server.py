"""Standard-library HTTP server for the local shopping assistant."""
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
from urllib.parse import urlparse

from backend.chat import respond
from backend.tools import createOrder

ROOT = Path(__file__).resolve().parent.parent
FRONTEND = ROOT / "frontend"


class ShoppingHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(FRONTEND), **kwargs)

    def _json(self, status: HTTPStatus, value: dict):
        payload = json.dumps(value).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_POST(self):
        try:
            size = int(self.headers.get("Content-Length", "0"))
            body = json.loads(self.rfile.read(size) or b"{}")
        except (ValueError, json.JSONDecodeError):
            self._json(HTTPStatus.BAD_REQUEST, {"error": "Please send a valid request."})
            return
        endpoint = urlparse(self.path).path
        if endpoint == "/api/chat":
            self._json(HTTPStatus.OK, respond(body.get("message", "")))
        elif endpoint == "/api/orders":
            order = createOrder(body.get("cartDetails", {}), body.get("customerInfo", {}))
            self._json(HTTPStatus.CREATED if order else HTTPStatus.BAD_REQUEST, order or {"error": "Please provide an item, your name, and email."})
        else:
            self._json(HTTPStatus.NOT_FOUND, {"error": "Not found."})


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", 3001), ShoppingHandler)
    print("Shopping assistant running at http://localhost:3001")
    server.serve_forever()
