import ekeys
from ekeys import KeyScheduler
from packet_utils import xor_2d_matrices, shift_rows, inv_shift_rows, alpha_numeric_to_packet, matrix_mult, enc, dec


class Ecryptor:
    def __init__(self, key, security=8, encrypt=True):
        if type(key) == str:
            self.__key__ = alpha_numeric_to_packet(key)
        else:
            self.__key__ = key

        self.__security__ = security
        self.__scheduler__ = KeyScheduler(self.__key__, self.__security__, encrypt)

        if encrypt:
            self.__algorithm__ = encryption
        else:
            self.__algorithm__ = decryption

    def cypher(self, message):
        result = []

        for p in message:
            result.append(self.__algorithm__(p, self.__scheduler__, self.__security__))

        return result


def encryption(p, ks, r):
    t = p

    for R in range(r-1):
        t = matrix_mult(shift_rows(xor_2d_matrices(t, ks.get_key())), enc)

    return matrix_mult(xor_2d_matrices(t, ks.get_key()), enc)


def decryption(p, ks, r):
    t = xor_2d_matrices(matrix_mult(p, dec), ks.get_key)

    for R in range(r-1):
        t = xor_2d_matrices(inv_shift_rows(matrix_mult(t, dec)), ks.get_key())

    return t
