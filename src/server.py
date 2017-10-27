# -*- coding: utf-8 -*-
"""Open a server and listen for messages from the client."""
import socket
import sys
from requests import HTTPError


def response_ok(URI):
    """Return a successfull http 200 response."""
    byte_URI = str(URI).encode('UTF8')
    print("BYTE URI")
    print(byte_URI)
    return byte_URI + " " + b'HTTP/1.1 200 OK\r\n'


def response_error(err):
    """Return http 500 response error."""
    return err + b' HTTP/1.1 500 OK\r\n'


def parse_request(request):
    """Parse request to make sure it is a GET request."""
    print("THIS IS REQUEST")
    print(type(request))
    print(request)
    if b"GET" not in request:
        raise ValueError("405 error: only GET method accepted")
    elif b"HTTP/1.1" not in request:
        raise ValueError("505 error: HTTP Request is not version 1.1.")
    elif b"Host: 127.0.0.1:5000" not in request:
        raise ValueError("400 error: Bad Request")
    elif b"GET /http-server/src/server.py HTTP/1.1 200\r\n" not in request:
        raise ValueError("400: Malformed-Request")
    else:
        return str(request).split(" ")[1]


def server():  # pragma no cover
    """Open a server to echo back a message."""
    server = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM, socket.IPPROTO_TCP)
    server.bind(('127.0.0.1', 5000))
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
                URI = parse_request(msg)
                conn.sendall(response_ok(URI))
            except ValueError as err:
                byte_err = str(err).encode('UTF8')
                conn.sendall(response_error(byte_err))
            conn.close()
    except KeyboardInterrupt:
        conn.close()
        server.close()
        print("\nClosing the server!")
        sys.exit(1)

if __name__ == "__main__":
    server()
