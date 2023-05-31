import base64

import mpmath
from crypto2.utils.subs import s_box
from crypto2.ecc.ecc import Curve
import crypto2.utils.matrices as matrices


class Hasher:
    def __init__(self, b64_seed=None):
        self.ecc = Curve()

        # I used sqrt of 2 and 3 as the initialization vector because it is a well known irrational number
        # I did not use pi because it is used as part of my one-way function (more below)
        self.__internal_1 = matrices.def_root2rix()
        self.__internal_2 = matrices.def_root3rix()
        self.__internal = matrices.def_pitrix()  # This will be what is returned

        if b64_seed:
            self.__seed = base64.b64decode(b64_seed)

    def hash(self, bytes_in=None, is_b64_encoded=False):
        # If no additional information is provided, then we just want to generate some data and hash again
        # I choose sqrt 3 since it is a well-known irrational number that shouldn't be related to pi in any way
        if not bytes_in:
            bytes_in = matrices.def_root3rix()

        # Decode input as a bytearray if needed
        if is_b64_encoded:
            _64_bytes = bytearray(base64.b64decode(bytes_in))

        # Pad data with 0's if needed. This normalizes the data to 128 bytes, since this uses 2
        if len(bytes_in) < 128:
            for _ in range(128 - len(bytes_in)):
                bytes_in.append(0x00)
        elif len(bytes_in) > 128:
            for _ in range(128 - (len(bytes_in) % 128)):
                bytes_in.append(0x00)

        i1 = int.from_bytes(self.__internal_1, byteorder="big")
        i2 = int.from_bytes(self.__internal_2, byteorder="big")
        pint = int.from_bytes(self.__internal, byteorder="big")

        # break data into blocks
        for j in range((len(bytes_in) // 128)):
            sub_bytes = [0] * 128
            for i in range(128):
                sub_bytes[i] = s_box[bytes_in[j * 128 + i]]

            i1 ^= int.from_bytes(sub_bytes[j * 128: j * 128 + 63], byteorder="big")
            i2 ^= int.from_bytes(sub_bytes[j * 128 + 64: j * 128 + 127], byteorder="big")

            pi1 = self.ecc.point(i1 % self.ecc.K)
            pi2 = self.ecc.point(i2 % self.ecc.K)
            pi = self.ecc.point(pint % self.ecc.K)

            print(pi1)
            print(pi2)
            print(pi)

            add = self.ecc.point_addition(pi1, pi2)
            pint = self.ecc.point_addition(add, pi).x

        print(pint)
        # Pitrix is a matrix made if pi... It has no multiplicative inverse, so this function is irreversible
        self.__internal = matrices.mult_matrix(bytearray(int.to_bytes(pint, length=64, byteorder='big')),
                                               matrices.def_pitrix())

    def digest(self, as_b64=False):
        return bytearray(self.__internal) if not as_b64 else base64.b64encode(bytearray(self.__internal))



h = Hasher()
print(h.digest(as_b64=True))

for _ in range(1):
    r = _
    b64 = base64.b64encode(b"this is a really long bit of information that is designed to make it so that the entire thing is just super long. In this code, you can replace process_chunk with the specific function or operations you need to perform on each 64-byte chunk. You can modify the buffer size (64 in this example) based on your requirements.In this code, you can replace process_chunk with the specific function or operations you need to perform on each 64-byte chunk. You can modify the buffer size (64 in this example) based on your requirements.In this code, you can replace process_chunk with the specific function or operations you need to perform on each 64-byte chunk. You can modify the buffer size (64 in this example) based on your requirements.")
    h.hash(None, is_b64_encoded=False)
    print("", h.digest(as_b64=True))

