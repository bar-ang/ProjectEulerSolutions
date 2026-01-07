import numpy as np
from sympy import divisors, sieve
from sympy.ntheory import factorint
   
def mat_power_mod(A, n, p):
    '''
    A     - matrix
    n, p  - integers

    returns the n-th power of A modulo p
    '''

    t = 0
    res = np.eye(2)
    while n > 0:
        k = 1
        m = A
        while 2*k <= n:
            m = np.matmul(m, m) % p
            k *= 2
        res = np.matmul(res, m) % p
        n -= k

    return res


def solve_for_prime(p):
    '''
    assuming p is prime,
    (for none prime numbers we shall use 'solve_for_all')
    
    The function returns the minimum integer 'n' such that:
    [1 7]^n = I mod p
    [1 1]
    (where 'I' is the identity matrix)
    
    To calculate it efficiently we'll take advantage of these two observations:
    1) The solution must divide p^2-1. In case 7 is quadratic
       residue modulo p, the solution must also divide p-1,
    2) The solution 'n' must satisfy the equation: (-6)^n = 1 (mod p)

    The function will iterate over all values of n that meet these criteria, and
    returns the first that is found.
    '''

    # for p <= 7 we'll solve manually:
    if p == 2 or p == 3:
        return 0
    if p == 5:
        return 12
    if p == 7:
        return 7


    if pow(7, (p-1)//2, p) != 1: #checking whether 7 is a quadratic residue mod p
        candids = divisors(p**2-1)
    else:
        candids = divisors(p-1)

    A = np.array([[1, 7], [1, 1]])

    # to avoid wasting time on re-calculating powers of A on every loop iteration,
    # we can save the maximal power of A that we've calculated so far for the next iterations
    known = dict(power=0, matrix=np.eye(2))
    
    for c in candids:
        #checking whether (-6)^c = 1 (mod p)
        # if not, withdraw this candidate
        if pow(-6, c, p) != 1:
            continue

        # calculating m := A^c mod p
        k = mat_power_mod(A, c - known["power"], p)
        m = np.matmul(known["matrix"], k) % p
        known = dict(power=c, matrix=m)

        # if 'm' is the identity matrix, we've found the solution! g(p) = c
        if np.array_equal(m, np.eye(2)):
            return c

    assert False, f"failed for prime {p}"
    return None


def solve_for_prime_power(p, k, s):
    # using the rule: g(p^k) = g(p) * p^(k-1)
    if k <= 1 or s == 0:
        return s
    return s * (p ** (k-1))


def orderof(p, n):
    '''
    returning max 't' such that (p^t) divides n
    '''
    t = 0
    while n %  (p ** (t+1)) == 0:
        t += 1
    return t


def solve_for_all(primes, lim):
    '''
    primes - a list of all primes <= lim
    lim - integer
    
    returns an array 'res' of size lim+1
    where res[i] = g(i) for all i <= lim

    using the fact that the function g satisfies:
    if a, b are coprime then: g(ab) = LCM(g(a), g(b))
    
    this allows to implement an algorithm that is somewhat
    similar to the sieve of Eratosthenes.
    '''

    res = [1] * (lim+1)
    res[0] = 0
    res[1] = 0
    res[2] = 0
    res[3] = 0

    for i,p in enumerate(primes):

        #printing progress...
        if i % 2400 == 13:
            print(f"Solving... {round(float(i*100)/len(primes), 2)}%")


        if p <= lim:
            res[p] = solve_for_prime(p)
        for n in range(2*p, lim+1, p):

            # g(n) = 0 if and only if n is divisible by either 2 or 3
            if p == 2 or p == 3:
                res[n] = 0
                continue

            k = orderof(p, n)
            res[n] = np.lcm(res[n], solve_for_prime_power(p, k, res[p]))
    return res
    

def solve(n):
    sieve.extend(n+1)
    primes = list(sieve._list) #returns a list of all primes smaller than or equal to n+1
    return sum(solve_for_all(primes, n))



print(f"== Answer is: {solve(10 ** 6)} ==")
