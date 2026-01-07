from project_euler import Progress, Measure, solution, validation
import numpy as np
from numpy import pi, arctan, sqrt, tan, isclose, sin
from numpy.random import rand
from scipy.integrate import quad

def circ(t):
    a = pi - arctan(30/t)
    per = 50 * pi / sin(a)
    if t <= 22.5:
        c = per * (2*a-pi)/(2*pi)
    else:
        c = per * arctan(0.75)/pi
    return c

def f(t):
    a = pi - arctan(3/t)
    per = 5*pi*sqrt(t*t+9)/3
    if t <= 2.25:
        c = per * (2*a-pi)/(2*pi)
    else:
        c = per * arctan(0.75)/pi
    return a*c

NUM_DEC_PLACES = 10

def find_circle(p1, p2, p3):
    # Extract points
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3

    # Formulate the matrices for the system of equations
    A = np.array([
        [x1, y1, 1],
        [x2, y2, 1],
        [x3, y3, 1]
    ])

    B = np.array([
        [-x1**2 - y1**2],
        [-x2**2 - y2**2],
        [-x3**2 - y3**2]
    ])

    s = np.linalg.solve(A, B)

    a = -s[0]/2
    b = -s[1]/2
    r = np.sqrt(a*a+b*b-s[2])

    return a[0], b[0], r[0]

def brute_force_single(below=0):
    rot = rand()*2*pi
    if rot > pi:
        return False
    x, y = rand() * 50 - 18, rand() * 24
    tries = 1
    while 3*x > 96 - 4*y or 4*x < 3*y-72 or (120-3*below) < 4*y*below:
        tries += 1
        x, y = rand() * 50 - 18, rand() * 24

    t = x + y / tan(rot)
    return t < 32 and t > -18

def solve():
    bottom, _ = 0,0  # quad(f, 0, 2.25, epsabs=1e-13)
    top, _ = quad(f, 2.25, 4, epsabs=1e-13)
    sol = 8*bottom / 27 + 8*top / 21
    sol /= (2*pi)
    return round(sol, NUM_DEC_PLACES)

@validation
def validate():
    circ1, _ = quad(circ, 0, 22.5, epsabs=1e-13)
    assert isclose(circ1, 337.5), (circ1, 337.5)
    circ2, _ = quad(circ, 22.5, 40, epsabs=1e-13)
    assert isclose(circ2, 600-337.5), (circ2, 600-337.5)
    circ3, _ = quad(circ, 0, 4, epsabs=1e-13)
    assert isclose(circ3, 6), circ3

    for t in np.arange(0, 4, 0.01):
        cx, cy, cr = find_circle((0, 4), (3, 0), (0, t))
        if t <= 2.25:
            w1 = np.array([cx-4*t/3, cy])
            w2 = np.array([cx, cy-t])
            assert isclose(w1.dot(w2), -25*(t*t-9)/36), (w1.dot(w2), -25*(t*t-9)/36)
        else:
            w1 = np.array([cx-3, cy])
            w2 = np.array([cx, cy-t])
            assert isclose(w1.dot(w2), 7*cr*cr/25)
        assert isclose(cr, 5*sqrt(t*t+9)/6)

    total = 137091
    hits = 0
    for _, i in Progress(range(total), "validating"):
        if brute_force_single(below=2.25):
            hits += 1

    s = solve()
    estim = hits / total
    print("ESTIM: %s%% %s of %s" % (estim*100, hits, total))
    print("REAL: %s%%" % (solve()*100))

    if not isclose(estim, solve(), atol=1e-03):
        print("VALIDATION FAILED!")

@solution
def solve_all():
    return solve()
