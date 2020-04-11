#!/usr/bin/env python
import http.client as httplib
import re
import socket
import os

host = "localhost"
port = 8080
DOCUMENT_ROOT = 'root'
default_file = 'index.html'

conn = httplib.HTTPConnection(host, port, timeout=30)


def test_empty_request():
    """ Send bad http headers """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.sendall(b"\n")
    s.close()


def test_server_header():
    """Server header exists"""
    conn.request("GET", "/httptest/")
    r = conn.getresponse()
    data = r.read()
    server = r.getheader("Server")
    print(data)
    print(server)
    print(r.getheaders())


if __name__ == "__main__":
    test_server_header()
    # import time
    # html = b'Hello'
    # content_type = 'text/html'
    # content_length = len('Hello')
    # h = f'HTTP/1.1 200 OK\r\n'
    # current_date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
    # h += 'Date: ' + current_date + '\r\n'
    # h += 'Server: Simple-Python-HTTP-Server\r\n'
    # h += 'Connection: close\r\n'  # signal that the conection will be closed after compliting the request
    # h += f'Content-Length: {content_length}\r\n'
    # h += f'Content-Type: {content_type}\n\n'
    # print(h.encode() + html)

    # request = b'GET /httptest/ HTTP/1.1\r\nHost: localhost:8080\r\nAccept-Encoding: identity\r\n\r\n'
    # head = request.decode().split('\r\n')[0]
    # method, path, _ = head.split()
    # file_path = os.path.join(DOCUMENT_ROOT, path.replace('/', ''), 'index.html')
    # with open(file_path, 'rb') as f:
    #     html = f.read().decode()
    # content_len = len(html)
    # response = b'HTTP/1.1 200 OK\r\nDate: Tue, 07 Apr 2020 01:06:51\r\nServer: Simple-Python-HTTP-Server\r\nConnection: close\r\n'
    # response += f'Content-Length: {content_len}\r\nContent-Type: text/html\n\n{html}'.encode()
    # print(response)

    # f = open(os.path.abspath(file_path))
