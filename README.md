# HTTP Server

### This branch checks message from the client and checks that its a valid http GET request

-  The server function will take a single argument which is the request from the client.
- The server function will  only accept GET requests.
-  Any other request method will raise an appropriate Python exception.
-  The server function will only accept HTTP/1.1 requests.
-  A request of any other HTTP version will raise an appropriate Python exception.
-  The server function will validate that a proper Host header was included in the request and if not, raise an appropriate Python exception.
-  The server function will validate that the request is well-formed. If the request is malformed in some way, it will raise an appropriate Python exception.
-  If none of the conditions above arise, the server function will return the URI from the request.
