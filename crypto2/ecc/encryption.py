


def encrypt(key, data, rounds=20):
    for r in range(rounds):
        data = ?

def decrypt(key, data, rounds=20):
    pass


"""
def encryption(p, ks, r):

    for R in range(r-1):
        p = shift_rows(xor_2d_matrices(matrix_mult(p, enc), ks.get_key()))

    return xor_2d_matrices(matrix_mult(p, enc), ks.get_key())


def decryption(p, ks, r):

    p = matrix_mult(xor_2d_matrices(p, ks.get_key()), dec)

    for R in range(r-1):
        p = matrix_mult(xor_2d_matrices(inv_shift_rows(p), ks.get_key()), dec)

    return p
"""


"""
v = "This is 64 bytes worth of stuff that I will be encrypting.12345"
key1 = MyHash().set_internal_matrix("username").hash_packs(string_to_packets("supersecret"), 8)
key2 = MyHash().set_internal_matrix("username").hash_packs(string_to_packets("supersecret"), 8)
my_cryptor = Ecryptor(key1, security=8, encrypt=True)
my_decryptor = Ecryptor(key2, security=8, encrypt=False)
mess = string_to_packets("This will be our secret")
print("message:  ", packet_to_alpha_numeric(mess[0]))
encrypt = my_cryptor.cypher(mess)
print("encrypted:", packet_to_alpha_numeric(encrypt[0]))
decrypt = my_decryptor.cypher(encrypt)
print("decrypted:", packet_to_alpha_numeric(decrypt[0]))
"""
