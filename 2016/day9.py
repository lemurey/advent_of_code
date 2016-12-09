with open('instructions_day9.txt', 'r') as f:
    instructions = f.read().strip()

def process_line(line):
    location = 0
    output = ''
    for i, char in enumerate(line):
        if location > i:
            continue
        if char == '(':
            searching = True
            command = ''
            addition = 0
            while searching:
                addition += 1
                next_char = line[i + addition]
                if next_char != ')':
                    command += next_char
                else:
                    searching = False
            distance, repeats  = (int(num) for num in command.split('x'))
            start = i + addition + 1
            to_repeat = line[start:start + distance]
            output += to_repeat * repeats
            location += distance + addition + 1
        else:
            output += char
            location += 1
    return output


def advanced_process_line(line):
    length = 0
    while '(' in line:
        start = line.find('(')
        length += start
        line = line[start + 1:]
        end = line.find(')')
        grab, repeats = (int(val) for val in line[:end].split('x'))
        line = line[end + 1:]
        length += advanced_process_line(line[:grab] * repeats)
        line = line[grab:]
    length += len(line)
    return length


def combine_instructions(instructions):
    return ''.join(instructions.split())


def get_results(instructions):
    joined = combine_instructions(instructions)
    print len(process_line(joined))
    return advanced_process_line(joined)

#### stolen from reddit
import re
def day9b(d):
    bracket = re.search(r'\((\d+)x(\d+)\)', d[0:])
    if not bracket:
        return len(d)
    pos = bracket.start(0)
    size = int(bracket.group(1))
    repeat = int(bracket.group(2))
    i = pos + len(bracket.group())
    return len(d[:pos]) + day9b(d[i:i+size]) * repeat + day9b(d[i+size:])


if __name__ == '__main__':
    # print get_results(instructions)
    print day9b(combine_instructions(instructions))
