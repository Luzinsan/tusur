from initialize import *
import numpy as np
import time
from numpy.polynomial import Polynomial
from collections import deque
from constant import S_BOX, R_CON, INV_S_BOX, MATRIX_ENC, MATRIX_DEC, \
    Nb, Nr, Nk

encoding_key, encoding_text = 'utf-8', 'utf-8'
sleeping = 0.0001


def get_input_data():
    if dpg.get_value('input_method') == 'File':
        file_path = dpg.get_value('file')
        file = open(file_path, 'r', encoding="utf-8")
        input_data = file.read()
    else:
        input_data = dpg.get_value('Manually')
    return input_data


def split_to_blocks(input_data, by_bytes):
    original_length = len(input_data)
    input_data = input_data.encode(encoding=encoding_text)
    blocks = []
    for i in range(0, len(input_data), by_bytes):
        block = np.array(list(input_data[i:i + by_bytes]))
        if len(block) < by_bytes:
            block = np.append(block, [0x01] * (by_bytes - len(block)))
        block = block.reshape((4, by_bytes // 4)).transpose()
        blocks.append(block)
    return np.array(blocks), original_length


def decrypt(cipher_data, key, text_length):
    print("\n\t\t\tDecrypting\n")
    decrypted_data = ''
    try:
        blocks, _ = split_to_blocks(cipher_data, 16)
        key_schedule = key_expansion(key)
        num_dots = 1
        dpg.configure_item('dots', color=(0, 0, 255, 255))
        for block in blocks:
            # initializing
            print('Start block:\n', block)
            state = add_round_key(block, key_schedule[:, Nr * Nb:Nb * (Nr + 1)])
            for round in range(Nr - 1, 0, -1):
                time.sleep(sleeping)
                state = shift_rows(state, invert=True)
                state = sub_bytes_state(state, inverse=True)
                state = add_round_key(state, key_schedule[:, round * Nb:(round + 1) * Nb])
                state = mix_columns(state, MATRIX_DEC)
                dpg.set_value('dots', value='Decrypting: ' + '.  ' * num_dots)
                num_dots += 1
            state = shift_rows(state, invert=True)
            state = sub_bytes_state(state, inverse=True)
            state = add_round_key(state, key_schedule[:, :Nb])
            print('Finish of handling a block:\n', state)
            state = state.transpose()
            decrypted_data += str(bytes(list(state.flatten())), encoding=encoding_text)
        return decrypted_data[:text_length]
    except:
        return "Error in decrypting"


def sub_bytes(orig, inverse=False):
    """
    Нелинейная замена байтов массива orig
    на соответствующее значение из box
    Вычисление элемента: 4 старших бита - индекс строки в box
                         4 младших бита - индекс столбца в box

    :param inverse:
    :param orig: исходный массив
    :param box: 8-битная таблица шифрования
    :return: массив с сопоставленными значениями из box
    """
    box = INV_S_BOX if inverse else S_BOX
    return np.vectorize(lambda item: box[16 * (item // 0x10) +
                                         (item % 0x10)])(orig)


def sub_bytes_state(state, inverse=False):
    return np.vectorize(sub_bytes)(state, inverse=inverse)


# Сдвиг элементов массива на указанное количество ячеек
def rot_word(word: np.array, rotnumber=-1):
    rot = deque(word)
    rot.rotate(rotnumber)
    return np.array(rot)


# Создание раундовых ключей (Round Keys)
def key_expansion(key):
    key_schedule = np.array(list(key.encode(encoding=encoding_key)))
    if len(key_schedule) < (Nk * 4):  # Расширение до Nk байт
        key_schedule = np.append(key_schedule, [0x01] * ((Nk * 4) - len(key_schedule)))
    elif len(key_schedule) > (Nk * 4):
        key_schedule = key_schedule[:Nk * 4]
    key_schedule = key_schedule.reshape((4, Nk)).transpose()
    for col in range(Nk, Nb * (Nr + 1)):  # Дополняем оставшиеся строки таблицы ключей
        temp = key_schedule[:, col - 1]
        if col % Nk == 0:
            temp = sub_bytes(rot_word(temp)) ^ np.array(R_CON[col // Nk])
        elif (Nk > 6) and (col % Nk == 4):
            temp = sub_bytes(temp)
        temp = key_schedule[:, col - Nk] ^ temp
        key_schedule = np.insert(key_schedule, col,
                                 np.array(temp), axis=1)
    return key_schedule


def add_round_key(state, key_schedule):
    return state ^ key_schedule


def shift_rows(state, invert=False):
    direction = 1 if invert else -1
    new_state = state.copy()
    for index, row in enumerate(new_state):
        new_state[index] = rot_word(row, index * direction)
    return new_state


def mult_bytes(byte1, byte2):
    poly1 = Polynomial(list(map(int, list(f'{byte1:0>8b}')[::-1])))
    poly2 = Polynomial(list(map(int, list(f'{byte2:0>8b}')[::-1])))
    polynom_GF = [0x01, 0x00, 0x00, 0x00, 0x01, 0x01, 0x00, 0x01, 0x01]

    def default_list(sequence):
        sequence = map(abs, map(int, sequence))
        return list(sequence)

    mult_polys = np.bitwise_and(default_list((poly1 * poly2).coef[::-1]), 1)
    _, poly_res = np.polydiv(mult_polys, polynom_GF)
    poly_res = np.bitwise_and(default_list(poly_res), 1)
    byte_res = int(''.join(map(str, poly_res)), 2)
    return byte_res


def mix_columns(state, matrix):
    new_state = state.copy()
    for col in range(state.shape[1]):
        new_state[:, col] = [np.bitwise_xor.reduce([mult_bytes(state[index][col], matrix[row][index])
                                                    for index
                                                    in range(len(matrix[0]))])
                             for row
                             in range(len(matrix))]
    return new_state


# Алгоритм обрабатывает блоки по 128-бит,
# шифруя блок симметричным секретным ключом key (128 бит)
def encrypt(input_data, key):
    np.set_printoptions(formatter={'int': hex})
    encrypted_data = ''
    try:
        blocks, text_length = split_to_blocks(input_data, 16)
        key_schedule = key_expansion(key)
        num_dots = 1
        dpg.configure_item('dots', color=(0, 0, 255, 255))
        for block in blocks:
            print('\tBlock:\n', block)
            # initializing
            state = add_round_key(block, key_schedule[:, :Nb])
            for round in range(1, Nr):
                time.sleep(sleeping)
                state = sub_bytes_state(state)
                state = shift_rows(state)
                state = mix_columns(state, MATRIX_ENC)
                state = add_round_key(state, key_schedule[:, round * Nb:(round + 1) * Nb])
                dpg.set_value('dots', value='Encrypting: ' + '.  ' * num_dots)
                num_dots += 1
            state = sub_bytes_state(state)
            state = shift_rows(state)
            state = add_round_key(state, key_schedule[:, Nr * Nb:(Nr + 1) * Nb])
            print('Finish of handling a block:\n', state)
            state = state.transpose()
            encrypted_data += str(bytes(list(state.flatten())), encoding=encoding_text)
        return encrypted_data, text_length
    except:
        return "Error in encrypting", 0


def preparing(sender, app_data, user_data):
    global encoding_key, encoding_text
    encoding_key, encoding_text = dpg.get_value('encoding_key'), dpg.get_value('encoding_text')
    dpg.show_item('Cipher method')
    input_data = get_input_data()
    dpg.set_value('input data', value=input_data)
    # длина ключа = 128/192/256 бит
    key = dpg.get_value('key')
    ciphertext, text_length = encrypt(input_data, key)
    dpg.set_value('encrypted', value=ciphertext)
    fout = open('output.txt', 'a', encoding=encoding_text)
    fout.writelines("\n\n\tPlaintext:\n" + input_data + "\n\tCiphertext:\n" + ciphertext)
    fout.close()
    # region test
    decrypttext = decrypt(ciphertext, key, text_length)
    dpg.set_value('test', value=decrypttext)
    if ''.join(input_data) == ''.join(decrypttext):
        dpg.configure_item('dots', default_value='True', color=(0, 255, 0, 255))
    else:
        dpg.configure_item('dots', default_value='False', color=(255, 0, 0, 255))
    # endregion


def set_encoding_key(sender, add_data, _):
    global encoding_key
    encoding_key = add_data


def set_encoding_text(sender, add_data, _):
    global encoding_text
    encoding_text = add_data


def initialize_lr2():
    with dpg.window(label="Лабораторная работа #2", tag='lr2', show=True, width=500, height=700, pos=(100, 100),
                    on_close=lambda: dpg.delete_item('lr2')):
        initialize()
        dpg.add_input_text(tag='key', label='Key', default_value='passwordfbsfv', show=False, before='Manually')
        encoding_items = ['cp866', 'utf-8', 'utf-16', 'latin-1', 'ascii', 'cp1253']
        dpg.add_combo(items=encoding_items, label='Encoding for key', tag='encoding_key', show=True,
                      default_value='cp866', callback=set_encoding_key, before='Cipher method')
        dpg.add_combo(items=encoding_items, label='Encoding for plaintext', tag='encoding_text', show=True,
                      default_value='cp866', callback=set_encoding_text, before='Cipher method')
        dpg.add_button(label="Continue: AES", callback=preparing, show=False, tag='continue')
