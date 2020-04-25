import socket
import threading
import os
from urllib.parse import unquote
from collections import namedtuple
from datetime import datetime
import argparse


HOST = "0.0.0.0"
PORT = 8080
QUEUE_SIZE = 5
DOCUMENT_ROOT = 'root'
DEFAULT_FILE = 'index.html'

CONTENT_TYPES = {
    "html": "text/html",
    "png": "image/png",
    "css": "text/css",
    "txt": "text/html",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "swf": "application/x-shockwave-flash",
    "js": "application/javascript",
    "gif": "image/gif",
}

STATUS_MESSAGE = {
    200: "OK",
    403: "Forbidden",
    404: "Not Found",
    405: "Not Allowed"
}


class HTTPServer:
    def __init__(self, host, port, workers_count, document_root):
        self.host = host
        self.port = port
        self.workers_count = workers_count
        self.document_root = document_root
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def get_request(self, client_socket):
        request = b""
        while not (b"\r\n\r\n" in request or b"\n\n" in request):
            request += client_socket.recv(65536)
        return request

    def handle_client_connection(self, client_sock):
        request = HTTPRequest(self.get_request(client_sock))
        response = HTTPResponse(request)
        client_sock.sendall(response.generate_response())
        client_sock.close()

    def start(self):
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(QUEUE_SIZE)
        for _ in range(self.workers_count):
            while True:
                client_sock, address = self.server.accept()
                client_sock.settimeout(60)
                client_handler = threading.Thread(
                    target=self.handle_client_connection,
                    args=(client_sock,)
                )
                client_handler.setDaemon(True)
                client_handler.start()


class HTTPRequest:
    def __init__(self, request):
        self.request = request
        self.data = self.get_data()
        self.method = self.get_method()
        self.url_info = self.parse_url()
        self.request_url = self.url_info.url
        self.file_ext = self.url_info.file_ext
        self.file_status = self.url_info.file_status

    def get_data(self):
        return self.request.decode().split('\r\n')[0]

    def get_method(self):
        return self.data.split()[0]

    def get_url(self):
        return self.data.split()[1]

    def parse_url(self):
        url = self.get_url()
        url_info = namedtuple("url_info", "url file_ext file_status")
        if "?" in url:
            url = url[:url.find("?")]
        url = unquote(url)
        url = os.path.join(DOCUMENT_ROOT, url.replace("/", "", 1))
        file_ext = url.split(".")[-1]
        if url.find("../../") > 0:
            return url_info(url, file_ext, "root escaping")
        if os.path.isdir(url):
            url = os.path.join(url, DEFAULT_FILE)
        if os.path.isfile(url):
            return url_info(url, file_ext, "ok")
        return url_info(url, file_ext, "not found")


class HTTPResponse:
    def __init__(self, request: HTTPRequest):
        self.request = request
        self.status = self.get_status()
        self.message = self.get_message()

    def get_status(self):
        if self.request.method == "POST":
            return 405
        if self.request.file_status == "not found":
            return 404
        if self.request.file_status == "root escaping":
            return 403
        else:
            return 200

    def get_message(self):
        return STATUS_MESSAGE.get(self.status)

    def get_body(self):
        with open(self.request.request_url, 'rb') as f:
            return f.read()

    def generate_response(self):
        head = "HTTP/1.1"
        content_type = CONTENT_TYPES.get(self.request.file_ext, "text/html")
        date_time = datetime.now().strftime("%a, %d %b %Y %H:%M:%S")
        server_name = "MyServer"
        response = (
                f"{head} {self.status} {self.message}\r\n" +
                f"Date: {date_time}\r\n" +
                f"Server:{server_name}\r\n" +
                "Connection: close\r\n"
        ).encode()
        if self.status == 200:
            body = self.get_body()
            content_length = len(body)
            response += (
                    f"Content-Length: {content_length}\r\n" +
                    f"Content-Type: {content_type}\r\n\r\n"
            ).encode()
            if self.request.method == 'GET':
                response += body
        return response


if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument("-w", "--workers_count", default=10)
    # parser.add_argument("-r", "--root", default=DOCUMENT_ROOT)
    # args = parser.parse_args()
    # server = HTTPServer(HOST, PORT, args.workers_count, args.document_root)
    server = HTTPServer(HOST, PORT, 5, DOCUMENT_ROOT)
    server.start()
