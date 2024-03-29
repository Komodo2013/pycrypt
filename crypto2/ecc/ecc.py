"""
This is an updated version of my ECC algorith that will be used
"""
import base64
import math
import random
# Designed for use of the M-511 as defined:
# y**2 ≡ x**3 + 486662x**2 + x (mod 2**255 - 19)
# B * y^2 = x^3 + A * x^2 + x + 0
# most models use: y^2 = x^3 + B * x^2 +A * x + 0
from collections import namedtuple
import sympy
Point = namedtuple("Point", "x y")


class Curve:

    Origin = 'Origin'

    def __init__(self):
        self.A = 0x081806
        self.B = 1
        self.K = 0x7FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF45
        self.Order = 0x100000000000000000000000000000000000000000000000000000000000000017B5FEFF30C7F5677AB2AEEBD13779A2AC125042A6AA10BFA54C15BAB76BAF1B
        self.G = Point(0x05, 0x2fbdc0ad8530803d28fdbad354bb488d32399ac1cf8f6e01ee3f96389b90c809422b9429e8a43dbf49308ac4455940abe9f1dbca542093a895e30a64af056fa5)
        self.Cofactor = 0x08

    def define_curve(self, a, b, k, order, g, cofactor):
        self.A = a
        self.B = b
        self.K = k
        self.Order = order
        self.G = g
        self.cofactor = cofactor

    def is_valid_point(self, p):
        """
        Determine whether we have a valid representation of a point
        on our curve.  We assume that the x and y coordinates
        are always reduced modulo p, so that we can compare
        two points for equality with a simple ==.
        """
        if p == self.Origin:
            return True
        elif p.x is None or p.y is None:
            return False
        else:
            return (
                    (self.B * p.y ** 2) % self.K == (p.x ** 3 + self.A * p.x ** 2 + p.x) % self.K and
                    0 <= p.x < self.K and 0 <= p.y < self.K)

    def inv_mod_p(self, x):
        """
        I used to have my own function here, then replaced it with python pow and now sympy
        """
        return sympy.mod_inverse(x, self.K)

    def ec_inv(self, p):
        """
        Inverse of the point P on the elliptic curve
        """
        if p == self.Origin:
            return p
        return Point(p.x, (-p.y) % self.K)

    def point_double(self, p):
        l = ((3 * p.x ** 2 + 2 * self.A * p.x + 1) * self.inv_mod_p(2 * self.B * p.y))
        x = (self.B * l ** 2 - self.A - 2 * p.x) % self.K
        y = ((3 * p.x + self.A) * l - self.B * l ** 3 - p.y) % self.K
        return Point(x, y)

    def point_addition(self, p1, p2):
        x3 = ((self.B * (p2.y - p1.y) ** 2) * self.inv_mod_p((p2.x - p1.x) ** 2) - self.A - p1.x - p2.x) % self.K
        y3 = ((2 * p1.x + p2.x + self.A) * (p2.y - p1.y) * self.inv_mod_p((p2.x - p1.x)) - self.B * (p2.y - p1.y) ** 3 *
              self.inv_mod_p((p2.x - p1.x) ** 3) - p1.y) % self.K
        return Point(x3, y3)

    def point_calc(self, p1, p2):
        if not (self.is_valid_point(p1) and self.is_valid_point(p2)):
            raise ValueError('Input is not a valid point')

        if p1 == self.Origin:
            return p2
        elif p2 == self.Origin:
            return p1
        elif p1 == self.ec_inv(p2):
            return self.Origin
        else:
            if p1 == p2:
                return self.point_double(p1)
            else:
                return self.point_addition(p1, p2)

    def multiply_np(self, n, p):
        pmultplier = p
        p2 = p
        n = n - 1
        for _ in range(512):
            if n & 1:
                p2 = self.point_calc(p2, pmultplier)

            pmultplier = self.point_double(pmultplier)
            n = n >> 1
        return p2

    def point(self, x):
        return Point(x, sympy.sqrt_mod((x ** 3 + self.A * x ** 2 + x) % self.K, self.K))

    def lossy_get_point(self, x):
        """
        This will always* return a valid point, however you can no longer ensure that you know what value
        yielded the point
        * Technically the probability is 2**-2**l of no point being found... at 16 the probability is ~ < 1 in 10^20000
        This is, for all intents and purposes, equivalent to 0, however since our data is not random, I chose to double
         it again to 32
        """
        for i in range(32):
            p = Point(x, sympy.sqrt_mod((x ** 3 + self.A * x ** 2 + x) % self.K, self.K))
            if self.is_valid_point(p):
                return p
            if x & 0x1:
                x ^= 2 ** 511  # Prime K is 512 bits long, 511 ensures it will always be smaller
            x >>= 1

        raise("Unencodeable value")

    def encode_point(self, x):
        """
        This will always return a valid point, it encodes one byte with how many bitshifts were preformed
        in this curve, a maximum of 512 bits are available for a point. 496 are used for message (32 bytes)
        8 bits are used for encoding bitshifts and the remaining 8 are discarded

        param x: a 62 byte number (yes 62.... not a power of 2)
        * Technically the probability is 2**-2**l of no point being found... at 16 the probability is ~ < 1 in 10^20000
        This is, for all intents and purposes, equivalent to 0, however since our data is not random, I chose to double
         it again to 32
        """

        for i in range(32):
            v = (i << 497) + x  # i is the encoded bitshifts, x the message
            p = Point(v, sympy.sqrt_mod((v ** 3 + self.A * v ** 2 + v) % self.K, self.K))
            if self.is_valid_point(p):
                return p
            if x & 0x1:
                x ^= 2 ** 497  # Prime K is 512 bits long, however the most significant 8 are discarded
                # and 8 reserved for encoded bitshifts, leaving 496 working bits
            x >>= 1

        raise("Unencodeable value")

    def decode_point(self, p):
        v = (p.x >> 497) & 0xFF  # get bitshifts number
        return ((p.x << v) % 2 ** 496 + (p.x >> (497 - v)) % 2**v) % 2**496 # move all bits to preshift, add the gsbits beyond 496 and discard


"""
Ecc = Curve()
for i in range(512):
    r = random.randint(0, 2**256)
    e = Ecc.encode_point(r)
    d = Ecc.decode_point(e)
    if r != d:
        print(r == d, hex(r), e, hex(d))
"""


"""
my_curve = Curve()
p = my_curve.multiply_np(1554984656165654065651606516561556568436516519849898491, my_curve.G)
print(my_curve.is_valid_point(p), p)

p1n = 79
p2n = 8991

p1 = my_curve.multiply_np(p1n, my_curve.G)
p2 = my_curve.multiply_np(p2n, my_curve.G)

p11 = my_curve.multiply_np(p1n, p2)
p22 = my_curve.multiply_np(p2n, p1)

print(p11 == p22, p11.x)
print(my_curve.is_valid_point(p11))

print(my_curve.multiply_np(my_curve.Order, my_curve.G))
"""
