from crypto.galois import galois_multiply, galois_inv
import ehash
from crypto.packet_utils import string_to_packets

size = 8

e = (
    # [0][5] 67->66 I had to change this because with > 6x6, the inverse becomes unsolvable. By changing the lsb here,
    # I was able to adapt pi's matrix to become solvable again.
    [58, 159, 9, 102, 211, 66,  # This value right here
     78, 8],
    [82, 71, 182, 32, 163, 204, 171, 169],
    [254, 70, 97, 238, 203, 230, 13, 128],
    [116, 108, 131, 94, 35, 226, 22, 211],
    [194, 30, 214, 40, 139, 72, 230, 152],
    [197, 128, 204, 187, 58, 223, 172, 23],
    [172, 44, 80, 111, 233, 28, 154, 14],
    [193, 84, 110, 43, 196, 206, 38, 127]
)

d = (
    [220, 188, 146, 102, 214, 19, 3, 27],
    [29, 242, 140, 110, 208, 218, 107, 159],
    [80, 24, 33, 111, 57, 109, 171, 27],
    [95, 143, 74, 241, 192, 214, 144, 121],
    [118, 240, 214, 97, 66, 120, 220, 98],
    [241, 204, 100, 97, 153, 76, 73, 120],
    [250, 165, 76, 45, 31, 224, 73, 62],
    [43, 122, 123, 216, 2, 111, 142, 185]
)

f = (
    [28, 180, 37, 12, 37, 231, 41, 113],
    [165, 196, 127, 50, 125, 168, 215, 197],
    [15, 89, 203, 188, 127, 38, 185, 15],
    [248, 205, 161, 35, 39, 102, 142, 9],
    [168, 156, 153, 108, 181, 24, 173, 3],
    [246, 178, 29, 90, 91, 243, 43, 162],
    [28, 214, 198, 226, 239, 187, 142, 141],
    [174, 174, 223, 206, 171, 214, 135, 169]
)


def matrix_mult(a, b):
    m = []
    for ii in range(size):
        m.append([])
        for ll in range(size):
            m[-1].append(0)

    for k in range(size):
        for j in range(size):
            res = 0
            for i in range(size):
                res ^= galois_multiply(a[i][k], b[j][i])
            m[j][k] = res

    return m


def solve_for(_i, prim, inv):
    for _j in range(size):
        if prim[_j][_i] != 0:
            div = galois_inv(prim[_j][_i])
            for c in range(size):
                prim[_j][c] = galois_multiply(prim[_j][c], div)
                inv[_j][c] = galois_multiply(inv[_j][c], div)

    return prim, inv


def subtract(_i, prim, inv):
    for _j in range(size):
        if _i != _j:
            for _k in range(size):
                prim[_j][_k] ^= prim[_i][_k]
                inv[_j][_k] ^= inv[_i][_k]

    return prim, inv


def inverse_matrix(a):
    inv = [[0x1, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0],
           [0x0, 0x1, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0],
           [0x0, 0x0, 0x1, 0x0, 0x0, 0x0, 0x0, 0x0],
           [0x0, 0x0, 0x0, 0x1, 0x0, 0x0, 0x0, 0x0],
           [0x0, 0x0, 0x0, 0x0, 0x1, 0x0, 0x0, 0x0],
           [0x0, 0x0, 0x0, 0x0, 0x0, 0x1, 0x0, 0x0],
           [0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x1, 0x0],
           [0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x1]]
    prim = []

    for r in a:
        prim.append(r[:])

    for _i in range(size):
        prim, inv = solve_for(_i, prim, inv)
        prim, inv = subtract(_i, prim, inv)

    for _i in range(size):
        prim, inv = solve_for(_i, prim, inv)

    return inv


# inverted = inverse_matrix(e)
# print("Inverted:")
# for ro in inverted:
#     print(f"\t{ro}")
#
# multa = matrix_mult(e, f)
# print("\n\nmultiplied")
# for ro in multa:
#     print(f"\t{ro}")
#
# mult = matrix_mult(inverted, multa)
#
# print("\n\nmultiplied")
# for ro in mult:
#     print(f"\t{ro}")
