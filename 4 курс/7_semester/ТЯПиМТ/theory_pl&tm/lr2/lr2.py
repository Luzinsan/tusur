import dearpygui.dearpygui as dpg
import regex as re
from __init__ import initialize


class RegexAnalyze:
    pattern: re
    __container__: set
    __errors__: str

    def __init__(self, file_path_regex: str = "lr2/regex.txt"):
        with open(file_path_regex) as file:
            self.pattern = re.compile(''.join(file.readlines()).replace(" ", '').replace("\n", ''))
        self.__container__ = set()
        self.__errors__ = ''

    def get_dupl_ids(self, ids: list, match_spans):
        dupl_ids = list(dict.fromkeys([ii for n, ii  # дубликаты идентификаторов
                                       in enumerate(ids)
                                       if (ids + list(self.__container__)).count(ii) > 1]))
        match_spans = list({ii: match_spans[n]  # spans дубликатов идентификаторов (last)
                            for n, ii
                            in enumerate(ids)
                            if (ids + list(self.__container__)).count(ii) > 1}.values())
        self.__container__.update(set(dict.fromkeys(ids)))  # +ids (drop duplicates)
        return dupl_ids, match_spans

    def catch_errors(self, error: str, captures: list, curr_match: str, spans: list, start_pos: int, curr_row: int):
        for index, capture in enumerate(captures):
            pos = spans[index][0] - start_pos
            row_error = curr_row
            start_row = 0
            if re.search('\n', curr_match, endpos=pos):
                spaces = [_match for _match in re.finditer('\n', curr_match, endpos=pos)]
                row_error = curr_row + len(spaces)
                start_row = spaces[-1].end()
                pos -= start_row
            last_n = re.search('\n', curr_match, pos=start_row)
            str_row = curr_match[start_row:last_n.start()] if last_n else curr_match[start_row:]
            self.__errors__ += f'{str_row}\n' \
                               + f'{"~" * pos}^\n' \
                               + f'{error}: {capture}\n' \
                               + f'row={row_error}\tpos={pos + 1}\n\n'

    def analyze(self, input_string: str):
        row = 1
        for match in re.finditer(self.pattern, input_string, partial=True):
            print('capturesdict: ', match.capturesdict())
            capture_dict = match.capturesdict()
            for error in ['error_type', 'error_id_like_type', 'error_id', 'error_op', 'error_punc', 'id']:
                match_spans = match.spans(error)
                if len(capture_dict[error]):
                    if error == 'id':
                        capture_dict[error], match_spans = self.get_dupl_ids(capture_dict[error], match_spans)
                    self.catch_errors(error, capture_dict[error], match[0], match_spans, match.start(), row)

            row += len(re.findall('\n', match[0]))
        if self.__errors__ != '':
            raise SyntaxError(self.__errors__)


def main():
    dpg.show_item('Analyzing')
    input_data = get_input_data()
    data_with_numering = '\n'.join([f'{index}\t{row}'
                                    for index, row
                                    in enumerate(input_data.split('\n'), 1)])
    dpg.set_value('input data', value=data_with_numering)
    try:
        engine: RegexAnalyze = RegexAnalyze()
        engine.analyze(input_data)
        dpg.configure_item('test', default_value=input_data, color=(0, 255, 0, 255))
    except BaseException as err:
        dpg.configure_item('test', default_value=f"Exception error during analyzing:\n{err}", color=(255, 0, 0, 255))


def initialize_lr2():
    with dpg.window(label="Лабораторная работа #2", tag='lr2', show=True, autosize=True, min_size=(1000, 800),
                    modal=True, pos=(480, 0),
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
        return dpg.get_value('Manually_text')
