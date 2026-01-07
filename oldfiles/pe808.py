from math import sqrt

def is_square(n):
    return sqrt(n) % 1 == 0

def reverse(n):
    return int(str(n)[::-1])

def palindrom(c):
    s = str(c)
    for i in range(len(s)):
        if s[i] != s[-i-1]:
            return False
    return True

def force(count=5):
    res = []
    c = 12
    while len(res) < count:
        if not palindrom(c) and is_square(c) and is_square(reverse(c)):
            res.append(c)
        c += 1

    return res


def validation():
    assert is_square(36)
    assert is_square(9)
    assert is_square(1)
    assert is_square(74**2)
    assert is_square(45**4)
    assert not is_square(30)
    assert not is_square(35)
    assert not is_square(37)
    assert not is_square(98**2+3)
    assert reverse(2459) == 9542
    assert reverse(322) == 223
    assert reverse(300) == 3
    print("forcing...")
    print(force(50))

validation()

