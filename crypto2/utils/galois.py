def galois_multiply(a, b):
    p = 0
    """
    a 10= 0 0 0 1
    b 1 = 0 0 0 0
    p 5 = 0 0 0 0 
    """
    for _ in range(8):
        if b & 1 == 0x01:  # Check if the rightmost bit of b is set
            p ^= a  # XOR the product p by the value of a

        b >>= 1  # Shift b one bit to the right

        carry = a & 0x80  # Check if the leftmost bit of a is set
        a = (a << 1) & 0xff  # Shift a one bit to the left
        if carry:
            a ^= 0x1b  # XOR a with 0x1b if carry is 1 01010011 19 + 64 83 0x53

    return p % 0xff  # Take the result modulo 256 to stay within the field range (0 to 255)

def galois_divide(dividend, divisor):
    """
    Divides the dividend by the divisor in GF(256) arithmetic.
    Returns the quotient as an integer in the range [0, 255].
    If the divisor is 0 or not invertible, returns None.
    """
    if divisor == 0 or galois_inverse(divisor) is None:
        return None
    return galois_multiply(dividend, galois_inverse(divisor))


# Inverse mod lookup table... I got this from:
# https://tratliff.webspace.wheatoncollege.edu/2016_Fall/math202/inclass/sep21_inclass.pdf
# accessed 11 May 2023
galois_inverse_table = [
    0x00, 0x01,  0x8D,  0xF6, 0xCB, 0x52, 0x7B, 0xD1, 0xE8, 0x4F, 0x29, 0xC0, 0xB0, 0xE1, 0xE5, 0xC7,
    0x74, 0xB4,  0xAA,  0x4B, 0x99, 0x2B, 0x60, 0x5F, 0x58, 0x3F, 0xFD, 0xCC, 0xFF, 0x40, 0xEE, 0xB2,
    0x3A, 0x6E,  0x5A,  0xF1, 0x55, 0x4D, 0xA8, 0xC9, 0xC1, 0x0A, 0x98, 0x15, 0x30, 0x44, 0xA2, 0xC2,
    0x2C, 0x45,  0x92,  0x6C, 0xF3, 0x39, 0x66, 0x42, 0xF2, 0x35, 0x20, 0x6F, 0x77, 0xBB, 0x59, 0x19,
    0x1D, 0xFE,  0x37,  0x67, 0x2D, 0x31, 0xF5, 0x69, 0xA7, 0x64, 0xAB, 0x13, 0x54, 0x25, 0xE9, 0x09,
    0xED, 0x5C,  0x05,  0xCA, 0x4C, 0x24, 0x87, 0xBF, 0x18, 0x3E, 0x22, 0xF0, 0x51, 0xEC, 0x61, 0x17,
    0x16, 0x5E,  0xAF,  0xD3, 0x49, 0xA6, 0x36, 0x43, 0xF4, 0x47, 0x91, 0xDF, 0x33, 0x93, 0x21, 0x3B,
    0x79, 0xB7,  0x97,  0x85, 0x10, 0xB5, 0xBA, 0x3C, 0xB6, 0x70, 0xD0, 0x06, 0xA1, 0xFA, 0x81, 0x82,
    0x83, 0x7E,  0x7F,  0x80, 0x96, 0x73, 0xBE, 0x56, 0x9B, 0x9E, 0x95, 0xD9, 0xF7, 0x02, 0xB9, 0xA4,
    0xDE, 0x6A,  0x32,  0x6D, 0xD8, 0x8A, 0x84, 0x72, 0x2A, 0x14, 0x9F, 0x88, 0xF9, 0xDC, 0x89, 0x9A,
    0xFB, 0x7C,  0x2E,  0xC3, 0x8F, 0xB8, 0x65, 0x48, 0x26, 0xC8, 0x12, 0x4A, 0xCE, 0xE7, 0xD2, 0x62,
    0x0C, 0xE0,  0x1F,  0xEF, 0x11, 0x75, 0x78, 0x71, 0xA5, 0x8E, 0x76, 0x3D, 0xBD, 0xBC, 0x86, 0x57,
    0x0B, 0x28,  0x2F,  0xA3, 0xDA, 0xD4, 0xE4, 0x0F, 0xA9, 0x27, 0x53, 0x04, 0x1B, 0xFC, 0xAC, 0xE6,
    0x7A, 0x07,  0xAE,  0x63, 0xC5, 0xDB, 0xE2, 0xEA, 0x94, 0x8B, 0xC4, 0xD5, 0x9D, 0xF8, 0x90, 0x6B,
    0xB1, 0x0D,  0xD6,  0xEB, 0xC6, 0x0E, 0xCF, 0xAD, 0x08, 0x4E, 0xD7, 0xE3, 0x5D, 0x50, 0x1E, 0xB3,
    0x5B, 0x23,  0x38,  0x34, 0x68, 0x46, 0x03, 0x8C, 0xDD, 0x9C, 0x7D, 0xA0, 0xCD, 0x1A, 0x41, 0x1C
]

def galois_inverse(a):
    return galois_inverse_table[a]
