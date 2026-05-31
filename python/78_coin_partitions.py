from project_euler import validation, solution, Progress

def partitions(lim, given=[]):
    p = [None] * lim

    for i, g in enumerate(given):
        p[i] = g

    p[0] = 1
    p[1] = 1
    p[2] = 2
    p[3] = 3


    for _, n in Progress(range(max(len(given), 4), lim)):
        p[n] = 0
        penta1 = 1
        penta2 = 2
        k = 1
        while penta1 <= n:
            d = p[n-penta1]
            if penta2 <= n:
                d += p[n-penta2]
            p[n] += d * ((-1) ** (k-1))
            penta1 += 3 * k + 1
            penta2 += 3 * k + 2
            k += 1

    return p

@validation
def validate():
    p = partitions(30)
    print("\n".join([
        f"p({i}) = {v}" for i, v in enumerate(p)
    ]))

    assert p[4] == 5, p[4]
    assert p[5] == 7, p[5]
    assert p[6] == 11, p[6]
    assert p[7] == 15, p[7]
    assert p[8] == 22, p[8]
    assert p[9] == 30, p[9]
    assert p[27] == 3010, p[27]

    p = partitions(40, given=p)
    assert p[4] == 5, p[4]
    assert p[5] == 7, p[5]
    assert p[6] == 11, p[6]
    assert p[7] == 15, p[7]
    assert p[8] == 22, p[8]
    assert p[9] == 30, p[9]
    assert p[27] == 3010, p[27]
    assert p[39] == 31185, p[39]

@solution
def solve():
    div = 10 ** 6
    delta = 10**5

    lim = 0

    res =  None
    while not res:
        lim += delta
        p = partitions(lim)
        res = next((i for i, x in enumerate(p) if x % div == 0), None)

    print(res, p[res])
    return res
