from settings import *
from lr1.lr1 import *
from lr2.lr2 import *
# from lr3 import *


with dpg.window(tag="Primary Window"):
    dpg.add_button(label="Лабораторная работа #1",
                   callback=initialize_lr1)
    dpg.add_button(label="Лабораторная работа #2",
                   callback=initialize_lr2)
    # dpg.add_button(label="Лабораторная работа #3",
    #                callback=initialize_lr3)


dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()
