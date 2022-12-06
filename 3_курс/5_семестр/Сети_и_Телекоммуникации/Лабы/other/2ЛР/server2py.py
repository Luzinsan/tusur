import socket
import ssl
import base64


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 10000))
server.listen(4)
print("----------------\nServer listening\n----------------")



def sendingLetter():
    mailserver = 'smtp.mail.ru'
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((mailserver, 465)),

    clientSSL = ssl.wrap_socket(client)
    recv = clientSSL.recv(1024)
    print('\n')
    print(recv)

    clientSSL.send('HELO host\r\n'.encode('utf-8'))
    recv = clientSSL.recv(1024)
    print(recv)

    clientSSL.send('AUTH LOGIN\r\n'.encode('utf-8'))
    recv = clientSSL.recv(1024)
    print(recv)

    user64 = base64.b64encode('fominmal@mail.ru'.encode('utf-8'))
    pass64 = base64.b64encode('TD0b53TykLwv2h0LGuWi'.encode('utf-8'))

    clientSSL.send(user64)
    clientSSL.send('\r\n'.encode('utf-8'))
    recv = clientSSL.recv(1024)
    print(recv)

    clientSSL.send(pass64)
    clientSSL.send('\r\n'.encode('utf-8'))
    recv = clientSSL.recv(1024)
    print(recv)

    clientSSL.send('MAIL FROM: fominmal@mail.ru\r\n'.encode('utf-8'))
    recv = clientSSL.recv(1024)
    print(recv)

    clientSSL.send('RCPT TO: fominmal@mail.ru\r\n'.encode('utf-8'))
    recv = clientSSL.recv(1024)
    print(recv)

    clientSSL.send('DATA \r\n'.encode('utf-8'))
    recv = clientSSL.recv(1024)
    print(recv)

    clientSSL.send('Subject: BEEPSIT\r\n'.encode('utf-8'))

    clientSSL.send('Message beep\r\n'.encode('utf-8'))

    clientSSL.send('.\r\n'.encode('utf-8'))
    recv = clientSSL.recv(1024)
    print(recv)


def deletingLetter():
    mailserver = 'pop.mail.ru'
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((mailserver, 995))

    clientSSL = ssl.wrap_socket(client)
    recv = clientSSL.recv(1024)
    print('\n')

    clientSSL.send('user fominmal@mail.ru\r\n'.encode('utf-8'))
    recv = clientSSL.recv(1024)
    print(recv)

    clientSSL.send('pass TD0b53TykLwv2h0LGuWi\r\n'.encode('utf-8'))
    recv = clientSSL.recv(1024)
    print(recv)

    clientSSL.send('LIST\r\n'.encode('utf-8'))
    recv = clientSSL.recv(1024)
    while bytes.decode(recv, encoding='utf-8')[-3:] != '.\r\n':
        recv = clientSSL.recv(1024)
        print(recv)

    clientSSL.send(f'DELE {str(int(recv[4]) - 48)}\r\n'.encode('utf-8'))
    recv = clientSSL.recv(1024)
    print(recv)

    clientSSL.send('QUIT\r\n'.encode('utf-8'))
    recv = clientSSL.recv(1024)
    print(recv)

def start():
    client_socket, address = server.accept()
    print(f"user < {address[0]} > connected")
    client_socket.send("You are connect\n".encode("utf-8"))
    sig = client_socket.recv(1024)
    print(sig.decode('utf-8'))
    if sig.decode('utf-8') == '1':
        sendingLetter()
        client_socket.send("OK\n".encode("utf-8"))
    else:
        deletingLetter()
    sig = client_socket.recv(1024)
    print(sig.decode('utf-8'))
    if sig.decode('utf-8') == '1':
        sendingLetter()
        client_socket.send("OK\n".encode("utf-8"))
    else:
        deletingLetter()
 


if __name__ == "__main__":
    start()
    input()
