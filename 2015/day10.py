import re

NUMS = re.compile(r'(\d)\1*')

def get_results(instructions):
    sequence = instructions
    for _ in xrange(40):
        sequence = play_game(sequence)
    print len(sequence)
    for _ in xrange(10):
        sequence = play_game(sequence)
    return len(sequence)


def play_game(string):
    output = ''
    for match in NUMS.finditer(string):
        length = len(match.group(0))
        num = match.group(1)
        output += '{}{}'.format(length, num)
    return output


if __name__ == '__main__':
    with open('instructions_day10.txt', 'r') as f:
        instructions = f.read().strip()
    print get_results(instructions)