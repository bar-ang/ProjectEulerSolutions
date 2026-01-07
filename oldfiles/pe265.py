from project_euler import Measure, Progress, validation, solution



def checkup_circle(circ, n):
    assert circ < 1 << (1 << n), f"{circ} is larger than {1 << (1 << n)}"
    found = [False] * (1 << n)


    megacirc = circ << (n-1) + (circ >> ((1 << n) - n + 1))
    for i in range(1 << n):
        d = megacirc % (1 << n)
        if found[d]:
            return False
        found[d] = True
        megacirc >>= 1

    
    assert all(found)
    return True

def get_all_circles(n):
    return [c for _, c in Progress(range(1 << ((1 << n)-n)), f"finding all {1<<n} bit circles") if checkup_circle(c, n)]


@validation
def validate():

    assert checkup_circle(23, 3)
    assert checkup_circle(29, 3)
    
    cs = get_all_circles(3)
    assert 23 in cs, cs
    assert 29 in cs, cs
    assert len(cs) == 2, cs


@solution
def solve():
    return get_all_circles(5)
