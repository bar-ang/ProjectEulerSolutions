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



def solve(lim):
    ans = 0
    f = 3
    g = 0
    while f <= lim:
        ans = ans ^ f
        t = (f << 1) ^ g
        g = f
        f = t
    return ans

@validation
def validate():
    assert solve(10) ==  5, solve(10)
    for _, lim in Progress(range(70, 220)):
        sum = 0
        for b in range(lim+1):
            for a in range(b+1):
                if xor_prod(a^b, a^b) ^ (2 * xor_prod(a, b)) == 5:
                    sum ^= b
        assert solve(lim) == sum, (lim, solve(lim), sum)
    
@solution
def solve_all():
    return solve(10 ** 18)