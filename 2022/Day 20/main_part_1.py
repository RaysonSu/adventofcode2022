F = open("python/Advent of Code/2022/Day 20/input.txt", "r")
F = list(map(str.strip, F.readlines()))

def parse_inp(F):
    return list(enumerate(map(int, F)))

def main(inp):
    order = inp.copy()
    
    for char in order:
        index = inp.index(char)
        char = inp.pop(index)
        index = (index + char[1]) % len(inp)
        if index == 0:
            inp.append(char)
        else:
            inp.insert(index, char)

    index = inp.index(([index for index, value in inp if value == 0][0], 0))

    return inp[(index + 1000) % len(order)][1] + inp[(index + 2000) % len(order)][1] + inp[(index + 3000) % len(order)][1]

print(main(parse_inp(F)))
