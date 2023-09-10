from settings import *
from lr1 import *

with dpg.window(tag="Primary Window"):
    dpg.add_button(label="Лабораторная работа #1",
                   callback=lambda: dpg.show_item('lr1'))
    dpg.add_button(label="Лабораторная работа #2")
    dpg.add_button(label="Лабораторная работа #3")
    dpg.add_button(label="Лабораторная работа #4")


dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()
