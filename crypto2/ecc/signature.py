import ecc
import random

class Signer:
    self.curve = ecc.Curve()

    def __init__(self):
        pass


def generate_private_key():
    """Generates a random private key (integer) between 1 and n-1."""
    return random.randint(1, n-1)

def generate_signature(hash, private_key):
    """Generates an ECDSA signature for the given message using the specified private key."""
    k = random.randint(1, n-1)
    r, y = point_multiplication(k, G)
    s = pow(k, -1, n) * (hash + r*private_key) % n
    return r, s

def verify_signature(hash, signature, public_key):
    """Verifies an ECDSA signature for the given message using the specified public key."""
    r, s = signature
    if not 0 < r < n or not 0 < s < n:
        return False
    w = pow(s, -1, n)
    u1 = (hash * w) % n
    u2 = (r * w) % n
    x, y = point_addition
