import base64

from hash import Hasher
import threading
from crypto2.utils.matrices import mult_matrix, def_pitrix, subs_matrix
from ecc import Curve

def psuedo_combine(a, b):
    for i in range(64):
        a[i] ^= b[a[i] & 63]
    return a

class KeyScheduler:
    def __init__(self, generator_hash, rounds, blocks):
        self.__rounds__ = rounds
        self.__blocks__ = blocks

        self.__key_hash__ = base64.b64decode(generator_hash)

        self.__matrix__, self.__inv_matrix__ = self.def_matrices()
        self.__block_starts__ = None

    def block_keys(self, block_start):
        __block_keys__ = [block_start]
        for i in range(self.__rounds__ * 2):
            __block_keys__.append(psuedo_combine(__block_keys__[-1], block_start)[:])
        return __block_keys__[0:-1]

    def gen_block_starts(self):
        if self.__block_starts__:
            return self.__block_starts__

        self.__block_starts__ = []

        for i in range(self.__blocks__):
            if i == 0:
                self.__block_starts__.append(self.__key_hash__)
            else:
                """
                This provides high resistance to quantum and traditional attacks, but is very expensive
                I decided pitrix should be non-linear enough, with a few other combinations and sboxes to form a light-
                weight hash function of sufficient strength for a key scheduler
                """
                self.__block_starts__.append(
                    mult_matrix(subs_matrix(psuedo_combine(self.__block_starts__[-1], self.__key_hash__)), def_pitrix())
                )

        return self.__block_starts__

    def def_matrices(self):
        return 1, 2



def encrypt(key_hash, data, rounds=4):
    # This ensures that the KeyScheduler is unique per file/key combo
    # It also reduces memory attack potential for pass the hash
    hasher = Hasher(key_hash)
    hasher.hash(data)
    generator_hash = int(hasher.digest(as_b64=True)[2:])  # sooooo we need to only play with 62 bytes

    ks_hash = KeyScheduler(key_hash, rounds=rounds, blocks=1)
    ks_data = KeyScheduler(generator_hash, rounds=rounds, blocks=len(data)//62 + 1)
    blocks = data
    output = None
    curve = Curve()

    # Encrypt generator hash
    for i in range(rounds):
        h = curve.point_addition(curve.encode_point(5))

    """
    encrypt(key_scheduler_hash as ks, file_hash as h):
        for rounds min 4:
            h = ECC.add( h as ecc.point, ks.next as ecc.point)
        for rounds min 4:
            h = ks.matrix_mult(h as matrix)
            h += ks.next

        h, -1 -> encrypted

    encrypt(key_scheduler as ks, data as data):
        ks.generate_starts(data#), block, block# -> queue
        encrypted;

        queue -> get(ks, block)
            for rounds min 4:
                block = ECC.add( block as ecc.point, ks.next as ecc.point)
            for rounds min 4:
                block = ks.matrix_mult(block as matrix)
                block += ks.next
            block, block# -> encrypted

        return order(encrypted)
    """

    pass


def decrypt(key_hash, encrypted, rounds=4):
    """
    key_scheduler_hash(key_hash, rounds, reverse)
    file_hash:
        decrypt(encrypted[0] as e, key_scheduler_hash as ks):
            for rounds min 4:
                e += ks.next
                e = ks.matrix_mult_inv(e as matrix)
            for rounds min 4:
                e = ECC.add( e as ecc.point, ks.next as ecc.point)

    key_scheduler(key_hash, file_hash, rounds, reverse)

    decrypt(key_scheduler as ks, encrypted as e):
        ks.generate_starts(e#), e, e# -> queue
        decrypted;

        queue -> get(ks, block)
            for rounds min 4:
                block += ks.next
                block = ks.matrix_mult(block as matrix)
            for rounds min 4:
                block = ECC.add( block as ecc.point, ks.next as ecc.point)
            block, block# -> decrypted

    if file_hash(decrypted) == file_hash:
        return decrypted
    else:
        raise("Error in ")
    """

    pass


"""
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


c = Curve()
v= 65189726
p = c.encode_point(v)
d = c.decode_point(p)
print(v==d, v, p, d)

