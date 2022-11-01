import dearpygui.dearpygui as dpg
from socket import *
import re
import time

DEFAULT_SERVER = "ftp.pureftpd.org"
DEFAULT_LOGIN = "anonymous"
DEFAULT_PASS = "anonymous"
DEFAULT_PORT = 21  # сетевой порт для управляющего соединения
TIMEOUT = 0.0

dpg.create_context()


# CMD_LIST = b"NLST\r\n"
# CMD_QUIT = b"QUIT\r\n"
# CMD_CWD = b"CWD /docs/\r\n"
# CMD_HELP = b"HELP\r\n"
# CMD_RETR = b"RETR readme.txt\r\r"
# CMD_STRU = b"STRU P\r\n"


# region ####################################### Stage #1: INITIALIZATION SERVER  ######################################
def recv_all(socket_manager):
    while True:
        answer = socket_manager.recv(1024).decode('utf-8')
        match = re.search(r'\d{3}\s.*', answer)
        if match:
            print(match[0])
            break
        print(answer, end='')
    return match[0]


def init_server(sender, app_data, user_data):
    socket_manager = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)  # управляющее соединение
    try:
        # соединяемся с сервером для передачи управляющих команд
        socket_manager.connect((dpg.get_value('host'), dpg.get_value('port')))
        recv_all(socket_manager)
        dpg.add_text("1: Connected to host successful", tag='connect', before='sep')
        time.sleep(TIMEOUT)
        dpg.delete_item("connect")
        dpg.set_item_user_data("auth", socket_manager)
    except:
        dpg.add_text("Incorrect HOST or PORT", tag='err', before='sep')
        time.sleep(TIMEOUT)
        dpg.delete_item("err")
        socket_manager.close()
        return
    etc_server_data(socket_manager)
    update_dir(socket_manager)


def etc_server_data(socket_manager):
    # аутентификация пользователя
    init_user(socket_manager)
    # текущая кодировка
    update_text(socket_manager, b"TYPE I\r\n", 'type')
    # определяем систему хоста
    update_text(socket_manager, b"SYST\r\n", 'system')


def update_dir(socket_manager):
    # определяем текущую директорию
    update_text(socket_manager, b"PWD\r\n", 'path')
    socket_data = init_pasv(socket_manager)
    output_list(socket_manager, socket_data)
    socket_data.close()


def update_text(socket_manager, cmd: bytes, tag: str):
    socket_manager.send(cmd)
    response = recv_all(socket_manager)
    dpg.set_value(tag, response[3:])
    return response[:3]


def output_list(socket_manager, socket_data):
    print('\n\t\tOUTPUT_LIST')
    dpg.configure_item('list', items=[])

    socket_manager.send(b"LIST\r\n")
    recv_all(socket_manager)  # Подтверждаем соединение с сервером для передачи списка
    response = recv_all(socket_manager)[4:]  # Получаем количество строк в текущей директории
    num_dir = int(re.search(r'\d+', response)[0])  # Узнаём кол-во директорий/файлов
    dpg.set_value('numdir', num_dir)

    count = 0
    ftp_list = []
    print("READING...")
    while count < num_dir:
        ftp_list += socket_data.recv(1024).decode('utf-8').splitlines()
        count += len(ftp_list)
        print(count)
    dpg.configure_item('list', items=ftp_list, num_items=num_dir)
    print("\t\tOutputting list DONE\n")


########################################## Stage #2: AUTHENTICATION USER #############################################
def send_recv_cmd(socket_manager: socket, cmd: bytes, tag: str = 'response', before: str = '') -> str:
    """ Посылает команду на подключенных хост, выводит в GUI ответ (tag='response') и возвращает код ответа

    :param socket_manager: сокет управляющего соединения
    :param cmd: отправляемая команда на подключенный сервер
    :param tag: tag добавляемого в GUI ответа
    :param before: tag элемента, перед которым выводится ответ (если '', то вывод в консоль)
    :return: код ответа
    """
    socket_manager.send(cmd)
    res = recv_all(socket_manager)
    if before != '':
        dpg.add_text(res[3:], tag=tag, before=before)
    return res[:3]


def init_user(socket_manager):
    CMD_USER = f"USER {dpg.get_value('user')}\r\n".encode("utf-8")
    CMD_PASS = f"PASS {dpg.get_value('pass')}\r\n".encode("utf-8")
    # Имя пользователя для входа на сервер.
    send_recv_cmd(socket_manager, CMD_USER, 'user_auth', 'pass')
    # Пароль пользователя для входа на сервер.
    res = send_recv_cmd(socket_manager, CMD_PASS, 'pass_user', 'answers')
    if res == '230':  # если аутентификация прошла успешно, закрываем окно
        dpg.add_text("Authorization successful", tag='success', before="answers")
        time.sleep(TIMEOUT)
        dpg.configure_item('auth', show=False)
        dpg.delete_item('success')
    time.sleep(TIMEOUT)
    dpg.delete_item('pass_user')
    dpg.delete_item('user_auth')


