from project_euler import Measure, Test, Progress, validation, solution

SEQUENCE = [1, 2, 3, 4, 3, 2]


def brute_force(n):
    pos = 0
    all_res = []
    for k in range(1, n+1):
        s = 0
        res = []
        while s < k:
            s += SEQUENCE[pos]
            res.append(SEQUENCE[pos])
            pos += 1
            pos %= len(SEQUENCE)
        all_res.append(int("".join([str(r) for r in res])))
    return all_res

def calc_u(n, u_series, l_series, mod):
    n -= 1
    t = n % 15
    d = pow(10, n//15, mod)
    d6 = pow(d,6, mod)
    pl = (d6 - 1) * pow(10 ** 6 - 1, -1, mod)
    pu = d6

    return (l_series[t] * pl + u_series[t] * pu) % mod


def brute_force_single(n):
    return brute_force(n)[-1]

def compute_l_series():
    bf = brute_force(30)
    return [q % (10 ** 6) for q in bf[15:30]]

MOD = 123454321



def S(n, mod=MOD):
    m = n // 15
    r = n % 15

    l_series = compute_l_series()
    u_series = brute_force(15)

    if m == 0:
        return sum(u_series[:r]) % mod

    L = sum(l_series)
    U = sum(u_series)

    inv = pow(10**6 - 1, -1, mod)
    q = pow(10, 6*m, mod)
    a = ((q - 1) % mod) * inv
    base = L * (a - m) * inv + a*U
    a %= mod
    base %= mod


    more = sum([calc_u(15*m + i+1, u_series, l_series, mod) for i in range(r)])
    return (base + more) % mod

@validation
def validate():
    Test.equals(2, brute_force_single, 2)
    Test.equals(32, brute_force_single, 5)
    Test.equals(32123, brute_force_single, 11)
    Test.equals(123432, brute_force_single, 15)
    Test.equals(4321234,  brute_force_single, 19)


    lim = 1003
    bf = brute_force(lim)
    u_s = bf[:15]
    l_s = compute_l_series()
    for i in range(1, lim+1):
        Test.equals(bf[i-1] % 10**20, calc_u, i, u_s, l_s, mod=10**20)
        Test.equals(bf[i-1] % MOD, calc_u, i, u_s, l_s, mod=MOD)


    for i in range(lim):
        Test.equals(sum(bf[:i]) % 10**20, S, i, mod=10**20)
        Test.equals(sum(bf[:i]) % MOD, S, i, mod=MOD)

    Test.equals(36120, S, 11, MOD)
    Test.equals(18232686, S, 1000, MOD)

@solution
def solution():
    return S(10 ** 14, MOD)
