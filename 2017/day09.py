from aoc_utilities import get_instructions
import os


def get_answer(data, part2=False):
    total_score = 0
    local_score = 0
    in_group = False
    in_garbage = False
    prev = ''
    garbage_score = 0
    for char in data:
        if prev == '!':
            prev = ''
            continue
        prev = char
        if char == '>' and in_garbage:
            in_garbage = False
            continue
        if char == '}' and not in_garbage:
            total_score += local_score
            local_score -= 1
        if char == '{' and not in_garbage:
            local_score += 1
            in_group = True
        if char == '<' and not in_garbage:
            in_garbage = True
            continue
        if char == '!':
            continue

        if in_garbage:
            garbage_score += 1

    if part2:
        return garbage_score
    return total_score


def run_tests():
    print(get_answer('<>' ,True) == 0)
    print(get_answer('<random characters>' ,True) == 17)
    print(get_answer('<<<<>', True) == 3)
    print(get_answer('<{!>}>', True) == 2)
    print(get_answer('<!!>', True) == 0)
    print(get_answer('<!!!>>', True) == 0)
    print(get_answer('<{o"i!a,<{i<a>', True) == 10)


if __name__ == '__main__':
    day = int(os.path.basename(__file__).split('.')[0].split('y')[1])
    inputs = get_instructions(day)
    # run_tests()
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
