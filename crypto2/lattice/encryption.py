import numpy as np
import random

# Generate a random n x m matrix with entries in Z_q
def generate_random_matrix(n, m, q):
    return np.random.randint(0, q, (n, m))

# Generate a random vector with entries in Z_q
def generate_random_vector(n, q):
    return np.random.randint(0, q, n)

# Generate a random error vector e with entries in {-1, 0, 1}
def generate_random_error(n):
    return np.array([random.choice([-1, 0, 1]) for _ in range(n)])

# Encrypt a message m using a public key A and noise vector e
def encrypt(m, A, q):
    n, m = A.shape
    r = generate_random_vector(m, q)
    e = generate_random_error(n)
    c = (np.dot(A, r) + q*m + e) % q
    ct = (m + c).tolist()
    return ct

# Decrypt a ciphertext c using a private key s
def decrypt(c, s, q):
    m = (c - np.dot(s, c)) % q
    return m

# Example usage
n = 5 # number of rows in matrix A
m = 4 # number of columns in matrix A
q = 17 # modulus for encryption
A = generate_random_matrix(n, m, q) # public key
s = generate_random_vector(m, q) # private key
m = 7 # message to encrypt
c = encrypt(m, A, q) # ciphertext
decrypted_message = decrypt(c, s, q) # decrypted message
print(f"Original message: {m}")
print(f"Decrypted message: {decrypted_message}")
