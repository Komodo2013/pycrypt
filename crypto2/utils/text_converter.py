import math

import scipy

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


def byte_to_string(byte, charset='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,'
                                 '-./:;<=>?@[\\]^_`{|}~', p=97):
    b1 = byte >> 8
    b2 = byte & 0xff
    return charset[(b2 ^ (galois_multiply(b1, p) % (2 ** 4))) % len(charset)]


"""
char_set = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
Standard deviation: 122.40873506990367
Range: 369
Pval: 1.1102230246251565e-16
Is equal: False
Power: 0.974006065039719
"""

"""
char_set = 0'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
Standard deviation: 92.33154226187767
Range: 370
Pval: 1.1102230246251565e-16
Is equal: False
Power: 0.9419767711966611
"""
"""
char_set = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_:;-=+'
Standard deviation: 107.28593649015195
Range: 357
Pval: 1.1102230246251565e-16
Is equal: False
Power: 0.9502895581141863
"""

"""

import random
import statistics

char_set = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_:;-=+'
test_set = {char: 0 for char in char_set}
print(len(char_set))

for _ in range(65536):
    # Example usage
    random_string = byte_to_string(random.randint(0, 65536), charset=char_set, p=67)
    test_set[random_string] += 1

expected = (2 ** 16) // len(char_set)
print("expected values: ", expected)
fails = ''

for k, v in test_set.items():
    if v == 0:
        fails += k

print(test_set)
print(f"Test did not include: {fails}")

for v in char_set:
    test_set[v] -= expected

# Get the values from the dictionary
values = list(test_set.values())

# Calculate quartiles
q1 = statistics.quantiles(values, n=4)[0]
q2 = statistics.quantiles(values, n=4)[1]
q3 = statistics.quantiles(values, n=4)[2]

# Calculate standard deviation
stdev = statistics.stdev(values)

# Calculate range
range_val = max(values) - min(values)

# Print the results
print("Quartiles:")
print(f"Q1: {q1}")
print(f"Q2: {q2}")
print(f"Q3: {q3}")
print(f"Standard deviation: {stdev}")
print(f"Range: {range_val}")

n = len(test_set)
mean = sum(test_set.values()) / n
ssd = sum([(x - mean) ** 2 for x in test_set.values()])
stdev = math.sqrt(ssd / (n - 1))

# Calculate the F statistic
f_stat = (n - 1) * ssd / stdev ** 2

# Calculate the p-value using the F distribution
p_value = 1 - scipy.stats.f.cdf(f_stat, n - 1, n - 1)

# Return whether the values are equal and the power of the test
is_equal = p_value > 0.05
power = 1 - scipy.stats.f.sf(1.5, n - 1, n - 1)

print(f"Pval: {p_value}\nIs equal: {is_equal}\nPower: {power}")
"""
