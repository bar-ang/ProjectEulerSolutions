from project_euler import Measure, Progress, validation, solution
import math
import sys

def get_diffs(lst, gap=1):
    s = set([g - lst[i-gap] for i, g in enumerate(lst) if i > gap-1])
    lst = list(s)
    lst.sort()
    return lst

LOG10_2 = math.log10(2)

def pow2_begin(pow, d):
    num_digs = math.ceil(pow*LOG10_2)
    if num_digs < d:
        return 1 << pow
    return (1 <<  pow) // 10 ** (num_digs - d)

def num_digits(k):
    return int(math.log10(k))+1

def brute_p_list(L, n, verbose=False):
    l_dig = num_digits(L)

    c = 0
    found = []
    while len(found) < n:
        if pow2_begin(c, l_dig) == L:
            found.append(c)
            if verbose:
                print(f"found: {len(found)}/{n}")
        c += 1
    return found    

def brute_p(L, n):
    p_list = brute_p_list(L, n)
    return p_list[-1]

def _p123(n):
    lst = brute_p_list(123, 50)
    diffs = get_diffs(lst)
    p0 = brute_p(123, 1)

    curr_pow = p0
    for _, i in Progress(range(2, n+1), f"solving p(123, {n})", announce_every_seconds=9):
        with Measure(f"powering {curr_pow}", print_threshold_sec=0.002):
            for d in diffs[:-1]:
                if pow2_begin(curr_pow + d, 3) == 123:
                    curr_pow += d
                    break
            else:
                curr_pow += diffs[-1]
                
        
    return curr_pow

def p123(n):
    lst = brute_p_list(123, 10)
    diffs = get_diffs(lst)
    p0 = brute_p(123, 1)
    print(diffs)

    b = diffs[1]
    a = diffs[0]
    prefix = p0 + (a + b) * n
    
    lim = prefix//b
    results = []
    map = {}
    for _, x in Progress(range(lim // 10, lim+1)):
        rng = range(x-20, x+20)
        if x < lim // 10 + 20:
            rng = Progress(rng)
        else:
            rng = enumerate(rng)
        for _, y in rng:
            if y <= 3:
                continue
            t = prefix - b * (x+1) - a * (y+1)
            if t < 0:
                break
            if n - 1 - x - y < 0:
                break
            with Measure(f"pow2 {(x, y)}", print_threshold_sec=1):
                po2 = pow2_begin(t, 3)
            if po2 == 123:
                results.append(t)
                map[t] = (x, y, n-1 - x - y, t)

    results.sort()
    print(results)
    print(map)
    return 4


@validation
def validate():
    p123(45)
    print("done presenting.")
    p123(678910)    
    
    assert num_digits(123) == 3
    assert num_digits(1) == 1
    assert num_digits(9) == 1
    assert num_digits(10001) == 5
    assert num_digits(12345678911) == 11
    assert num_digits(10 ** 7) == 8
    assert num_digits(10 ** 7 - 1) == 7
    assert num_digits(10 ** 2) == 3
    
    assert pow2_begin(777, 7) == 7948892
    assert pow2_begin(90, 3) == 123
    assert pow2_begin(10, 2) == 10
    assert pow2_begin(5, 1000) == 32
    
    assert brute_p(12, 1) == 7, brute_p(12, 1)
    assert brute_p(12, 2) == 80
    assert brute_p(123, 45) == 12710
 
    for n in range(42, 100, 11):
        print(n)
        pp = p123(n)
        bp = brute_p(123, n)
        assert pp == bp, (n, pp, bp)
    print("passed alidation!")

@solution
def solve():
    with Measure("bruting"):
        lst = brute_p_list(1111, 20, verbose=True)
    diffs = get_diffs(lst)
    print(lst)
    print("diffs", diffs)
#    return p123(678910)
    return "wow"
