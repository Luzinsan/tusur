import dearpygui.dearpygui as dpg
import regex as re
from __init__ import initialize


class LL:
    __container__: set
    __errors__: str

    def __init__(self, file_path_LL: str = "lr3/LL"):
        with open(file_path_LL) as file:
            pass

    def analyze(self, input_string: str):
       pass


def main():
    dpg.show_item('Analyzing')
    input_data = get_input_data()
    data_with_numering = '\n'.join([f'{index}\t{row}'
                                    for index, row
                                    in enumerate(input_data.split('\n'), 1)])
    dpg.set_value('input data', value=data_with_numering)
    try:
        engine: LL = LL()
        engine.analyze(input_data)
        dpg.configure_item('test', default_value=input_data, color=(0, 255, 0, 255))
    except BaseException as err:
        dpg.configure_item('test', default_value=f"Exception error during analyzing:\n{err}", color=(255, 0, 0, 255))


def initialize_lr3():
    with dpg.window(label="Лабораторная работа #3", tag='lr3', show=True, autosize=True, min_size=(1000, 800),
                    modal=True, pos=(480, 0),
                    on_close=lambda: dpg.delete_item('lr3')):
        initialize()
        dpg.add_button(label="Analyze", callback=main, show=False, tag='continue')


def get_input_data():
    if dpg.get_value('input_method') == 'File':
        file_path = dpg.get_value('file')
        file = open(file_path, 'r')
        input_data = ''.join(file.readlines())
        file.close()
        return input_data
    else:
        return dpg.get_value('Manually_text')
