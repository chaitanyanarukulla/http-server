# -*- coding: utf-8 -*-
"""Create a client socket to send messages to the server."""
import socket
import sys


def client(message):  # pragma no cover
    """Open a client to send messages."""
    client = socket.socket(*socket.getaddrinfo("127.0.0.1", 5000)[0][:3])
    client.connect(("127.0.0.1", 5000))
    msg_header = ("GET /http-server/src/server.py"
                  " HTTP/1.1 200\r\nHost: 127.0.0.1:5000\r\n")
    message = msg_header + message + "@@"
    if sys.version_info.major == 3:
        client.sendall(message.encode("utf-8"))
    else:
        client.sendall(message)
    msg = b''
    timer = True
    while timer:
        part = client.recv(17)
        msg += part
        if msg.endswith(b'200 OK\r\n'):
            timer = False
        elif msg.endswith(b'500 OK\r\n'):
            timer = False
    print(msg)
    client.close()
    if sys.version_info.major == 3:
        return msg.decode("utf-8").replace("@@", "")
    else:
        return msg.decode("utf-8").replace("@@", "")


if __name__ == "__main__":
    msg = sys.argv[1]
