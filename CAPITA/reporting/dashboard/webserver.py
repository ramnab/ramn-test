import json
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 8080


class TestServer(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        self._set_headers()

        self.send_response(200, 'Testing...')

    def do_POST(self):
        self._set_headers()
        data_string = self.rfile.read(int(self.headers['Content-Length']))

        self.send_response(200)
        self.end_headers()

        data = json.loads(data_string)
        print(data)


with HTTPServer(('', PORT), TestServer) as httpd:
    print("serving as port", PORT)
    httpd.serve_forever()
