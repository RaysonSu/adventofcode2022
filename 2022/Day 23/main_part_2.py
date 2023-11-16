import time
import threading

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


def generate_proposals(elves, roun):
    proposal_slots = {}
    moved = 0
    for index, elf in enumerate(elves):
        value = proposal_single(elves, elf, roun)
        try:
            if proposal_slots[value] == -1:
                proposal_slots[value] = index
                moved += 1
            elif proposal_slots[value] != -2:
                proposal_slots[value] = -2
                moved -= 1
        except:
            proposal_slots[value] = index
            moved += 1

    return proposal_slots, moved


def handle_proposals(elves, proposals):
    for proposal in proposals.items():
        if proposal[1] >= 0:
            elves[proposal[1]] = proposal[0]

    return elves


def main(inp):
    start_time = time.time()
    prev_inp = []
    roun = 0
    while prev_inp != inp:
        prev_inp = inp.copy()
        proposals = generate_proposals(inp, roun)
        inp = handle_proposals(inp, proposals[0])
        roun += 1
        print(
            f"Round: {roun}, Elves moved: {proposals[1]}, (t = {time.time() - start_time}s)")

    return roun


print(main(parse_inp(F)))
