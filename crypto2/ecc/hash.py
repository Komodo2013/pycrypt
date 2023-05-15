"""
I'd like to improve the speed of this
"""

import base64

import mpmath
from crypto2.utils.subs import s_box
from crypto2.ecc.ecc import Curve


class Hasher:
    def __init__(self, b64_seed=None):
        self.__shifted = bytearray(64)
        self.__r = bytearray(8)
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
        if not _64_bytes:
            _64_bytes = self.__internal

        if is_b64_encoded:
            _64_bytes = bytearray(base64.b64decode(_64_bytes))

        if len(_64_bytes) < 64:
            for _ in range(64 - len(_64_bytes)):
                _64_bytes.append(0x00)
        elif len(_64_bytes) > 64:
            for _ in range(64 - (len(_64_bytes) % 64)):
                _64_bytes.append(0x00)

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
        return self.__internal if not as_b64 else base64.b64encode(self.__internal)


"""
h = Hasher()
print(h.digest(as_b64=True))

for _ in range(1):
    r = _
    b64 = base64.b64encode(b"this is a really long bit of information that is designed to make it so that the entire thing is just super long. In this code, you can replace process_chunk with the specific function or operations you need to perform on each 64-byte chunk. You can modify the buffer size (64 in this example) based on your requirements.In this code, you can replace process_chunk with the specific function or operations you need to perform on each 64-byte chunk. You can modify the buffer size (64 in this example) based on your requirements.In this code, you can replace process_chunk with the specific function or operations you need to perform on each 64-byte chunk. You can modify the buffer size (64 in this example) based on your requirements.")
    h.hash(None, is_b64_encoded=False)
    print(h.digest(as_b64=True))
"""
