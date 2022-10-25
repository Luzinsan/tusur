from socket import *


if __name__ == '__main__':

    send_command(CMD_USER)

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
