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
    repeats = 0
    counted = []
    for block in inp:
        edges = generate_edges(block)
        for edge in edges: 
            if edge in counted: repeats += 1
        counted.append(block)

    return len(inp) * 6 - 2 * repeats

print(main(parse_inp(F)))
