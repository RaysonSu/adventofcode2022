F = open("python/Advent of Code/2022/Day 23/input.txt", "r")
F = list(map(str.strip, F.readlines()))


def parse_inp(F):
    return [(row, col) for col, line in enumerate(F) for row, val in enumerate(line) if val == "#"]


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def rotate(l, n):
    n %= len(l)
    return l[n:] + l[:n]


def proposal_single(elves, elf, roun):
    directions = [[-1, -1], [0, -1], [1, -1],
                  [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0]]
    new_elves = [add(elf, direction) in elves for direction in directions]

    if True not in new_elves:
        return elf

    for index, locations in rotate(list(enumerate([[0, 1, 2], [4, 5, 6], [6, 7, 0], [2, 3, 4]])), roun):
        if True not in [new_elves[location] for location in locations]:
            return add(elf, directions[[1, 5, 7, 3][index]])

    return elf


def proposals(elves, roun):
    proposal_slots = {}
    for index, elf in enumerate(elves):
        value = proposal_single(elves, elf, roun)
        try:
            if proposal_slots[value] == -1:
                proposal_slots[value] = index
            else:
                proposal_slots[value] = -2
        except:
            proposal_slots[value] = index

    return proposal_slots


def handle_proposals(elves, proposals):
    for proposal in proposals.items():
        if proposal[1] >= 0:
            elves[proposal[1]] = proposal[0]

    return elves


def main(inp):
    rounds = 10
    for roun in range(rounds):
        inp = handle_proposals(inp, proposals(inp, roun))

    x_values = []
    y_values = []
    for elf in inp:
        x_values.append(elf[0])
        y_values.append(elf[1])

    return (max(x_values) - min(x_values) + 1) * (max(y_values) - min(y_values) + 1) - len(inp)


print(main(parse_inp(F)))
