import socket
import threading
import os
from urllib.parse import unquote
from datetime import datetime
import argparse
import time
from http import HTTPStatus
import mimetypes


HOST = "0.0.0.0"
PORT = 8080
QUEUE_SIZE = 10
DOCUMENT_ROOT = 'root'
DEFAULT_FILE = 'index.html'
WORKERS_COUNT = 5
TIMEOUT = 60
REQUEST_MAX_SIZE = 10 * 1024


class HTTPServer:
    def __init__(self, host, port, workers_count, document_root):
        self.host = host
        self.port = port
        self.workers_count = workers_count
        self.document_root = document_root

    def get_request(self, client_socket):
        request = b""
        while not (b"\r\n\r\n" in request or b"\n\n" in request or len(request) > REQUEST_MAX_SIZE):
            chunk = client_socket.recv(1024)
            if not chunk:
                break
            request += chunk
        return request

    def handle_client_connection(self, client_sock):
        with client_sock:
            request = HTTPRequest(self.get_request(client_sock))
            response = HTTPResponse(request)
            client_sock.sendall(response.generate_response())

    def wait_connection(self, sock):
        while True:
            client_sock, address = sock.accept()
            client_sock.settimeout(TIMEOUT)
            self.handle_client_connection(client_sock)

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((self.host, self.port))
            sock.listen(QUEUE_SIZE)
            for _ in range(self.workers_count):
                client_handler = threading.Thread(
                    target=self.wait_connection,
                    args=(sock,)
                )
                client_handler.setDaemon(True)
                client_handler.start()
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    print("Interrupted by user")
                    return


class HTTPRequest:
    def __init__(self, request):
        self.request = request
        self.request_url, self.file_ext, self.status, self.method = self.parse_request()

    def parse_request(self):
        request_url = file_ext = method = None
        status = HTTPStatus.OK
        try:
            data = self.request.decode().split('\r\n')[0]
            method = data.split()[0]
            url = data.split()[1]
            request_url, file_ext = self.parse_url(url)
            if not request_url:
                status = HTTPStatus.NOT_FOUND
        except:
            status = HTTPStatus.BAD_REQUEST
        finally:
            return request_url, file_ext, status, method

    def parse_url(self, url):
        url_norm = url.split("?")[0]
        url_norm = unquote(url_norm)
        url_norm = os.path.abspath(url_norm)
        url_norm = os.path.join(DOCUMENT_ROOT, url_norm.lstrip("/"))
        if url.endswith("/"):
            url_norm += "/"
        file_ext = os.path.splitext(url_norm)[-1]
        if os.path.isdir(url_norm):
            url_norm = os.path.join(url_norm, DEFAULT_FILE)
        if os.path.isfile(url_norm):
            return url_norm, file_ext
        return None, None


class HTTPResponse:
    def __init__(self, request):
        self.request = request
        self.status = self.get_status()
        self.message = self.get_message()

    def get_status(self):
        if self.request.method == "POST":
            return HTTPStatus.METHOD_NOT_ALLOWED
        else:
            return self.request.status

    def get_message(self):
        return self.status.phrase

    def get_body(self):
        with open(self.request.request_url, 'rb') as f:
            return f.read()

    def generate_response(self):
        head = "HTTP/1.1"
        content_type = mimetypes.types_map.get(self.request.file_ext, "text/html")
        date_time = datetime.now().strftime("%a, %d %b %Y %H:%M:%S")
        server_name = "MyServer"
        response = "\r\n".join([
            f"{head} {self.status} {self.message}",
            f"Date: {date_time}",
            f"Server:{server_name}",
            "Connection: close",
            ""]
        )
        if self.status != HTTPStatus.OK:
            return response.encode()
        body = self.get_body()
        content_length = len(body)
        response += "\r\n".join([
            f"Content-Length: {content_length}",
            f"Content-Type: {content_type}"
        ])
        response += "\r\n\r\n"
        response = response.encode()
        if self.request.method == 'GET':
            response += body
        return response


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--workers_count", type=int, default=WORKERS_COUNT)
    parser.add_argument("-r", "--document_root", default=DOCUMENT_ROOT)
    args = parser.parse_args()
    server = HTTPServer(HOST, PORT, args.workers_count, args.document_root)
    server.start()
