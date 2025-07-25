from http.server import HTTPServer, SimpleHTTPRequestHandler
import mimetypes
import os
import socket

mimetypes.add_type('application/x-mpegURL', '.m3u8')
mimetypes.add_type('video/MP2T', '.ts')

class HLSRequestHandler(SimpleHTTPRequestHandler):
    def guess_type(self, path):
        if path.endswith('.m3u8'):
            return 'application/x-mpegURL'
        elif path.endswith('.ts'):
            return 'video/MP2T'
        else:
            return super().guess_type(path)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

def get_local_ip():
    """
    Detects the local IP address of the current machine by creating a dummy
    connection to a public IP (does not send data) and reading the socket's own IP.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

if __name__ == '__main__':
    web_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(web_dir)

    local_ip = get_local_ip()
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, HLSRequestHandler)
    print(f"Serving at http://{local_ip}:8000")
    httpd.serve_forever()
