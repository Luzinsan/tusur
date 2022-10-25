import dearpygui.dearpygui as dpg
from socket import *
import re
import time

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
    print("1: ", answer, end='')
    count = 1
    while re.search(r"ddd ", answer):
        answer = socket_manager.recv(1024).decode('utf-8')
        print(count, answer, end='')
        count += 1
    return answer


def init_server(sender, app_data, user_data):
    socket_manager = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
    try:
        socket_manager.connect((dpg.get_value(ftp_server_id), dpg.get_value(ftp_port_id)))
        buffer_init = recv_all(socket_manager)
        #buffer_init = socket_manager.recv(1024).decode("utf-8")
        dpg.add_text(buffer_init[4:], tag='connect', before=sep)
    except:
        dpg.add_text("Incorrect Server or PORT", tag='err', before=sep)
        time.sleep(2.0)
        dpg.delete_item("err")
        return
    init_user(socket_manager)


############################################ Stage #2: INITIALIZATION USER #############################################
def init_user(socket_manager):
    CMD_USER = f"USER {dpg.get_value(login_id)}\r\n".encode("utf-8")
    CMD_PASS = f"PASS {dpg.get_value(password_id)}\r\n".encode("utf-8")
    # Имя пользователя для входа на сервер.
    socket_manager.send(CMD_USER)
    recv_all(socket_manager)
    #print(socket_manager.recv(1024).decode('utf-8'), end='')
    # Пароль пользователя для входа на сервер.
    socket_manager.send(CMD_PASS)
    #response_handler(socket_manager)
    dpg.delete_item("connect")


############################################# Stahe #3: RESPONSE HANDLER ###############################################
def response_handler(socket_manager):
    answer = recv_all(socket_manager)
    # answer = socket_manager.recv(1024).decode('utf-8')
    # print(answer)
    # while answer[3] == '-':
    #     answer = socket_manager.recv(1024).decode('utf-8')
    #     print(answer, end='')
    print(answer, end='')
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
            socket_manager.close()
################################################ END AUTHORIZATION #####################################################


############################################# AUTHORIZATION ############################################################
with dpg.window(label="AUTHORIZATION", modal=True, show=False, tag="auth", no_title_bar=True, autosize=True, ):
    ftp_server_id = dpg.add_input_text(label="Server", default_value="ftp.gnu.org")
    ftp_port_id = dpg.add_input_int(label="PORT", default_value=DEFAULT_PORT)
    sep = dpg.add_separator()
    login_id = dpg.add_input_text(label="login", default_value="anonymous")
    password_id = dpg.add_input_text(label="password", default_value="anonymous", password=True)
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
