import galois


def get(_all):
    if _all:
        prompts = ["working", "first", "second"]
    else:
        prompts = ["first"]

    results = []

    for p in prompts:
        print(f"----- {p:7} -----")
        a = []
        for k in range(8):
            print(f"v{k} > ", end="")
            a.append(int(input().strip(), 16))
        results.append(a)

    if _all:
        return results[0], results[1], results[2]
    else:
        return results[0], [0]


def x():
    # w, a1, a2 = get(True)
    a1, a2 = get(False)
    w = [0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff]
    r1, r2 = [], []

    for j in range(8):
        r1.append(galois.galois_add(a1[j], w[j]))
        r2.append(galois.galois_add(a2[j], w[j]))

    print_(r1)
    print_(r2)


def m():
    print(f"multiplicand > ", end="")
    w = int(input().strip(), 16)
    a1, a2 = get(False)
    r1, r2 = [], []

    for j in range(8):
        r1.append(galois.galois_multiply(a1[j], w))
        r2.append(galois.galois_multiply(a2[j], w))

    print_(r1)
    print_(r2)


def d():
    print(f"divisor > ", end="")
    w = int(input().strip(), 16)
    a1, a2 = get(False)
    r1, r2 = [], []

    for j in range(8):
        r1.append(galois.galois_divide(a1[j], w))
        #r2.append(galois.galois_divide(a2[j], w))

    print_(r1)
    print_(r2)


def print_(r):
    mes = ""
    for s in r:
        mes += f"{hex(s):4}\t"

    print(mes)


while True:
    # print(f"mul/div/xor > ", end="")
    # o = input().strip().lower()
    o = "d"
    if "d" in o:
        d()
    elif "x" in o:
        x()
    else:
        m()
