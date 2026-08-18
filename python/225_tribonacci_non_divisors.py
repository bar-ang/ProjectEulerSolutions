from sympy import factorint
from project_euler import validation, solution, Testing, Progress, Measure


# def tribonacci(n, t1=1, t2=1, t3=1):
#     seq = [t1, t2, t3]
#     while len(seq) < n:
#         seq.append(seq[-1] + seq[-2] + seq[-3])
#     return seq[:n]


# def first_divisible(k, lim=70000, t1=1, t2=1, t3=1):
#     for n, t in enumerate(tribonacci(lim, t1, t2, t3), start=1):
#         if t % k == 0:
#             return n, t
#
#     raise ValueError(f"no n <= {lim} found such that {k} divides T_n")

def find_cycle(m, t1=1, t2=1, t3=1):
    seq = [t1 % m, t2 % m, t3 % m]
    while len(seq) <= 3 or seq[-1] != t3 or seq[-2] != t2 or seq[-3] != t3:
        seq.append((seq[-1] + seq[-2] + seq[-3]) % m)
    return seq

# def combine(primes, clip=None):
#     divisors = [1]
#     for p, e in primes.items():
#         divisors = [d * p ** k for d in divisors for k in range(e + 1)]
#         if clip is not None:
#             divisors = [d for d in divisors if d <= clip]
#     return divisors

# def collect_factors(collect):
#     t1, t2, t3 = 1, 1,  1
#     primes = {}
#     while len(primes.keys()) < collect:
#         n = t1 + t2 + t3
#         facts = factorint(n)
#         for k, v in facts.items():
#             if k not in primes.keys():
#                 primes[k] = 0
#             primes[k] = max(primes[k], v)
#
#         t1 = t2
#         t2 = t3
#         t3 = n
#     return primes

def collect_non_divisors(T):
    nons = []
    m = 1
    bar_len = 30
    while len(nons) < T:
        m += 2
        cycle = find_cycle(m)
        if cycle.count(0) == 0:
            nons.append(m)
            pct = len(nons) / T * 100
            filled = int(bar_len * len(nons) / T)
            bar = "█" * filled + "░" * (bar_len - filled)
            print(f"\r[{bar}] {pct:6.2f}%  ({len(nons)}/{T})", end="", flush=True)
    print()
    return nons

@validation
def validate():
    T = 44
    nons = collect_non_divisors(T)
    print(nons)


@solution
def solve():
    return collect_non_divisors(124)[-1]
