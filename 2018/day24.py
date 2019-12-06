import os
from aoc_utilities import get_instructions
import re

class Unit:

    def __init__(self, size, hp, damage, dtype, initiative, immune, weak, team,
                 num):
        self.size = int(size)
        self.hp = int(hp)
        self.damage = int(damage)
        self.dtype = dtype
        self.initiative = int(initiative)
        self.immune = immune
        self.weak = weak
        self.team = team
        self.num = num

    def effective_power(self):
        return self.size * self.damage

    def calc_damage(self, other):
        if other is None:
            return 0
        if other.size == 0:
            return 0
        mod = 1
        if self.dtype in other.weak:
            mod = 2
        elif self.dtype in other.immune:
            mod = 0
        return mod * self.effective_power()

    def pick_target(self, options):
        max_damage = 0
        selected = None
        for target in options:
            if target.team == self.team:
                continue
            if target.size == 0:
                continue
            damage = self.calc_damage(target)
            if damage == 0:
                continue
            if damage > max_damage:
                selected = target
                max_damage = damage
            elif damage == max_damage:
                if target.effective_power() > selected.effective_power():
                    selected = target
                if target.effective_power() == selected.effective_power():
                    if target.initiative > selected.initiative:
                        selected = target
        return selected

    def __str__(self):
        return '{} -- {}: {}, {}'.format(self.team, self.num, self.size,
                                         self.hp)

    def __repr__(self):
        return '{} -- {}'.format(self.team, self.num)

    def __eq__(self, other):
        return (self.team == other.team and
                self.size == other.size and
                self.damage == other.damage and
                self.initiative == other.initiative and
                self.dtype == other.dtype)


class Fight:
    def __init__(self, groups):
        self.groups = groups
        self.damage_done = {'Immune System': False, 'Infection': False}

    def _select_sort(self, unit):
        return (-unit.effective_power(), -unit.initiative)

    def _attack_sort(self, *args):
        att, _ = args[0]
        return -att.initiative

    def _select_targets(self):
        options = [x for x in self.groups if x.size != 0]
        targets = []
        for unit in sorted(self.groups, key=self._select_sort):
            target = unit.pick_target(options)
            targets.append((unit, target))
            if target is None:
                continue

            options.remove(target)
        return targets

    def _get_target_string(self, targets):
        o = ''
        for att, tar in sorted(targets, key=lambda x: (x[0].team, -x[0].num),
                               reverse=True):
            if tar is None:
                continue
            o += '{} group {} would deal defending group {} {} damage\n'.format(
                    att.team, att.num, tar.num, att.calc_damage(tar))
        return o

    def _run_fight(self, verbose=False):
        if verbose:
            print(self)
        targets = self._select_targets()

        if verbose:
            o = self._get_target_string(targets)
            o += '\n'
        self.damage_done = {'Immune System': False, 'Infection': False}
        for attacker, target in sorted(targets, key=self._attack_sort):
            damage = attacker.calc_damage(target)
            if damage == 0:
                continue

            units_removed, rem = divmod(damage, target.hp)
            if units_removed > target.size:
                units_removed = target.size
            if verbose:
                o += ('{} group {} attacks defending group {}, kiling {} '
                      'units\n'.format(attacker.team, attacker.num,
                                       target.num, units_removed))
            target.size -= units_removed
            if units_removed > 0:
                self.damage_done[attacker.team] = True

        if verbose:
            print(o)

    def __call__(self, verbose=False):
        self._run_fight(verbose)

    def __str__(self):
        o = 'Immune System:\n'
        for unit in self.groups:
            if unit.team != 'Immune System':
                continue
            if unit.size == 0:
                continue
            o += 'Group {} contains {} units\n'.format(unit.num, unit.size)
        o += 'Infection:\n'
        for unit in self.groups:
            if unit.team != 'Infection':
                continue
            if unit.size == 0:
                continue
            o += 'Group {} contains {} units\n'.format(unit.num, unit.size)
        return o


