# -*- coding: utf-8 -*-
"""Open a server and listen for messages from the client."""
import socket
import sys


def response_ok():
    """Return a successfull http 200 response."""
    return b'HTTP/1.1 200 OK\r\n'


def response_error():
    """Return http 500 response error."""
    return b'HTTP/1.1 500 OK\r\n'


def server():  # pragma no cover
    """Open a server to echo back a message."""
    server = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM, socket.IPPROTO_TCP)
    server.bind(('127.0.0.1', 5010))
    server.listen(1)
    try:
        while True:
            conn, addr = server.accept()
            msg = b''
            timer = True
            while timer:
                part = conn.recv(8)
                msg += part
                if b"@@@" in msg:
                    timer = False
            print(msg)
            conn.sendall(response_ok())
            conn.close()
    except KeyboardInterrupt:
        conn.sendall(response_error())
        conn.close()
        server.close()
        print("\nClosing the server!")
        sys.exit(1)

if __name__ == "__main__":
    server()