def init_pasv(socket_manager):
    #  Войти в пассивный режим. Сервер вернёт адрес и порт, к которому нужно подключиться, чтобы забрать данные
    socket_manager.send(b"PASV\r\n")
    pasv = recv_all(socket_manager)
    # ищем подстроку соответствующую регулярному выражению
    match = re.search(r'(\d+,\d+,\d+,\d+,\d+,\d+)', pasv)
    # разбиваем через запятую получая список чисел соответствующих ip port
    match = re.split(r",", match[0])
    ip = ".".join(match[:4])
    port = int(match[4]) * 256 + int(match[5])
    dpg.set_value('ip_port', f"ip: {ip}\tport: {port}")
    print(f"ip {ip} port {port}")

    socket_data = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
    try:
        socket_data.connect((ip, port))
        return socket_data
    except:
        dpg.add_text("Discard Connection", tag='discard_socket_data', before='path')
        time.sleep(TIMEOUT)
        dpg.delete_item("discard_socket_data")
        socket_data.close()


# endregion ################################################ END AUTHORIZATION #########################################


def move_to(sender, app_data, user_data):
    socket_manager, directory = dpg.get_item_user_data('auth'),  dpg.get_value('move_to_path')
    # переходим в указанную директорию
    if send_recv_cmd(socket_manager, f"CWD {directory}\r\n".encode('utf-8')) == '250':
        update_dir(socket_manager)
        dpg.set_value('move_to_path', '')
    else:
        dpg.set_value('move_to_path', 'Invalid directory')
    print(f"Moving to {directory} done")


def download(sender, app_data, user_data):
    socket_manager, directory = user_data[0], user_data[1]
    socket_data = init_pasv(socket_manager)
    socket_data.send(b"RETR {directory}\r\n")
    file = open("download", 'w')
    while socket_data:
        ftp_list = socket_data.recv(1024).decode('utf-8')
        file.write(ftp_list)
    file.close()


def on_exit(sender, app_data, user_data):
    socket_manager = dpg.get_item_user_data('auth')
    socket_manager.close()
    print("socket_manager closed successfully")


############################################# AUTHORIZATION ############################################################
with dpg.window(label="AUTHORIZATION", modal=True, show=False, tag="auth", no_title_bar=True, autosize=True):
    dpg.add_input_text(label=":HOST", tag='host', default_value=DEFAULT_SERVER)
    dpg.add_input_int(label=":PORT", tag='port', default_value=DEFAULT_PORT)
    dpg.add_separator(tag='sep')
    dpg.add_input_text(label=":user", tag='user', default_value=DEFAULT_LOGIN)
    dpg.add_input_text(label=":password", tag='pass', default_value=DEFAULT_PASS, password=True)
    with dpg.group(horizontal=True, tag="answers"):
        dpg.add_button(label="Connect", width=75, callback=init_server)
        dpg.add_button(label="Cancel", width=75, callback=lambda: dpg.configure_item("auth", show=False))
########################################################################################################################


################################################# MAIN ################################################################
with dpg.window(label="Main", tag="Main", autosize=True):
    with dpg.menu_bar():
        with dpg.menu(label="Connection"):
            dpg.add_menu_item(label="Log in", callback=lambda: dpg.configure_item("auth", show=True))
    dpg.add_text(label=":System of Host", tag='system')  # система хоста
    dpg.add_text(label=":IP/PORT of Host", tag='ip_port')  # после перехода в пассивный режим определяем IP и PORT хоста
    dpg.add_text(label=":TYPE data", tag='type')  # переключаемся в бинарный режим
    dpg.add_text(label=":PATH", tag='path')  # текущая директория хоста
    dpg.add_text(label=":Number of Lines", tag='numdir')  # количество директорий/файлов в текущем каталоге

    dpg.add_listbox(tag='list')  # список файлов текущей директории

    with dpg.group(horizontal=True, tag="move_to"):
        dpg.add_input_text(label=":PATH", tag='move_to_path', width=75)
        dpg.add_button(label="MOVE", width=75, callback=move_to, before='move_to_path')

    with dpg.group(horizontal=True, tag="download"):
        dpg.add_button(label="DOWNLOAD", width=75, callback=download)
        dpg.add_input_text(label=":FILE", tag='download_file', width=75)
########################################################################################################################
dpg.create_viewport(title='FTP CLIENT', width=1080, height=920)
dpg.set_global_font_scale(1.25)
dpg.set_exit_callback(on_exit)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Main", True)
dpg.start_dearpygui()
dpg.destroy_context()
