import ehash
from packet_utils import xor_1d_matrices

big = 0xFFFFFFFFFFFFFFFF


class KeyScheduler:

    def __init__(self, hash_bytes, rounds, __encrypting__=True):
        if len(hash_bytes) == 8:
            for __i__ in hash_bytes:
                if len(__i__) != 8:
                    raise Exception('invalid key length')
        else:
            raise Exception('invalid key length')

        self.__tr__, self.__r__ = rounds, rounds

        if __encrypting__:
            self.key_stream = KeyStream(rounds + 1, hash_bytes[:], ehash.MyHash().hash_packs([hash_bytes[:]], 8)[:])
        else:
            self.key_stream = RKeyStream(rounds + 1, hash_bytes[:], ehash.MyHash().hash_packs([hash_bytes[:]], 8)[:])

    def get_key(self):
        if self.__r__ == self.__tr__:
            self.__r__ = 1
            self.key_stream.new_round()
            return expand(self.key_stream.next())
        else:
            self.__r__ += 1
            return expand(self.key_stream.next())


def flatten(__2d_array__):
    __result__ = []
    for __r__ in __2d_array__:
        __num__ = 0
        for __b__ in __r__:
            __num__ = (__num__ << 8) ^ __b__

        __result__.append(__num__)
    return __result__

def expand(__1d_array__):
    __result__ = []
    for __r__ in __1d_array__:
        __result__.append([])

        __result__[-1].append(__r__ & 0xFF)
        for __i__ in range(7):
            __r__ >>= 8
            __result__[-1].append(__r__ & 0xFF)
    return __result__


def l_mix(num, m):
    result = []
    for n in num:
        result.append(galois_multiply((n << 29 & big ^ n >> 35), m))
    return result


def r_mix(num, m):
    result = []
    for n in num:
        result.append(galois_multiply((n >> 23 ^ n << 41 & big), m))
    return result


def galois_multiply(a, b):
    p = 0x00
    for i in range(64):
        if b & 0x01 == 0x01:
            p ^= a
        b = b >> 1
        if a & 0x80 == 0x80:
            a = (a << 1) & big
            a ^= 0x1b
        else:
            a = (a << 1) & big
    return p


class KeyStream:
    def __init__(self, __rounds__, __left__, __right__):
        self.__rounds__ = __rounds__
        self.__keys__ = []
        self.__left__ = flatten(__left__)
        self.__right__ = flatten(__right__)

    def new_round(self):
        self.__keys__.clear()

        for __r__ in range(self.__rounds__):
            self.__keys__.append(self.mix())

    def next(self):
        self.__keys__.pop(-1)
        return self.__keys__[-1][:]

    def mix(self):
        k = xor_1d_matrices(self.__left__, self.__right__)

        self.__left__ = l_mix(self.__left__, k[-1])
        self.__right__ = r_mix(self.__right__, k[-1])

        return k


class RKeyStream:
    def __init__(self, __rounds__, __left__, __right__):
        self.__rounds__ = __rounds__
        self.__keys__ = []
        self.__left__ = flatten(__left__)
        self.__right__ = flatten(__right__)

    def new_round(self):
        self.__keys__.clear()

        for __r__ in range(self.__rounds__):
            self.__keys__.append(self.mix())

    def next(self):
        t = self.__keys__[0][:]
        self.__keys__.pop(0)
        return t

    def mix(self):
        k = xor_1d_matrices(self.__left__, self.__right__)

        self.__left__ = l_mix(self.__left__, k[-1])
        self.__right__ = r_mix(self.__right__, k[-1])

        return k


# hasher = ehash.MyHash("username")
# _hash = hasher.hash_packs(ehash.string_to_packets("password123"), 8)
#
# k = 32
#
# ks = KeyScheduler(_hash, 8)
# rks = KeyScheduler(_hash, 8, False)
# for i in range(k):
#     print(ehash.packet_to_alpha_numeric(ks.get_key()))
#
# print("-"*64)
#
# for i in range(k):
#     print(ehash.packet_to_alpha_numeric(rks.get_key()))
