import hashlib

import ecc
import random

curve = ecc.Curve()
N = curve.K  # The large Prime for the curve

def generate_private_key():
    return random.randint(1, N - 1)


def generate_signature(hash, private_key):
    z = int.from_bytes(hash, byteorder='big') >> 1
    ran = random.randint(1, N - 1)
    p = curve.multiply_np(ran, curve.G)
    r = p.x % N
    s = (pow(ran, -1, N) * (z + r * private_key)) % N
    return r, s


def verify_signature(hash, signature, public_key):
    z = int.from_bytes(hash, byteorder='big') >> 1
    r, s = signature
    if not curve.is_valid_point(public_key):
        return 'Invalid Public Key'
    if not 0 < r < N or not 0 < s < N:
        return 'Invalid Signature'
    w = pow(s, -1, N)
    u1 = (z * w) % N
    u2 = (r * w) % N
    p = curve.point_addition(
        curve.multiply_np(u1, curve.G), curve.multiply_np(u2, public_key))
    print(p)
    return r == p.x % N


z = hashlib.sha3_512(b"hi")
print(z.digest_size)  # prints 64
signature = generate_signature(z.digest(), 54498)
print(signature)
print(verify_signature(z.digest(), signature, curve.multiply_np(54498, curve.G)))  # outputs false


