import dearpygui.dearpygui as dpg
import re
from socket import *
from ssl import *
from http_parser.http import HttpStream
from http_parser.reader import SocketReader
from html.parser import HTMLParser

hostname = "www.example.com"
path = "/"
DEFAULT_PORT = 443
TIMEOUT = 0.0

dpg.create_context()
sslcontext = create_default_context()


class tHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        dpg.add_text(f"Start tag: {tag}", parent='content')
        print("Start tag:", tag)
        for attr in attrs:
            print("     attr:", attr)
            if attr[0] == 'href':
                if re.search(r'(\w/.*\..*)', attr[1]):
                    dpg.add_button(label=attr[1], parent='content', callback=download_source, user_data=attr[1])
                    print("This is file")
                else:
                    dpg.add_button(label=attr[1], parent='content', callback=follow_link, user_data=attr[1])
                print(attr[1])
            else:
                dpg.add_text(f"     attr: {attr}", parent='content')


def download_source(sender, app_data, user_data):
    pass
def follow_link(sender, app_data, user_data):
    parse_path(user_data)
    dpg.set_value('path', user_data)
    open_link(None, None, None)


def parse_path(full_path: str):
    print("PARSE_PATH: ", full_path)
    # full_path = 'https://example.com/'
    global hostname, path
    if re.search(r'(//[\w.]*)', full_path):
        hostname = re.search(r'(//[\w.]*)', full_path)[0][2:]
    print("parsed hostname: ", hostname)
    if re.search(r'(\w/.*)', full_path) and not re.search(r'(\w/.*\..*)', full_path):
        path = re.search(r'(\w/.*)', full_path)[0][1:]
    else:
        path = '/'
    print("parsed path: ", path)
    dpg.set_value('correct_host', f"{hostname}{path}")


def open_link(sender, app_data, full_path):
    print("open_link: ", full_path)
    dpg.delete_item('content', children_only=True)
    if not full_path:
        print(dpg.get_value('path'))
        parse_path(dpg.get_value('path'))
    with create_connection((hostname, DEFAULT_PORT)) as sock:
        with sslcontext.wrap_socket(sock, server_hostname=hostname) as ssock:
            print(ssock.version())
            receive_page = f"GET {path} HTTP/1.1\r\n" \
                           f"Host:{hostname}\r\n" \
                           f"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0\r\n" \
                           "\r\n"
            ssock.send(receive_page.encode())
            r = SocketReader(ssock)
            p = HttpStream(r)
            # print(p.headers())
            body = p.body_file().read()
            dpg.add_text(body.decode(), parent='content')
            # print(body.decode())
            parser = tHTMLParser()
            parser.feed(body.decode('utf8'))
            # parser.handle_starttag('a', 'href')


with dpg.window(label="BROWSER", tag="main", autosize=True):
    with dpg.menu_bar():
        dpg.add_input_text(label=":PATH", tag='path', default_value='https://example.com/', callback=open_link)
        dpg.add_input_text(label="Host", tag='correct_host', default_value='example.com/', readonly=True)
    dpg.add_child_window(tag='content')

# region other
with dpg.theme() as global_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (77, 7, 143), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)
    with dpg.theme_component(dpg.mvInputInt):
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (30, 77, 70), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)
    with dpg.theme_component(dpg.mvText):
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (15, 61, 131), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)

dpg.bind_theme(global_theme)
########################################################################################################################
dpg.create_viewport(title='BROWSER', width=960, height=750)
dpg.set_global_font_scale(1.25)
# dpg.set_exit_callback(on_exit)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("main", True)
dpg.start_dearpygui()
dpg.destroy_context()

# endregion
