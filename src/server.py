# -*- coding: utf-8 -*-
"""Open a server and listen for messages from the client."""
import socket
import sys


def server():  # pragma: no cover
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
                if b"@@@" in msg:
                    timer = False
            conn.sendall(msg)
            conn.close()
    except KeyboardInterrupt:
        conn.close()
        server.close()
        print("\nClosing the server!")
        sys.exit()

if __name__ is "__main__":
    server()
