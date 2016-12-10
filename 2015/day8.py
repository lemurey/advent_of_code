import re


def get_results(instructions):
    total_chars = 0
    memory_total = 0
    encoded_total = 0
    parser = re.compile(r'\\x\w\w|\\\\|\\"')
    qreplacer = re.compile(r'"')
    sreplacer = re.compile(r'\\')
    for line in instructions.split():
        total_chars += len(line)
        parsed = parser.sub(' ',line)
        memory_total += len(parsed) - 2 
        sreplaced = sreplacer.sub(r'\\\\', line)
        breplaced = qreplacer.sub('\\"', sreplaced)
        encoded_total += len(breplaced) + 2
    print total_chars - memory_total
    return encoded_total - total_chars



if __name__ == '__main__':
    with open('instructions_day8.txt', 'r') as f:
        instructions = f.read().strip()
    print get_results(instructions)