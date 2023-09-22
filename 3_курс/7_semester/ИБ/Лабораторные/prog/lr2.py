from initialize import *
import time
import numpy as np
from collections import deque
from constant import S_BOX, R_CON, INV_S_BOX, \
                     Nb, Nr, Nk


def get_input_data():
    if dpg.get_value('input_method') == 'File':
        file_path = dpg.get_value('file')
        file = open(file_path, 'r', encoding="utf-8")
        input_data = file.readlines()
    else:
        input_data = dpg.get_value('Manually')
    return input_data


def split_to_blocks(input_data, by_bytes):
    original_length = len(input_data)
    input_data = input_data.encode(encoding='utf-8')
    blocks = []
    for i in range(0, len(input_data), by_bytes):
        block = np.array(list(input_data[i:i + by_bytes]))
        if len(block) < by_bytes:
            block = np.append(block, [0x01] * (by_bytes - len(block)))
        block = block.reshape((4, by_bytes // 4)).transpose()
        blocks.append(block)
        # block = block.transpose()
        # print(str(bytes(list(block.flatten())), 'utf-8'))
    return np.array(blocks), original_length


def decrypt(cipher_data, key):
    decrypted_data = []
    blocks, text_length = split_to_blocks(cipher_data, 16)
    for i in range(len(blocks)):
        decrypted_data.append(decrypt_block(blocks[i], key))
    # for row in input_data:
    # decrypted_data.append(''.join(encrypting_row(row, -shift, area_alphabetic)))
    return decrypted_data


def encrypt_block(block, key):
    return block


def decrypt_block(block, key):
    return block


def sub_bytes(orig, box=S_BOX):
    """
    Нелинейная замена байтов массива orig
    на соответствующее значение из box
    Вычисление элемента: 4 старших бита - индекс строки в box
                         4 младших бита - индекс столбца в box

    :param orig: исходный массив
    :param box: 8-битная таблица шифрования
    :return: массив с сопоставленными значениями из box
    """
    return np.vectorize(lambda item: box[16 * (item // 0x10) +
                                              (item % 0x10)])(orig)


def sub_bytes_state(state):
    return np.vectorize(sub_bytes)(state)


# Сдвиг элементов массива на указанное количество ячеек
def rot_word(word: np.array, rotnumber=-1):
    rot = deque(word)
    rot.rotate(rotnumber)
    return np.array(rot)


# Создание раундовых ключей (Round Keys)
def key_expansion(key):
    key_schedule = np.array(list(key.encode('utf-8')))
    if len(key_schedule) < (Nk*4):  # Расширение до Nk байт
        key_schedule = np.append(key_schedule, [0x01] * ((Nk*4) - len(key_schedule)))
    key_schedule = key_schedule.reshape((4, Nk)).transpose()
    for col in range(Nk, Nb * (Nr + 1)):  # Дополняем оставшиеся строки таблицы ключей
        temp = key_schedule[:, col-1]
        if col % Nk == 0:
            temp = sub_bytes(rot_word(temp)) ^ np.array(R_CON[col // Nk])
        else:
            temp = sub_bytes(temp)
        temp = key_schedule[:, col-Nk] ^ temp
        key_schedule = np.insert(key_schedule, col,
                                 np.array(temp), axis=1)
    return key_schedule


def add_round_key(state, key_schedule):
    # print('state: ', state)
    return state ^ key_schedule


def shift_rows(state):
    new_state = state.copy()
    for index, row in enumerate(new_state):
        new_state[index] = rot_word(row, -index)
    return new_state

def mix_columns():
    pass


# Алгоритм обрабатывает блоки по 128-бит,
# шифруя блок симметричным секретным ключом key (128 бит)
def encrypt(input_data, key):
    encrypted_data = []
    blocks, text_length = split_to_blocks(input_data, 16)
    key_schedule = key_expansion(key)
    for block in blocks:
        # initializing
        state = add_round_key(block, key_schedule[:, :Nb])
        for round in range(1):
            state = sub_bytes_state(state)
            state = shift_rows(state)
        # encrypted_data.append(encrypt_block(block, key))

    # num_dots = 1
    # dpg.configure_item('dots', color=(0, 0, 255, 255))
    return encrypted_data


def md5(password):
    return password


def keyexpansion(hash):
    return hash


def preparing(sender, app_data, user_data):
    dpg.show_item('Cipher method')
    input_data = get_input_data()
    dpg.set_value('input data', value=input_data)
    key = dpg.get_value('key')

    # длина ключа = 128/192/256 бит
    if True:  # полученный ключ - password
        hash = md5(key)
        key = keyexpansion(hash)
    encrypted_data = encrypt(input_data, key)

    dpg.set_value('encrypted', value=encrypted_data)
    fout = open('output.txt', 'a', encoding="utf-8")
    fout.writelines(encrypted_data)
    fout.close()
    # region test
    # test = decrypt(encrypted_data, key)
    # dpg.set_value('test', value=test)
    # if ''.join(input_data) == ''.join(test):
    #     dpg.configure_item('dots', default_value='True', color=(0, 255, 0, 255))
    # else:
    #     dpg.configure_item('dots', default_value='False', color=(255, 0, 0, 255))
    # endregion


def initialize_lr2():
    with dpg.window(label="Лабораторная работа #2", tag='lr2', show=True, width=500, height=700, pos=(100, 100),
                    on_close=lambda: dpg.delete_item('lr2')):
        initialize()
        dpg.add_button(label="Continue: AES", callback=preparing, show=False, tag='continue')
