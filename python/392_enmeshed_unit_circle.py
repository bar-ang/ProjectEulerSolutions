from project_euler import Measure, Progress, validation, solution
from numpy import cos, sin, pi, sqrt, log10

def S(*theta):
    n = len(theta)
    te = [0] + list(theta) + [pi/2]
    return 4*sum([cos(te[i]) * (sin(te[i+1]) - sin(te[i])) for i in range(0, n+1)])

def gradient(*theta):
    def d(i, *t):
        return 4*(cos(t[i])*cos(t[i-1]) - sin(t[i+1])*sin(t[i]) - cos(2*t[i]))

    t = [0] + list(theta) + [pi/2]
    return [d(i, *t) for i in range(1, len(theta)+1)]

@validation
def validate():
    pass

def gradient_descent(f, gradient, gamma, *params, iters=10 ** 7):
    for i in range(iters):
        derivs = gradient(*params)
        params = [p - gamma * grad for p, grad in zip(params, derivs)]
        sgrad = log10(sum([d ** 2 for d in derivs]))
        if i <= 15 or i % 2737 == 122:
            print(f"{i+1}:\t{f.__name__}(...) = {round(f(*params), 20)}. grad: {round(sgrad,2)}")
        if sgrad <= -16:
            break

    print(f"BEST:\t{f.__name__}(...) = {round(f(*params), 20)}. grad: {sgrad}") 
    return params

@solution
def solve_all():
    n = 400 // 2
    theta = [(pi * i) / (2 * (n+1)) for i in range(1, n+1)]
    s1 = S(*theta)
    print(f"R({n}) = S({", ".join([str(round(t, 3)) for t in theta][:7])}...) = {round(s1,4)} ({round(abs(s1 - pi/2), 4)})")
    theta_best = gradient_descent(S, gradient, 0.15, *theta)

    print("list of points:")
    print("\n". join([
        f"({round(sin(t), 3)}, {round(cos(t), 3)}) [angle: {round(t * 180 / pi, 3)}]" for t in theta_best
    ]))
    
    return round(S(*theta_best),10)
