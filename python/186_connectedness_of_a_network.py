from project_euler import Measure, validation, solution


def user_generator():
    memory = []
    for k in range(1, 56):
        t = (100003 - 200003 * k + 300007 * k * k * k) % 1000000
        yield t
        memory.append(t)

    while True:
        a, b = memory[55-55], memory[55-24]
        c = (a + b) % 1000000
        yield c
        memory = memory[1:] + [c]


def pair_generator(gen):
    friend = None
    for user in gen():
        if not friend:
            friend = user
        else:
            yield friend, user
            friend = None


def clique_of(id, cliques):
    for i, clique in enumerate(cliques):
        if id in clique:
            return i, clique

    return None, {id}

def solve_once(stop_at=None):
    pm = 524287
    cliques = [{pm}]
    clique_of_pm_idx = 0
    calls = 0
    for caller, called in pair_generator(user_generator):
        if caller == called:
            continue

        calls += 1
        if stop_at and calls > stop_at:
            print("broken")
            break

        if calls % 13000 == 13:
            print(f"{calls} calls already. {len(cliques)} cliques.")

        if len(cliques[clique_of_pm_idx]) > 1:
            print(cliques[clique_of_pm_idx], len(cliques[clique_of_pm_idx]), calls)
            if 100 * len(cliques[clique_of_pm_idx]) >= 99 * calls:
                break

        i, c1 = clique_of(caller, cliques)
        j, c2 = clique_of(called, cliques)
        if i is not None and i == j:
            continue

        if i is None:
            i = len(cliques)
            cliques.append(c1)

        cliques[i] = c1 | c2
        if pm in c2:
            clique_of_pm_idx = i

        if j is not None:
            del cliques[j]


    return calls, cliques

@validation
def validate():
    expects = {
        1: 200007,
        2: 100053,
        3: 600183,
        55: 764463,
        56: 529290,
        57: 951516,
        60: 627350,
        61: 655960,
        100: 586613,
        200: 157522
    }

    for i, c in enumerate(user_generator()):
        v = i + 1
        if v in expects:
            assert c == expects[v], f"S_{v} = {c}, expected: {expects[v]}"

        if i > 300:
            break

    for i, c in enumerate(pair_generator(user_generator)):
        v = i + 1
        if 2*v - 1 in expects:
            assert c[0] == expects[2*v-1], f"S_{2*v-1} = {c[0]}, expected: {expects[v]}"

        if 2*v in expects:
            assert c[1] == expects[2*v], f"S_{2*v} = {c[1]}, expected: {expects[v]}"

        if i > 200:
            break

    _, cliques = solve_once(12000)
    assert all(a.isdisjoint(b) for i, a in enumerate(cliques) for b in cliques[i+1:]) # all cliques are disjoined in pairs.


@solution
def solve():
    res, cliques = solve_once()
    return res
