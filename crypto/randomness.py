from PIL import Image

import ehash
from ecryptor import Ecryptor
from ekeys import KeyScheduler

results = []
tests = 256
iterations = 4



for i in range(tests):
    print(f"{i+1}/{tests}")
    v = ehash.string_to_packets("This is 64 bytes worth of stuff that I will be encrypting.1234" + str(i))
    key = ehash.MyHash("username").hash_packs(ehash.string_to_packets("password"), 2)
    # key = ehash.MyHash(key).hash_packs(v, 4)
    results.append(Ecryptor(key, security=8, encrypt=True).cypher(v)[0])

"""
entropy = get_entropy(100, 10, True)
my_secure_random = SecureRandom(entropy)

# print(hash.packet_to_alpha_numeric(my_secure_random.hasher.internal_matrix))
for i in range(tests):
    my_secure_random.get_rand_int(100)
    results.append(my_secure_random.hasher.internal_matrix)
"""

reduced = []

for r in results:
    vals = []
    for c in r:
        t = 0
        for v in c:
            t = t << 8 | v
        vals.append(t)
    #  print(vals)
    n = 0
    for v in vals:
        n = n << (8 * 8) | v

    reduced.append(n)


#  print(reduced)

all_time_longest = 0
for value in reduced:
    ones = 0
    tested = 0
    run = 0
    longest_run = 0
    for i in range(8*8*8):
        if value >> i & 0x01 == 0x01:
            ones += 1
            run += 1
        else:
            if run > longest_run:
                longest_run = run
                if longest_run > all_time_longest:
                    all_time_longest = longest_run
            run = 0
        tested += 1
    print(ones, longest_run)

print(all_time_longest)


out_image = Image.new("RGB", (8*8*8, tests))
out_pixels = out_image.load()

for x in range(8*8*8):
    for y in range(tests):
        if reduced[y] >> x & 0x01 == 0x01:
            out_pixels[x, y] = (0, 0, 0)
        else:
            out_pixels[x, y] = (255, 255, 255)

out_image.save('bitmap_consecutive_encryptions_message1.png')
