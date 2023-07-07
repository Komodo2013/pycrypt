from crypto2.utils.galois import galois_multiply
from subs import s_box

# sooooooo pi has no inverse.... this is super important later... but it doesn't work for this
""" Here are the values as I attempt to inverse the matrices:
201	196	41	2	81	239	48	79	
15	198	2	11	74	149	43	225	
218	98	78	190	8	25	10	53	
162	139	8	166	121	179	109	109	
33	128	138	59	142	205	242	109	
104	220	103	19	52	58	95	81	
194	28	204	155	4	67	20	194	
52	209	116	34	221	27	55	69	

122	157	224	238	206	83	2	137	
0	0	0	0	0	0	0	0	
140	125	78	140	242	6	87	27	
229	63	65	109	220	163	160	196	
75	105	167	183	77	118	39	103	
99	141	1	144	174	158	127	56	
149	178	44	238	175	33	154	39	
2	124	253	10	23	191	51	119	

96	0	181	99	65	221	36	37	
31	0	135	128	29	93	95	12	
48	0	212	191	174	224	18	156	
158	0	48	6	249	160	214	195	
101	0	194	198	19	248	34	130	
100	0	205	51	77	108	120	213	
168	0	10	182	32	180	139	80	
54	0	71	217	179	2	183	123	

0	0	0	0	0	0	0	0	
0	0	0	0	0	0	0	0	
0	0	0	0	0	0	0	0	
0	0	0	0	0	0	0	0	
0	0	0	0	0	0	0	0	
0	0	0	0	0	0	0	0	
0	0	0	0	0	0	0	0	
0	0	0	0	0	0	0	0	
# By 4th matrix, pi has reduced to an irreducible  matrix
"""


def def_pitrix():
    # This is pi with a precision of 512 bits generated like
    # mpmath.mp.dps = 512
    # pi = mpmath.mp.pi
    # piis = bytearray(int(pi * 2 ** 510).to_bytes(length=64, byteorder='big'))
    # I then broke the bytearray into a 2d array of the first 64 bytes
    # This matrix has no inverse, see note above
    return [
        201, 196, 41, 2, 81, 239, 48, 79,
        15, 198, 2, 11, 74, 149, 43, 225,
        218, 98, 78, 190, 8, 25, 10, 53,
        162, 139, 8, 166, 121, 179, 109, 109,
        33, 128, 138, 59, 142, 205, 242, 109,
        104, 220, 103, 19, 52, 58, 95, 81,
        194, 28, 204, 155, 4, 67, 20, 194,
        52, 209, 116, 34, 221, 27, 55, 69
    ]


def def_root2rix():
    # sqrt_two = mpmath.mp.sqrt(2)
    # sqrt_two_bits = bytearray(int(sqrt_two * 2 ** 511).to_bytes(length=64, byteorder='big'))
    return [
        181, 89, 29, 237, 74, 168, 15, 120,
        4, 125, 111, 23, 252, 177, 116, 4,
        243, 137, 96, 172, 131, 254, 168, 135,
        51, 179, 186, 133, 4, 111, 94, 54,
        249, 117, 137, 131, 58, 220, 67, 61,
        222, 74, 59, 51, 184, 131, 156, 250,
        100, 190, 168, 153, 162, 219, 123, 39,
        132, 159, 76, 21, 195, 57, 74, 104
    ]


def def_inv_root2rix():
    return [
        87, 194, 111, 169, 200, 38, 195, 160,
        133, 246, 115, 224, 69, 75, 164, 97,
        155, 206, 56, 19, 16, 247, 147, 165,
        24, 60, 164, 231, 234, 158, 195, 147,
        149, 240, 53, 0, 197, 233, 113, 150,
        28, 21, 24, 67, 69, 88, 150, 99,
        167, 156, 77, 74, 207, 170, 136, 3,
        78, 70, 195, 198, 174, 97, 235, 255
    ]

def def_root3rix():
    # sqrt_three = mpmath.mp.sqrt(3)
    # sqrt_three_bits = bytearray(int(sqrt_three * 2 ** 511).to_bytes(length=64, byteorder='big'))
    return [
        221, 146, 146, 99, 36, 212, 230, 104,
        179, 186, 236, 144, 133, 201, 38, 102,
        215, 22, 26, 83, 231, 133, 121, 153,
        66, 184, 102, 36, 236, 87, 38, 208,
        194, 60, 41, 55, 175, 9, 209, 13,
        101, 92, 237, 34, 120, 17, 208, 108,
        83, 29, 35, 211, 174, 71, 246, 209,
        157, 196, 204, 113, 222, 195, 52, 193
    ]

def def_inv_root3rix():
    return [
        127, 125, 125, 252, 78, 184, 127, 19,
        246, 24, 113, 97, 244, 241, 45, 175,
        102, 53, 102, 140, 97, 15, 112, 42,
        52, 211, 198, 89, 183, 72, 121, 220,
        146, 211, 198, 7, 119, 80, 251, 166,
        81, 182, 139, 53, 145, 138, 240, 190,
        42, 179, 228, 199, 63, 191, 123, 136,
        87, 170, 152, 30, 80, 220, 90, 118,
    ]

def print_matrix(e, size=8):
    s = ""

    for j in range(size):
        for l in range(size):
            s += f"{e[j * size + l]}\t"
        s += "\n"

    print(s)


def mult_matrix(a, b, size=8):
    r = bytearray(size * size)  # Initialize result bytearray with zeros

    for i in range(size):  # for each row
        for j in range(size):
            for k in range(size):
                r[i*size + j] ^= galois_multiply(a[i*size + k], b[k*size + j])

    return r


def subs_matrix(a):
    r = bytearray(len(a))  # Initialize result bytearray with zeros

    for i in range(len(a)):  # for each row
        r[i] ^= s_box[a[i]]

    return r


def identity_matrix():
    return [
        1, 0, 0, 0, 0, 0, 0, 0,
        0, 1, 0, 0, 0, 0, 0, 0,
        0, 0, 1, 0, 0, 0, 0, 0,
        0, 0, 0, 1, 0, 0, 0, 0,
        0, 0, 0, 0, 1, 0, 0, 0,
        0, 0, 0, 0, 0, 1, 0, 0,
        0, 0, 0, 0, 0, 0, 1, 0,
        0, 0, 0, 0, 0, 0, 0, 1
    ]

def empty_matrix():
    return [
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0
    ]
