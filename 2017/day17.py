from aoc_utilities import get_instructions
import os


# stolen from reddit (for speed, my original way did all 500000 loops,
# I did figure out that 0 is stationary so you dont' need to mess with the
# array for part2)
def part_2(num_steps):
    value = 0
    position = 0
    while value < 50000000:
        if position == 1:
            value_after_zero = value
        jump = (value - position) // num_steps
        value += jump + 1
        position = 1 + (position + (jump + 1) * (num_steps + 1) - 1) % value
    return value_after_zero


def get_answer(data, part2=False):
    num_steps = int(data.strip())
    location = 0
    array = [0]
    if part2:
        return part_2(num_steps)

    size = 2017
    for step in range(1, size + 1):
        location = 1 + (location + num_steps) % step
        array.insert(location, step)

    return array[location + 1]


if __name__ == '__main__':
    day = int(os.path.basename(__file__).split('.')[0].split('y')[1])
    inputs = get_instructions(day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
