import ekeys
from crypto.ehash import MyHash
from ekeys import KeyScheduler
from packet_utils import xor_2d_matrices, shift_rows, inv_shift_rows, alpha_numeric_to_packet, matrix_mult, enc, dec, \
    create_packets, string_to_packets, packet_to_alpha_numeric


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

    for R in range(r-1):
        p = shift_rows(xor_2d_matrices(matrix_mult(p, enc), ks.get_key()))

    return xor_2d_matrices(matrix_mult(p, enc), ks.get_key())


def decryption(p, ks, r):

    p = matrix_mult(xor_2d_matrices(p, ks.get_key()), dec)

    for R in range(r-1):
        p = matrix_mult(xor_2d_matrices(inv_shift_rows(p), ks.get_key()), dec)

    return p


"""
v = "This is 64 bytes worth of stuff that I will be encrypting.12345"
key1 = MyHash().set_internal_matrix("username").hash_packs(string_to_packets("supersecret"), 8)
key2 = MyHash().set_internal_matrix("username").hash_packs(string_to_packets("supersecret"), 8)
my_cryptor = Ecryptor(key1, security=8, encrypt=True)
my_decryptor = Ecryptor(key2, security=8, encrypt=False)
mess = string_to_packets("This will be our secret")
print("message:  ", packet_to_alpha_numeric(mess[0]))
encrypt = my_cryptor.cypher(mess)
print("encrypted:", packet_to_alpha_numeric(encrypt[0]))
decrypt = my_decryptor.cypher(encrypt)
print("decrypted:", packet_to_alpha_numeric(decrypt[0]))
"""
