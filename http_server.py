#! /usr/bin/python3.6
import http.server, os, socketserver, ssl

PORT = 443
DIR = '/home/joe/blocks_multiplayer/'

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        fs = [f for f in os.listdir() if f in self.path]
        f  = fs[0] if len(fs) else 'index.html'
        with open(f, 'rb') as fh:
            body = fh.read()
        ctype = 'text/html' if f == 'index.html' else 'text/plain'

        self.send_response(200)
        self.send_header('Content-Type', ctype)
        self.end_headers()
        self.wfile.write(body)
    def log_message(*args):
        return

os.chdir(DIR)
socketserver.TCPServer.allow_reuse_address = 1
with socketserver.TCPServer(('',PORT), Handler) as httpd:
    httpd.socket = ssl.wrap_socket(httpd.socket,
                                   certfile='/etc/letsencrypt/live/joe.iddon.com/fullchain.pem',
                                   keyfile ='/etc/letsencrypt/live/joe.iddon.com/privkey.pem',
                                   server_side=True)
    httpd.serve_forever()
