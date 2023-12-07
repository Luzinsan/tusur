import pandas as pd
import dearpygui.dearpygui as dpg
import re
from __init__ import initialize

pd.set_option('display.max_columns', None)


class DFSM:
    __DELTA__: pd.DataFrame
    __container__: set
    __buffer__: str
    __header__: re

    def __init__(self,
                 file_transition):
        self.__DELTA__ = pd.read_excel(file_transition, index_col=0, engine="odf", dtype=str)
        self.__container__ = set()
        self.__buffer__ = str()
        self.__header__ = re.compile('(' + ')|('.join([str(column) for column in self.__DELTA__.columns]) + ')')
        print(f'Функция переходов: \n{self.__DELTA__}\n\n')

    def func(self, _func: int, row: int, column: int, symbol: str):
        match _func:
            case 1:
                self.__buffer__ += symbol
            case 2:
                if self.__buffer__ in self.__container__:
                    raise ValueError(f'Repeated id on the row={row}\tcolumn={column}'
                                     f'\nid={self.__buffer__}'
                                     f'\nfor container:{self.__container__}')
                self.__container__ |= {self.__buffer__}
                self.__buffer__ = ''
        print(f'row={row}\tcolumn={column}'
              f'\nbuffer={self.__buffer__}'
              f'\ncontainer:{self.__container__}')

    def analyze(self, input_string: str):
        q, row, column = 0, 1, 0
        input_string += '\0'
        print(f"PATTERN: {self.__header__}")
        index = 0
        while True:
            symbol = input_string[index]
            print(f"CURR: {symbol}")
            if symbol == '\n':
                column = 0
                row += 1
            print(f"current string: {input_string[index:]}")
            match = self.__header__.match(input_string, pos=index)
            if match:
                print('match: ', match.groups())
                symbol = match.group()
                len_shift = len(symbol)
                match = [i for i, val in enumerate(match.groups()) if val is not None][0]
                print('column: ', self.__DELTA__.columns[match], ' index of col: ', match)
                data_zp = self.__DELTA__.iloc[int(q), int(match)]
                if data_zp == 'HALT':
                    return True
                elif type(data_zp) is str:
                    if len(data_zp.split()) == 2:
                        q, _func = map(int, data_zp.split())
                        self.func(_func, row, column, symbol)
                    else:
                        q = int(data_zp)
                    index += len_shift
                    column += len_shift
                else:
                    raise ValueError(f'Syntax error on the row={row}\tcolumn={column}'
                                     f'\n{input_string[:-1]}'
                                     f'\nsymbol={symbol}\tq={q}\tbuffer={self.__buffer__}\t\ncontainer={self.__container__}')
            else:
                raise ValueError(f'Syntax error on the row={row}\tcolumn={column}'
                                 f'\n{input_string[:-1]}')


def get_input_data():
    if dpg.get_value('input_method') == 'File':
        file_path = dpg.get_value('input_file')
        file = open(file_path, 'r', encoding="utf-8")
        input_data = ''.join(file.readlines())
        file.close()
        return input_data
    else:
        return dpg.get_value('Manually_text')


def main():
    dpg.show_item('Analyzing')
    input_data = get_input_data()
    data_with_numering = '\n'.join([f'{index}\t{row}'
                                    for index, row
                                    in enumerate(input_data.split('\n'), 1)])
    dpg.set_value('input data', value=data_with_numering)
    try:
        engine: DFSM = DFSM(dpg.get_value('file_grammar'))
        engine.analyze(input_data)
        dpg.configure_item('test', default_value=input_data, color=(0, 255, 0, 255))
    except ValueError as err:
        dpg.configure_item('test', default_value=f"Exception error during analyzing:\n{err}", color=(255, 0, 0, 255))


def initialize_lr1():
    with dpg.window(label="Лабораторная работа #1", tag='lr1', show=True, autosize=True, min_size=(1000, 800), pos=(480, 0),
                    on_close=lambda: dpg.delete_item('lr1')):
        initialize()
        dpg.configure_item('file_grammar', default_value='lr1/transition.ods')
        dpg.configure_item('input_file', default_value='test.txt')
        dpg.add_button(label="Analyze", callback=main, show=False, tag='continue')
