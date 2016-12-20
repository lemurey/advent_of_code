from utilities import timeit

WEAPONS = [{'attack': 4, 'cost': 8},
           {'attack': 5, 'cost': 10},
           {'attack': 6, 'cost': 25},
           {'attack': 7, 'cost': 40},
           {'attack': 8, 'cost': 74}]

ARMOR = [{'armor': 0, 'cost': 0},
         {'armor': 1, 'cost': 13},
         {'armor': 2, 'cost': 31},
         {'armor': 3, 'cost': 53},
         {'armor': 4, 'cost': 75},
         {'armor': 5, 'cost': 102}]

RINGS = [{'armor': 0, 'attack': 0, 'cost': 0},
         {'armor': 0, 'attack': 1, 'cost': 25},
         {'armor': 0, 'attack': 2, 'cost': 50},
         {'armor': 0, 'attack': 3, 'cost': 100},
         {'armor': 1, 'attack': 0, 'cost': 20},
         {'armor': 2, 'attack': 0, 'cost': 40},
         {'armor': 3, 'attack': 0, 'cost': 80}]


def boss_stats(instructions):
    boss = {}
    for line in instructions.split('\n'):
        stat, value = line.split(': ')
        boss[stat] = int(value)

    return boss


def boss_fight(a, d, boss):
    b = [boss['Hit Points'], boss['Damage'], boss['Armor']]
    hp = 100
    while True:
        b[0] -= max(d - b[2], 1)
        if b[0] <= 0:
            return True
        hp -= max(b[1] - a, 1)
        if hp <= 0:
            return False


def run_sim(boss, part2):
    outcomes = []
    for w in WEAPONS:
        for a in ARMOR:
            for r1 in RINGS:
                for r2 in RINGS:
                    if r1['cost'] != 0 and r1['cost'] == r2['cost']:
                        continue
                    armor = a['armor'] + r1['armor'] + r2['armor']
                    attack = w['attack'] + r1['attack']  + r2['attack']
                    cost = a['cost'] + w['cost'] + r1['cost'] + r2['cost']
                    if boss_fight(armor, attack, boss):
                        outcomes.append(('win', cost))
                    else:
                        outcomes.append(('lose', cost))
    if part2:
        return sorted(outcomes, key=lambda x: -x[1])
    else:
        return sorted(outcomes, key=lambda x: x[1])



@timeit
def get_results(instructions, part2=False):
    boss = boss_stats(instructions)
    t = run_sim(boss, part2)
    for e in t:
        if e[0] == 'win' and not part2:
            return '{}: {}'.format(*e)
        elif part2 and e[0] == 'lose':
            return '{}: {}'.format(*e)
        


if __name__ == '__main__':
    with open('instructions_day21.txt', 'r') as f:
        instructions = f.read().strip()
    print get_results(instructions, part2=False)
    print get_results(instructions, part2=True)
