import re
import time
from initialize import *


def decrypting(input_data, shift, area_alphabetic):
    decrypted_data = []
    for row in input_data:
        decrypted_data.append(''.join(encrypting_row(row, -shift, area_alphabetic)))
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


def get_alphabet_area():
    falphabets = open('alphabetic.txt', 'r', encoding="utf-8")
    alphabet_area = falphabets.readlines()
    alphabets = {}
    for item in alphabet_area:
        item = item[:3]
        alphabets[item] = tuple(chr(symbol)
                                for symbol in range(ord(item[0]), ord(item[-1]) + 1))
    falphabets.close()
    return alphabets


def encrypting_row(row, shift, area_alphabetic):
    combined_pattern = [f'[{pattern}]' for pattern in area_alphabetic.keys()]
    sign = -1 if shift < 0 else 1
    shift = abs(shift)
    enc_row = []
    for symbol in row:
        index_alphabetic = ''.join([pattern[1:-1]
                            for pattern in combined_pattern
                            if re.search(pattern, symbol)])
        if index_alphabetic:
            alphabetic = area_alphabetic[index_alphabetic]
            shift_for_symbol = (shift % (len(alphabetic) - 1)) * sign
            index = (alphabetic.index(symbol) + shift_for_symbol) % (len(alphabetic))
            enc_row.append(alphabetic[index])
        else:
            enc_row.append(symbol)
    return enc_row


def encrypting(sender, app_data, user_data):
    dpg.show_item('Cipher method')
    input_data, is_multiline = get_input_data()

    dpg.set_value('input data', value=is_multiline.join(input_data))
    shift = dpg.get_value('key')
    encrypted_data = []
    num_dots = 1
    dpg.configure_item('dots', color=(0, 0, 255, 255))
    area_alphabetic = get_alphabet_area()
    if type(input_data) is list:
        for row in input_data:
            time.sleep(0.1)
            encrypted_data.append(''.join(encrypting_row(row, shift, area_alphabetic)))
            dpg.set_value('dots', value='.  ' * num_dots)
            num_dots += 1
    else:
        encrypted_data = is_multiline.join(encrypting_row(input_data, shift, area_alphabetic))

    dpg.set_value('encrypted', value=is_multiline.join(encrypted_data))
    fout = open('output.txt', 'a', encoding="utf-8")
    fout.writelines(is_multiline.join(encrypted_data) + '\n')
    fout.close()
    # region test
    test = decrypting(encrypted_data, shift, area_alphabetic)
    dpg.set_value('test', value=is_multiline.join(test))
    if ''.join(input_data) == ''.join(test):
        dpg.configure_item('dots', default_value='True', color=(0, 255, 0, 255))
    else:
        dpg.configure_item('dots', default_value='False', color=(255, 0, 0, 255))
    # endregion


def initialize_lr1():
    with dpg.window(label="Лабораторная работа #1", tag='lr1', show=True, width=500, height=700, pos=(100, 100),
                    on_close=lambda: dpg.delete_item('lr1')):
        initialize()
        dpg.add_input_int(tag='key', label='Key', default_value=1, show=False, before='Manually')
        dpg.add_button(label="Continue: 'Caesar\'s cipher", callback=encrypting, show=False, tag='continue')
