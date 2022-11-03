from socket import *
from http_parser.http import HttpStream
from http_parser.reader import SocketReader
from html.parser import HTMLParser

http_server = 'example.org'
cSock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
cSock.connect((http_server, 80))

cSock.send(b"GET /index.html HTTP/1.0\r\n")
cSock.send(b"HOST: example.org\r\n")
cSock.send(b"\r\n")

r = SocketReader(cSock)
p = HttpStream(r)
print(p.headers())
body = p.body_file().read()


class tHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Start tag:", tag)
        for attr in attrs:
            print("     attr:", attr)

parser = tHTMLParser()
parser.feed(body.decode('utf8'))



# #!/usr/bin/env python
# from socket import socket, AF_INET, SOCK_STREAM
#
# from http_parser.http import HttpStream
# from http_parser.reader import SocketReader
#
#
# def main():
#     client_socket = socket(AF_INET, SOCK_STREAM)
#     try:
#         client_socket.connect(('gunicorn.org', 80))
#         client_socket.send(b"GET / HTTP/1.1\r\nHost: gunicorn.org\r\n\r\n")
#         r = SocketReader(client_socket)
#         p = HttpStream(r)
#         print(p.headers())
#         print(p.body_file().read())
#     finally:
#         client_socket.close()
#
#
# if __name__ == "__main__":
#     main()