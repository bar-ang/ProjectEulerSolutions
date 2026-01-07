from project_euler import Measure, Progress, validation, solution
#from functool import partial
import numpy as np
import scipy as sp

def func(n, goal, *args):
    s = sum([np.exp(k/n)-1 for k in args])
    return abs((s - goal))

    
def directions(n_params, steps=1, backwards=True):
    if n_params == 0:
        return [[]]
    dirs = directions(n_params-1, steps=steps, backwards=backwards)
    #import pdb; pdb.set_trace()
    #dirs.append([0]*n_params)
    res = []
    for d in dirs:
        end = steps
        start = (-steps) if backwards else 0
        res += [d+[i] for i in range(start, end+1)]
    return res

@validation
def validate():
    assert func(100, 15, 0, 0, 0) == 15

    dirs = directions(3, 2, backwards=True)
    print("\n-->".join([str(d) for d in dirs]))

def _directions(n_params):
    res = []
    for i in range(n_params):
        for j in [-1, 1]:
            p = [0] * n_params
            p[i] += j
            res.append(p)
    return res

def solve(n, goal, n_params, start_point):
    min_so_far = goal**2
    done = False
    params = start_point
    dirs = directions(n_params, 6)
    c = 0
    while True:
        c += 1
        next_params = None
        m = min_so_far
        for dir in dirs:
            t = [params[i] + d for i, d in enumerate(dir)]
            if any([i < 0 for i in t]):
                continue
            val = func(n, goal, *t)
            if val < min_so_far:
                m = val
                next_params = t
        if next_params is not None:
            params = next_params
            min_so_far = m
        else:
            break

        if c > 50000:
            if c % 10000:
                print(f"iterations: {c}")
            if c > 100000:
                print("too many iterations")
                break
            
    print(params)
    print(func(n, goal, *params))
    return params

def solve_many(n, goal, n_params, starts):
    min_val = None
    min_params = None
    for start in starts:
        params = solve(n, goal, n_params, start)
        v = func(n, goal, *params)
        if min_val is None or v < min_val:
            min_val = v
            min_params = params
    return min_params

@solution
def solve_all():
    return solve_many(200, np.pi, 4, [(285,0,0,0), (0, 285, 0, 0), (0, 0, 285, 0), (0, 0, 0, 285)])
