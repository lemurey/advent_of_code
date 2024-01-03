from aoc_utilities import get_instructions
from pathlib import Path


def make_graph(data):
    graph = {}
    for line in data:
        left, right = line.split(': ')
        if left not in graph:
            graph[left] = set()
        for entry in right.split():
            if entry not in graph:
                graph[entry] = set()
            graph[left].add(entry)
            graph[entry].add(left)
    return graph


def get_answer(data, part2=False):
    '''
    we are going to keep track of two sets. one is just all the keys in the graph
    the other is the complement of that. Every iteration remove from other the
    element with the most neighbors in the full set. Once the difference is 3
    elements, we have the two groups we want.
    '''
    graph = make_graph(data)
    other = set(graph)
    count = lambda x: len(graph[x] - other)
    while sum(map(count, other)) != 3:
        other.remove(max(other, key=count))
    return len(other) * len(set(graph) - other)


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs = '''jqt: rhn xhk nvd
# rsh: frs pzl lsr
# xhk: hfx
# cmg: qnr nvd lhk bvb
# rhn: xhk bvb hfx
# bvb: xhk hfx
# pzl: lsr hfx nvd
# qnr: nvd
# ntq: jqt hfx bvb xhk
# nvd: lhk
# lsr: lhk
# rzs: qnr cmg lsr rsh
# frs: qnr lhk lsr'''.split('\n')
    print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))
