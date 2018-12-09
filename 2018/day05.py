from aoc_utilities import get_instructions
import os


def check(a, b):
    if a.lower() == b.lower():
        if ((a.isupper() and b.islower()) or
            (a.islower() and b.isupper())):
            return True
    return False


def folding(line):
    output = ''
    location = 0
    for char in line:
        if not output:
            output += char
            continue
        prev = output[-1]
        if check(char, prev):
            output = output[:-1]
        else:
            output += char
    return output


def get_answer(data, part2=False):
    if part2:
        shortest = len(data)
        for char in 'abcdefghijklmnopqrstuvwxyz':
            temp = data.replace(char, '').replace(char.upper(), '')
            check = folding(temp)
            if len(check) < shortest:
                folded = check
                shortest = len(check)
    else:
        folded = folding(data)
    return len(folded)


if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])
    inputs = get_instructions(year, day)[0]
    sample = 'dabAcCaCBAcCcaDA'
    print(get_answer(sample))
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))