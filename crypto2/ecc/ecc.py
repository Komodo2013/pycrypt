# Designed for use of the M-511 as defined:
# y^2 = x^3 + x^2 + x mod 2**521-1
from collections import namedtuple
Point = namedtuple("Point", "x y")


class EllipticCurve:
    def __init__(self):
        self.A = 1
        self.B = 1
        self.K = 2**521 - 1
        self.Order = 2**519 - 337554763258501705789107630418782636071904961214051226618635150085779108655765
        self.G = Point(0x1b9a6fc6f479155c6936baa30f0d8c32a86aaa40cdedc09b5ea0c5bfc8, 0x3f0eba4a9d8c0a057e569b3d00bceda8d7a6f9ec03e13ae1a)
        self.Origin = Point(None, None)

    def define_curve(self, a, b, k, order, g):
        self.A = a
        self.B = b
        self.K = k
        self.Order = order
        self.G = g

    def is_valid_point(self, p):
        if p == self.Origin:
            return True
        else:
            return True
            y2 = p.y ** 2
            x3_ax_b = p.x ** 3 + self.A * p.x + self.B
            if y2 - x3_ax_b < 0:
                return False
            return (y2 - x3_ax_b) % self.K == 0

    def inv_mod_p(self, x):
        if x % self.K == 0:
            raise ZeroDivisionError('Cannot divide by zero')

        return pow(x, self.K - 2, self.K)

    def ec_inv(self, p):
        if p == self.Origin:
            return p

        return Point(p.x, (-p.y) % self.K)

    def point_double(self, p):
        if p == self.Origin:
            return self.Origin

        l = ((3 * p.x ** 2 + 2 * self.A * p.x + 1) * self.inv_mod_p(2 * self.B * p.y)) % self.K
        x = (self.B * l ** 2 - self.A - 2 * p.x) % self.K
        y = ((3 * p.x + self.A) * l - self.B * l ** 3 - p.y) % self.K
        return Point(x, y)

    def point_addition(self, p1, p2):
        if p1 == self.Origin:
            return p2
        elif p2 == self.Origin:
            return p1

        if p1.x == p2.x and p1.y != p2.y:
            return self.Origin

        if p1 == self.ec_inv(p2) or p2 == self.ec_inv(p1):
            return self.Origin

        if p1 == p2:
            return self.point_double(p1)

        l = ((p2.y - p1.y) * self.inv_mod_p(p2.x - p1.x)) % self.K
        x = (self.B * l ** 2 - self.A - p1.x - p2.x) % self.K
        y = ((p1.x + x) * l - p1.y) % self.K
        return Point(x, y)

    def point_calc(self, p1, p2):
        if not (self.is_valid_point(p1) and self.is_valid_point(p2)):
            raise ValueError('Input is not a valid point')

        if p1 == self.Origin:
            return p2
        elif p2 == self.Origin:
            return p1

        if p1 == self.ec_inv(p2):
            return self.Origin

        if p1 == p2:
            return self.point_double(p1)

        return self.point_addition(p1, p2)

    def multiply_np(self, n, p):
        if not self.is_valid_point(p):
            raise ValueError('Input is not a valid point')

        if n % self.K == 0:
            return self.Origin

        if n < 0:
            n = -n
            p = self.ec_inv(p)

        pmultiplier = p
        p2 = self.Origin

        while n > 0:
            if n & 1:
                p2 = self.point_calc(p2, pmultiplier)


my_curve = EllipticCurve()
print(my_curve.is_valid_point(my_curve.G))
p = my_curve.multiply_np(1554984656165654065651606516561556568436516519849898491, my_curve.G)
print(my_curve.is_valid_point(p), p)

p1n = 79
p2n = 8991

p1 = my_curve.multiply_np(p1n, my_curve.G)
p2 = my_curve.multiply_np(p2n, my_curve.G)

p11 = my_curve.multiply_np(p1n, p2)
p22 = my_curve.multiply_np(p2n, p1)

print(p11 == p22, p11.x)
