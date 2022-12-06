import socket
import ssl
import base64
from socket import *
#mailserver = 'smtp.mail.ru'
sock = socket(AF_INET, SOCK_STREAM)

sock.bind(('127.0.0.1',7777))
sock.listen (1)
conn, addr = sock.accept()
print ("connected: ", addr)

print ("Wait data...")
data = conn.recv(1024)
print (data)

conn.close()
sock.close()

username = 'ilya_petrovskij_2019'.encode()
username = base64.b64encode(username)

password = 'zxcvbnm098765'.encode()
password = base64.b64encode(password)


mailserver = 'pop.mail.ru'
cSock = socket(AF_INET, SOCK_STREAM)

cSock.connect((mailserver, 995))
cSockSSL = ssl.wrap_socket(cSock)
recv = cSockSSL.recv(1024)
print(recv)

cSockSSL.send("USER ilya_petrovskij_2019\r\n".encode('utf-8'))
recv = cSockSSL.recv(1024)
print(recv)

cSockSSL.send("PASS zxcvbnm098765\r\n".encode('utf-8'))
recv = cSockSSL.recv(1024)
print(recv)

cSockSSL.send("STAT\r\n".encode('utf-8'))
recv = cSockSSL.recv(1024)
print(recv)

cSockSSL.send("RETR ".encode()+ data +"\r\n".encode('utf-8'))
recv = cSockSSL.recv(1024)
while bytes.decode(recv, encoding='utf-8')[-3:] != '.\r\n':
        recv = cSockSSL.recv(1024)
        print(recv)

cSockSSL.send("STAT\r\n".encode('utf-8'))
recv = cSockSSL.recv(1024)
print(recv)

cSockSSL.send("QUIT\r\n".encode('utf-8'))
recv = cSockSSL.recv(1024)
print(recv)


cSockSSL.close()
cSock.close()
#input()
