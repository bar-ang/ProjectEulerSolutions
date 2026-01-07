from project_euler import Measure, Progress, validation, solution, Test
import random

LIM = 10 ** 6


def num_matches_no_operators(n):
    units = {    
        0: 6,
        1: 2,
        2: 5,
        3: 5,
        4: 4,
        5: 5,
        6: 6,
        7: 3,
        8: 7,
        9: 6
    }

    if n == 0:
        return units[0]
    
    res = 0
    while n > 0:
        res += units[n % 10]
        n //= 10
    return res

def skip_num(n):
    # try n with 1 or 7.
    if n < 10:
        return None

    c = 0
    while n > 0:
        if n % 10 in [1, 7, 0]:
            return c
        n //= 10
        c += 1
    return None

def all_M(lim, verbose=False):
    min_matches = [num_matches_no_operators(n) for n in range(lim+1)]

    if verbose:
        sol = [str(n) for n in range(lim+1)]

    n = 0
    while n <= lim:
        if random.random() < 0.002:
            print(f"progres... {round(float(n)*100/lim, 2)}%")
    #for _, n in Progress(range(lim+1), announce_every_seconds=57):

#        s = skip_num(n)
#        if s is not None:
            #if s >= 4:
            #    print(n, s)
#            n += 10 ** s
#            continue
        for a in range(1, n//2 + 1):
            additive = 2 + min_matches[a] + min_matches[n-a]
            if min_matches[n] > additive:
                min_matches[n] = additive
                if verbose:
                    sol[n] = f"({a} + {n-a})"
            if a > 1 and n % a == 0:
                multi = 2 + min_matches[a] + min_matches[n // a]
                if min_matches[n] > multi:
                    min_matches[n] = multi
                    if verbose:
                        sol[n] = f"({a} X {n//a})"

        n += 1
    if verbose:
        return min_matches, sol
    else:
        return min_matches

def solve(n):
    return sum(all_M(n)[1:])

@validation
def validate():
    Test.equals(916, solve, 100)
    mini, form = all_M(800, True)
    assert mini[0] == 6
    assert mini[1] == 2
    print("\n".join(form))

    Test.equals(0, skip_num, 227)
    Test.equals(None, skip_num, 228)    
    Test.equals(5, skip_num, 123456)
    Test.equals(None, skip_num, 23456)   
    Test.equals(1, skip_num, 345672)
    Test.equals(2, skip_num, 123456788)

@solution
def solve_all():
    return solve(LIM)
