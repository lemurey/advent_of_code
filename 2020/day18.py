from aoc_utilities import get_instructions
from pathlib import Path
from operator import add, mul
from functools import reduce


def run_expresion(expression):
    total = 0
    op = add
    for statement in expression.split():
        if statement.isdigit():
            val = int(statement)
            total = op(total, val)
        elif statement == '+':
            op = add
        elif statement == '*':
            op = mul
    return total


def run_expression_2(expression):
    values = []
    left = None
    for statement in expression.split():
        if statement.isdigit():
            current = int(statement)
            if left is not None:
                current += left
                left = None
            values.append(current)
        elif statement == '+':
            left = values.pop()
    return reduce(mul, values, 1)


def run_line(row, func=run_expresion):
    locs = []
    for i, char in enumerate(row):
        if char == '(':
            locs.append(i)
        elif char == ')':
            start = locs.pop()
            expression = row[start + 1:i]
            result = func(expression)
            new = f'{row[:start]} {result} {row[i+1:]}'
            return run_line(new, func=func)
    return func(row)


def get_answer(data, part2=False):
    results = []
    for row in data:
        if part2:
            current = run_line(row, run_expression_2)
        else:
            current = run_line(row)
        results.append(current)
    return sum(results)


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
