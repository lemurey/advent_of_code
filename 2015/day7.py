OPERATORS = {
             '->'  : lambda x: x,
             'AND' : lambda x, y: x & y,
             'OR' : lambda x, y: x | y,
             'NOT' : lambda x: ~x & 0xffff,
             'LSHIFT' : lambda x, y: x << y,
             'RSHIFT' : lambda x, y: x >> y}

def get_results(instructions, part2=None):
    tree = parse_instructions(instructions, part2)
    return find_key(tree, 'a')


def parse_instructions(instructions, override=None):
    tree = {}
    for line in instructions.split('\n'):
        temp = line.split()
        if len(temp) == 3:
            value = (temp[1], temp[0])
        elif len(temp) == 4:
            value = (temp[0], temp[1])
        else:
            value = (temp[1], temp[0], temp[2])
        if temp[-1] in tree:
            raise KeyError('assigned result alreayd in caluclation dictionary')
        tree[temp[-1]] = value
        if temp[-1] == 'b' and override:
            print 'EXECUTING OVERRIDE'
            tree[temp[-1]] = (temp[1] , str(override))
    return tree


def memoize(f):
    memo = {}
    def helper(graph, key):
        if key not in memo:
            memo[key] = f(graph, key)
        return memo[key]
    return helper


@memoize
def find_key(graph, key):
    if key.isdigit():
        return int(key)
    value = graph[key]
    operation = value[0]
    if len(value) == 2:
        return OPERATORS[operation](find_key(graph, value[1]))
    return OPERATORS[operation](find_key(graph, value[1]), find_key(graph, value[2]))


if __name__ == '__main__':
    with open('instructions_day7.txt', 'r') as f:
        instructions = f.read().strip()
    #### for part two add result of part1 as argument to get_results
    print get_results(instructions, 16076)
