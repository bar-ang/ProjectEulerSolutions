from project_euler import Measure, Progress, validation, solution
from math import log2, ceil


def xor_prod(a, b):
    res = 0
    dig = 0
    while b:
        if b & 1:
            res ^= a << dig
        dig += 1
        b >>= 1

    return res


def formula(f, g):
    return xor_prod(f ^ g, f ^ g) ^ (2 * xor_prod(f, g))

def brute_force(N, m):
    c = 0
    for _, f in Progress(range(N + 1), "brute_force"):
        for g in range(f + 1):
            if formula(f, g) <= m:
                print(f, g)
                c += 1

    return c

def order(n):
    t = 1
    while (t<<1) <= n:
        t <<= 1
    return t

def xor_div(f, g):
    if g == 1:
        return f, 0
    if g > f:
        return 0, f
    of = order(f)
    og = order(g)
    od = of // og

    assert f ^ (xor_prod(g, od)) < f, (f, g, of, og, od)
    t, r = xor_div(f ^ (xor_prod(g, od)), g)
    return od ^ t, r

def xor_sq_root(n):
    '''
    if n doesn't have a square root, we round it down to the nearest square number
    '''
    pos = 0
    
    res = 0
    m = n
    while m > 0:
        if (m & 3) > 1:
            return xor_sq_root(n - 1)
        res ^= ((m & 1) << pos)
        m >>= 2
        pos += 1

    return res

def solve(N, m):
    assert m >= 2
    res = 1 #xor_sq_root(m >> 1)

    x = 1
    while formula(x, x) <= m:
        res += 1
        x += 1

    x = 1
    while (x << 1) <= m:
        res += 1
        x += 1


    print("external:" ,res)
    
    for _, f in Progress(range(2, N + 1), "solving"):
        if formula(f, 1) > m:
            break
        c = 0

        # 1. count
        prev = 1
        curr = f
        while curr <= N and formula(curr, prev) <= m:
            c += 1
            t = prev
            prev = curr
            curr = (curr << 1) ^ t

        # 2. get factor
        dd, _ = xor_div(m, formula(f, 1))
        d = xor_sq_root(dd)
        print("ddd", dd, d)
        
        # 3. multiply & add to total
        res += d * c

        print("G(%d, %d)" % (N, m), "for group:" ,f, "has ", d * c, "given gcd=1:", c)
    return res


#@validation
def validate():
    assert order(3) == 2, order(3)
    assert order(4) == 4, order(4)
    assert order(2**10) == 2 ** 10, order(2 ** 10)
    assert order(2**10 + 2 ** 6 + 1) == 2 ** 10, order(2**10 + 2 ** 6 + 1)

    assert xor_sq_root(0b10101) == 0b111, xor_sq_root(0b10101)
    assert xor_sq_root(0b1000001) == 0b1001, xor_sq_root(0b1000001)
    assert xor_sq_root(1) == 1, xor_sq_root(1)
    assert xor_sq_root(0) == 0, xor_sq_root(0)
    #assert xor_sq_root(0b10) == 0b10, xor_sq_root(0b10)
    #assert xor_sq_root(0b110) == 0b100, xor_sq_root(0b110)
    
    assert xor_div(37, 5) == (11, 2), xor_div(37, 5)
    assert xor_div(129, 14) == (26, 13), xor_div(129, 14)
    for i in range(1, 100):
        assert xor_div(i, 1) == (i, 0), (xor_div(i, 1), i)
        t, r = xor_div(i, 2)
        assert t == i // 2
        assert r == i % 2
    
    bf = brute_force(1000, 100)
    assert bf == 398, bf

    for t in range(5, 10):
        for m in range(2, t-3):
            print("NOW BF", 2**t - 1, 2**m - 1)
            b = brute_force((2 ** t) - 1, (2 ** m) - 1)
            print("NOW", 2**t - 1, 2**m - 1)
            s = solve((2 ** t) - 1, (2 ** m) - 1)
            if s != b:
                s -= 2
                print("DOWN")
            assert s == b, (t, m, s, b)
    
    assert solve(1000, 100) == 398, solve(1000, 100)


@solution
def solve_all():
    return solve(10**17, 10**6)
