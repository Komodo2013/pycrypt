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
        return None

    return s % 256

print(galois_multiply(0x03, 0x09))
print(galois_inverse(0x19))
print(galois_multiply(0x09, galois_inverse(0x19)))
