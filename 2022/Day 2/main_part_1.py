F = open("python/Advent of Code/2022/Day 2/input.txt", "r").readlines()

# A Y
# B Z
# C X

#   L D W
# R 3 1 2
# P 1 2 3
# S 2 3 1


def points(line):
    return {"A X": 4, "A Y": 8, "A Z": 3, "B X": 1, "B Y": 5, "B Z": 9, "C X": 7, "C Y": 2, "C Z": 6}[line.strip()]


total = 0
for i in F:
    total += points(i)

print(total)
