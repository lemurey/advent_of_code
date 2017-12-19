import requests
import os


def get_instructions(day):
    file_name = 'instructions_day_{:0>2}.txt'.format(day)
    if file_name not in os.listdir('.'):
        print('downloading from web')
        if 'aoc_code' not in os.environ:
            with open('.env', 'r') as f:
                for line in f:
                    key, value = line.split('=')
                    if key == 'cookie_value':
                        os.environ['aoc_code'] = value.strip()
        cookie = {'session': os.environ['aoc_code']}
        url = 'http://adventofcode.com/2017/day/{}/input'.format(day)
        instructions = requests.get(url, cookies=cookie).text.rstrip()
        with open(file_name, 'w') as f:
            f.write(instructions)
    else:
        print('loading from local')
        with open(file_name, 'r') as f:
            instructions = f.read()
    return instructions


if __name__ == '__main__':
    max_test_day = 1
    for test_day in range(1, max_test_day + 1):
        f_name = 'instructions_day_{:0>2}.txt'.format(test_day)
        with open(f_name, 'r') as f:
            real = f.read().strip()
        os.remove(f_name)
        test = get_instructions(test_day)
        print(test == real)
