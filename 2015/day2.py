def get_paper_and_ribbon(w, h, l):
    sides, perimeters = get_data(w, h, l)
    return sum(sides) + min(sides), min(perimeters) + w * h * l


def get_data(w, h, l):
    sides = []
    perimeters = []
    for dim1, dim2 in zip((w, h, l), (l, w, h)):
        area = dim1 * dim2
        perimeter = 2 * dim1 + 2 * dim2
        sides.extend((area, area))
        perimeters.append(perimeter)
    return sides, perimeters


def get_results(instructions):
    paper_needed = 0
    ribbon_neeeded = 0
    for line in instructions.split('\n'):
        w, h, l = map(int, line.split('x'))
        paper, ribbon = get_paper_and_ribbon(w, h, l)
        paper_needed += paper
        ribbon_neeeded += ribbon
    print paper_needed
    return ribbon_neeeded


if __name__ == '__main__':
    with open('instructions_day2.txt', 'r') as f:
        instructions = f.read().strip()
    print get_results(instructions)
