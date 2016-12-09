import re

vowels = re.compile(r'[aeiou]')
repeats = re.compile(r'([a-z])\1', re.IGNORECASE)
disallowed = re.compile(r'ab|cd|pq|xy')
double_repeats = re.compile(r'([a-z][a-z]).*\1')
triple = re.compile(r'([a-z]).\1')


def get_results(instructions):
    nice1 = 0
    nice2 = 0
    for line in instructions.split('\n'):
        if disallowed.search(line):
            pass
        elif repeats.search(line) and len(vowels.findall(line)) >= 3:
            nice1 += 1
        if double_repeats.search(line) and triple.search(line):
            nice2 += 1
    print nice1
    return nice2


if __name__ == '__main__':
    with open('instructions_day5.txt', 'r') as f:
        instructions = f.read().strip()
    print get_results(instructions)