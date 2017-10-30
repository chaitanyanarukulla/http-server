# -*- coding: utf-8 -*-
"""Create a client socket to send messages to the server."""
import socket
import sys


def client(message):
    """Open a client to send messages."""
    print("MESSAGE JUST INSIDE CLIENT", message)
    client = socket.socket(*socket.getaddrinfo("127.0.0.1", 5000)[1][:3])
    client.connect(("127.0.0.1", 5000))
    msg_header = "GET {} HTTP/1.1 200\r\nHost: 127.0.0.1:5000\r\n".format(message)
    message = msg_header + message + "*@*@*@"
    if sys.version_info.major == 3:
        client.sendall(message.encode("utf-8"))
    else:
        client.sendall(message)
    msg = b''
    timer = True
    while timer:
        part = client.recv(17)
        msg += part
        if msg.endswith(b'*@*@*@'):
            print("ENDSWITH *@*@*@")
            timer = False
        elif msg.endswith(b'500 OK\r\n'):
            print("ENDSWITH 500 OK")
            timer = False
    print(msg)
    client.close()
    if sys.version_info.major == 3:
        return msg.decode("utf-8").replace("*@*@*@", "")
    else:
        return msg.decode("utf-8").replace("*@*@*@", "")


if __name__ == "__main__":
    msg = sys.argv[1]
