from project_euler import Measure, Progress, validation, solution
import numpy as np
import numpy.random as rnd
import numpy.linalg as lin
import scipy.linalg as lins

def play(n):
    done = False
    iter = 0
    chunk = max(n, 1)
    while not done:
        vec = rnd.randint(n, size=(chunk))
        for i, v in enumerate(vec):
            for j in range(i):
                if v+ vec[j] == n:
                    return 1+ i+chunk*iter
        iter+=1

def play_alot(n, reps=35000):
    s = sum([play(n) for _ in range(reps)])
    return s / reps

def build_markov_even(n):
    assert n % 2 == 0
    states = n+1
    
    a = np.zeros((states, states))

    # state x (half val not seen) -> 2x
    # state x* (half val seen) -> 2x+1
    i = 0
    while 2*i+2 <= n:
#    for i in range(states//2+2):
#        assert n >= 2*i+2, "too many states"
        k = 2*i
        r = 2*i+1
        a[k, k] = i+1
        a[k, -1] = i
        a[k, r] = 1

        a[r, r] = i+1
        a[r, -1] = i+1

        if n > 2*i + 2:
            a[k, k+2] = n - 2*i - 2
            a[r, r+2] = n - 2*i - 2
        i+=1

    a[-1, 0] = n
    a /= n
    return a

def build_markov_odd(n):
    assert n % 2 == 1
    states = 2 + (n-1)//2
    
    a = np.zeros((states, states))

    for i in range(states-1):
        a[i, i] = i+1
        a[i, -1] = i
        if n > 2*i + 1:
            a[i, i+1] = n - 2*i - 1
        assert n >= 2*i+1, "too many states"

    a[-1, 0] = n
    a /= n
    return a
    
def build_markov(n):
    if n % 2 == 0:
        return build_markov_even(n)
    else:
        return build_markov_odd(n)

def get_stationary(a):
    n = a.shape[0]
    p = a.T - np.eye(n)
    ns = lins.null_space(p)
    return (ns/sum(ns))[-1][0]

@validation
def validate():
    n = 11
    a = build_markov_odd(n)
    print(a*n)
    st = get_stationary(a)
    print(1/st)
    print(play_alot(n))

    n += 1
    a = build_markov_even(n)
    print(a*n)
    st = get_stationary(a)
    print(1/st)
    print(play_alot(n))

@solution
def solve_all():
    n = 1000

    a = build_markov(n)
    s = 1/get_stationary(a)
    return round(s, 8)
