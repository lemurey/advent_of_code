from aoc_utilities import get_instructions
from pathlib import Path
from functools import reduce


def parse_data(data):
    allergens = {}
    all_ingredients = {}
    foods = []

    for row in data:
        if '(' in row:
            base, ca = row.split('(')
            current_allergens = [x.strip(',') for x in ca.strip(')').split()[1:]]
        else:
            base = row
            current_allergens = ''

        ingredients = set(base.strip().split())

        foods.append(ingredients)

        for ingredient in ingredients:
            if ingredient not in all_ingredients:
                all_ingredients[ingredient] = set()
            all_ingredients[ingredient] = all_ingredients[ingredient].union(set(current_allergens))

        for allergen in current_allergens:
            if allergen not in allergens:
                allergens[allergen] = []
            allergens[allergen].append(ingredients)

    return allergens, all_ingredients, foods


def categorize_allergens(ingredients, allergens):
    output = {}
    for k, v in ingredients.items():
        allowed = set()
        for possible_allergen in v:
            for subset in allergens[possible_allergen]:
                if k not in subset:
                    break
            else:
                allowed.add(possible_allergen)
        output[k] = allowed

    return output


def extract_allergens(categorized, allergens):
    found = {}
    while len(found) < len(allergens):
        for ingredient, possibles in categorized.items():
            if len(possibles) == 1:
                allergen = list(possibles)[0]
                found[allergen] = ingredient

        nc = {}
        for ingredient, possibles in categorized.items():
            new_possibilites = possibles.difference(found)
            nc[ingredient] = new_possibilites

        categorized = nc
    return found


def run_part2(categorized, allergens):
    found = extract_allergens(categorized, allergens)
    return ','.join([found[k] for k in sorted(found)])


def get_answer(data, part2=False):
    allergens, ingredients, foods = parse_data(data)

    categorized = categorize_allergens(ingredients, allergens)

    ## part1
    count = 0
    for item in foods:
        for ingredient, possibles in categorized.items():
            if len(possibles) == 0 and (ingredient in item):
                count += 1

    print(count)

    cannonical_dangerous_list = run_part2(categorized, allergens)

    return cannonical_dangerous_list


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)

#     inputs = '''mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
# trh fvjkl sbzzf mxmxvkd (contains dairy)
# sqjhc fvjkl (contains soy)
# sqjhc mxmxvkd sbzzf (contains fish)'''.split('\n')

    print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))
