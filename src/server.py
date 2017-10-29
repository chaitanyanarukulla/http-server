# -*- coding: utf-8 -*-
"""Open a server and listen for messages from the client."""
import os
import socket
import sys
from mimetypes import MimeTypes


def response_ok(URI):
    """Return a successfull http 200 response."""
    byte_URI = str(URI).encode('UTF8')
    return byte_URI + b" " + b'HTTP/1.1 200 OK\r\n'


def response_error(err):
    """Return http 500 response error."""
    return err + b' HTTP/1.1 500 OK\r\n'


def resolve_uri(URI):
    uri_path = os.path.abspath(URI)
    print(uri_path, "This is uri_path")
    print(type(os.path.isdir(uri_path)))
    if os.path.isdir(str(uri_path)):
        return html_listing(os.listdir(uri_path), uri_path, URI)
    else:
        pass


def html_listing(dir_list, uri_path, URI):
    body = """{} Listing:

    <ul>
      <li>{}</li>
      <li>{}</li>
      <li>{}</li>
      <li>{}</li>
    </ul>
    """.format(URI, *dir_list)
    mime = MimeTypes()
    mime_type = mime.guess_type(uri_path)
    print('This is what we need')
    print(body)
    print(mime_type)
    return body, mime_type


def parse_request(request):
    """Parse request to make sure it is a GET request."""
    if "GET" not in str(request):
        raise ValueError("405 error: only GET method accepted")
    elif "HTTP/1.1" not in str(request):
        raise ValueError("505 error: HTTP Request is not version 1.1.")
    elif "Host: 127.0.0.1:5000" not in str(request):
        raise ValueError("400 error: Bad Request")
    elif "GET test_dir HTTP/1.1 200" not in str(request):
        raise ValueError("400: Malformed-Request")
    else:
        return resolve_uri(str(request).split(" ")[1])


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


if __name__ == "__main__":  # pragma no cover
    server()
