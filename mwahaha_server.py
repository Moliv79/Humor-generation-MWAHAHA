"""
MWAHAHA offline server
-----------------------
Runs the joke generation fully on your machine via Ollama, so the
MWAHAHA webpage works with no internet connection.

Setup (one time):
    1. Install Ollama: https://ollama.com
    2. Pull the model used by humor_engine.py:
           ollama pull qwen2.5:3b
    3. Install the Python client:
           pip install ollama

Run:
    python mwahaha_server.py

Then just open mwahaha.html in your browser (double-click it, or
File > Open). The page will automatically detect this server and
use it instead of the internet.

Keep this terminal window open while you use the site. Stop it
with Ctrl+C.
"""

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import humor_engine

HOST = "127.0.0.1"
PORT = 8765


class Handler(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self._cors()
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"status": "ok", "model": humor_engine.MODEL}).encode("utf-8"))

    def do_POST(self):
        if self.path != "/joke":
            self.send_response(404)
            self._cors()
            self.end_headers()
            return

        length = int(self.headers.get("Content-Length", 0))
        try:
            body = json.loads(self.rfile.read(length) or b"{}")
            prompt = body["prompt"]
            language = body.get("language", "English")

            joke = humor_engine.generate_best_joke(prompt, language)

            self.send_response(200)
            self._cors()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"joke": joke}).encode("utf-8"))
        except Exception as exc:  # noqa: BLE001 - report any failure to the page
            self.send_response(500)
            self._cors()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(exc)}).encode("utf-8"))

    def log_message(self, format, *args):  # quieter console output
        pass


if __name__ == "__main__":
    print(f"MWAHAHA offline server running at http://{HOST}:{PORT}")
    print("Make sure Ollama is running and qwen2.5:3b is pulled.")
    print("Open mwahaha.html in your browser now. Press Ctrl+C to stop.")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
