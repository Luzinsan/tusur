from socket import *
import dearpygui
import re
import time

CMD_USER = b"USER demo\r\n"
CMD_PASS = b"PASS password\r\n"
CMD_PASV = b"PASV\r\n"
CMD_LIST = b"LIST\r\n"
CMD_QUIT = b"QUIT\r\n"


def send_command(command: bytes):
    time.sleep(0.1)
    print(command.decode("utf-8"))
    socket_manager.send(command)
    buffer = socket_manager.recv(1024).decode("utf-8")
    print(buffer)
    while True:
        if buffer[:4] == "xyz-":
            buffer = socket_manager.recv(1024).decode("utf-8")
            print(buffer)
        else:
            break
    return buffer


if __name__ == '__main__':
    socket_manager = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
    try:
        socket_manager.connect(("test.rebex.net", 21))
        print("Connection OK")
    except:
        print("Error connection")

    buffer_init = socket_manager.recv(1024).decode("utf-8")
    print(buffer_init)

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
    list_data = send_command(CMD_LIST)
    buf = socket_data.recv(1024).decode("utf-8")
    print(buf)
    send_command(CMD_QUIT)
    socket_manager.close()



