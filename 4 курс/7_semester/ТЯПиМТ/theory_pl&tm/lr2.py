import dearpygui.dearpygui as dpg
import regex as re
from __init__ import initialize


class RegexAnalyze:
    __TYPES__: frozenset = {'int', 'double', 'float'}
    pattern: re
    __CONTAINER__: set

    def __init__(self, file_path_regex: str = "regex.txt"):
        with open(file_path_regex) as file:
            self.pattern = re.compile(''.join(file.readlines()).replace(" ", '').replace("\n", ''))

        self.__CONTAINER__ = set()

    def analyze(self, input_string: str):
        row = 1
        error_message = str()
        for match in re.finditer(self.pattern, input_string, partial=True):
            print('capturesdict: ', match.capturesdict())
            capture_dict = match.capturesdict()
            for error in ['error_type', 'error_id_like_type', 'error_id', 'error_op', 'error_punc']:
                if len(capture_dict[error]):
                    for index, capture in enumerate(capture_dict[error]):
                        pos = match.spans(error)[index][0] - match.start()
                        search_n = re.search('\n', match[0], endpos=pos)
                        if search_n:
                            spaces = [_match for _match in re.finditer('\n', match[0], endpos=pos)]
                            pos -= spaces[-1].span()[1]
                        error_message += f'{error}: {capture}\n' \
                                      + f'row={row}\tpos={pos+ 1}\n\n' \
                                    #  + f'{match.spans(error)[index]}\n\n'
            row += len(re.findall('\n', match[0]))
        if error_message is not '':
            raise SyntaxError(error_message)



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
    with dpg.window(label="Лабораторная работа #2", tag='lr2', show=True, autosize=True, min_size=(1000, 800), modal=True, pos=(480, 0),
                    on_close=lambda: dpg.delete_item('lr2')):
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
        return dpg.get_value('Manually')
