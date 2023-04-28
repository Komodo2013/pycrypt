
# Create the lookup table
galois_field = [0] * 256
for i in range(256):
    __c = i
    for j in range(8):
        if __c & 0x80:
            __c = (__c << 1) ^ 0x1b
        else:
            __c <<= 1
        galois_field[i] = __c


def galois_multiply(__a, __b):
    p = 0x00
    while __b:
        if __b & 0x01:
            p ^= __a
        __a = galois_field[__a]
        __b >>= 1
    return p



"""Functions gf_degree and galois_inv retrieved from stackoverflow.com 8th of Apr 2022
https://stackoverflow.com/questions/45442396/a-pure-python-way-to-calculate-the-multiplicative-inverse-in-gf28-using-pytho
by redit user Jonas https://stackoverflow.com/users/2378300/jonas
answered 1 Aug 2017"""
def gf_degree(a):
    if a == 0:
        return 0
    res = 1
    while a > 1:
        a >>= 1
        res <<= 1
    return res


def galois_inv(a, mod=0x1B):
    s, old_s = 0, 1
    t, old_t = 1, 0
    r, old_r = mod, a

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    if old_r != 1:
        return None

    return old_s % 256


def galois_divide(a, b):
    return galois_multiply(a, galois_inv(b))


def galois_add(a, b):
    return a ^ b



class Galois:

    # 2, 3, 9, 11, 13, 14
    look_indexes = [2, 3, 9, 11, 13, 14]
    look_inv = [-1, -1, 0, 1,
                -1, -1, -1, -1,
                -1, 2, -1, 3,
                -1, 4, 5, -1]
    look_ups = []

    def __init__(self):
        for i in self.look_indexes:
            self.look_ups.append([])
            for j in range(256):
                self.look_ups[-1].append(galois_multiply(j, i))

    def multiply(self, a, b):
        if self.look_inv[b] == -1:
            return a
        return self.look_ups[self.look_inv[b]][a]


"""
g = Galois()
print(g.look_ups)
print(g.multiply(5, 9))
print("-"*64)
"""
"""
for k in range(258):
    print(k, galois_multiply(73, k))
"""
"""
j = galois_multiply(9, 12)
print(j)
i = galois_inv(12)
print(i)
z = galois_multiply(j, i)
print(z)
"""
