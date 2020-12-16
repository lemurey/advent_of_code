from aoc_utilities import get_instructions
from pathlib import Path


def parse_data(data):
    rules = {}
    tickets = []
    get_tickets = False
    get_mine = False
    for row in data:
        if row == 'nearby tickets:':
            get_tickets = True
            continue
        if get_tickets:
            vals = [int(x) for x in row.split(',')]
            tickets.append(vals)
            continue
        if row == 'your ticket:':
            get_mine = True
            continue
        if get_mine:
            my_ticket = [int(x) for x in row.split(',')]
            get_mine = False
            continue
        if ':' in row:
            label, values = row.split(': ')
            left, right = values.split(' or ')
            ll, lh = left.split('-')
            rl, rh = right.split('-')

            vals = (list(range(int(ll), int(lh) + 1)) +
                    list(range(int(rl), int(rh) + 1)))
            rules[label] = set(vals)

    return rules, tickets, my_ticket


def match_fields(fields):
    aligned = {}
    while len(aligned) < len(fields):
        for k, v in fields.items():
            if len(v) == 1:
                val = list(v)[0]
                aligned[k] = val
                to_remove = val

        for v in fields.values():
            if to_remove in v:
                v.remove(to_remove)

    return aligned


def check_fields(rules, tickets):
    results = {}
    for label, options in rules.items():
        possible = set(range(len(tickets[0])))

        for ticket in tickets:
            for i, entry in enumerate(ticket):
                if entry not in options:
                    if i in possible:
                        possible.remove(i)
        results[label] = possible
    return results


def check_ticket(rules, ticket):
    invalids = []
    for field in ticket:
        for options in rules.values():
            if field in options:
                break
        else:
            invalids.append(field)
    return invalids


def check_valid(rules, tickets, verbose=False):
    error_rate = 0
    valid_tickets = []
    for ticket in tickets:
        invalids = check_ticket(rules, ticket)
        if verbose:
            print(invalids)
        error_rate += sum(invalids)
        if len(invalids) == 0:
            valid_tickets.append(ticket)

    return error_rate, valid_tickets


def get_answer(data, part2=False):
    rules, tickets, my_ticket = parse_data(data)
    error_rate, valid_tickets = check_valid(rules, tickets)
    if not part2:
        return error_rate

    valid_tickets = valid_tickets + [my_ticket]

    results = check_fields(rules, valid_tickets)
    results = match_fields(results)

    output = 1
    for k, v in results.items():
        if 'departure' in k:
            output *= my_ticket[v]

    return output


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)

#     inputs = '''class: 1-3 or 5-7
# row: 6-11 or 33-44
# seat: 13-40 or 45-50

# your ticket:
# 7,1,14

# nearby tickets:
# 7,3,47
# 40,4,50
# 55,2,20
# 38,6,12'''.split('\n')

#     inputs = '''class: 0-1 or 4-19
# row: 0-5 or 8-19
# seat: 0-13 or 16-19

# your ticket:
# 11,12,13

# nearby tickets:
# 3,9,18
# 15,1,5
# 5,14,9'''.split('\n')

    # print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
