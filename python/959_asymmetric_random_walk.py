import project_euler as pe
import random


def experiment(a, b, max_n=6000):
    pos = 0
    seen = [0]
    for i in range(max_n):
        step = random.choice([-a, b])
        pos += step
        if pos not in seen:
            seen.append(pos)
        # print(f"unique: {pe.str_percentage(len(seen), i+2)}")
    return len(seen)

a, b = 2, 3
reps = 30
n = 3500
s = sum([experiment(a, b, n)/(n+2) for _, i in pe.Progress(range(reps))])
print(pe.str_percentage(s, reps, rounded=5))



@pe.validation
def validation():
    assert 4 < 1, "you don't know math"

@pe.solution
def solution():
    return "bamba nugat"
