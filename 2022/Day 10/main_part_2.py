F = open("python/Advent of Code/2022/Day 10/input.txt", "r")
F = F.readlines()

add_next = False
cycle_count = 0
line = 0
register = 1
total = 0


def cycle():
    global add_next, line, register, cycle_count, total
    if (cycle_count - 19) % 40 == 0:
        total += register * cycle_count
    if add_next:
        register += int(F[line][5:])
        add_next = False
        line += 1
    elif F[line].count("addx") == 1:
        add_next = True
    else:
        line += 1
    cycle_count += 1


def is_visible():
    return abs(cycle_count % 40 - register) < 2


ret = ""
while line < len(F):
    if is_visible():
        ret += "#"
    else:
        ret += "."
    cycle()
    if len(ret) >= 40:
        print(ret)
        ret = ""