class War:
    def __init__(self, groups):
        self.groups = groups
        self.orig = [self._copy_unit(u) for u in self.groups]
        self.ndc = 0

    def _copy_unit(self, u):
        copy = {'size': u.size,
                'hp': u.hp,
                'damage': u.damage,
                'dtype': u.dtype,
                'initiative': u.initiative,
                'immune': u.immune,
                'weak': u.weak,
                'team': u.team,
                'num': u.num}
        return Unit(**copy)

    def _apply_boost(self, boost):
        self._reset()
        for unit in self.groups:
            if unit.team != 'Immune System':
                continue
            unit.damage += boost

    def _reset(self):
        self.groups = [self._copy_unit(u) for u in self.orig]

    def _count_units(self, fight):
        team_counts = {'Immune System': 0, 'Infection': 0}
        for u in self.groups:
            team_counts[u.team] += u.size
        return team_counts

    def _check_status(self, fight, verbose):
        if sum(fight.damage_done.values()) > 0:
            self.ndc = 0
        if sum(fight.damage_done.values()) == 0:
            self.ndc += 1
        if self.ndc > 1:
            return fight
        team_counts = self._count_units(fight)
        if team_counts['Immune System'] == 0:
            if verbose:
                print('Infection Wins')
            return team_counts, 'Infection'
        if team_counts['Infection'] == 0:
            if verbose:
                print('Immune System Wins')
            return team_counts, 'Immune System'

    def _search_helper(self, boost):
        result = self._run_war(boost, verbose=False)
        self._show_damage(boost)
        if isinstance(result, Fight):
            print('boost: {} -- stalemate'.format(boost))
            return False
        else:
            winner = result[1]
            count = result[0][winner]
            print('boost: {} -- winner: {}, count: {}'.format(boost, winner,
                                                              count))
            if winner == 'Immune System':
                return count
            else:
                return False

    def search(self):
        low = 0
        results = {}
        high = 1
        results[low] = self._search_helper(low)
        while True:
            results[high] = self._search_helper(high)
            if results[high] != False:
                break
            high *= 2
        best_result = results[high]
        while low < high:
            mid = (low + high) // 2
            if mid in results:
                result = results[mid]
            else:
                result = self._search_helper(mid)
            if result:
                high = mid
                if result < best_result:
                    best_result = result
            else:
                low = mid + 1
        return best_result

    def _show_damage(self, boost):
        for cur_u, orig_u in zip(self.groups, self.orig):
            if cur_u.team != 'Immune System':
                continue
            if cur_u.damage - orig_u.damage != boost:
                print('boost error, {}: {}'.format(cur_u, orig_u))

    def _run_war(self, boost=0, verbose=False):
        self._apply_boost(boost)
        f = Fight(self.groups)
        while True:
            f(verbose)
            check = self._check_status(f, verbose)
            if check:
                return check
        return f

    def __call__(self, boost=0, verbose=False):
        return self._run_war(boost, verbose)


def extract_weak(text, u):
    base = text.strip('() ')
    for entry in base.split('; '):
        if entry.startswith('immune'):
            grab = entry.lstrip('immune to ')
            for imm in grab.split(', '):
                u['immune'].add(imm)
        if entry.startswith('weak'):
            grab = entry.lstrip('weak to ')
            for weak in grab.split(', '):
                u['weak'].add(weak)
    return u


def parse_text(data):
    r = re.compile(r'^(?P<size>\d+) units each with (?P<hp>\d+) hit points '
                    '(?P<extra>.*)?with an attack that does (?P<damage>\d+) '
                    '(?P<dtype>.*) damage at initiative (?P<initiative>\d+)$')
    groups = []
    for line in data:
        if line.startswith('Immune'):
            team = 'Immune System'
            num = 0
        elif line.startswith('Infection'):
            team = 'Infection'
            num = 0
        result = r.search(line)
        if result is None:
            continue
        num += 1
        d = result.groupdict()
        updates = {'weak': set(), 'immune': set()}
        if d['extra'] != '':
            updates = extract_weak(d['extra'], updates)
        d.update(updates)
        del d['extra']
        d['team'] = team
        d['num'] = num
        groups.append(Unit(**d))
    return groups


def get_answer(data, part2=False, verbose=False):
    groups = parse_text(data)
    w = War(groups)
    if part2:
        winner = w.search()
    else:
        outcome = w(verbose=verbose)
        winner = outcome[0][outcome[1]]
    return winner


if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])
    sample = '''
Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4
    '''.split('\n')
    # print(get_answer(sample, part2=True, verbose=True))
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
