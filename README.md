# Socket Echo Server

 Created a function client which takes a message. When called, the client function will open a socket connection to the server. It will send the message passed as an argument to the server through the socket. It will accumulate any reply sent by the server into a string. Once the full reply is received, it will close the socket and return the message.