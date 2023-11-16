F = open("python/Advent of Code/2022/Day 3/input.txt", "r").readlines()


def points(line1: str):
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    line1 = line1.strip()

    for i in alphabet:
        if line1[:len(line1) // 2].count(i) > 0 and line1[len(line1) // 2:].count(i) > 0:
            return alphabet.index(i) + 1

    return 0


total = 0
for i in range(len(F)):
    total += points(F[i])

print(total)
