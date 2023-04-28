def galois_multiply(a, b):
    p = 0x00
    for i in range(8):
        if b & 0x01 == 0x01:
            p ^= a
        b = b >> 1
        if a & 0x80 == 0x80:
            a = (a << 1) ^ 0x1B
        else:
            a = a << 1
        a &= 0xFF
    return p


def galois_inverse(a):
    s, old_s = 0, 1
    t, old_t = 1, 0
    r, old_r = 0x1B, a

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    if old_r != 1:
        raise ValueError("input is not invertible")

    return s % 256


def galois_divide(dividend, divisor):
    """
    Divides the dividend by the divisor in GF(256) arithmetic.
    Returns the quotient as an integer in the range [0, 255].
    If the divisor is 0 or not invertible, returns None.
    """
    if divisor == 0 or galois_inverse(divisor) is None:
        return None
    return galois_multiply(dividend, galois_inverse(divisor))

