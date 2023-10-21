from typing import Union

from initialize import *


def get_input_data():
    if dpg.get_value('input_method') == 'File':
        file_path = dpg.get_value('file')
        file = open(file_path, 'r')
        input_data = file.read()
        file.close()
    else:
        input_data = dpg.get_value('Manually')
    return [ord(c) for c in input_data], input_data


class RSA:
    __public_key__: tuple
    __private_key__: tuple

    def __init__(self, _p: int, _q: int, _e: int):
        self.__make_keys__(_p, _q, _e)

    @staticmethod
    def are_relatively_prime(a, b):
        """Return ``True`` if ``a`` and ``b`` are two relatively prime numbers.

        Two numbers are relatively prime if they share no common factors,
        i.e. there is no integer (except 1) that divides both.
        """
        for n in range(2, min(a, b) + 1):
            if a % n == b % n == 0:
                return False
        return True

    @staticmethod
    def bezout_recursive(a, b) -> tuple[int, int, int]:
        """
        A recursive implementation of extended Euclidean algorithm.
        Returns integer x, y and gcd(a, b) for Bezout equation:
            ax + by = gcd(a, b).
        """
        if not b:
            return 1, 0, a
        y, x, g = RSA.bezout_recursive(b, a % b)
        return x, y - (a // b) * x, g

    @staticmethod
    def mod_inverse(a, m):
        x, y, gcd = RSA.bezout_recursive(a, m)
        return (x % m + m) % m if gcd == 1 else -1

    @staticmethod
    def fast_pow_module(base, degree, module):
        degree = list(map(int, bin(degree)[:1:-1]))
        r = 1
        for i in degree:
            if i:  r = (r * base) % module
            base = pow(base, 2, module)
        return r

    def __make_keys__(self, _p: int, _q: int, _e: int):
        p, q, e = _p, _q, _e
        phi = (p - 1) * (q - 1)
        d = RSA.mod_inverse(e, phi)
        N = p * q
        print(f"\t\tPublic key: [{e}], [{N}]")
        self.__public_key__, self.__private_key__ = (e, N), (d, N)

    def encrypt(self, input_bytes: list) -> tuple[list, str]:
        e, N = self.__public_key__
        __cipher_bytes__ = [RSA.fast_pow_module(c, e, N) for c in input_bytes]
        return __cipher_bytes__, ''.join([chr(c) for c in __cipher_bytes__])

    def decrypt(self, cipher_bytes: list) -> tuple[list, str]:
        d, N = self.__private_key__
        decipher_bytes = [RSA.fast_pow_module(c, d, N) for c in cipher_bytes]
        return decipher_bytes, ''.join([chr(c) for c in decipher_bytes])


def preparing(sender, app_data, user_data):
    dpg.show_item('Cipher method')
    input_bytes, input_data = get_input_data()
    dpg.set_value('input data', value=input_data)
    p, q, e = dpg.get_value('key_p'), \
        dpg.get_value('key_q'), \
        dpg.get_value('key_e')
    rce = RSA(p, q, e)
    fout = open('plaintext.txt', 'w')
    fout.writelines("\n\n\tText:\n" + input_data)
    fout.close()
    cipher_bytes, cipher_text = rce.encrypt(input_bytes)
    dpg.set_value('encrypted', value=cipher_text)
    fout = open('ciphertext.txt', 'w')
    fout.writelines(cipher_text)
    fout.close()
    # region test
    decrypted_bytes, decrypted_data = rce.decrypt(cipher_bytes)
    dpg.set_value('test', value=decrypted_data)
    fout = open('decrypted_text.txt', 'w')
    fout.writelines("\n\tDecrypted:\n" + decrypted_data)
    fout.close()
    if ''.join(input_data) == ''.join(decrypted_data):
        dpg.configure_item('dots', default_value='True', color=(0, 255, 0, 255))
    else:
        dpg.configure_item('dots', default_value='False', color=(255, 0, 0, 255))
    # endregion


def initialize_lr3():
    with dpg.window(label="Лабораторная работа #3", tag='lr3', show=True, width=500, height=700, pos=(100, 100),
                    on_close=lambda: dpg.delete_item('lr3')):
        initialize()
        dpg.add_input_int(tag='key_p', label='Key: p', default_value=857, show=True, before='Manually')
        dpg.add_input_int(tag='key_q', label='Key: q', default_value=673, show=True, before='Manually')
        dpg.add_input_int(tag='key_e', label='Key: e', default_value=5, show=True, before='Manually')
        dpg.add_button(label="Continue: RCA", callback=preparing, show=False, tag='continue')
