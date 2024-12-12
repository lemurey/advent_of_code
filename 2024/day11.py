from aoc_utilities import get_instructions
from pathlib import Path
from functools import cache


@cache
def how_many(stone, count):
    if count == 0:
        return 1

    if stone == 0:
        return how_many(1, count - 1)

    stone_length = len(str(stone))

    if stone_length % 2 == 0:
        left = str(stone)[(stone_length // 2):]
        right = str(stone)[:(stone_length // 2)]
        return how_many(int(left), count - 1) + how_many(int(right), count - 1)

    return how_many(stone * 2024, count - 1)


def apply_rules(stone):
    if int(stone) == 0:
        return [str(1)]
    if len(str(stone)) % 2 == 0:
        split_val = len(str(stone)) // 2
        left = str(stone)[:split_val]
        right = str(stone)[split_val:].lstrip('0')
        if right == '':
            right = '0'
        return [left, right]
    return [str(int(stone) * 2024)]


def blink(stones):
    new = []
    for stone in stones:
        update = apply_rules(stone)
        new.extend(update)
    return new


def get_answer(data, part2=False):
    stones = data[0].split()
    if part2:
        return sum(how_many(int(x), 75) for x in stones)
    for _ in range(25):
        stones = blink(stones)
    return len(stones)


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
