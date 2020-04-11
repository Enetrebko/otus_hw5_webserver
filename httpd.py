from socket import *
import threading
import os

host = "localhost"
port = 8080
queue_size = 1
DOCUMENT_ROOT = 'root'
default_file = 'index.html'

server = socket(AF_INET, SOCK_STREAM)
server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server.bind((host, port))
server.listen(queue_size)


def handle_client_connection(client_socket):
    request = b""
    while b'\r\n\r\n' not in request:
        request += client_socket.recv(65536)
    print('Received {}'.format(request))
    head = request.decode().split('\r\n')[0]
    method, path, _ = head.split()
    # GET handler
    if method == 'GET':
        # path = os.path.join(DOCUMENT_ROOT, path.replace('/', ''))
        # file_path = os.path.join(path, default_file) if os.path.isdir(path) else path
        file_path = os.path.join(DOCUMENT_ROOT, path.replace('/', ''), 'index.html')
        with open(file_path, 'rb') as f:
            html = f.read().decode()
    elif method == 'HEAD':
        pass
    elif method == 'POST':
        raise ValueError('POST not allowed')

    response = b'HTTP/1.1 200 OK\r\nDate: Tue, 07 Apr 2020 01:06:51\r\nServer: Simple-Python-HTTP-Server\r\nConnection: close\r\nContent-Length: 116\r\nContent-Type: text/html\n\n<!doctype html>\n<html>\n  <head>\n    <title>Main Page</title>\n  </head>\n  <body>\n    <p>Example</p>\n  </body>\n</html>'
    # response = b'HTTP/1.1 200 OK\r\nDate: Tue, 07 Apr 2020 01:06:51\r\nServer: Simple-Python-HTTP-Server\r\nConnection: close\r\nContent-Length: 5\r\nContent-Type: text/html\n\nHello'
    client_socket.sendall(response)
    print('resp sent')
    client_socket.close()


while True:
    client_sock, address = server.accept()
    print('Accepted connection from {}:{}'.format(address[0], address[1]))
    client_handler = threading.Thread(
        target=handle_client_connection,
        args=(client_sock,)
    )
    client_handler.start()



