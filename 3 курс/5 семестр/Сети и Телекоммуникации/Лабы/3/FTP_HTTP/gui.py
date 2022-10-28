import dearpygui.dearpygui as dpg
from socket import *
import re
import time

DEFAULT_SERVER = "ftp.slackware.com"
DEFAULT_LOGIN = "anonymous"
DEFAULT_PASS = "password"
DEFAULT_PORT = 21

dpg.create_context()
CMD_PASV = b"PASV\r\n"

CMD_LIST = b"LIST\r\n"
CMD_QUIT = b"QUIT\r\n"
CMD_CWD = b"CDUP\r\n"
CMD_HELP = b"HELP\r\n"
CMD_RETR = b"RETR readme.txt\r\r"


####################################### Stage #1: INITIALIZATION SERVER  ###############################################
def recv_all(socket_manager):
    answer = socket_manager.recv(1024).decode('utf-8')
    print(answer, end='')
    while not re.search(r'\d{3} ', answer):
        answer = socket_manager.recv(1024).decode('utf-8')
        print(answer, end='')
    return answer


def init_server(sender, app_data, user_data):
    socket_manager = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
    try:
        socket_manager.connect((dpg.get_value(ftp_server_id), dpg.get_value(ftp_port_id)))
        buffer_init = recv_all(socket_manager)
        dpg.add_text(buffer_init[4:], tag='connect', before=sep)
    except:
        dpg.add_text("Incorrect Server or PORT", tag='err', before=sep)
        time.sleep(2.0)
        dpg.delete_item("err")
        socket_manager.close()
        return
    init_user(socket_manager)
    socket_data = init_pasv(socket_manager)
    response_handler("220" if socket_data else "520", socket_data)


############################################ Stage #2: INITIALIZATION USER #############################################
def init_user(socket_manager):
    CMD_USER = f"USER {dpg.get_value(login_id)}\r\n".encode("utf-8")
    CMD_PASS = f"PASS {dpg.get_value(password_id)}\r\n".encode("utf-8")
    # Имя пользователя для входа на сервер.
    socket_manager.send(CMD_USER)
    recv_all(socket_manager)

    # Пароль пользователя для входа на сервер.
    socket_manager.send(CMD_PASS)
    answer = recv_all(socket_manager)
    dpg.delete_item("connect")


def init_pasv(socket_manager):
    #  Войти в пассивный режим. Сервер вернёт адрес и порт, к которому нужно подключиться, чтобы забрать данные
    socket_manager.send(CMD_PASV)
    pasv = recv_all(socket_manager)
    # ищем подстроку соответствующую регулярному выражению
    match = re.search(r"(\d+,\d+,\d+,\d+,\d+,\d+)", pasv)
    # разбиваем через запятую получая список чисел соответствующих ip port
    match = re.split(r",", match[0])
    ip = ".".join(match[0:4])
    port = int(match[4]) * 256 + int(match[5])
    print(f"ip {ip} port {port}")

    socket_data = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
    try:
        socket_data.connect((ip, port))
        dpg.add_text("Connection OK", tag='socket_data', before='answers')
        time.sleep(2.0)
        dpg.delete_item("socket_data")
        return socket_data
    except:
        dpg.add_text("Discard Connection", tag='socket_data', before='answers')
        time.sleep(2.0)
        dpg.delete_item("socket_data")
        socket_data.close()


############################################# Stahe #3: RESPONSE HANDLER ###############################################
def response_handler(answer, socket):
    match answer[0]:
        case '2':
            dpg.add_text("Connection successful.", tag='success', before="answers")
            time.sleep(2.0)
            dpg.configure_item('auth', show=False)
            dpg.delete_item("success")
        case '3' | '5':
            dpg.add_text("Incorrect login or password.", tag='incorrect', before="answers")
            time.sleep(2.0)
            dpg.delete_item("incorrect")
            socket.close()
################################################ END AUTHORIZATION #####################################################


############################################# AUTHORIZATION ############################################################
with dpg.window(label="AUTHORIZATION", modal=True, show=False, tag="auth", no_title_bar=True, autosize=True, ):
    ftp_server_id = dpg.add_input_text(label="Server", default_value=DEFAULT_SERVER)
    ftp_port_id = dpg.add_input_int(label="PORT", default_value=DEFAULT_PORT)
    sep = dpg.add_separator()
    login_id = dpg.add_input_text(label="login", default_value=DEFAULT_LOGIN)
    password_id = dpg.add_input_text(label="password", default_value=DEFAULT_PASS, password=True)
    with dpg.group(horizontal=True, tag="answers"):
        dpg.add_button(label="Save", width=75, callback=init_server)
        dpg.add_button(label="Cancel", width=75, callback=lambda: dpg.configure_item("auth", show=False))
########################################################################################################################

################################################# MAIN ################################################################
with dpg.window(label="Main", tag="Main", autosize=True):
    with dpg.menu_bar():
        with dpg.menu(label="Connection"):
            dpg.add_menu_item(label="Log in", callback=lambda: dpg.configure_item("auth", show=True))
    # dpg.add_button(label="SELECT INBOX", callback=lambda: dpg.configure_item("select", show=True))
    # dpg.add_button(label="FETCH FLAGS", callback=lambda: dpg.configure_item("flags", show=True))
    # dpg.add_button(label="FETCH BODIES", callback=lambda: dpg.configure_item("bodies", show=True))
########################################################################################################################
dpg.create_viewport(title='FTP CLIENT', width=1080, height=920)
dpg.set_global_font_scale(1.25)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Main", True)
dpg.start_dearpygui()
dpg.destroy_context()
