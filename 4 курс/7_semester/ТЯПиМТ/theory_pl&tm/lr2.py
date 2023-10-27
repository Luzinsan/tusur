import dearpygui.dearpygui as dpg
import re
from __init__ import initialize


class RegexAnalyze:
    __TYPES__: frozenset = {'int', 'double', 'float'}
    __CONTAINER__: set

    def __init__(self):
        self.__CONTAINER__ = set(self.__TYPES__)

    def analyze(self, input_string: str):
        types_str = '|'.join(self.__TYPES__)
        print(types_str)
        pattern = re.compile(
            f"(\s*(?:(?P<type>{types_str})\\b|(?P<id>[a-zA-Z_]\w*(?P<op>\[\s*(?:(?:[a-zA-Z_]\w*\[\d+\]|\d+)(?:\s*,\s*(?:[a-zA-Z_]\w*\[\d+\]|\d+))*)\s*\])?)\s*[,;])\s*)")

        # if ''.join([match[0] for match in re.findall(pattern, input_string)]) != input_string:
        iterator = re.finditer(pattern, input_string)
        desired_type = next(iterator)
        index = desired_type.end()

        if desired_type['type'] not in self.__TYPES__:
            raise TypeError(f"Invalid type on the row={1}; column={desired_type.start()}")
        for match in iterator:
            print(f"index in orig string: {index}\trest_str={input_string[index:]}")
            if not match['id']:
                raise KeyError("Using a reserved name in an identifier\n"
                               f" on the row={1}; column={match.start()}")
            print(f"index of match: {match.start()}\tmatch={match['id']}\n")
            if index != match.start():
                raise KeyError(
                    f"Invalid id on the row={1}; column={index}\nmatch={match['id']}\trest_str={input_string[index:]}")
            elif match['id'] in self.__CONTAINER__:
                raise KeyError(f'Repeated id or using reserved name on the row={1}\tcolumn={match.start()}'
                                     f'\nid={match["id"]}'
                                     f'\nfor container:{self.__CONTAINER__ - set(self.__TYPES__)}'
                                     f'\nand types: {self.__TYPES__}')
            else:
                self.__CONTAINER__ |= set(match['id'])
                index = match.end()
        print(f"index in orig string: {index}\trest_str={input_string[index:]}")
        print(f"index of match: {len(input_string) - 1}\n")
        if index != len(input_string) :
            raise SyntaxError("Reference to an unresolved external character\n"
                              f"on the row={1}; column={len(input_string)}")


def main():
    dpg.show_item('Analyzing')
    input_data = get_input_data()
    dpg.set_value('input data', value=input_data)
    try:
        engine: RegexAnalyze = RegexAnalyze()
        engine.analyze(input_data)
        dpg.configure_item('test', default_value=input_data, color=(0, 255, 0, 255))
    except BaseException as err:
        dpg.configure_item('test', default_value=f"Exception error during analyzing:\n{err}", color=(255, 0, 0, 255))


def initialize_lr2():
    with dpg.window(label="Лабораторная работа #2", tag='lr2', show=True, width=500, height=700, pos=(100, 100),
                    on_close=lambda: dpg.delete_item('lr2')):
        initialize()
        dpg.add_button(label="Analyze", callback=main, show=False, tag='continue')


def get_input_data():
    if dpg.get_value('input_method') == 'File':
        file_path = dpg.get_value('file')
        file = open(file_path, 'r', encoding="utf-8")
        input_data = '\n'.join(file.readlines())
        file.close()
        return input_data
    else:
        return dpg.get_value('Manually')
