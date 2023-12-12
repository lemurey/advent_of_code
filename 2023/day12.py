from aoc_utilities import get_instructions
from pathlib import Path
from itertools import groupby


# first day I couldn't come up with anything, looked at reddit and saw people
# mentioning DP, then I wrote this

def run_counts(memo, string, nums, string_index, nums_index, hashcount):
    key = (string_index, nums_index, hashcount)
    if key in memo:
        return memo[key]

    # end condition if we are at final character
    if string_index == len(string):
        # if we are at end of numbers and we have no extraneous #
        if nums_index == len(nums) and hashcount == 0:
            return 1 # valid arrangement found
        # if we are at second to last number and have found correct number of #
        if nums_index == (len(nums) - 1) and nums[nums_index] == hashcount:
            return 1 # valid arrangement found
        return 0 # invalid arrangment found

    # we are not at the end because end condtion didn't hit
    # so check current character and keep track of the values
    val = 0
    cur_char = string[string_index]

    if cur_char == '#':
        # keep looking for strings of #
        val += run_counts(memo, string, nums, string_index + 1, nums_index, hashcount + 1)
    elif cur_char == '.':
        # if we are at 0 hashcount keep looking
        if hashcount == 0:
            val += run_counts(memo, string, nums, string_index + 1, nums_index, 0)
        # if we have the correct hashnumber increment string and nums and keep looking
        elif nums_index < len(nums) and hashcount == nums[nums_index]:
            val += run_counts(memo, string, nums, string_index + 1, nums_index + 1, 0)
    else:
        # pretend its a #
        val += run_counts(memo, string, nums, string_index + 1, nums_index, hashcount + 1)
        # pretend its a .
        if hashcount == 0:
            val += run_counts(memo, string, nums, string_index + 1, nums_index, 0)
        elif nums_index < len(nums) and hashcount == nums[nums_index]:
            val += run_counts(memo, string, nums, string_index + 1, nums_index + 1, 0)

    memo[key] = val
    return val


def get_answer(data, part2=False):
    total = 0
    for row in data:
        string, nums = row.split()
        if part2:
            string = '?'.join([string for _ in range(5)])
            nums = ','.join([nums for _ in range(5)])
        nums = list(map(int, nums.split(',')))
        n = run_counts({}, string, nums, 0, 0, 0)
        # print(string, nums, n)
        total += n
    return total

if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs = '''???.### 1,1,3
# .??..??...?##. 1,1,3
# ?#?#?#?#?#?#?#? 1,3,1,6
# ????.#...#... 4,1,1
# ????.######..#####. 1,6,5
# ?###???????? 3,2,1'''.split('\n')
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
