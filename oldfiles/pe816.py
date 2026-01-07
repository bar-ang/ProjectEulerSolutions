from math import gcd, isclose
from common.data_structures.kdtree import KDTree, euclidean
from project_euler import Measure, Progress, validation, solution

S_0 = 290797
MOD = 50515093

class PointGenerator:
    def __init__(self, stop, s_0=S_0, mod=MOD):
        assert gcd(s_0, mod) == 1
        self.s_0 = s_0
        self.mod = mod
        self.stop = stop

    def __len__(self):
        return self.stop

    def __iter__(self):
        self.s_i = self.s_0
        self.i = 0
        return self

    def next_single(self):
        if self.i > self.stop:
            raise StopIteration
        x = self.s_i
        self.s_i *= self.s_i 
        self.s_i %= self.mod
        return x
    
    def __next__(self):
        x = self.next_single()
        y = self.next_single()
        self.i += 1
        return (x, y)

def solve(n, s_0=S_0, mod=MOD):
    point_gen = PointGenerator(n, s_0, mod)
    tree = KDTree(2)
    min_d = 2*mod
    for _, p in Progress(point_gen, announce_every_seconds=11):
        if not tree.empty():
            _, d = tree.nearest_neighbour_search(p)
            if d == 0:
                continue
            if d < min_d:
                min_d = d
        tree.insert(p)
    return min_d

def brute_force(n, s_0, mod):
    point_gen = PointGenerator(n, s_0, mod)
    points = [p for p in point_gen]
    min_d = 2*mod
    for p1 in points:
        for p2 in points:
            d = euclidean(p1, p2)
            if d < min_d and d > 0:
                min_d = d
    return min_d
        
    
    
    

@validation
def validation():
    assert euclidean((0, 0), (3, 4)) == 5
    assert euclidean((10, 15), (13, 19)) == 5
    assert euclidean((80, 55), (80, 35)) == 20
    assert isclose(brute_force(14, S_0, MOD), 546446.46684), brute_force(14, S_0, MOD)
    
    for _, s_0 in Progress(range(22, 30)):
        for mod in range(s_0+10, s_0+20):
            if gcd(s_0, mod) != 1:
                continue
            for n in range(3, 10):
                bf = brute_force(n, s_0, mod)
                sol = solve(n, s_0, mod)
                assert isclose(sol, bf), (n, s_0, mod, sol, bf)

@solution
def solve_all():
    return solve(2*10**6)