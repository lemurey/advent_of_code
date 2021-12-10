from aoc_utilities import get_instructions
from pathlib import Path


def check_line(line):
    opens = '([{<'
    closes = ')]}>'
    stack = []
    for i, char in enumerate(line):
        if char in opens:
            stack.append(char)
        else:
            index = closes.index(char)
            if (len(stack) > 0) and (stack[-1] == opens[index]):
                stack.pop()
            else:
                return char, i
    return None, stack


def get_answer(data, part2=False):
    points = {')': 3, ']': 57, '}': 1197, '>': 25137}
    total = 0
    finishes = []
    for line in data:
        c, i  = check_line(line)
        if c:
            total += points[c]
        else:
            finishes.append(''.join(i[::-1]))

    if part2:
        points = {'(': 1, '[': 2, '{': 3, '<': 4}
        scores = []
        for line in finishes:
            score = 0
            for char in line:
                score *= 5
                score += points[char]
            scores.append(score)
        c = len(scores) // 2
        print(len(scores), c)
        total = sorted(scores)[c - 1:c + 2]
    return total


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs = '''[({(<(())[]>[[{[]{<()<>>
# [(()[<>])]({[<{<<[]>>(
# {([(<{}[<>[]}>{[]{[(<()>
# (((({<>}<{<{<>}{[]{[]{}
# [[<[([]))<([[{}[[()]]]
# [{[{({}]{}}([{[{{{}}([]
# {<[[]]>}<{[{[{[]{()[[[]
# [<(<(<(<{}))><([]([]()
# <{([([[(<>()){}]>(<<{{
# <{([{{}}[<[[[<>{}]]]>[]]'''.split('\n')
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
