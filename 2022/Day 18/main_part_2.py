F = open("python/Advent of Code/2022/Day 18/input.txt", "r")
F = list(map(str.strip, F.readlines()))

def parse_inp(F):
    ret = []
    for i in F:
        i = i.split(",")
        i = list(map(int, i))
        ret.append(i)
    return ret

def generate_edges(vec3):
    x, y, z = tuple(vec3)
    return [
        [x + 1, y, z],
        [x - 1, y, z],
        [x, y + 1, z],
        [x, y - 1, z],
        [x, y, z + 1],
        [x, y, z - 1],
    ]

def main(inp):
    maximum = max([item for sublist in inp for item in sublist]) + 1
    minimum = min([item for sublist in inp for item in sublist]) - 1

    ret = 0
    base_list = []
    to_generate = [[0, 0, 0]]
    while to_generate != []:
        working = to_generate.pop(0)
        if working in base_list:
            continue

        for edge in generate_edges(working):
            if min(edge) < minimum or max(edge) > maximum:
                continue
            if edge in inp:
                ret += 1
                continue
            if edge in base_list:
                continue

            to_generate.append(edge)
        
        base_list.append(working)
    return ret

print(main(parse_inp(F)))