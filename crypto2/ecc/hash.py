import base64

import statistics

import mpmath
from crypto2.utils.subs import s_box
from crypto2.ecc.ecc import Curve
import time


class Hasher:
    def __init__(self, b64_seed=None):
        self.__shifted = bytearray(64)
        self.__r = bytearray(8)
        bytearray()
        self.ecc = Curve()

        # I use an initialization vector for this hash algorith of pi, built to 512 bits
        # I chose this because
        mpmath.mp.dps = 512  # Set the desired precision in decimal places
        pi = mpmath.mp.pi  # Compute pi with the specified precision
        # convert pi to 512 bit int... remember 3 in 3.13 is 2 bits thus 512-2 = 510

        self.__internal = bytearray(int(pi * 2 ** 510).to_bytes(length=64, byteorder='big'))

        if b64_seed:
            self.__seed = base64.b64decode(b64_seed)

    def hash(self, _64_bytes, is_b64_encoded=False):
        if is_b64_encoded:
            _64_bytes = base64.b64decode(_64_bytes)

        # OLD:
        # byte_matrix = mix_columns(shift_rows(s.sub_matrix(xor_2d_matrices(self.internal_matrix, byte_matrices[i]))))
        # for i in range(security):
        #    byte_matrix = mix_columns_galois(shift_rows(s.sub_matrix(xor_2d_matrices(
        #        byte_matrix, aes_matrix_from_matrix(byte_matrix)))))
        # return xor_2d_matrices(byte_matrix, aes_matrix_from_matrix(byte_matrix))

        for i in range(64):
            # This xors the internal and input byte matrices, puts the output through the aes substitution box,
            # then shifts the order of the bytes such that the order is now 1, 2, 3, 4, 5, 6, 7, 0 etc...
            __s = s_box[self.__internal[i] ^ _64_bytes[i]]
            self.__shifted[((i - 1) & 7) + (i & ~7)] = __s
            self.__r[(i >> 3)] ^= __s

        for i in range(64):
            self.__internal[i] = self.__shifted[i] ^ self.__r[(i >> 3)]

        i = int.from_bytes(self.__internal, byteorder='big')
        i ^= self.ecc.multiply_np(i, self.ecc.G).x
        self.__internal = bytearray(int.to_bytes(i, length=64, byteorder='big'))

        for i in range(64):
            __s = s_box[self.__internal[i] ^ _64_bytes[i]]
            self.__shifted[((i - 1) & 7) + (i & ~7)] = __s
            self.__r[(i >> 3)] ^= __s

        for i in range(64):
            self.__internal[i] = self.__shifted[i] ^ self.__r[(i >> 3)]

    def digest(self, as_b64=False):
        return self.__internal if not as_b64 else base64.b64encode(self.__internal)


"""
h = Hasher()
tests = []

for _ in range(256):
    r = _
    start = time.time()
    h.hash(int.to_bytes(r, length=64, byteorder='big'))
    tests.append(time.time() - start)
    print(r, h.digest(as_b64=True))

print(f"Mean:\t{statistics.mean(tests)}\nSt Dev:\t{statistics.stdev(tests)}\n")
"""
