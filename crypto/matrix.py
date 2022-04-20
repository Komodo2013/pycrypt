from crypto.galois import galois_multiply, galois_inv

e = (
        [58, 159, 9, 102, 211, 67, 78, 8],
        [82, 71, 182, 32, 163, 204, 171, 169],
        [254, 70, 97, 238, 203, 230, 13, 128],
        [116, 108, 131, 94, 35, 226, 22, 211],
        [194, 30, 214, 40, 139, 72, 230, 152],
        [197, 128, 204, 187, 58, 223, 172, 23],
        [172, 44, 80, 111, 233, 28, 154, 14],
        [193, 84, 110, 43, 196, 206, 38, 127]
)

d = (
        [0x20, 0x66, 0x3b, 0x74, 0x25, 0xb8, 0x03, 0x1b],
        [0xa8, 0xbd, 0xfa, 0x81, 0xf1, 0x38, 0x1a, 0x66],
        [0xbe, 0xc2, 0x16, 0x9c, 0xb7, 0x8c, 0x7e, 0x0b],
        [0x43, 0x5a, 0x2b, 0xbb, 0x91, 0xe8, 0x64, 0xbe],
        [0xa6, 0x9a, 0x31, 0x35, 0xde, 0x79, 0x17, 0x0a],
        [0xfc, 0xb6, 0xd1, 0x61, 0xd2, 0x8b, 0x2a, 0x4b],
        [0xc4, 0x7f, 0xe4, 0xec, 0xd1, 0x23, 0x07, 0x9c],
        [0x0b, 0x11, 0xdd, 0x6a, 0x27, 0xe1, 0xc6, 0xc8]
)


def solve(r, c, a, b):
    solution = 0x00
    for i in range(8):
        solution ^= galois_multiply(a[r][i], b[i][c])
    return solution


def matrix_mult(a, b):
    c = []
    for i in range(8):
        c.append([])
        for j in range(8):
            c[-1].append(solve(i, j, a, b))

    return c


def solve_for(i, prim, inv):
    for j in range(8):
        if prim[j][i] != 0:
            div = galois_inv(prim[j][i])
            for c in range(8):
                prim[j][c] = galois_multiply(prim[j][c], div)
                inv[j][c] = galois_multiply(inv[j][c], div)

    return prim, inv


def subtract(i, prim, inv):
    for j in range(8):
        if i != j and prim[j][i] != 0:
            for k in range(8):
                prim[j][k] ^= prim[i][k]
                inv[j][k] ^= prim[i][k]

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

    prim = a[:]

    for i in range(8):
        print(f"starting row {i}")
        prim, inv = solve_for(i, prim, inv)
        print(f"row mult")
        prim, inv = subtract(i, prim, inv)
        print(f"finished row {i}")
        for j in range(8):
            print(f"\t{prim[j]}")

    for i in range(8):
        prim, inv = solve_for(i, prim, inv)
        print(prim[i])

    return inv


inverted = inverse_matrix(e)
print("Inverted:")
for ro in inverted:
    print(f"\t{ro}")


v = matrix_mult(e, inverted)

print("\n\nmultiplied")
for ro in v:
    print(f"\t{ro}")

