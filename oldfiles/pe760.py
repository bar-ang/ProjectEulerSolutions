from project_euler import Measure, Progress, validation, solution, Test

def flip(n, t): # negate bits only in the odd opsitions.
    mask = 2 * (4 ** (t//2) - 1) // 3
    return n ^ mask

def g(m, n):
    return (m ^ n) + (m & n) + (m | n)

def bwor(m, n):
    return 2 * (m | n)

def first_bit(n):
    assert n > 0
    c = 0
    while n & 1 == 0:
        n >>= 1
        c += 1
    return c

def h_brute(n):
    return sum([g(k, n-k) for k in range(n+1)])

def G(N):
    return sum([sum([g(k, n-k) for k in range(n+1)]) for _, n in Progress(range(N+1))])


def h_part1(n, k, bits=15): # equals to (n-k) V k
    if n < k:
        return 0
    assert n < 1 << bits
    return flip(n, 1 << bits) | k

def h_part2(n, k):
    if n < k:
        return 0
    return (n - k) | k

@validation
def vaildate():
    Test.equals(5, first_bit, 2 ** 5)
    Test.equals(5, first_bit, 2 ** 5 + 2 ** 6)
    Test.equals(5, first_bit, 2 ** 5 + 2 ** 7)

    Test.equals(682, flip, 0, 10)
    Test.equals(683, flip, 1, 10)
    Test.equals(21, flip, 31, 5)
    Test.equals(32, flip, 10, 6)
    Test.equals(34, flip, 8, 6)

    Test.are_the_same(g, bwor, range(1000), range(1000))

    print(h_part1(20, 0))

    for n in range(1, 1000):
        for k in range(n+1):
            print(h_part1(n, k))
            Test.funcs_equal(h_part1, h_part2, n, k)
    
    Test.are_the_same(h_part1, h_part2, range(1000), range(1000))

    Test
   
    for t in range(4, 10):
        n = 2 ** t - 1
        for k in range(1, n+1):
            Test.equals(2 * n, g, k, n - k)

        n = 2 ** t
        for k in range(1, n):
            Test.equals(2 ** (t+1)- 2 ** (first_bit(k)+1), g, k, n-k)

    Test.equals(754, G, 10)
    Test.equals(583766, G, 100)

@solution
def solve():
    n = 2**7
    res = [g(k, n-k) for k in range(n+1)]

    print(res)

    dres = list(set(res))
    dres.sort()
    histo = {d:len([t for t in res if t == d]) for _, d in Progress(res, "paterning1")}
    distinct = [format(b, "019b") + f"={b}: {histo[b]}" for _, b in Progress(dres, "paterning2")]
    print(f"{len(distinct)} items:")
    print("\n".join(distinct))
    
#    print("distinct:", set(res), "len", len(set(res)))
    return G(10 ** 1)
