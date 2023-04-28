import numpy as np
from scipy.linalg import solve_triangular
from numpy.linalg import matrix_rank

def generate_lattice(n, m, q):
    """
    Generates an m x n lattice with coefficients in Z_q
    """
    return np.random.randint(low=-q, high=q+1, size=(m, n))

def lattice_hash(msg, lattice, q):
    """
    Computes the hash of a message using the SIS problem in a lattice
    """
    m, n = lattice.shape
    A = np.hstack([lattice, msg.reshape(-1, 1)])
    reduced_A = np.linalg.qr(A)[0][:, :-1]
    if matrix_rank(reduced_A) < n:
        raise ValueError("Hashing failed. Please try again with a different message or lattice.")
    y = np.random.randint(low=-q, high=q+1, size=(n, 1))
    b = np.matmul(lattice, y) % q
    s = solve_triangular(reduced_A, b)
    hash_val = np.vstack([s, y]).flatten()
    return hash_val


