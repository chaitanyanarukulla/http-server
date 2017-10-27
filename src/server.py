# -*- coding: utf-8 -*-
"""Open a server and listen for messages from the client."""
import socket
import sys


def response_ok():
    """Return a successfull http 200 response."""
    return b'HTTP/1.1 200 OK\r\n'


def response_error(erro):
    """Return http 500 response error."""
    return b'erro' + b' HTTP/1.1 500 OK\r\n'


def parse_request(request):
    """Parse request to make sure it is a GET request."""
    print(request)
    if b"GET" not in request:
        raise ValueError("Server Only accepting GET requests.")
    elif b"HTTP/1.1" not in request:
        raise ValueError("HTTP Request is not version 1.1.")
    elif b"HOST: 127.0.0.1:5000" not in request:
        raise ValueError("Bad Request: No Host ")
    elif b"GET /http-server/src/server.py HTTP/1.1\r\n" not in request:
        raise ValueError("Malformed-Request")
    else:
        return request.split(" ")[1]


def server():  # pragma no cover
    """Open a server to echo back a message."""
    server = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM, socket.IPPROTO_TCP)
    server.bind(('127.0.0.1', 5011))
    server.listen(1)
    try:
        while True:
            conn, addr = server.accept()
            msg = b''
            timer = True
            while timer:
                part = conn.recv(8)
                msg += part
                if b"@@" in msg:
                    timer = False
            try:
                parse_request(msg)
                conn.sendall(response_ok())
            except ValueError as err:
                print(err)
                erro = err
                conn.sendall(response_error(erro))
            conn.close()
    except KeyboardInterrupt:
        conn.close()
        server.close()
        print("\nClosing the server!")
        sys.exit(1)

if __name__ == "__main__":
    server()
