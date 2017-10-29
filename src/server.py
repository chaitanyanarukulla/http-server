# -*- coding: utf-8 -*-
"""Open a server and listen for messages from the client."""
import socket
import sys


def response_ok(uri):
    """Return a successfull http 200 response."""
    byte_uri = str(uri).encode('UTF8')
    print("BYTE uri")
    print(byte_uri)
    return byte_uri + b" " + b'HTTP/1.1 200 OK\r\n'


def response_error(err):
    """Return http 500 response error."""
    return err + b' HTTP/1.1 500 OK\r\n'


def parse_request(request):
    """Parse request to make sure it is a GET request."""
    if "GET" not in str(request):
        raise ValueError("405 error: only GET method accepted")
    elif "HTTP/1.1" not in str(request):
        raise ValueError("505 error: HTTP Request is not version 1.1.")
    elif "Host: 127.0.0.1:5000" not in str(request):
        raise ValueError("400 error: Bad Request")
    elif "GET /http-server/src/server.py HTTP/1.1 200" not in str(request):
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
                uri = parse_request(msg)
                conn.sendall(response_ok(uri))
            except ValueError as err:
                byte_err = str(err).encode('UTF8')
                conn.sendall(response_error(byte_err))
            conn.close()
    except KeyboardInterrupt:
        conn.close()
        server.close()
        print("\nClosing the server!")
        sys.exit(1)


if __name__ == "__main__":  # pragma no cover
    server()
