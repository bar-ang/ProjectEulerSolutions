


FIBS_COUNT = 90

def get_fibonaccis(count):
    res = [0, 1, 1]
    for i in range(3, count+1):
        res.append(res[-1] + res[-2])
    return res

def J(n, fibs):
    return fibs[n+2] - fibs[n+1] - 1 

def _G(b, fibs):
    ''' calculate G(n) where n is the b-th fibonacci number '''
    ''' works only for fibonacci numbers '''
    s = fibs[b+2] - 2
    for k in range(2, b):
        s += fibs[k]*J(b-k, fibs)

    return s

def G(b, fibs):
    ''' calculate G(n) where n is the b-th fibonacci number '''
    ''' works only for fibonacci numbers '''
    s = fibs[b]
    for k in range(2, b):
        s += fibs[k]*fibs[b-k]

    return s

def valdation():
    A = 20
    fibs = get_fibonaccis(A)
    assert fibs[:10] == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34], fibs[:10]

    assert G(7, fibs) == 43,  G(7, fibs)

valdation()

fibs = get_fibonaccis(FIBS_COUNT)
print(G(80,fibs))
