from project_euler import Measure, validation, solution

PM = 524287

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
        if friend is None:
            friend = user
        else:
            yield friend, user
            friend = None

def friends_of(v, graph, seen=None, seen_size=0, clients=10**6):
    q = [-1]*clients

    if seen is None:
        seen = bytearray(clients)
    q_start = 0
    q_end = 0

    q[q_end] = v
    q_end += 1

    if seen[v] == 0:
        seen[v] = 1
        seen_size += 1

    i = 0
    while q_end - q_start > 0:
        i += 1

        v = q[q_start]
        q_start += 1

        if v in graph:
            for u in graph[v]:
                if seen[u] == 0:
                    q[q_end]=  u
                    q_end += 1
                    seen[u] = 1
                    seen_size += 1

    return seen, seen_size


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

    graph = {
        0: [1, 2, 3, 4],
        1: [5],
        2: [6],
        3: [7],
        4: [8],
        5: [],
        6: [],
        9: [10],
        10: [9, 11, 12],
        12: [10]
    }

    clients = 13
    friends, num_friends = friends_of(0, graph, clients=clients)
    assert num_friends == 9, num_friends
    friends = [u for u, is_friend in enumerate(friends) if is_friend]
    assert friends == list(range(9)), friends

    friends, num_friends = friends_of(9, graph, clients=clients)
    assert num_friends == 4, num_friends
    friends = [u for u, is_friend in enumerate(friends) if is_friend]
    assert friends == [9, 10, 11, 12], friends

    friends, num_friends = friends_of(1, graph, clients=clients)
    assert num_friends == 2, num_friends
    friends = [u for u, is_friend in enumerate(friends) if is_friend]
    assert friends == [1, 5], friends

    friends, num_friends = friends_of(7, graph, clients=clients)
    assert num_friends == 1, num_friends
    friends = [u for u, is_friend in enumerate(friends) if is_friend]
    assert friends == [7], friends

    #adding edge
    friends, num_friends = friends_of(0, graph, clients=clients)
    graph[1].append(9)
    friends, num_friends = friends_of(1, graph, seen=friends, seen_size=num_friends, clients=clients)
    assert num_friends == clients, num_friends
    friends = [u for u, is_friend in enumerate(friends) if is_friend]
    assert friends == list(range(clients)), friends


    with Measure("Find PM"):
        for i, c in enumerate(user_generator()):
            if c == PM:
                print(f"PM is the {i}th user ({i//2}th call)")
                break
            if i % 240000 == 1:
                print(f"on the {i}th user PM still not found...")

@solution
def solve():
    graph = {}

    calls = 0
    users = 0

    pm_was_called = False
    friends_of_pm = bytearray(10**6)
    friends_of_pm[PM] = 1
    num_friends = 1
    for caller, called in pair_generator(user_generator):
        if caller == called:
            continue

        calls += 1

        if caller not in graph.keys():
            graph[caller] = []
        if called not in graph.keys():
            graph[called] = []

        graph[caller].append(called)
        graph[called].append(caller)

        if friends_of_pm[caller] ^ friends_of_pm[called] == 1:
            curr_friend = caller if friends_of_pm[caller] == 1 else called
            friends_of_pm, num_friends = friends_of(curr_friend, graph, seen=friends_of_pm, seen_size=num_friends)

            if num_friends % 4000 < 10 or num_friends >= 990000:
                print(f"Num friends of the pm: {num_friends} ({round(num_friends*100/10**6, 2)}%)")
            if num_friends >= 990000:
                return calls

    return -1
