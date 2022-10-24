from socket import *
import dearpygui
import re
import time

CMD_USER = b"USER demo\r\n"
CMD_PASS = b"PASS password\r\n"
CMD_PASV = b"PASV\r\n"
CMD_LIST = b"LIST\r\n"
CMD_QUIT = b"QUIT\r\n"
CMD_CWD = b"CDUP\r\n"
CMD_HELP = b"HELP\r\n"
CMD_RETR = b"RETR readme.txt\r\r"

def send_command(command: bytes):
    time.sleep(0.1)
    print("Client: ", command.decode("utf-8"), end='')
    socket_manager.send(command)
    while True:
        buffer = socket_manager.recv(1024).decode("utf-8")

        if buffer[:4] == "xyz-":
            print(buffer)
            buffer = socket_manager.recv(1024).decode("utf-8")
            print(buffer)
        else:
            match buffer[0]:
                case '2':
                    print("Server: Successful response: ", buffer, end='')
                case '4' | '5':
                    print("Server: Command cannot be executed: ", buffer, end='')
                case '1' | '3':
                    print("Server: Error or incomplete answer: ", buffer, end='')
            match buffer[1]:
                case '0':
                    print("Response type: Syntactic")
                case '1':
                    print("Response type: Informational. Corresponds to the informational message.")
                case '2':
                    print("Response type: Compound. The message refers to either a control connection or a data connection.")
                case '3':
                    print("Response type: Corresponds to messages about user authentication and rights.")
                case '4':
                    print("Response type: Undefined.")
                case '5':
                    print("Response type: File system. Corresponds to a file system status message.")
            break
    return buffer


if __name__ == '__main__':
    socket_manager = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
    try:
        socket_manager.connect(("test.rebex.net", 21))
        buffer_init = socket_manager.recv(1024).decode("utf-8")
        print(buffer_init)
    except:
        print("Error connection")

    # Имя пользователя для входа на сервер.
    send_command(CMD_USER)
    # Пароль пользователя для входа на сервер.
    send_command(CMD_PASS)
    #  Войти в пассивный режим. Сервер вернёт адрес и порт, к которому нужно подключиться, чтобы забрать данные
    ret = send_command(CMD_PASV)
    # ищем подстроку соответствующую регулярному выражению
    match = re.search(r"(\d+,\d+,\d+,\d+,\d+,\d+)", ret)
    # разбиваем через запятую получая список чисел соответствующих ip port
    match = re.split(r",", match[0])
    ip = ".".join(match[0:4])
    port = int(match[4]) * 256 + int(match[5])
    print(f"ip {ip} port {port}")

    socket_data = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
    try:
        socket_data.connect((ip, port))
        print("Connection OK")
    except:
        print("Error connection")
    # после команды LIST возвращается список файлов каталога. Список передаётся через соединение данных.
    send_command(CMD_LIST)
    list_data = socket_data.recv(1024).decode("utf-8")
    print(list_data)

    time.sleep(0.1)
    print("Client: ", CMD_RETR.decode("utf-8"), end='')
    socket_manager.send(CMD_RETR)
    print(socket_manager.recv(1024))

    # send_command(CMD_HELP)
    # help = socket_data.recv(1024).decode("utf-8")
    # print(help)

    # send_command(CMD_CWD)
    # send_command(CMD_LIST)
    # list_data = socket_data.recv(1024).decode("utf-8")
    # print(list_data)

    send_command(CMD_QUIT)
    socket_manager.close()
