from project_euler import Measure, Progress, validation, solution, Test
from numpy import sqrt, pi, round, abs
import scipy.integrate as integrate
from functools import partial

V = 2-sqrt((22-5*pi) / 3)

ACCURACY = 10

def derivative_x(t, v):
    return (9*v-6)*t*t + 6*(1-2*v)*t + 3*v

def derivative_y(t, v):
    return -derivative_x(1-t, v)

def func_to_integrate(t, v):
    return sqrt(derivative_x(t, v) ** 2 + derivative_y(t, v) ** 2)

@validation
def validate():
    def x(t, v):
        return t**3 + 3*t*t*(1-t) + 3*v*t*((1-t)**2)

    #validate V value by calculating the area
    def func(t):
        return x(1-t, V) * derivative_x(t, V)

    integral, err = integrate.quad(func, 0, 1)
    assert err < 10 ** (-ACCURACY), err

    diff = abs(integral - (pi*0.25))

    print(f"for v={V} area under curve is {integral}")
    assert diff < 10 ** (-ACCURACY)
    print(f"mistake is: {diff} - FINE!")
    

@solution
def solve():
    func = partial(func_to_integrate, v=V)
    integral, error = integrate.quad(func, 0, 1)

    assert error < 10 ** (-ACCURACY), error
    
    print(f"Best approx: {integral}")
    print(f"Error rate : {error}")

    result = 100*((2 * integral / pi) - 1)
    print(f"exact: {format(result, '.10')}")
    return round(result, ACCURACY)
