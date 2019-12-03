from aoc_utilities import get_instructions
import os


def parse_instructions(data):
    return [int(x) for x in data]


def fuel_for_mass(mass):
    return (mass // 3) - 2


def recurse_fuel(mass):
    current_fuel = fuel_for_mass(mass)
    total_fuel = 0
    while current_fuel > 0:
        total_fuel += current_fuel
        current_fuel = fuel_for_mass(current_fuel)
    return total_fuel


def get_answer(data, part2=False):
    if part2:
        return sum([recurse_fuel(x) for x in parse_instructions(data)])

    return sum([fuel_for_mass(x) for x in parse_instructions(data)])


if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))