import openpyxl

file_path_LL: str = "LL"
dict_LL = dict()
wb = openpyxl.Workbook()
list_ods: openpyxl.Workbook = wb.create_sheet("List1", 0)
list_ods.append(('ПРАВИЛО', "START0"))

with open(file_path_LL) as file:
    index = 0
    for row in file.readlines():
        if len(list_splitted := row.split(" ->")) == 2:
            left, right = list_splitted
            rules = {}
            for rule in right.split('|'):
                rule = rule.strip()
                rules.update({index: rule})
                state0 = "∅" if rule[0].isupper() else rule.split(" ")[0]
                list_ods.append((f"{left} -> {rule}", state0))
                index += 1
            dict_LL[left] = rules
            # print(rules)
# print(dict_LL)


def is_equal_cols(rows: int, worksheet: openpyxl.Workbook, compare_col1: int, compare_col2: int) -> bool:
    for row in range(2, rows+1):
        # print(f"compare: {worksheet.cell(row=row, column=compare_col1).value} with { worksheet.cell(row=row, column=compare_col2).value}")
        if worksheet.cell(row=row, column=compare_col1).value != worksheet.cell(row=row, column=compare_col2).value:
            return False
    # print("Columns is equal!")
    return True


col = 2
num_rows_sheet = 0
while True:
    list_ods.cell(row=1, column=col + 1, value=f"START{col-1}")
    # print(f"-----------------------ITERATION: {check}------------------------")
    for key in dict_LL.keys():
        # print(f"\n\t\tkey:{key}\tvalues:{dict_LL[key]}")
        for index, rule in dict_LL[key].items():
            new_starts = []
            if rule[0].isupper():
                key_start = rule.split(" ")[0]
                # print(f"key_start:{key_start}")
                # print(f"from rules: {dict_LL[key_start]}")
                for start_index_row in dict_LL[key_start].keys():
                    # print("start_index: ", start_index_row)
                    new_starts.append(list_ods.cell(row=start_index_row+2, column=col).value)
                    # print("new_starts: ", new_starts)
                new_starts = list(filter('∅'.__ne__, new_starts))
                if len(new_starts) == 0:
                    new_starts.append('∅')
            else:
                new_starts = [list_ods.cell(row=index + 2, column=col).value]

            list_ods.cell(row=index + 2, column=col+1, value=" ".join(new_starts))
            num_rows_sheet = index + 2
            # print("\t\t\tResulting new_starts: ", new_starts)
    if is_equal_cols(num_rows_sheet, list_ods, col, col+1):
        break
    col += 1

wb.save('LL.xlsx')

