from aoc_utilities import get_instructions
from pathlib import Path
from collections import deque
from functools import cache


def parse_input(lines):
    connections = {}
    for line in lines:
        key, rest = line.split(': ')
        if key not in connections:
            connections[key] = set()
        for entry in rest.split():
            connections[key].add(entry)
    return connections


@cache
def dfs(start, end, forbidden):
    if start == end:
        return 1
    return sum(dfs(node, end, forbidden) for node in connections[start] if node not in forbidden)


def search(start, end, connections, forbidden=None):
    paths = set()
    Q = deque([(start, (start,))])
    if forbidden is None:
        forbidden = set()
    c = 0
    while Q:
        node, path = Q.pop()

        c += 1
        if c % 1000000 == 0:
            print(c, len(Q))

        for n in connections.get(node, []):
            new_path = path + (n,)
            if n == end:
                paths.add(new_path)
            elif (n not in forbidden):
                Q.append((n, new_path))
    return paths


def get_answer(data, part2=False):
    global connections
    connections = parse_input(data)
    if part2:
        p_svr_dac = dfs('svr', 'dac', ('out', 'fft'))
        p_dac_fft = dfs('dac', 'fft', ('out', 'svr'))
        p_fft_out = dfs('fft', 'out', ('dac', 'svr'))
        p_svr_fft = dfs('svr', 'fft', ('out', 'dac'))
        p_fft_dac = dfs('fft', 'dac', ('svr', 'out'))
        p_dac_out = dfs('dac', 'out', ('fft', 'svr'))

        return (p_svr_dac * p_dac_fft * p_fft_out +
                p_svr_fft * p_fft_dac * p_dac_out)
    else:
        paths = search('you', 'out', connections)
    # for path in paths:
    #     print(path)
    return len(paths)




if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)

#     inputs = '''aaa: you hhh
# you: bbb ccc
# bbb: ddd eee
# ccc: ddd eee fff
# ddd: ggg
# eee: out
# fff: out
# ggg: out
# hhh: ccc fff iii
# iii: out'''.split('\n')

#     inputs = '''svr: aaa bbb
# aaa: fft
# fft: ccc
# bbb: tty
# tty: ccc
# ccc: ddd eee
# ddd: hub
# hub: fff
# eee: dac
# dac: fff
# fff: ggg hhh
# ggg: out
# hhh: out'''.split('\n')

    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
