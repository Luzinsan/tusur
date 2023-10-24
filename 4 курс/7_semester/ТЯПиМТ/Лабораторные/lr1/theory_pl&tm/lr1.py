import pandas as pd
import dearpygui.dearpygui as dpg
from __init__ import initialize


class DFSM:
    __ALPHABET__: dict[str, str]
    __HEADER__: list[str]
    __ERROR__ = 'ERROR'
    __HALT__ = 'HALT'
    __DELTA__: pd.DataFrame

    def __init__(self,
                 file_alphabetic: str = 'theory_pl&tm/alphabetic.txt'):
        file = open(file_alphabetic, 'r', encoding="utf-8")
        alphabet_area = file.readlines()
        file.close()

        custom_alphabetic = []
        pattern_alphabetic = ''
        for item in alphabet_area:
            item = item[:3]
            pattern_alphabetic += item + ', '
            custom_alphabetic += [chr(symbol)
                                  for symbol in range(ord(item[0]), ord(item[-1]) + 1)]
        self.__ALPHABET__ = {symbol: pattern_alphabetic + '_' for symbol in custom_alphabetic} \
                            | {'_': pattern_alphabetic + '_'} \
                            | {chr(symbol): '0-9' for symbol in range(ord('0'), ord('9'))} \
                            | {',': ','} \
                            | {'\t': '└┘', '\n': '└┘', ' ': '└┘'} \
                            | {'\0': '\0'}
        self.__header__ = [pattern_alphabetic + '_', '0-9', ',', '└┘', '\0']
        print(f"Алфавит: {self.__header__}")

        self.__DELTA__ = pd.DataFrame(columns=self.__header__,
                                      data=[[(1, 1), (self.__ERROR__, 0), (self.__ERROR__, 0), (0, 0),
                                             (self.__ERROR__, 0)],
                                            [(1, 1), (1, 1), (0, 2), (2, 2), (self.__HALT__, 2)],
                                            [(self.__ERROR__, 0), (self.__ERROR__, 0), (0, 0), (2, 0),
                                             (self.__HALT__, 0)]])
        print(f'Функция переходов: \n{self.__DELTA__}\n\n')

    def analyze(self, input_string: str):
        q = 0
        container = []
        buffer = ''
        row = 1
        column = 0
        input_string += '\0'
        for symbol in input_string:
            q, func = self.__DELTA__.iloc[q][self.__ALPHABET__[symbol]]
            if symbol == '\n':
                column = 0
                row += 1
            else:
                column += 1
            match func:
                case 1:
                    buffer += symbol
                case 2:
                    if buffer in container:
                        raise ValueError(f'Repeated id on the row={row}\tcolumn={column}'
                                         f'\nid={buffer}'
                                         f'\nfor container:{container}')
                    container.append(buffer)
                    buffer = ''

            print(f'symbol={symbol}\tq={q}\tfunc={func}\tbuffer={buffer}\tcontainer={container}'
                  f'\nanalyzing: row={row}\tcolumn={column}')
            match q:
                case 'ERROR':
                    raise ValueError(f'Syntax error on the row={row}\tcolumn={column}'
                                     f'\n{input_string[:-1]}'
                                     f'\n{" " * len(input_string[:-1])}\r^')
                case 'HALT':
                    return True


def get_input_data():
    if dpg.get_value('input_method') == 'File':
        file_path = dpg.get_value('file')
        file = open(file_path, 'r', encoding="utf-8")
        input_data = '\n'.join(file.readlines())
        file.close()
        return input_data
    else:
        return dpg.get_value('Manually')


def main():
    dpg.show_item('Analyzing')
    input_data = get_input_data()
    dpg.set_value('input data', value=input_data)
    try:
        engine: DFSM = DFSM()
        engine.analyze(input_data)
        dpg.configure_item('test', default_value=input_data, color=(0, 255, 0, 255))
    except ValueError as err:
        dpg.configure_item('test', default_value=f"Exception error during analyzing:\n{err}", color=(255, 0, 0, 255))


def initialize_lr1():
    with dpg.window(label="Лабораторная работа #1", tag='lr1', show=True, width=500, height=700, pos=(100, 100),
                    on_close=lambda: dpg.delete_item('lr1')):
        initialize()
        dpg.add_button(label="Analyze", callback=main, show=False, tag='continue')
