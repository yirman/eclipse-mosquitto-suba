import os
import socket
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

TARGET_HOST = os.getenv('TARGET_HOST', 'localhost')
TARGET_PORT = int(os.getenv('TARGET_PORT', '1883'))
LISTEN_PORT = int(os.getenv('PORT', '8080'))
TIMEOUT = float(os.getenv('TIMEOUT', '2'))

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Log client address for debugging health probes
        try:
            client = self.client_address[0]
        except Exception:
            client = 'unknown'
        print(f"Health request from {client} to path {self.path}")

        if self.path != '/health':
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not found')
            return

        healthy, err = check()
        if healthy:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            payload = {'status': 'ok', 'target': f'{TARGET_HOST}:{TARGET_PORT}'}
            self.wfile.write(json.dumps(payload).encode())
        else:
            self.send_response(503)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            payload = {'status': 'unhealthy', 'error': str(err)}
            self.wfile.write(json.dumps(payload).encode())

    def log_message(self, format, *args):
        return


def check():
    try:
        s = socket.create_connection((TARGET_HOST, TARGET_PORT), timeout=TIMEOUT)
        s.close()
        return True, None
    except Exception as e:
        return False, e


if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', LISTEN_PORT), Handler)
    print(f'Health server listening on 0.0.0.0:{LISTEN_PORT}, checking {TARGET_HOST}:{TARGET_PORT}')
    server.serve_forever()
