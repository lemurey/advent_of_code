from aoc_utilities import get_instructions
from pathlib import Path
from collections import deque


def get_connections(data):
    connections = {}
    for line in data:
        c1, c2 = line.split('-')
        if c1 not in connections:
            connections[c1] = set()
        if c2 not in connections:
            connections[c2] = set()
        connections[c1].add(c2)
        connections[c2].add(c1)
    return connections


def sets_of_three(connections):
    sets = set()
    for c1 in connections:
        for c2 in connections[c1]:
            for c3 in connections[c2]:
                if c3 in connections[c1]:
                    key = sorted([c1, c2, c3])
                    sets.add(tuple(key))
    return sets


# implementation of Bron Kerbosch algorith
def get_network(N, P, R=None, X=None):
    if R is None:
        R = set()
    if X is None:
        X = set()
    if not P and not X:
        yield R
    for v in list(P):
        yield from get_network(N, P & N[v], R | {v}, X & N[v])
        P -= {v}
        X |= {v}


def get_answer(data, part2=False):
    connections = get_connections(data)
    threes = sets_of_three(connections)
    t_count = 0
    for c1, c2, c3 in threes:
        if c1.startswith('t') or c2.startswith('t') or c3.startswith('t'):
            # print(c1, c2, c3)
            t_count += 1
    print(t_count)
    network = get_network(connections, set(connections.keys()))
    for sub_network in sorted(network, key=len, reverse=True):
        return ','.join(sorted(sub_network))


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)

#     inputs = '''kh-tc
# qp-kh
# de-cg
# ka-co
# yn-aq
# qp-ub
# cg-tb
# vc-aq
# tb-ka
# wh-tc
# yn-cg
# kh-ub
# ta-co
# de-co
# tc-td
# tb-wq
# wh-td
# ta-ka
# td-qp
# aq-cg
# wq-ub
# ub-vc
# de-ta
# wq-aq
# wq-vc
# wh-yn
# ka-de
# kh-ta
# co-tc
# wh-qp
# tb-vc
# td-yn'''.split('\n')

    print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))
