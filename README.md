This is just a project from my networking class. I think it is pretty well commented so there should not be much trouble reading and understanding. Enjoy!

The program is writen in python so no compile commands. There will be a Makefile but all it will do is echo out usage instructions.

While running TCP(sending) follow the normal smpt protacal i.e. helo/mail from/rcpt to/data/quit
While running udp(receiving). After typing receiveing in the prompt follow it with a standard get request.
The get request must be in this format:
GET /db/<name>/HTTP/1.1
Host: <hostname>
Count: <number of emails to retrieve>
