# -*- coding: utf-8 -*-
"""Open a server and listen for messages from the client."""
# import socket
import sys

from gevent.monkey import patch_all

from gevent.server import StreamServer

from server import response_error, parse_request


def server():  # pragma no cover
    """Open a server to echo back a message."""
    print("ENTERED SERVER")
    try:
        patch_all()
        server = StreamServer(('127.0.0.1', 5000), echo)
        print('Starting echo server on port 5000')
        server.serve_forever()
    except KeyboardInterrupt:
        server.close()
        print("\nClosing the server!")
        sys.exit(1)


def echo(socket, addr):  # pragma no cover
    """Concurrency echo chamber."""
    while True:
        msg = b''
        timer = True

        while timer:
            data = socket.recv(16)
            msg += data
            if b"*@*@*@" in msg:
                timer = False

        try:
            header_and_body = parse_request(msg)
            socket.sendall(header_and_body)
        except ValueError as err:
                byte_err = str(err).encode('UTF8')
                socket.sendall(response_error(byte_err))
                socket.close()

if __name__ == "__main__":  # pragma no cover
    server()
