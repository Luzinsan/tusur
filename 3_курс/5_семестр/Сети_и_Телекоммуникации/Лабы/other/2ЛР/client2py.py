import socket


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 10000))



def main():
    data = client.recv(1024)
    print(data.decode("utf-8"))
    client.send('1'.encode("utf-8"))
    data = client.recv(1024)
    print(data.decode("utf-8"))
    client.send('2'.encode("utf-8"))


if __name__ == "__main__":
    main()
    input()
