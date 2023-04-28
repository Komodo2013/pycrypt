import math
from galois import galois_multiply
primes = [
    67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157,
    163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257
]

def pad_message(message):
    # Convert the message to bytes
    if isinstance(message, str):
        message = message.encode()
    # Determine how many null bytes need to be added
    padding_len = 64 - (len(message) % 64)
    # Add the null bytes and the length of the message
    padded_message = message + b'\x00' * padding_len + len(message).to_bytes(8, byteorder='big')
    return padded_message


def chunk_message(message):
    # Break the message into 512-bit (64-byte) chunks
    num_chunks = math.ceil(len(message) / 64)
    chunks = []
    for i in range(num_chunks):
        chunk = message[i*64:(i+1)*64]
        chunks.append(chunk)
    return chunks


import random


def byte_to_string(byte, charset='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,'
                                 '-./:;<=>?@[\\]^_`{|}~', p=97):
    b1 = byte >> 8
    b2 = byte & 0xff
    return charset[(b2 ^ galois_multiply(b1, b2)) % len(charset)]


char_set = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
test_set = {char: 0 for char in char_set}
print(len(char_set))

for _ in range(256):
    # Example usage
    random_string = byte_to_string(random.randint(0, 65536))
    test_set[random_string] += 1

for k, v in test_set.items():
    if v == 0:
        print(k)
