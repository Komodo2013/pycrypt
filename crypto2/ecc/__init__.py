import mpmath
from crypto2.utils.galois import galois_multiply, galois_inverse

def print_matrix(e, size=8):
    s = ""

    for j in range(size):
        for l in range(size):
            s += f"{e[j][l]}\t"
        s += "\n"

    print(s)


def mult_matrix(a, b, size=8):
    r = [[], [], [], [], [], [], [], []]
    for _i in range(size):  # for each row
        for _j in range(size):
            r[_i].append(0)
            for _k in range(size):
                r[_i][_j] ^= galois_multiply(a[_i][_k], b[_k][_j])
    return r


# I use an initialization vector for this hash algorith of pi, built to 512 bits
# I chose this because
mpmath.mp.dps = 512  # Set the desired precision in decimal places
pi = mpmath.mp.pi  # Compute pi with the specified precision
# convert pi to 512 bit int... remember 3 in 3.13 is 2 bits thus 512-2 = 510

piis = bytearray(int(pi * 2 ** 510).to_bytes(length=64, byteorder='big'))


def def_pitrix():
    r = [[], [], [], [], [], [], [], []]
    for _j in range(8):
        for _l in range(8):
            r[_l].append(piis[(_l & 7) + (_j * 8)])
    return r

def def_identity():
    # Create identity matrix
    _ident = []
    for j in range(8):
        _ident.append([])
        for l in range(8):
            _ident[j].append(0x00)
    for j in range(8):
        _ident[j][j] = 0x01
    # _inverse is now an identity matrix
    return _ident

def invert_matrix(_a, size=8):
    _inverse = def_identity()

    for k in range(size): # setting all the digits to 0 >:)
        for i in range(size):  # for each row
            div = galois_inverse(_a[i][k])
            for j in range(size):  # for each column
                _inverse[i][j] = galois_multiply(_inverse[i][j], div)
                _a[i][j] = galois_multiply(_a[i][j], div)

        for i in range(size): #for each row
            if i != k:
                for j in range(size):
                    _inverse[i][j] ^= _inverse[k][j]
                    _a[i][j] ^= _a[k][j]

    for k in range(size-1):
        div = galois_inverse(_a[k][k])
        for j in range(size):  # for each column
            _inverse[k][j] = galois_multiply(_inverse[k][j], div)
            _a[k][j] = galois_multiply(_a[k][j], div)

    return _inverse


array = def_pitrix()
inverse = invert_matrix(array)
array = def_pitrix()  # reset the array with pitrix (pi as a matrix)

print_matrix(array)
print_matrix(inverse)

m = mult_matrix(array, inverse)
print_matrix(m)

print_matrix(mult_matrix(m, inverse))
