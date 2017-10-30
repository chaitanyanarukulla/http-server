# -*- coding: utf-8 -*-
"""Open a server and listen for messages from the client."""
import os
# import socket
import sys

from mimetypes import MimeTypes

from gevent.monkey import patch_all

from gevent.server import StreamServer


def response_ok(body, mimetype):
    print("IN RESPONSSE FUNCTION")
    print(mimetype)
    """Return a successfull http 200 response."""
    # byte_URI = str(URI).encode('UTF8')
    message = "HTTP/1.1 200 OK\r\n" \
              "Content-Type: {}\r" \
              "\r" \
              "{}" \
              "\r\n*@*@*@".format(mimetype[0], body)
    print("THE MESSAGE!!!!", message)
    print(type(message))
    message = message.encode('UTF8')
    print("\n\n")
    print("THE MESSAGE UNICODE", message)
    return message


def response_error(err):
    """Return http 500 response error."""
    return err + b' HTTP/1.1 500 OK\r\n'


def resolve_uri(URI):
    the_path = os.path.abspath(URI)
    if os.path.isdir(the_path):
        print("THE DIR IF OCCURED")
        return html_listing(os.listdir(the_path), the_path, URI)
    elif os.path.isfile(the_path):
        print("THE FILE  IF OCCURED")
        return get_file_contents(the_path)

    else:
        pass


def get_file_contents(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
        print("CONTENT", content)
        print(type(content))
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
    print("\n\n\nURIURI", uri)
    """Parse request to make sure it is a GET request."""
    if "GET" not in str(request):
        raise ValueError("405 error: only GET method accepted")
    elif "HTTP/1.1" not in str(request):
        raise ValueError("505 error: HTTP Request is not version 1.1.")
    elif "Host: 127.0.0.1:5000" not in str(request):
        raise ValueError("400 error: Bad Request")
    elif "GET {} HTTP/1.1 200".format(str(uri)) not in str(request):
        print("UNCLE BOB")
        print("GET {} HTTP/1.1 200".format(str(uri)))
        print(str(request))
        raise ValueError("400: Malformed-Request")
    else:
        return resolve_uri(uri)


# def server():  # pragma no cover
#     """Open a server to echo back a message."""
#     server = socket.socket(socket.AF_INET,
#                            socket.SOCK_STREAM, socket.IPPROTO_TCP)
#     server.bind(('127.0.0.1', 5001))
#     server.listen(1)
#     try:
#         while True:
#             conn, addr = server.accept()
#             msg = b''
#             timer = True
#             while timer:
#                 part = conn.recv(8)
#                 msg += part
#                 if b"*@*@*@" in msg:
#                     timer = False
#             try:
#                 heeader_and_body = parse_request(msg)
#                 conn.sendall(heeader_and_body)
#             except ValueError as err:
#                 byte_err = str(err).encode('UTF8')
#                 conn.sendall(response_error(byte_err))
#             conn.close()
#     except KeyboardInterrupt:
#         conn.close()
#         server.close()
#         print("\nClosing the server!")
#         sys.exit(1)


def server():  # pragma no cover
    """Open a server to echo back a message."""
    try:
        patch_all()
        server = StreamServer(('127.0.0.1', 5000), echo)
        print('Starting echo server on port 5000')
        server.serve_forever()
    except KeyboardInterrupt:
        server.close()
        print("\nClosing the server!")
        sys.exit(1)


def echo(socket, addr):
    while True:
        msg = b''
        timer = True
        while timer:
            data = socket.recv(8)
            msg += data
            if b"*@*@*@" in data:
                timer = False
        try:
            heeader_and_body = parse_request(msg)
            socket.sendall(heeader_and_body)
        except ValueError as err:
                byte_err = str(err).encode('UTF8')
                socket.sendall(response_error(byte_err))
                socket.close()

if __name__ == "__main__":  # pragma no cover
    server()
