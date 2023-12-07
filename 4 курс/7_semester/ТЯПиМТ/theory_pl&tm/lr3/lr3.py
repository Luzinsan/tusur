import dearpygui.dearpygui as dpg
import regex as re
from __init__ import initialize
from openpyxl import load_workbook
import openpyxl
from enum import IntEnum


class LL:
    ws: openpyxl.worksheet.worksheet.Worksheet

    class Column(IntEnum):
        TERMS = 2
        JUMP = 3
        ACCEPT = 4
        STACK = 5
        RETURN = 6
        ERROR = 7

    def open_parse_table(self, file_parse_table: str):
        try:
            wb = load_workbook(filename=file_parse_table, read_only=True)
            self.ws = wb['parse_table']
        except BaseException as err:
            raise FileNotFoundError(err)

    # region Generate parse table
    class ParseTable:
        wb: openpyxl.Workbook = openpyxl.Workbook()
        ws: openpyxl.worksheet.worksheet.Worksheet
        parse_table: openpyxl.worksheet.worksheet.Worksheet
        dict_LL = dict()
        dict_M = dict()
        start_col: int
        follow_col: int
        num_rows: int

        def __init__(self):
            self.ws = self.wb.create_sheet("parse_table", 0)
            self.ws.append(('ПРАВИЛО', "START0"))

        def generate_parse_table(self, file_grammar: str):
            self.parse_raw_rules(file_grammar)
            self.find_start_nodes()
            self.find_follow_nodes()
            self.find_direction_nodes()
            self.find_jumps()
            file_grammar = 'LL'
            self.wb.save(f"{file_grammar}.xlsx")

        @staticmethod
        def is_nonterm(s): return s[0].isupper()

        def parse_raw_rules(self, file_grammar):
            try:
                with open(file_grammar) as file:
                    index = 0
                    for row in file.readlines():
                        if len(list_splitted := row.split(" ->")) == 2:
                            left, right = list_splitted
                            rules = {}
                            for rule in right.split('|'):
                                rule = rule.strip()
                                rules.update({index: rule})
                                state0 = "∅" if LL.ParseTable.is_nonterm(rule) \
                                    else rule.split(" ")[0]
                                self.ws.append((f"{left} -> {rule}", state0))
                                index += 1
                            self.dict_LL[left] = rules
            except BaseException as err:
                raise FileExistsError(err)

        @staticmethod
        def is_equal_cols(rows: int, worksheet: openpyxl.worksheet.worksheet.Worksheet,
                          compare_col1: int, compare_col2: int) -> bool:
            for row in range(2, rows + 1):
                if worksheet.cell(row=row, column=compare_col1).value != worksheet.cell(row=row, column=compare_col2).value:
                    return False
            return True

        def find_start_nodes(self):
            self.start_col = 2
            self.num_rows = 0
            while True:
                self.ws.cell(row=1, column=self.start_col + 1, value=f"START{self.start_col - 1}")
                for key in self.dict_LL.keys():
                    for index, rule in self.dict_LL[key].items():
                        new_starts = []
                        if LL.ParseTable.is_nonterm(rule):
                            key_start = rule.split(" ")[0]
                            for start_index_row in self.dict_LL[key_start].keys():
                                new_starts.append(self.ws.cell(row=start_index_row + 2, column=self.start_col).value)
                            new_starts = list(filter('∅'.__ne__, new_starts))
                            if len(new_starts) == 0:
                                new_starts.append('∅')
                        else:
                            new_starts = [self.ws.cell(row=index + 2, column=self.start_col).value]
                        self.ws.cell(row=index + 2, column=self.start_col + 1, value=" ".join(new_starts))
                        self.num_rows = index + 2
                if LL.ParseTable.is_equal_cols(self.num_rows, self.ws, self.start_col, self.start_col + 1):
                    break
                self.start_col += 1

        def review_next(self, key, nodes, index_node, follows, base_col):
            try:
                next_node = nodes[index_node + 1]
                # итерация по правилам следующего узла для поиска его символов-предсшественников
                for start_index_row in self.dict_LL[next_node].keys():
                    start_terms: list = self.ws.cell(row=start_index_row + 2, column=self.start_col).value.split(" ")
                    if 'e' in start_terms:
                        start_terms.remove('e')
                        follows += self.review_next(key, nodes, index_node + 1, follows, base_col)
                    else:
                        follows += start_terms
            except IndexError as _:
                follows += self.ws.cell(row=min(self.dict_LL[key].keys()) + 2, column=base_col).value.split(" ")
            except KeyError as _:
                follows.append(next_node)
            return list(set(follows))

        def put_follows(self, col: int):
            self.ws.cell(row=1, column=col, value=f"FOLLOWS{col - self.start_col - 1}")
            # итерация по нетерминалам
            for key in self.dict_LL.keys():
                # итерация по правилам нетерминала
                for index_rule, rule in self.dict_LL[key].items():
                    nodes = rule.split(" ")
                    # итерация по терминальным и нетерминальным узлам
                    for index_node, node in enumerate(nodes):
                        # для каждого нетерминала определяем последующие узлы
                        if LL.ParseTable.is_nonterm(node):
                            old_follows = self.ws.cell(row=min(self.dict_LL[node].keys()) + 2, column=col).value
                            follows = old_follows.split(" ") if old_follows else []
                            follows = self.review_next(key, nodes, index_node, follows, col)
                            self.ws.cell(row=min(self.dict_LL[node].keys()) + 2, column=col, value=" ".join(follows))

        def find_follow_nodes(self):
            self.start_col += 1
            self.follow_col = self.start_col + 1
            for key in self.dict_LL.keys():
                self.ws.merge_cells(start_row=min(self.dict_LL[key].keys()) + 2, start_column=self.follow_col,
                                    end_row=max(self.dict_LL[key].keys()) + 2, end_column=self.follow_col)
            self.ws.cell(row=2, column=self.follow_col, value="⊥")

            self.put_follows(self.follow_col)
            self.follow_col += 1
            while True:
                for key in self.dict_LL.keys():
                    self.ws.merge_cells(start_row=min(self.dict_LL[key].keys()) + 2, start_column=self.follow_col,
                                         end_row=max(self.dict_LL[key].keys()) + 2, end_column=self.follow_col)
                    old_value = self.ws.cell(row=min(self.dict_LL[key].keys()) + 2, column=self.follow_col - 1).value
                    self.ws.cell(row=min(self.dict_LL[key].keys()) + 2, column=self.follow_col, value=old_value)
                self.put_follows(self.follow_col)
                if LL.ParseTable.is_equal_cols(self.num_rows, self.ws, self.follow_col - 1, self.follow_col):
                    break
                self.follow_col += 1

        def next_starts(self, key, starts, nodes, index_node):
            try:
                next_node = nodes[index_node + 1]
                for start_index_row in self.dict_LL[next_node].keys():
                    starts += self.ws.cell(row=start_index_row + 2, column=self.start_col).value.split(" ")
                    if 'e' in starts:
                        starts.remove("e")
                        starts = self.next_starts(key, starts, nodes, index_node + 1)
            except IndexError as _:
                starts += self.ws.cell(row=min(self.dict_LL[key].keys()) + 2, column=self.follow_col).value.split(" ")
            except KeyError as _:
                starts.append(next_node)
            return starts

        @staticmethod
        def is_last_node(current_index, rule_nodes):
            try:
                if rule_nodes[current_index + 1]:
                    return False
            except IndexError as _:
                return True

        def find_direction_nodes(self):
            self.ws.cell(row=1, column=self.follow_col + 1, value="DIRECTIONS")
            self.parse_table = self.wb.create_sheet("parse_table", 1)
            self.parse_table.append(('НЕТЕРМИНАЛЫ', "terminals", "jump", "accept", "stack", "return", "error"))
            index_term = 1
            for key in self.dict_LL.keys():
                index_term = self.find_left_direction_nodes(key, index_term)
                self.find_right_direction_nodes(key, index_term, index_term - 1)

        def find_left_direction_nodes(self, key, index_term):
            for index in self.dict_LL[key].keys():
                index_term += 1
                direction_terms: list = self.ws.cell(row=index + 2, column=self.start_col).value.split(" ")
                if 'e' in direction_terms:
                    direction_terms.remove("e")
                    follow_e = self.ws.cell(row=min(self.dict_LL[key].keys()) + 2, column=self.follow_col).value.split(" ")
                    direction_terms += follow_e
                self.ws.cell(row=index + 2, column=self.follow_col + 1, value=" ".join(direction_terms))
                self.dict_M.update({(key, index_term): {}})
                self.parse_table.append(
                    ("left: " + key, " ".join(direction_terms), "", "False", "False", "False", "False"))
            self.parse_table.cell(row=index_term, column=7, value="True")
            return index_term

        def find_right_direction_nodes(self, key, index_term, last_left_term):
            for index_rule, rule in self.dict_LL[key].items():
                nodes = rule.split(" ")
                # итерация по терминальным и нетерминальным узлам
                for index_node, node in enumerate(nodes):
                    index_term += 1
                    # для каждого нетерминала определяем направляющие узлы
                    accept = "False"
                    stack = "False"
                    if LL.ParseTable.is_nonterm(node):
                        stack = str(not LL.ParseTable.is_last_node(index_node, nodes))
                        starts = []
                        for start_index_row in self.dict_LL[node].keys():
                            starts += self.ws.cell(row=start_index_row + 2, column=self.start_col).value.split(" ")
                            if 'e' in starts:
                                starts.remove("e")
                                starts = self.next_starts(key, starts, nodes, index_node)
                    elif node == 'e':
                        starts = self.ws.cell(row=min(self.dict_LL[key].keys()) + 2, column=self.follow_col).value.split(" ")
                    else:
                        starts = [node]
                        accept = "True"
                    global_index_rule = index_rule - min(self.dict_LL[key].keys())
                    self.dict_M[(key, last_left_term - len(self.dict_LL[key]) + 2 + global_index_rule)].update(
                        {index_term: node})
                    self.parse_table.append(("right: " + node, " ".join(starts), "", accept, stack, "False", "True"))

        def find_jumps(self):
            for key, values in self.dict_M.items():
                self.parse_table.cell(row=key[1], column=3, value=min(values.keys()))
                for index_node, node in values.items():
                    if LL.ParseTable.is_nonterm(node):
                        for root_key in self.dict_M.keys():
                            if root_key[0] == node:
                                self.parse_table.cell(row=index_node, column=3, value=root_key[1])
                                break
                    else:
                        try:
                            next_node = values[index_node + 1]
                            self.parse_table.cell(row=index_node, column=3, value=index_node + 1)
                        except KeyError as _:
                            self.parse_table.cell(row=index_node, column=3, value=0)
                            self.parse_table.cell(row=index_node, column=6, value="True")
    # endregion

    def parse_value(self, row, name_col: Column):
        return self.ws.cell(row=row, column=name_col).value

    def analyze(self, input_string: str):
        input_string = input_string.split(" ")
        i = 2
        k = 0
        Stack = [0]
        while True:
            if input_string[k] in self.parse_value(i, LL.Column.TERMS).split(" "):
                if self.parse_value(i, LL.Column.ACCEPT) == 'True':
                    k += 1
                if self.parse_value(i, LL.Column.STACK) == "True":
                    Stack.append(i + 1)
                if self.parse_value(i, LL.Column.RETURN) == "True":
                    i = Stack.pop()
                    if i == 0:
                        break
                    else:
                        continue
                else:  # LL.Column.JUMP
                    i = self.parse_value(i, LL.Column.JUMP)
            elif self.parse_value(i, LL.Column.ERROR) == "False":
                i += 1
            else:
                break
        if len(Stack) == 0 and input_string[k] == '⊥':
            return "SUCCESS PARSED!"
        else:
            raise SyntaxError(f"FAILED PARSED! at: {k} - {input_string[k]}")


