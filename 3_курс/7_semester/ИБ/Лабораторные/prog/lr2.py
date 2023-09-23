from initialize import *
import time
import numpy as np
from numpy.polynomial import Polynomial
from collections import deque
from constant import S_BOX, R_CON, INV_S_BOX, MATRIX_ENC, MATRIX_DEC, \
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
    input_data = input_data.encode(encoding='latin-1')
    # input_data = [0x39, 0x25, 0x84, 0x1d, 0x02, 0xdc, 0x09, 0xfb, 0xdc, 0x11, 0x85, 0x97, 0x19, 0x6a, 0x0b, 0x32]
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


def decrypt(cipher_data, key, text_length):
    print("\n\t\t\tDecrypting\n")
    decrypted_data = ''
    blocks, _ = split_to_blocks(cipher_data, 16)
    key_schedule = key_expansion(key)
    for block in blocks:
        # initializing
        print('Start block:\n', block)
        # print("+ round key:\n", key_schedule[:, Nr * Nb:Nb * (Nr + 1)])
        state = add_round_key(block, key_schedule[:, Nr * Nb:Nb * (Nr + 1)])
        # print("after initializing:\n", state)
        for round in range(Nr-1, 0, -1):
            # print(f'start of round#{round}:\n{state}')
            state = shift_rows(state, invert=True)
            # print('after ShiftRows:\n', state)
            state = sub_bytes_state(state, inverse=True)
            # print('after SubBytes:\n', state)
            # print('+ RoundKey:\n', key_schedule[:, Nb * round: Nb * (round + 1)])
            state = add_round_key(state, key_schedule[:, round * Nb:(round + 1) * Nb])
            # print('after AddRoundKey:\n', state)
            state = mix_columns(state, MATRIX_DEC)
            # print('after MixColumns:\n', state)
        # print(f'start of the last iteration:\n{state}')
        state = shift_rows(state, invert=True)
        # print('after ShiftRows:\n', state)
        state = sub_bytes_state(state, inverse=True)
        # print('after SubBytes:\n', state)
        # print('+ RoundKey:\n', key_schedule[:, :Nb])
        state = add_round_key(state, key_schedule[:, :Nb])
        print('Finish of handling a block:\n', state)
        state = state.transpose()
        decrypted_data += str(bytes(list(state.flatten())), 'latin-1')
    # num_dots = 1
    # dpg.configure_item('dots', color=(0, 0, 255, 255))
    return decrypted_data[:text_length]


def encrypt_block(block, key):
    return block


def decrypt_block(block, key):
    return block


def sub_bytes(orig, inverse=False):
    """
    Нелинейная замена байтов массива orig
    на соответствующее значение из box
    Вычисление элемента: 4 старших бита - индекс строки в box
                         4 младших бита - индекс столбца в box

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
    # key = np.array([0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c])
    # key_schedule = np.array(key)
    key_schedule = np.array(list(key.encode('utf-8')))
    if len(key_schedule) < (Nk * 4):  # Расширение до Nk байт
        key_schedule = np.append(key_schedule, [0x01] * ((Nk * 4) - len(key_schedule)))
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
    blocks, text_length = split_to_blocks(input_data, 16)
    key_schedule = key_expansion(key)
    for block in blocks:
        print('\tBlock:\n', block)
        # initializing
        # print('Start block:\n', block)
        # print("+ round key:\n", key_schedule[:, :Nb])
        state = add_round_key(block, key_schedule[:, :Nb])
        # print("after initializing:\n", state)
        for round in range(1, Nr):
            # print(f'start of round#{round}:\n{state}')
            state = sub_bytes_state(state)
            # print('after SubBytes:\n', state)
            state = shift_rows(state)
            # print('after ShiftRows:\n', state)
            state = mix_columns(state, MATRIX_ENC)
            # print('after MixColumns:\n', state)
            # print('+ RoundKey:\n', key_schedule[:, round*Nb:(round+1)*Nb])
            state = add_round_key(state, key_schedule[:, round*Nb:(round+1)*Nb])
        # print(f'start of the last iteration:\n{state}')
        state = sub_bytes_state(state)
        # print('after SubBytes:\n', state)
        state = shift_rows(state)
        # print('after ShiftRows:\n', state)
        # print('+ RoundKey:\n', key_schedule[:, Nr * Nb:(Nr + 1) * Nb])
        state = add_round_key(state, key_schedule[:, Nr * Nb:(Nr + 1) * Nb])
        print('Finish of handling a block:\n', state)
        state = state.transpose()
        encrypted_data += str(bytes(list(state.flatten())), 'latin-1')

    # num_dots = 1
    # dpg.configure_item('dots', color=(0, 0, 255, 255))
    return encrypted_data, text_length


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
    ciphertext, text_length = encrypt(input_data, key)
    dpg.set_value('encrypted', value=ciphertext)
    fout = open('output.txt', 'a', encoding="utf-8")
    fout.writelines(ciphertext)
    fout.close()
    # region test
    decrypttext = decrypt(ciphertext, key, text_length)
    dpg.set_value('test', value=decrypttext)
    if ''.join(input_data) == ''.join(decrypttext):
        dpg.configure_item('dots', default_value='True', color=(0, 255, 0, 255))
    else:
        dpg.configure_item('dots', default_value='False', color=(255, 0, 0, 255))
    # endregion


def initialize_lr2():
    with dpg.window(label="Лабораторная работа #2", tag='lr2', show=True, width=500, height=700, pos=(100, 100),
                    on_close=lambda: dpg.delete_item('lr2')):
        initialize()
        dpg.add_button(label="Continue: AES", callback=preparing, show=False, tag='continue')
