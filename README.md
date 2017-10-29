# http-server

Implemented a function called response_ok that will return a well formed HTTP “200 OK” response. It will change the string to  byte string suitable for transmission through a socket. This method will accept no arguments and return a fully-formed proper response.
Implemented a function called response_error that will return a well formed HTTP “500 Internal Server Error” response.
Updated the server loop  so that it:
accumulates an incoming request into a variable
“logs” that request by printing it to stdout
returns a well-formed HTTP 200 response to the client.