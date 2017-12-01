import requests
import os


def get_instructions(day):
    file_name = 'instructions_day_{}.txt'.format(day)
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
        instructions = requests.get(url, cookies=cookie).text.strip()
        with open(file_name, 'w') as f:
            f.write(instructions)
    else:
        print('loading from local')
        with open(file_name, 'r') as f:
            instructions = f.read()
    return instructions


if __name__ == '__main__':
    test = get_instructions(1)
    with open('instructions_day_1.txt', 'r') as f:
        real = f.read().strip()
