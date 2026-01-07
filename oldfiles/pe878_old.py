from project_euler import Measure, Progress, validation, solution
from math import log2, ceil

def xor_prod(a, b):
    res = 0;
    dig = 0;
    while b:
        if b & 1:
            res ^= a << dig
        dig += 1
        b >>= 1

    return res

class BPMatrix:
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def __mul__(self, other):
        if type(other) == BPMatrix:
            return BPMatrix(
                xor_prod(self.a, other.a) ^ xor_prod(self.b, other.c),
                xor_prod(self.a, other.b) ^ xor_prod(self.b, other.d),
                xor_prod(self.c, other.a) ^ xor_prod(self.d, other.c),
                xor_prod(self.c, other.b) ^ xor_prod(self.d, other.d),
            )
        else:
            return BPMatrix(other * self.a, other * self.b, other * self.c, other * self.d)

    def __add__(self, other):
        return BPMatrix(self.a ^ other.a, self.b ^ other.b, self.c ^ other.c, self.d ^ other.d)

    def I():
        return BPMatrix(1, 0, 0, 1)

    def A():
        return BPMatrix(2, 1, 1, 0)

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b and self.c == other.c and self.d == other.d
    
    def __pow__(self, t):
        if t == 0:
            return BPMatrix.I()

        res = BPMatrix.I()
        for i in range(t):
            res *= self
        return res
    
    def __repr__(self):
        return "BPMatrix:\n[%s, %s]\n[%s, %s]\n" % (self.a, self.b, self.c, self.d)


def get_powers_of_2(lim):
    res = [BPMatrix.A()]
    for t in range(0, lim):
        a = res[-1]
        res.append(a * (2 ** (2 ** t)) + BPMatrix.I())
    return res

def calc_power(n, powers):
    A = powers[0]
    if n == 0:
        return BPMatrix.I()
    if n == 1:
        return A

    res = BPMatrix.I()
    c = 0
    while n > 0:
        if (n & 1) == 1:
            res *= powers[c]
        n >>= 1
        c += 1
    return res


def solve(lim):
    LIM = lim
    res = BPMatrix(0,0,0,0)

    powers = get_powers_of_2(6)
    
    i = 0
    curr = BPMatrix.I()
    while xor_prod(curr.a, 3) <= LIM:
        res += curr
        i += 1
        curr = calc_power(i, powers)

    ans = xor_prod(res.a, 3)
    return ans

def generate_basics(n):
    cap = 2

    for i in range(4):
        for j in range(i+1):
            yield (i, j)
    
    for _, f in Progress(range(4, n+1), "generating basics"):
        if f >= (cap << 2):
            cap <<= 1
        for g in range(0, cap):
            yield (f, g)
        for g in range(cap << 1, f+1):
            yield (f, g)

def count(f, g, n):
    assert f >= g
    if f == 0:
        return 1
    res = 0
    while f <= n:
        res += 1
        t = (f << 1) ^ g
        g = f
        f = t
    return res

def brute_G(n, m):
    res = 0
    for (f, g) in generate_basics(n):
        k = xor_prod(f^g, f^g) ^ (xor_prod(f, g) << 1)
        if k <= m:
            res += count(f, g, n=n)
    return res

@validation
def validate():
    for f, g in generate_basics(8):
        print(f,g)
    assert brute_G(1000, 100) == 398, brute_G(1000, 100)
                    
    
def _validate():
    assert BPMatrix.A() ** 0 == BPMatrix.I()
    assert BPMatrix.A() ** 1 == BPMatrix.A()
    assert BPMatrix.A() ** 2 == BPMatrix(5, 2, 2, 1)
    assert BPMatrix.A() ** 3 == BPMatrix(8, 5, 5, 2), BPMatrix.A() ** 3
    assert BPMatrix.A() ** 4 == BPMatrix(21, 8, 8, 5), BPMatrix.A() ** 4

    assert BPMatrix.A() + BPMatrix.A() == BPMatrix(0, 0, 0, 0)
    
    M = BPMatrix(0, 0, 0, 0)
    for i in range(0, 100):
        pa = BPMatrix.A() ** i
        a, b = xor_prod(pa.a, 3), xor_prod(pa.c, 3)
        assert xor_prod(a ^ b, a ^ b) ^ (2 * xor_prod(a, b)) == 5, (i, a, b, pa)
        if a <= 10:
            M += BPMatrix.A() ** i

    assert xor_prod(M.a, 3) == 5, (M, xor_prod(M.a, 3))
    
    lim = 10
    powers = get_powers_of_2(lim)
    actual_powers = [BPMatrix.A() ** (2 ** i) for i in range(lim+1)]
    assert len(powers) == len(actual_powers), (len(powers), len(actual_powers))
    assert powers == actual_powers, (powers, actual_powers)

    for i in range(200):
        assert calc_power(i, powers) == BPMatrix.A() ** i, i
        
    s = BPMatrix(0,0,0,0)
    for i in range(1):
        s += BPMatrix.A() ** i
    assert xor_prod(s.a, 5) == 5, s


    for _, lim in Progress(range(70, 220)):
        sum = 0
        for b in range(lim+1):
            for a in range(b+1):
                if xor_prod(a^b, a^b) ^ (2 * xor_prod(a, b)) == 5:
                    sum ^= b
        assert solve(lim) == sum, (lim, solve(lim), sum)
    
#@solution
def solve_all():
    return solve(10 ** 18)