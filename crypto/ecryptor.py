import ekeys
from ekeys import KeyScheduler
from packet_utils import xor_2d_matrices, shift_rows, inv_shift_rows, alpha_numeric_to_packet


class Ecryptor:
    def __init__(self, key, security=8, encrypt=True):
        if type(key) == str:
            self.key = alpha_numeric_to_packet(key)
        else:
            self.key = key

        self.__security__ = security
        self.__scheduler__ = KeyScheduler(self.key, self.security, encrypt)

        if encrypt:
            self.__algorithm__ = encryption
        else:
            self.__algorithm__ = decryption

    def cypher(self, message):
        result = []

        for p in message:
            result.append(self.__algorithm__(p, self.__scheduler__, self.__security__))


def encryption(p, ks, r):
    ks = ekeys.KeyScheduler().key_stream
    t = p

    for R in range(r):
        t = shift_rows(xor_2d_matrices(t, ks.next()))


def decryption(p, ks, r):
    ks = ekeys.KeyScheduler().key_stream
    t = p

    for R in range(r):
        t = xor_2d_matrices(inv_shift_rows(t), ks.next())
