import re

RED = re.compile(r':"red"')

def get_non_red(line):
    if not RED.search(line.group()):
        return get_results(line.group())
    return '0'


def get_results(instructions, part2=False):
    numbers = []
    if not part2 or len(instructions) == 0:
        return str(sum(map(int,re.findall(r'-?\d+', instructions))))
    subber = re.compile(r'{[^{}]*}')
    while RED.search(instructions):
        instructions = subber.sub(get_non_red, instructions)
    return get_results(instructions)


if __name__ == '__main__':
    with open('instructions_day12.txt', 'r') as f:
        instructions = f.read().strip()
    print get_results(instructions, part2=False)
    print get_results(instructions, part2=True)