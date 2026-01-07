from project_euler import Measure, Progress, validation, solution
import numpy as np
from hashlib import sha256
from graphviz import Digraph

#@alidation
def alidate():
    pass

def make_states(words):
    states = [""]
    for word in words:
        for i in range(1, len(word)+1):
            states.append(word[:i])
    states = list(set(states))
    states.sort()
    return states

def connect_states(states, letters):
    res = {}
    for state in states:
        for letter in letters:
            next_state = state + letter
            while next_state not in states:
                next_state = next_state[1:]
            res[(state, letter)] = next_state
    return res

def get_subsets(input_set):
  subsets = [[]]
  for element in input_set:
    new_subsets = []
    for subset in subsets:
      new_subset = subset.copy()
      new_subset.append(element)
      new_subsets.append(new_subset)
    subsets.extend(new_subsets)
  return subsets

def add_seen(connections, words, halt_on_found=False):
    seen_connections = {}
    all_seens = get_subsets(words)
    for k, new_state in connections.items():
        state, letter = k
        for seen_list in all_seens:
            if state in seen_list:
                continue
            new_seen_state = new_state
            new_seen = seen_list[:]
            if new_state in words:
                if new_state in seen_list or (halt_on_found and len(seen_list) == len(words)):
                    new_seen_state = "----"
                    new_seen = []
                else:
                    new_seen.append(new_state)
                    new_seen_state = ""

            seen_list.sort()
            seen_connections[((state, "|".join(seen_list)), letter)] = (new_seen_state, "|".join(new_seen))
    return seen_connections

def check_reachability(connections, letters):
    reachable = []
    def dfs(state):
        reachable.append(state)
        for let in letters:
            key = (state, let)
            if key in connections:
                if connections[key] not in reachable:
                    dfs(connections[key])
    dfs(('', ''))
    m = {}
    for k, v in connections.items():
        #import pdb; pdb.set_trace()
        st, let = k
        if st in reachable:
            m[(st, let)] = v
    #print(f"{len(reachable)} states are reachable")
    return m

def serialize(connections):
    hashed = {}
    accept = []
    def hash(s, len=2):
        return sha256(str(s).encode()).hexdigest()[:len]

    for k, v in connections.items():
        state, letter = k
        hashed[(hash(state), letter)] = hash(v)
    
    return hashed

def __serialize(connections):
    keys = list(set([x for x in connections.values()]))
    scon = {}
    import pdb; pdb.set_trace()
    for k, v in connections.items():
        state, letter = k
        i = [i for i, k2 in enumerate(keys) if k2 == state]
        j = [i for i, k2 in enumerate(keys) if k2 == v]
        assert len(i) == 1, (len(i), state)
        assert len(j) == 1, (len(j), v)
        i, j = i[0], j[0]
        scon[i] = j
    return scon

@solution
def sole():
    letters = {'B', 'A', 'R', 'X'}
    words = {"BAR", "RAX", "AXR"}
#    letters = {"B", "A", "R"}
#    words = {"BAR", "RAB"}
    subs = get_subsets(words)
    states = make_states(words)
    cons0 = connect_states(states, letters)
    cons = add_seen(cons0, words)
    cons = check_reachability(cons, letters)
    print("\n".join([f"{k} ->\t\t{g}" for k, g in cons.items()]))
    print(f"got {len(cons.keys())} states in total")

    scons = serialize(cons)
    print("\n".join([f"{k} ->\t{g}" for k, g in scons.items()]))


    # Create a new directed graph for FSM
    fsm = Digraph(format='jpeg')  # Set the output format to JPEG

    c = 100
    rendered = []
    for _, (k, v) in Progress(scons.items()):
        c-=1
#        if not c:
#            break
        st, l = k
        if st not in rendered:
            fsm.node(st)
            rendered.append(st)
        if v not in rendered:
            fsm.node(v)
            rendered.append(v)
        fsm.edge(st, v, label=l)
    # Optionally, specify the start state (usually marked with a special node or label)
    fsm.attr(label='FREEFAREA', labelloc='t')


    print("rendering....")
    # Save the FSM as a JPEG file
    fsm.render('fsm')  # This will save the file as 'fsm.jpeg'
