from typing import Union

from initialize import *
import numpy as np
import time
from numpy.polynomial import Polynomial
from collections import deque
from constant import S_BOX, R_CON, INV_S_BOX, MATRIX_ENC, MATRIX_DEC

sleeping = 0.0001


def get_input_data():
    if dpg.get_value('input_method') == 'File':
        file_path = dpg.get_value('file')
        file = open(file_path, 'r', encoding="utf-8")
        input_data = file.read()
    else:
        input_data = dpg.get_value('Manually')
    return input_data


class AES:
    plaintext: str
    original_length: int
    cipher_text: str
    key: str  # длина ключа = 128/192/256 бит
    key_schedule: np.array
    encoding_key: str
    encoding_text: str
    blocks: np.array
    Nb: int
    Nr: int
    Nk: int

    def __init__(self, key,
                 __Nb=4, __Nr=10, __Nk=4):
        """
        :param key:
        :param __Nb:
        :param __Nr:
        :param __Nk:
        """
        self.key = key
        self.Nb, self.Nr, self.Nk = __Nb, __Nr, __Nk

        def __key_expansion():
            """
            Создание раундовых ключей (Round Keys)
            :return:
            """
            try:
                key_schedule = np.array(list(self.key.encode()))
                if len(key_schedule) < (self.Nk * 4):  # Расширение до Nk байт
                    key_schedule = np.append(key_schedule, [0x01] * ((self.Nk * 4) - len(key_schedule)))
                elif len(key_schedule) > (self.Nk * 4):
                    key_schedule = key_schedule[:self.Nk * 4]
                key_schedule = key_schedule.reshape((4, self.Nk)).transpose()
            except:
                key_schedule = np.array(np.array([[0x01] * 4]) * 4)
                dpg.set_value('key', 'Error in key')
            # Дополняем оставшиеся строки таблицы ключей
            for col in range(self.Nk, self.Nb * (self.Nr + 1)):
                temp = key_schedule[:, col - 1]
                if col % self.Nk == 0:
                    temp = AES.InternalOperations.sub_bytes(AES.InternalOperations.rot_word(temp)) \
                           ^ np.array(R_CON[col // self.Nk])
                elif (self.Nk > 6) and (col % self.Nk == 4):
                    temp = AES.InternalOperations.sub_bytes(temp)
                temp = key_schedule[:, col - self.Nk] ^ temp
                key_schedule = np.insert(key_schedule, col,
                                         np.array(temp), axis=1)
            self.key_schedule = key_schedule
        __key_expansion()

    def set_plaintext(self, input_data: str):
        self.plaintext = input_data
        # self.encoding_text = chardet.detect(input_data.encode())['encoding']
        self.encoding_text = 'utf-16'
        self.original_length = len(self.plaintext)

    def set_ciphertext(self, cipher_text: str):
        self.cipher_text = cipher_text

    @staticmethod
    def __split_to_blocks(text: Union[str, list], by_bytes: int):
        blocks = []
        try:
            # text_bytes = bytes(text, encoding=chardet.detect(text.encode())['encoding'])
            # text_bytes = [ord(x) for x in text]
            if type(text) == str:
                text_bytes = text.encode(encoding='utf-16')
            else:
                text_bytes = text
            # print("text_bytes: ", text_bytes)
            for i in range(0, len(text_bytes), by_bytes):
                block = np.array(list(text_bytes[i:i + by_bytes]))
                if len(block) < by_bytes:
                    block = np.append(block, [0x00] * (by_bytes - len(block)))
                block = block.reshape((4, by_bytes // 4)).transpose()
                blocks.append(block)
        except Exception as err:
            print("Error in splitting a text: ", err)
        return blocks

    def encrypt(self):
        """
        Алгоритм обрабатывает блоки по 128-бит,
        шифруя блок симметричным секретным ключом key (128 бит)
        """
        # print("\n\t\t\tEncrypting\n")
        encrypted_bytes = []
        num_dots = 1
        dpg.configure_item('dots', color=(0, 0, 255, 255))
        self.blocks = AES.__split_to_blocks(self.plaintext, 16)
        for block in self.blocks:
            # print('\tBlock:\n', block)
            # initializing
            state = AES.InternalOperations.add_round_key(block, self.key_schedule[:, :self.Nb])
            for round in range(1, self.Nr):
                try:
                    # time.sleep(sleeping)
                    state = AES.InternalOperations.sub_bytes_state(state)
                    state = AES.InternalOperations.shift_rows(state)
                    state = AES.InternalOperations.mix_columns(state, MATRIX_ENC)
                    state = AES.InternalOperations.add_round_key(state,
                                                                 self.key_schedule[:,
                                                                 round * self.Nb:(round + 1) * self.Nb])
                    dpg.set_value('dots', value='Encrypting: ' + '.  ' * num_dots)
                    num_dots += 1
                except:
                    print(f"Error in encrypting in {round} round of {block} block")
            state = AES.InternalOperations.sub_bytes_state(state)
            state = AES.InternalOperations.shift_rows(state)
            state = AES.InternalOperations.add_round_key(state,
                                                         self.key_schedule[:,
                                                         self.Nr * self.Nb:(self.Nr + 1) * self.Nb])
            # print('Finish of handling a block:\n', state)
            state = state.transpose()
            encrypted_bytes += list(state.flatten())
        encrypted_data = ''.join([chr(x) for x in encrypted_bytes])
        return encrypted_data, encrypted_bytes

    def decrypt(self, encrypted_bytes):
        # print("\n\t\t\tDecrypting\n")
        decrypted_bytes = []
        num_dots = 1
        dpg.configure_item('dots', color=(0, 0, 255, 255))
        self.blocks = AES.__split_to_blocks(encrypted_bytes, 16)
        for block in self.blocks:
            # initializing
            # print('Start block:\n', block)
            state = AES.InternalOperations.add_round_key(block,
                                                         self.key_schedule[:,
                                                         self.Nr * self.Nb:self.Nb * (self.Nr + 1)])
            for round in range(self.Nr - 1, 0, -1):
                try:
                    # time.sleep(sleeping)
                    state = AES.InternalOperations.shift_rows(state, invert=True)
                    state = AES.InternalOperations.sub_bytes_state(state, inverse=True)
                    state = AES.InternalOperations.add_round_key(state,
                                                                 self.key_schedule[:,
                                                                 round * self.Nb:(round + 1) * self.Nb])
                    state = AES.InternalOperations.mix_columns(state, MATRIX_DEC)
                    dpg.set_value('dots', value='Decrypting: ' + '.  ' * num_dots)
                    num_dots += 1
                except:
                    print(f"Error in decrypting in {round} round of {block} block")

            state = AES.InternalOperations.shift_rows(state, invert=True)
            state = AES.InternalOperations.sub_bytes_state(state, inverse=True)
            state = AES.InternalOperations.add_round_key(state, self.key_schedule[:, :self.Nb])
            # print('Finish of handling a block:\n', state)
            state = state.transpose()
            decrypted_bytes += list(state.flatten())
        decrypted_data = bytes(decrypted_bytes).decode(encoding=self.encoding_text)
        return decrypted_data[:self.original_length]

    class InternalOperations:
        @staticmethod
        def sub_bytes(orig, inverse=False):
            """
            Нелинейная замена байтов массива orig
            на соответствующее значение из box
            Вычисление элемента: 4 старших бита - индекс строки в box
                                 4 младших бита - индекс столбца в box

            :param inverse:
            :param orig: исходный массив
            :return: массив с сопоставленными значениями из box
            """
            box = INV_S_BOX if inverse else S_BOX
            return np.vectorize(lambda item: box[16 * (item // 0x10) +
                                                 (item % 0x10)])(orig)

        @staticmethod
        def sub_bytes_state(state, inverse=False):
            return np.vectorize(AES.InternalOperations.sub_bytes) \
                (state, inverse=inverse)

        @staticmethod
        def rot_word(word: np.array, rotnumber=-1):
            """
            Сдвиг элементов массива на указанное количество ячеек
            :param word:
            :param rotnumber:
            :return:
            """
            rot = deque(word)
            rot.rotate(rotnumber)
            return np.array(rot)

        @staticmethod
        def add_round_key(state, key_schedule):
            return state ^ key_schedule

        @staticmethod
        def shift_rows(state, invert=False):
            direction = 1 if invert else -1
            new_state = state.copy()
            for index, row in enumerate(new_state):
                new_state[index] = AES.InternalOperations.rot_word \
                    (row, index * direction)
            return new_state

        @staticmethod
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

        @staticmethod
        def mix_columns(state, matrix):
            new_state = state.copy()
            for col in range(state.shape[1]):
                new_state[:, col] = [np.bitwise_xor.reduce([AES.InternalOperations.mult_bytes
                                                            (state[index][col], matrix[row][index])
                                                            for index
                                                            in range(len(matrix[0]))])
                                     for row
                                     in range(len(matrix))]
            return new_state


def preparing(sender, app_data, user_data):
    dpg.show_item('Cipher method')
    dpg.set_value('input data', value=get_input_data())
    aes = AES(dpg.get_value('key'))
    input_data = get_input_data()
    aes.set_plaintext(input_data)
    fout = open('plaintext.txt', 'a')
    fout.writelines("\n\n\tText:\n" + input_data)
    fout.close()
    ciphertext, encrypted_bytes = aes.encrypt()
    aes.set_ciphertext(ciphertext)
    dpg.set_value('encrypted', value=ciphertext)
    fout = open('ciphertext.txt', 'a')
    fout.writelines("\n\tCiphertext:\n" + ciphertext)
    fout.close()
    # region test
    decrypted_text = aes.decrypt(encrypted_bytes)
    dpg.set_value('test', value=decrypted_text)
    fout = open('decrypted_text.txt', 'a')
    fout.writelines("\n\tDecrypted:\n" + decrypted_text)
    fout.close()
    if ''.join(input_data) == ''.join(decrypted_text):
        dpg.configure_item('dots', default_value='True', color=(0, 255, 0, 255))
    else:
        dpg.configure_item('dots', default_value='False', color=(255, 0, 0, 255))
    # endregion


def initialize_lr2():
    with dpg.window(label="Лабораторная работа #2", tag='lr2', show=True, width=500, height=700, pos=(100, 100),
                    on_close=lambda: dpg.delete_item('lr2')):
        initialize()
        dpg.add_input_text(tag='key', label='Key', default_value='passwordfbsfv', show=False, before='Manually')
        dpg.add_button(label="Continue: AES", callback=preparing, show=False, tag='continue')
