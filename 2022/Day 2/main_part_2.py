F = open("python/Advent of Code/2022/Day 2/input.txt", "r").readlines()

# A Y
# B Z
# C X

#   L D W
# R 3 1 2
# P 1 2 3
# S 2 3 1


def points(line):
    ret = 0
    ret += ["X", "Y", "Z"].index(line[2]) * 3
    ret += (ord(line[2]) + ord(line[0]) - ord("A") - ord("X") - 1) % 3 + 1
    return ret


total = 0
for i in F:
    total += points(i)

print(total)
