import http.server
import socketserver
import hashlib
import os
import time
from email.utils import formatdate

PORT = 8080
FILE_NAME = "index.html"

class CachingHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == f"/{FILE_NAME}":
            self.serve_index()
        else:
            super().do_GET()

    def serve_index(self):
        try:
            with open(FILE_NAME, "rb") as f:
                content = f.read()

            etag = hashlib.md5(content).hexdigest()

            last_modified = formatdate(
                timeval=os.path.getmtime(FILE_NAME), usegmt=True
            )

            client_etag = self.headers.get("If-None-Match")
            client_modified = self.headers.get("If-Modified-Since")

            if client_etag == etag or (
                client_modified and
                time.mktime(time.strptime(client_modified, "%a, %d %b %Y %H:%M:%S %Z"))
                >= os.path.getmtime(FILE_NAME)
            ):
                self.send_response(304)
                self.end_headers()
                return

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("ETag", etag)
            self.send_header("Last-Modified", last_modified)
            self.end_headers()
            self.wfile.write(content)

        except FileNotFoundError:
            self.send_error(404, "File not found")

with socketserver.TCPServer(("", PORT), CachingHTTPRequestHandler) as httpd:
    print(f"Serving on port {PORT}...")
    httpd.serve_forever()
