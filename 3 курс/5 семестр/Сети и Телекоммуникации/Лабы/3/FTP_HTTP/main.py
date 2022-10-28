from socket import *


if __name__ == '__main__':

    send_command(CMD_USER)

    send_command(CMD_PASS)

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
