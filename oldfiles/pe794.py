from project_euler import Measure, Progress, validation, solution
import random
from math import ceil

def rand_rng(a, b):
    assert b > a
    return a + (random.random() * (b-a))

@solution
def solve():
    a = []

    seg_start = 0
    seg_end = 1

    while True:
        n = len(a)
        segs = [ceil((n+1)*k) for k in a]

        
        
        assert len(segs) == len(set(segs)), segs
        empty_segs = [t+1 for t in range(n+1) if t not in segs]
        import pdb; pdb.set_trace()
        if len(empty_segs) != 1:
            break

        empty_seg = empty_segs[0]
        seg_start, seg_end = (empty_seg-1)/(n+1), empty_seg/(n+1)
        
        c = rand_rng(seg_start, seg_end)
        a.append(c)

    return ", ".join([str(i) for i in a])
