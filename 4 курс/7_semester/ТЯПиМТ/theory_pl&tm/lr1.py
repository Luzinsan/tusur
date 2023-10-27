import pandas as pd
import dearpygui.dearpygui as dpg
from __init__ import initialize
pd.set_option('display.max_columns', None)

# TODO:
# указание файла алфавита
# указание файла таблицы преобразования

class DFSM:
    __ALPHABET__: dict[str, str]
    __HEADER__: list[str]
    __ERROR__ = -1
    __HALT__ = 99
    __DELTA__: pd.DataFrame
    __container__: set
    __types__: list

    def __init__(self,
                 file_alphabetic: str = 'alphabetic.txt',
                 file_transition: str = 'transition.txt'):
        file = open(file_alphabetic, 'r')
        alphabet_area = file.readlines()
        file.close()

        custom_alphabetic = []
        pattern_alphabetic = ''
        for item in alphabet_area:
            item = item[:3]
            pattern_alphabetic += item + ', '
            custom_alphabetic += [chr(symbol)
                                  for symbol in range(ord(item[0]), ord(item[-1]) + 1)]

        self.__types__ = ['int', 'double', 'float', 'long']
        self.__container__ = set(self.__types__)
        self.__ALPHABET__ = {_type: 'type' for _type in self.__types__}\
                            | {symbol: pattern_alphabetic + '_' for symbol in custom_alphabetic + ['_']} \
                            | {chr(symbol): '0-9' for symbol in range(ord('0'), ord('9'))} \
                            | {'\t': '└┘', '\n': '└┘', ' ': '└┘'} \
                            | {';': ';'} \
                            | {',': ','} \
                            | {'\0': '\0'}
        self.__header__ = ['type', pattern_alphabetic + '_', '0-9', '└┘', ';', ',', '\0']
        print(f"Алфавит: {self.__header__}")

        file = open(file_transition, 'r')
        transition = file.readlines()
        file.close()
        data = list()
        for row in transition:
            lst_row = row.split()
            data.append([(int(lst_row[index]), int(lst_row[index + 1])) for index in range(0, len(lst_row) - 1, 2)])
        print(data)
        self.__DELTA__ = pd.DataFrame(columns=self.__header__,
            data=data)
        print(f'Функция переходов: \n{self.__DELTA__}\n\n')

    def analyze(self, input_string: str):
        q = 0
        buffer: str = ''
        row = 1
        column = 0
        input_string += '\0'
        iterator = iter(input_string)
        index = -1
        for symbol in iterator:
            index += 1
            print(f"CURR: {symbol}")
            if symbol == '\n':
                column = 0
                row += 1
            else:
                column += 1

            if q == 0 and symbol.isalpha():
                print(f'q=={q} and symbol as alpha\n')
                symbol = input_string[index:].split()[0]
                [next(iterator) for interator in range(len(symbol) - 1)]
                index += len(symbol) - 1
            try:
                print(f'\t=>>>q={q}\tsymbol={symbol}\talphabet={self.__ALPHABET__[symbol]}')
                q, func = self.__DELTA__.iloc[q][self.__ALPHABET__[symbol]]
                print(f'\nq={q}\tfunc={func}')
            except KeyError as err:
                raise ValueError(f'Invalid type on the row={row}\tcolumn={column}'
                                 f'\nid={symbol}')

            match func:
                case 1:
                    buffer += symbol
                case 2:
                    if buffer in self.__container__:
                        raise ValueError(f'Repeated id or using reserved name on the row={row}\tcolumn={column}'
                                         f'\nid={buffer}'
                                         f'\nfor container:{self.__container__ - set(self.__types__)}'
                                         f'\nand types: {self.__types__}')
                    self.__container__ |= {buffer}
                    buffer = ''

            print(f'symbol={symbol}\tq={q}\tfunc={func}\tbuffer={buffer}\tcontainer={self.__container__ - set(self.__types__)}'
                  f'\nanalyzing: row={row}\tcolumn={column}')
            match q:
                case self.__ERROR__:
                    raise ValueError(f'Syntax error on the row={row}\tcolumn={column}'
                                     f'\n{input_string[:-1]}'
                                     f'\n{" " * len(input_string[:-1])}\r^')
                case self.__HALT__:
                    self.__container__ -= set(self.__types__)
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
