"""
I'd like to improve the speed of this
"""

import base64

import mpmath
from crypto2.utils.subs import s_box
from crypto2.ecc.ecc import Curve
import crypto2.utils.matrices as matrices


class Hasher:
    def __init__(self, b64_seed=None):
        self.__shifted = bytearray(64)
        self.__r = bytearray(8)
        self.ecc = Curve()

        # I used sqrt of 2 as the initialization vector because it is a well known irrational number
        # I did not use pi because it is used as part of my one-way function (more below)
        self.__internal = matrices.def_root2rix()

        if b64_seed:
            self.__seed = base64.b64decode(b64_seed)

    def hash(self, _64_bytes=None, is_b64_encoded=False):
        # If no additional information is provided, then we just want to generate some data and hash again
        # I choose sqrt 3 since it is a well-known irrational number that shouldn't be related to pi in any way
        if not _64_bytes:
            _64_bytes = matrices.def_inv_root3rix()

        # Decode input as a bytearray if needed
        if is_b64_encoded:
            _64_bytes = bytearray(base64.b64decode(_64_bytes))

        # Pad data with 0's if needed
        if len(_64_bytes) < 64:
            for _ in range(64 - len(_64_bytes)):
                _64_bytes.append(0x00)
        elif len(_64_bytes) > 64:
            for _ in range(64 - (len(_64_bytes) % 64)):
                _64_bytes.append(0x00)

        # break data into blocks
        for j in range(len(_64_bytes) // 64):
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

        _64_bytes = _64_bytes[64:]

    def digest(self, as_b64=False):
        return bytearray(self.__internal) if not as_b64 else base64.b64encode(bytearray(self.__internal))



h = Hasher()
print(h.digest(as_b64=True))

for _ in range(1):
    r = _
    b64 = base64.b64encode(b"this is a really long bit of information that is designed to make it so that the entire thing is just super long. In this code, you can replace process_chunk with the specific function or operations you need to perform on each 64-byte chunk. You can modify the buffer size (64 in this example) based on your requirements.In this code, you can replace process_chunk with the specific function or operations you need to perform on each 64-byte chunk. You can modify the buffer size (64 in this example) based on your requirements.In this code, you can replace process_chunk with the specific function or operations you need to perform on each 64-byte chunk. You can modify the buffer size (64 in this example) based on your requirements.")
    h.hash(None, is_b64_encoded=False)
    print(h.digest(as_b64=True))

