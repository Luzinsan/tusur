from typing import Union

from initialize import *

sleeping = 0.0001


def get_input_data():
    if dpg.get_value('input_method') == 'File':
        file_path = dpg.get_value('file')
        file = open(file_path, 'r', encoding="utf-8")
        input_data = file.read()
    else:
        input_data = dpg.get_value('Manually')
    return input_data


class RSA:
    __input_bytes__: list
    __cipher_bytes__: list

    cipher_text: str

    __public_key__: tuple
    __private_key__: tuple

    encoding_key: str
    encoding_text: str

    def __init__(self):
        self.make_keys(19, 41)

    @staticmethod
    def __are_relatively_prime(a, b):
        """Return ``True`` if ``a`` and ``b`` are two relatively prime numbers.

        Two numbers are relatively prime if they share no common factors,
        i.e. there is no integer (except 1) that divides both.
        """
        for n in range(2, min(a, b) + 1):
            if a % n == b % n == 0:
                return False
        return True

    def make_keys(self, _p: int, _q: int):
        p, q = _p, _q
        phi = (p - 1) * (q - 1)
        for e in range(3, phi, 2):
            if self.__are_relatively_prime(e, phi):
                break
        else:
            raise AssertionError("cannot find 'e' with p={!r} "
                                 "and q={!r}".format(p, q))

        # Third step: find ``d`` such that ``(d * e - 1)`` is divisible by
        # ``(p - 1) * (q - 1)``.
        for d in range(3, phi, 2):
            if d * e % phi == 1:
                break
        else:
            raise AssertionError("cannot find 'd' with p={!r}, q={!r} "
                                 "and e={!r}".format(p, q, e))
        N = p * q
        self.__public_key__, self.__private_key__ = (e, N), (d, N)

    def set_plaintext(self, input_data: str):
        self.__input_bytes__ = [ord(i) for i in input_data]
        print(self.__input_bytes__)

    def encrypt(self):
        self.__cipher_bytes__ = []
        e, N = self.__public_key__
        print(self.__public_key__)
        for i in self.__input_bytes__:
            self.__cipher_bytes__.append(i ** e % N)
        print(self.__cipher_bytes__)
        return ''.join([chr(i) for i in self.__cipher_bytes__])

    def decrypt(self):
        d, N = self.__private_key__
        decipher_bytes = []
        print(''.join([chr(i) for i in self.__cipher_bytes__]))
        for i in self.__cipher_bytes__:
            decipher_bytes.append(i ** d % N)
        print(decipher_bytes)
        return ''.join([chr(i) for i in decipher_bytes])


def preparing(sender, app_data, user_data):
    dpg.show_item('Cipher method')
    dpg.set_value('input data', value=get_input_data())
    rce = RSA()
    input_data = get_input_data()
    rce.set_plaintext(input_data)
    fout = open('plaintext.txt', 'a')
    fout.writelines("\n\n\tText:\n" + input_data)
    fout.close()
    ciphertext = rce.encrypt()
    dpg.set_value('encrypted', value=ciphertext)
    fout = open('ciphertext.txt', 'a')
    fout.writelines("\n\tCiphertext:\n" + ciphertext)
    fout.close()
    # # region test
    decrypted_text = rce.decrypt()
    dpg.set_value('test', value=decrypted_text)
    fout = open('decrypted_text.txt', 'a')
    fout.writelines("\n\tDecrypted:\n" + decrypted_text)
    fout.close()
    if ''.join(input_data) == ''.join(decrypted_text):
        dpg.configure_item('dots', default_value='True', color=(0, 255, 0, 255))
    else:
        dpg.configure_item('dots', default_value='False', color=(255, 0, 0, 255))
    # # endregion


def initialize_lr3():
    with dpg.window(label="Лабораторная работа #3", tag='lr3', show=True, width=500, height=700, pos=(100, 100),
                    on_close=lambda: dpg.delete_item('lr3')):
        initialize()
        dpg.add_input_text(tag='key', label='Key', default_value='passwordfbsfv', show=False, before='Manually')
        dpg.add_button(label="Continue: RCE", callback=preparing, show=False, tag='continue')
