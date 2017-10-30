# -*- coding: utf-8 -*-
"""Open a server and listen for messages from the client."""
import os
import socket
import sys
from mimetypes import MimeTypes


def response_ok(body, mimetype):
    """Return a successfull http 200 response."""
    # byte_URI = str(URI).encode('UTF8')
    message = "HTTP/1.1 200 OK\r\n" \
              "Content-Type: {}\r" \
              "\r" \
              "{}" \
              "\r\n*@*@*@".format(mimetype[0], body)
    message = message.encode('UTF8')
    return message


def response_error(err):
    """Return http 500 response error."""
    return err + b' HTTP/1.1 500 OK\r\n'


def resolve_uri(URI):
    the_path = os.path.abspath(URI)
    if os.path.isdir(the_path):
        return html_listing(os.listdir(the_path), the_path, URI)
    elif os.path.isfile(the_path):
        return get_file_contents(the_path)
    else:
        pass


def get_file_contents(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    return response_ok(content, get_mime_types(file_path))


def html_listing(dir_list, uri_path, URI):
    body = """{} Listing:

    <ul>
      <li>{}</li>
      <li>{}</li>
      <li>{}</li>
      <li>{}</li>
      <li>{}</li>
    </ul>
    """.format(URI, *dir_list)
    return response_ok(body, ('test/html', None))


def get_mime_types(uri):
    mime = MimeTypes()
    mime_type = mime.guess_type(uri)
    return mime_type


def parse_request(request):
    # uri = str(request).split('\n')[-1].replace('*@*@*@', '')
    uri = str(request).split("\\r\\n")[-1].replace("*@*@*@'", '')
    """Parse request to make sure it is a GET request."""
    if "GET" not in str(request):
        raise ValueError("405 error: only GET method accepted")
    elif "HTTP/1.1" not in str(request):
        raise ValueError("505 error: HTTP Request is not version 1.1.")
    elif "Host: 127.0.0.1:5000" not in str(request):
        raise ValueError("400 error: Bad Request")
    elif "GET {} HTTP/1.1 200".format(str(uri)) not in str(request):
        raise ValueError("400: Malformed-Request")
    else:
        return resolve_uri(uri)


def server():  # pragma no cover
    """Open a server to echo back a message."""
    server = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM, socket.IPPROTO_TCP)
    server.bind(('127.0.0.1', 5001))
    server.listen(1)
    try:
        while True:
            conn, addr = server.accept()
            msg = b''
            timer = True
            while timer:
                part = conn.recv(8)
                msg += part
                if b"*@*@*@" in msg:
                    timer = False
            try:
                heeader_and_body = parse_request(msg)
                conn.sendall(heeader_and_body)
            except ValueError as err:
                byte_err = str(err).encode('UTF8')
                conn.sendall(response_error(byte_err))
            conn.close()
    except KeyboardInterrupt:
        conn.close()
        server.close()
        sys.exit(1)


if __name__ == "__main__":  # pragma no cover
    server()
