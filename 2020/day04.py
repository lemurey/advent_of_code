from aoc_utilities import get_instructions
from pathlib import Path


def is_valid(passport):
    for k in ('byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'):
        if k not in passport:
            return False

    if 'cid' in passport:
        return True
    return True


def check_year(p, key, req_digits, min_year, max_year):
    if len(p[key]) != req_digits:
        return False
    if int(p[key]) < min_year:
        return False
    if int(p[key]) > max_year:
        return False
    return True


def check_height(h):
    if h.endswith('in'):
        end = 'in'
        num = int(h.split('i')[0])
    elif h.endswith('cm'):
        end = 'cm'
        num = int(h.split('c')[0])
    else:
        return False

    if end == 'in':
        if num < 59:
            return False
        if num > 76:
            return False
    else:
        if num < 150:
            return False
        if num > 193:
            return False
    return True


def check_hair_color(c):
    if not c.startswith('#'):
        return False
    rem = c.split('#')[1]

    return all([d in '0123456789abcdef' for d in rem])


def check_eye_color(c):
    if c not in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
        return False
    return True


def check_pid(pid):
    if len(pid) != 9:
        return False
    if not pid.isdigit():
        return False
    return True


def is_valid_2(passport, verbose=False):
    if not is_valid(passport):
        return False

    if not check_year(passport, 'byr', 4, 1920, 2002):
        return False

    if not check_year(passport, 'iyr', 4, 2010, 2020):
        return False

    if not check_year(passport, 'eyr', 4, 2020, 2030):
        return False

    if not check_height(passport['hgt']):
        return False

    if not check_hair_color(passport['hcl']):
        return False

    if not check_eye_color(passport['ecl']):
        return False

    if not check_pid(passport['pid']):
        return False

    return True


def parse_inputs(inputs):
    passports = []
    store = {}
    for row in inputs:
        if row == '':
            passports.append(store)
            store = {}
            continue
        for entry in row.split():
            key, value = entry.split(':')
            store[key] = value
    passports.append(store)
    return passports


def get_answer(data, part2=False):
    passports = parse_inputs(data)
    num_valid = 0

    for passport in passports:
        if part2:
            if is_valid_2(passport):
                num_valid += 1
        else:

            if is_valid(passport):
                num_valid += 1
    return num_valid


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
