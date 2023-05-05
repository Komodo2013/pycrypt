import hashlib
import random

def sha512(data):
    """Computes the SHA-512 hash of the given data."""
    return hashlib.sha512(data).digest()
