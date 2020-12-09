from aoc_utilities import get_instructions
from pathlib import Path


def is_sum(arr, num):
    vals = {}
    counts = {}
    for x in arr:
        if x not in counts:
            counts[x] = 0
        counts[x] += 1
        vals[num - x] = x

    for x in arr:
        if x in vals:
            if x == vals[x] and counts[x] < 2:
                continue
            else:
                return True
    return False


def solver(nums, offset):
    for i in range(offset, len(nums)):

        val = nums[i]
        if not is_sum(nums[(i - offset):i], val):
            return val


def get_exclusions(arr, num):
    exclusions = []
    for i, val in enumerate(arr):
        if val >= num:
            exclusions.append(i)
    return exclusions


def get_zones(arr, num):
    zone = []
    exclusions = get_exclusions(arr, num)
    low = 0

    for i in range(len(arr)):
        if i in exclusions:
            if low > (i - 1):
                low = i + 1
                continue
            zone.append((low, i - 1))
            low = i + 1
            prev = i

    return zone


def check_zone(low, high, nums, c_val):
    subset = nums[low: high + 1]
    end = len(subset) + 1

    for i in range(len(subset)):
        for j in range(i, end):
            check = sum(subset[i:j])
            if check == c_val:
                print(low + i, low + j)
                return subset[i:j]
            elif check > c_val:
                break

    return None


def run_part2(nums, part1):

    zones = get_zones(nums, part1)

    ordered = {}
    for low, high in zones:
        size = high - low
        if size not in ordered:
            ordered[size] = []
        ordered[size].append((low, high))

    for key in sorted(ordered):
        for low, high in ordered[key]:
            check = check_zone(low, high, nums, part1)
            if check is not None:
                return check


def get_answer(data, part2=False):

    offset = 25

    nums = [int(x) for x in data]

    part1 = solver(nums, offset)

    print(part1)

    subset = run_part2(nums, part1)

    return min(subset) + max(subset)


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)

#     inputs = '''35
# 20
# 15
# 25
# 47
# 40
# 62
# 55
# 65
# 95
# 102
# 117
# 150
# 182
# 127
# 219
# 299
# 277
# 309
# 576'''.split('\n')

    print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))
