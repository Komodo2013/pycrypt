import ecc
from crypto2.utils.secure_random import Secure_Random
from sympy import mod_inverse

curve = ecc.Curve()
N = curve.Order  # The large Prime for the curve
sr = Secure_Random()

def generate_private_key():
    return sr.get_random_int(1, N - 1)


def generate_signature(hash, private_key):
    """
    given da is a private key integer within [1, n-1] and public key q = da * G
    1. Calculate e = Hash(m)
    2. Let z be Ln leftmost bits of e where Ln is the bit length of the group order n
    3. select secure random int k from [1,n-1]
    4. find point p = k x G
    5. find r = px mod n if == 0 then redo
    6. calculate s = k-1 (z +r * da) mod n if == 0 then redo
    7. signature pair (r, s)
    """
    z = int.from_bytes(hash, byteorder='big')
    k = sr.get_random_int(1, N - 1)
    p = curve.multiply_np(k, curve.G)
    r = p.x % N
    s = (mod_inverse(k, N) * (z + r * private_key)) % N
    return r, s


def verify_signature(hash, signature, public_key):
    """
        given da is a private key integer within [1, n-1] and public key q = da * G
        check q is valid point not identity and n * q = identity else fail
        1. Calculate e = Hash(m)
        2. Let z be Ln leftmost bits of e where Ln is the bit length of the group order n
        3. find u1 = z * s-1 mod n and u2 = r * s-1 mod n
        4. find point p = u1 * G + u2 * q if identity then fail
        5. r == px mod n
        """
    z = int.from_bytes(hash, byteorder='big')
    r, s = signature
    if not curve.is_valid_point(public_key):
        return 'Invalid Public Key'
    if not 0 < r < N or not 0 < s < N:
        return 'Invalid Signature'
    w = mod_inverse(s, N)
    u1 = (z * w) % N
    u2 = (r * w) % N
    p = curve.point_addition(
        curve.multiply_np(u1, curve.G), curve.multiply_np(u2, public_key))
    print(p)
    return r == p.x % N


"""
z = hashlib.sha3_512(b"hi")
print(int.from_bytes(z.digest(), byteorder='big'))  # prints 64
signature = generate_signature(z.digest(), 54498)
print(signature)
print(verify_signature(z.digest(), signature, curve.multiply_np(54498, curve.G)))  # outputs false
"""
