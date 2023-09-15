import dearpygui.dearpygui as dpg
from initialize import *


def encrypting(sender, app_data, user_data):
    pass


def initialize_lr2():
    with dpg.window(label="Лабораторная работа #2", tag='lr2', show=True, width=500, height=700, pos=(100, 100),
                    on_close=lambda: dpg.delete_item('lr2')):
        initialize()
        dpg.add_button(label="Continue: AES", callback=encrypting, show=False, tag='continue')
