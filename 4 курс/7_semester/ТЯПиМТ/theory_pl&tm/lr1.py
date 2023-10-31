import pandas as pd
import dearpygui.dearpygui as dpg
import re
from __init__ import initialize

pd.set_option('display.max_columns', None)


class DFSM:
    __ERROR__ = -1
    __HALT__ = 99
    __DELTA__: pd.DataFrame
    __container__: set
    __types__: str
    __header__: re

    def __init__(self,
                 file_transition: str = 'transition.ods'):
        self.__DELTA__ = pd.read_excel(file_transition, index_col=0, engine="odf", dtype=str)
        self.__types__ = '|'.join(self.__DELTA__.columns[:5])
        self.__container__ = set(self.__types__.split('|'))
        self.__header__ = re.compile('(' + ')|('.join([str(column) for column in self.__DELTA__.columns]) + ')')
        print(f'Функция переходов: \n{self.__DELTA__}\n\n')

    def func(self, _func: int, row: int, column: int, buffer: str, symbol: str) -> str:
        match _func:
            case 1:
                buffer += symbol
            case 2:
                if buffer in self.__container__:
                    raise ValueError(f'Repeated id on the row={row}\tcolumn={column}'
                                     f'\nid={buffer}'
                                     f'\nfor container:{self.__container__ - set(self.__types__.split("|"))}')
                self.__container__ |= {buffer}
                buffer = ''
        return buffer

    def analyze(self, input_string: str):
        q = 0
        buffer: str = ''
        row = 1
        column = 0
        input_string += '\0'
        iterator = iter(input_string)
        index = 0
        print(f"PATTERN: {self.__header__}")
        for symbol in iterator:
            print(f"CURR: {symbol}")
            if symbol == '\n':
                column = 0
                row += 1
            print(f"current string: {input_string[index:]}")
            match = re.match(self.__header__, input_string[index:])
            if match:
                print('match: ', match.groups())
                symbol = match.group()
                len_shift = len(symbol)
                match = [i for i, val in enumerate(match.groups()) if val is not None][0]
                print('column: ', self.__DELTA__.columns[match], ' index of col: ', match)
                data_zp = self.__DELTA__.iloc[int(q), int(match)]
                if data_zp == 'HALT':
                    self.__container__ -= set(self.__types__)
                    return True
                elif type(data_zp) is str:
                    if len(data_zp.split()) == 2:
                        q, _func = map(int, data_zp.split())
                        buffer = self.func(_func, row, column, buffer, symbol)
                    else:
                        q = int(data_zp)
                    [next(iterator) for interator in range(len_shift - 1)]
                    index += len_shift
                    column += len_shift
                    print(f"next index={index}\titerator={iterator}")
                else:
                    raise ValueError(f'Syntax error on the row={row}\tcolumn={column}'
                                     f'\n{input_string[:-1]}'
                                     f'\nsymbol={symbol}\tq={q}\tbuffer={buffer}\t\ncontainer={self.__container__ - set(self.__types__.split("|"))}')
            else:
                raise ValueError(f'Syntax error on the row={row}\tcolumn={column}'
                                 f'\n{input_string[:-1]}')


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
