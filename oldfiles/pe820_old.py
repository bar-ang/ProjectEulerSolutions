from project_euler import Measure, Progress, validation, solution
from math import gcd, floor
from common.primes import prime_sieve

def build_euler_totient(n, primes):
    #def lcm(a, b):
    #    return a * b // gcd(a, b)
    phi = [i for i in range(n+1)]
    for _, p in Progress(primes):
        for i in range(p, n, p):
            phi[i] *= (p-1)
            phi[i] //= p
            #phi[i] //= gcd(n, p-1)

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

def cut_len(c_b, b):
    if b % 2 != 0:
        return c_b, b

    q = 10 ** (b//2)
    
    if c_b % q == c_b // q:
        return cut_len(c_b % q, b//2)

    return c_b, b

def get_cycle(n, phi):
    a, b = get_cycle_len(n, phi)
    c_a = 10 ** a // n
    c_b = (10 ** b - 1) * (10 ** a - n * c_a) // n
    c_b, b = cut_len(c_b, b)
    
    return c_a, c_b, a, b

def dig(n, i):
    return (n // 10 ** i) % 10

SHADOW = {}
def d(n, x, phi, lim=None):
    if x == 1:
        return 0
    lim  = lim or n
    #if x == 6:
    #    import pdb; pdb.set_trace()
    if (n, x) in SHADOW:
        #print("=========SHADOWED! n=%s x=%s == %s" % (n,x, SHADOW[(n,x)]))
        return SHADOW[(n,x)]
    with Measure("Cyclen", 0.06):
        c_a, c_b, a, b = get_cycle(x, phi)
    if n <= a:
        form = a - n - 2
    else:
        form=  b - (n - a - 1) % b - 1

    SHADOW[(n, x)] = dig(c_a, form)

    if x >= 3 and x % 2 != 0 and x % 5 != 0:
        for i in range(0, 23):
            for j in range(0, 23):
                v = 2**i * 5**j * x 
                if v <= lim:
                    SHADOW[(n, v)] = dig(c_a,  form - max(i, j))

    return SHADOW[(n, x)]

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
    global SHADOW
    SHADOW = {}
    primes = prime_sieve(10 ** 3)
    phi = build_euler_totient(3*10**5, primes)
    
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

    assert get_cycle(7, phi) == (0, 142857, 0, 6), get_cycle(7, phi)
    assert get_cycle(70, phi) == (0, 142857, 1, 6)
    assert get_cycle(26, phi) == (0, 384615, 1, 6), get_cycle(26, phi)
    assert get_cycle(312, phi) == (3, 205128, 3, 6), get_cycle(312, phi)
    assert get_cycle(336, phi) == (29, 761904, 4, 6), get_cycle(336, phi)

    assert dig(12345, 1) == 4
    assert dig(12345, 0) == 5
    assert dig(12345, 4) == 1
    assert dig(12345, 7) == 0

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
    SHADOW = {}

@solution
def solve_all():
    assert not SHADOW
    return solve(10 ** 5)