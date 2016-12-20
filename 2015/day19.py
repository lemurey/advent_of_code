from time import time

def substitute(string):
    singles = {'B', 'e', 'F', 'H', 'O', 'N', 'P', 'C', 'Y'}
    doubles = {'Mg', 'Ca', 'Al', 'Si', 'Th', 'Ti', 'Ar', 'Rn'}
    subs = {x : 'X' for x in list(singles) + list(doubles)}
    subs['Ar'] = ')'
    subs['Rn'] = '('
    subs['Y'] = ','

    output = ''
    i = 0
    while i < len(string):
        char = string[i]
        if i < len(string) - 1:
            phrase = char + string[i + 1]
        if phrase in doubles:
            output += subs[phrase]
            i += 2
        else:
            output += subs[char]
            i += 1
    return output


def parse_instructions(instructions):
    operations = {}
    for line in instructions.split('\n'):
        if '=>' in line:
            initial, transformed  = line.split(' => ')
            if initial not in operations:
                operations[initial] = []
            operations[initial].append(transformed)
        else:
            test = line
    return operations, test


def run_test(ops, string):
    singles = {'B', 'e', 'F', 'H', 'O', 'N', 'P'}
    doubles = {'Mg', 'Ca', 'Al', 'Si', 'Th', 'Ti'}
    output = set()
    index = 0
    while index < len(string):
        atom = string[index]
        mol = string[index:index + 2]
        add = []
        start = index
        mod = 1

        if atom in singles:
            add = ops[atom]
        elif mol in doubles:
            add = ops[mol]
            mod += 1
            index += 1

        for item in add:
            new = '{}{}{}'.format(string[:start], item, string[start + mod:])
            output.add(new)

        index += 1
    return output


def get_part2(instructions):
    final = substitute(instructions)
    base = len(final)
    l_parens = final.count('(')
    r_parens = final.count(')')
    commas = final.count(',')
    return base - l_parens - r_parens - 2 * commas - 1


def timeit(function):
    def timed(*args, **kwargs):
        s_t = time()
        result = function(*args, **kwargs)
        e_t = time()
        out = '{} {} took {:.2f} sec'
        print out.format(function.__name__, kwargs, e_t - s_t)
        return result
    return timed


@timeit
def get_results(instructions, part2=False):
    ops, test = parse_instructions(instructions)
    if part2:
        return get_part2(test)
    else:
        t = run_test(ops, test)
        return len(t)

if __name__ == '__main__':
    with open('instructions_day19.txt', 'r') as f:
        instructions = f.read().strip()
    print get_results(instructions, part2=False)
    print get_results(instructions, part2=True)