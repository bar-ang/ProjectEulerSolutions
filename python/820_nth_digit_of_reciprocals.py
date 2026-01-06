from project_euler import Measure, Progress, validation, solution
from math import gcd, floor, sqrt
from sympy import sieve

def prime_sieve(n):
    return list(sieve.primerange(1, n))

def build_euler_totient(n, primes):
    def lcm(a, b):
        return a * b // gcd(a, b)
    phi = [i for i in range(n+1)]
    m = [1 for i in range(n+1)]
    for _, p in Progress(primes, op_name="building euler totient"):
        rng = range(p, n, p)
        if p <= 23:
            rng = Progress(rng, op_name="calc phi for p=%s" % p) 
        else:
            rng = enumerate(rng)
        for _, i in rng:
            #phi[i] *= (p-1)
            phi[i] //= p
            m[i] = lcm(m[i], (p-1))

    for i, v in Progress(m, op_name="refine phi", announce_every_seconds=5):
        phi[i] *= v

    phi[0] = 0
    phi[1] = 1
    phi[2] = 1
    
    return phi

def euler_totient(n, phi):
    return phi[n]

def get_cycle_len(n, phi):
    t_2 = 0
    t_5 = 0
    while n % 2 == 0:
        n //= 2
        t_2 += 1
    while n % 5 == 0:
        n //= 5
        t_5 += 1

    a = max(t_2, t_5)
    if n == 0:
        return a, 0

    b = euler_totient(n, phi)
    return a, b

def extract(k, d):
    return (10 ** d // k) % 10

SHADOW = {}
def d(n, x, phi):
    if x == 1:
        return 0

    a, b = get_cycle_len(x, phi)
    dig = (n - a - 1) % b + a 

    roll = pow(10, dig, x)
    return 10 * roll // x 

def solve(n, lim=None):
    lim = lim or n
    primes = prime_sieve(lim + 10)
    with Measure("Euler totient"):
        phi = build_euler_totient(lim, primes)
    s = 0

    for _, k in Progress(range(2, lim+1, 1), announce_every_seconds=2):
        with Measure("D(%d, %d)" % (n, k), 0.08):
            q = d(n, k, phi)
            s += q
    return s

@validation
def validate():
    primes = prime_sieve(10 ** 3)
    phi = build_euler_totient(3*10**5, primes)

    def test_euler():
        assert phi[7] == 6
        assert phi[14] == 6
        assert phi[3 ** 5 * 7 ** 2] == 3 ** 4 * 7 * 12
        assert phi[1] == 1
        assert phi[1024] == 512
    
        assert euler_totient(1, phi) == 1
        assert euler_totient(2, phi) == 1
        assert euler_totient(4, phi) == 2, euler_totient(4, phi)
        assert euler_totient(2 ** 15, phi) == 2 ** 14
        assert euler_totient(7, phi) == 6
        assert euler_totient(7 ** 6, phi) == 6 * 7 ** 5
        assert euler_totient(66, phi) == 20, euler_totient(66, phi)
        assert euler_totient(87, phi) == 56
    
        assert get_cycle_len(7, phi) == (0, 6)
        assert get_cycle_len(13, phi) == (0, 12)
        assert get_cycle_len(13 * 4 * 5, phi) == (2, 12)

    #test_euler()
    from functools import partial
    dp = partial(d, phi=phi)

    y = dp(7, 1)
    assert y == 0, y
    assert dp(7, 2) == dp(7, 4) == dp(7, 5) == 0, (dp(7, 2), dp(7, 4), dp(7, 5))
    assert dp(7, 3) == 3, dp(7, 3)
    assert dp(7, 6) == 6, dp(7, 6)
    assert dp(7, 7) == 1, dp(7, 7)
    assert dp(7, 7*8) == 1, dp(7, 7 * 8)
    assert dp(7, 7 * 11) == 0, dp(7, 7 * 11)

    assert solve(7) == 10, solve(7)
    assert solve(100) == 418, solve(100)

@solution
def solve_all():
    return solve(10 ** 7)
