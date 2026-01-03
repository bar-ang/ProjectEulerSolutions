from project_euler import Measure, Progress, validation, solution
import math
from scipy.integrate import quad
from numpy import isclose, inf

def theta(t):
    return math.asin(2*t/(1+t*t))

def density_func(t):
    if t < 0.75:
        return ((12 - 6.25 *  theta(t)) * t) / 6
    elif t < 4.0/3:
        return (4.5-(6.25*math.acos(0.28)-6)*t) / 6
    else:
        return (12.5-6.25*theta(t)*t) / 6

def exit_angle(t):
    if t < 1:
        return (math.pi+theta(t))/2
    else:
        return math.pi-(theta(t)/2)


def integrand(t):
    return (exit_angle(t)*density_func(t)) / (2*math.pi)

# --- Main integration function ---
def compute_integral(integ, a, b):
    result, error = quad(integ, a, b)
    print(f"intgral from {a} to {b} of {integ.__name__} = {result}. Calc Error: {error}.")
    return result

@validation
def validate():
    value = compute_integral(density_func, 0, inf)
    print(value)
    assert isclose(value, 1), value
    
@solution
def solve_all():
    value = compute_integral(integrand, 0, inf)
    return round(value, 10)
