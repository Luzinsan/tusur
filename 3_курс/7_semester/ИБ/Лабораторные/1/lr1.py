import dearpygui.dearpygui as dpg
import time


def set_path(sender, app_data):
    dpg.set_value('file', value=app_data['file_path_name'])


with dpg.file_dialog(directory_selector=False, show=False, callback=set_path, tag="file_dialog",
                     width=700, height=400, modal=True):
    # dpg.add_file_extension(".*")
    # dpg.add_file_extension("", color=(150, 255, 150, 255))
    # dpg.add_file_extension("Source files (*.cpp *.h *.hpp){.cpp,.h,.hpp}", color=(0, 255, 255, 255))
    # dpg.add_file_extension(".h", color=(255, 0, 255, 255), custom_text="[header]")
    # dpg.add_file_extension(".py", color=(0, 255, 0, 255), custom_text="[Python]")
    dpg.add_file_extension(".txt", color=(0, 255, 0, 255), custom_text="[Text]")


def decrypting(input_data, shift):
    decrypted_data = []
    for row in input_data:
        decrypted_data.append(''.join(encrypting_row(row, -shift)))
    return decrypted_data


def get_input_data():
    if dpg.get_value('input_method') == 'File':
        file_path = dpg.get_value('file')
        file = open(file_path, 'r', encoding="utf-8")
        input_data = file.readlines()
        is_multiline = '\n'
    else:
        input_data = dpg.get_value('Manually')
        is_multiline = ''

    input_data = [row.replace('ё', 'е').replace('Ё', 'Е').replace('\n', '') for row in input_data]
    return input_data, is_multiline


def encrypting_row(row, shift):
    cyrillic_lower = [chr(symbol) for symbol in range(ord('а'), ord('я') + 1)]
    cyrillic = [chr(symbol) for symbol in range(ord('А'), ord('Я') + 1)]
    latin_lower = [chr(symbol) for symbol in range(ord('a'), ord('z') + 1)]
    latin = [chr(symbol) for symbol in range(ord('A'), ord('Z') + 1)]
    sign = -1 if shift < 0 else 1
    shift = abs(shift)
    enc_row = []
    for symbol in row:
        if symbol in cyrillic_lower + cyrillic + latin_lower + latin:
            if symbol in cyrillic_lower:
                alphabetic = cyrillic_lower
            elif symbol in cyrillic:
                alphabetic = cyrillic
            elif symbol in latin_lower:
                alphabetic = latin_lower
            elif symbol in latin:
                alphabetic = latin
            shift_for_symbol = (shift % (len(alphabetic) - 1)) * sign
            index = (alphabetic.index(symbol) + shift_for_symbol) % (len(alphabetic))
            enc_row.append(alphabetic[index])
        else:
            enc_row.append(chr(ord(symbol) + (shift * sign)))
    return enc_row


def encrypting(sender, app_data, user_data):
    dpg.show_item('Caesar\'s cipher')
    input_data, is_multiline = get_input_data()

    dpg.set_value('input data', value=is_multiline.join(input_data))
    shift = dpg.get_value('shift')
    encrypted_data = []
    num_dots = 1
    dpg.configure_item('dots', color=(0, 0, 255, 255))
    fout = open('output.txt', 'a', encoding="utf-8")
    if type(input_data) is list:
        for row in input_data:
            time.sleep(0.1)
            encrypted_data.append(''.join(encrypting_row(row, shift)))
            dpg.set_value('dots', value='.  ' * num_dots)
            num_dots += 1
    else:
        encrypted_data = is_multiline.join(encrypting_row(input_data, shift))

    dpg.set_value('encrypted', value=is_multiline.join(encrypted_data))
    fout.writelines(is_multiline.join(encrypted_data) + '\n')
    # region test
    test = decrypting(encrypted_data, shift)
    dpg.set_value('test', value=is_multiline.join(test))
    if ''.join(input_data) == ''.join(test):
        dpg.configure_item('dots', default_value='True', color=(0, 255, 0, 255))
    else:
        dpg.configure_item('dots', default_value='False', color=(255, 0, 0, 255))
    # endregion


def switch_method(sender, method):
    dpg.hide_item('Caesar\'s cipher')
    dpg.show_item('shift')
    dpg.show_item('continue')
    if method == 'File':
        dpg.hide_item('Manually')
        dpg.show_item(method)
    else:
        dpg.hide_item('File')
        dpg.show_item(method)


with dpg.window(label="Лабораторная работа #1", tag='lr1', show=False, width=500, height=700, pos=(100, 100)):
    dpg.add_radio_button(tag='input_method',
                         items=["Manually", "File"],
                         callback=switch_method,
                         horizontal=True)
    dpg.add_input_int(tag='shift', label='Set Shift', default_value=1, show=False)
    dpg.add_input_text(label='Input Text', tag='Manually', show=False,
                       default_value='абвэюя')
    with dpg.group(horizontal=True, show=False, tag='File'):
        dpg.add_input_text(tag='file',
                           default_value='/home/luzinsan/Documents/TUSUR_learn/3_курс/7_semester/ИБ/Лабораторные/1/test.txt')
        dpg.add_button(label='Select Path Manually', callback=lambda: dpg.show_item("file_dialog"))
    dpg.add_button(label='Continue: Caesar\'s cipher', callback=encrypting, show=False, tag='continue')
    with dpg.group(tag='Caesar\'s cipher', show=False):
        dpg.add_text(tag='input data', label='Input Data', show_label=True)
        dpg.add_separator()
        dpg.add_text(tag='encrypted', label='Encrypted Message', show_label=True)
        dpg.add_separator()
        dpg.add_text(tag='test', label='Test', show_label=True)
        dpg.add_separator()
        dpg.add_text(tag='dots', color=(0, 0, 255, 255))

