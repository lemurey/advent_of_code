from aoc_utilities import get_instructions
from pathlib import Path


def run_game(nums, num_rounds=2020):
    spoken = {}

    for i in range(num_rounds):
        if i < len(nums):
            spoken[nums[i]] = [i]
            last_spoken = nums[i]
            continue
        if last_spoken in spoken:
            previous = spoken[last_spoken]
            if len(previous) == 1:
                last_spoken = 0
            else:
                last_spoken = previous[-1] - previous[-2]
        if last_spoken not in spoken:
            spoken[last_spoken] = []
        spoken[last_spoken].append(i)

        if i == 2019:
            print(last_spoken)

    return last_spoken



def get_answer(data, part2=False):
    nums = list(map(int, data[0].split(',')))
    return run_game(nums, 30000000)


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))
