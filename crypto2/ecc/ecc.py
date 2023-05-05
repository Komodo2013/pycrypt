"""
This is an updated version of my ECC algorith that will be used
"""

# Designed for use of the M-511 as defined:
# y**2 ≡ x**3 + 486662x**2 + x (mod 2**255 - 19)
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

    def define_curve(self, a, b, k, order, g):
        self.A = a
        self.B = b
        self.K = k
        self.Order = order
        self.G = g

    def is_valid_point(self, p):
        """
        Determine whether we have a valid representation of a point
        on our curve.  We assume that the x and y coordinates
        are always reduced modulo p, so that we can compare
        two points for equality with a simple ==.
        """
        if p == self.Origin:
            return True
        else:
            return (
                    (self.B * p.y ** 2 - (p.x ** 3 + self.A * p.x ** 2 + p.x)) % self.K == 0 and
                    0 <= p.x < self.K and 0 <= p.y < self.K)

    def inv_mod_p(self, x):
        """
        Compute an inverse for x modulo p, assuming that x
        is not divisible by p.
        """
        if x % self.K == 0:
            raise ZeroDivisionError("Impossible inverse")
        return pow(x, self.K-2, self.K)

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
        for _ in range(256):
            if n & 1:
                p2 = self.point_calc(p2, pmultplier)

            pmultplier = self.point_double(pmultplier)
            n = n >> 1
        return p2

    def point(self, x):
        return {'x': x, 'y': sympy.sqrt_mod((x ** 3 + self.A * x ** 2 + x) % self.K, self.K)}


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
"""