def main():
    dpg.show_item('Analyzing')
    input_data = get_input_data()
    data_with_numering = '\n'.join([f'{index}\t{row}'
                                    for index, row
                                    in enumerate(input_data.split('\n'), 1)])
    dpg.set_value('input data', value=data_with_numering)
    try:
        engine: LL = LL()
        parse_table = LL.ParseTable()
        parse_table.generate_parse_table("lr3/test1")
        engine.open_parse_table(dpg.get_value('file_grammar'))
        engine.analyze(input_data)
        dpg.configure_item('test', default_value=input_data, color=(0, 255, 0, 255))
    except BaseException as err:
        dpg.configure_item('test', default_value=f"Exception error during analyzing:\n{err}", color=(255, 0, 0, 255))


def initialize_lr3():
    with dpg.window(label="Лабораторная работа #3", tag='lr3', show=True, autosize=True, min_size=(1000, 800),
                    pos=(480, 0), on_close=lambda: dpg.delete_item('lr3')):
        initialize()
        dpg.configure_item('file_grammar', default_value='lr3/LL.xlsx')
        # dpg.configure_item('file_parse_table', default_value='lr3/LL')
        dpg.configure_item('input_file', default_value='lr3/test.txt')
        dpg.add_button(label="Analyze", callback=main, show=False, tag='continue')


def get_input_data():
    if dpg.get_value('input_method') == 'File':
        file_path = dpg.get_value('input_file')
        file = open(file_path, 'r')
        input_data = ''.join(file.readlines())
        file.close()
        return input_data
    else:
        return dpg.get_value('Manually_text')
