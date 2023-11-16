F = open("python/Advent of Code/2022/Day 3/input.txt", "r").readlines()


def points(line1: str, line2: str, line3: str):
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    line1 = line1.strip()
    line2 = line2.strip()
    line3 = line3.strip()

    for i in alphabet:
        if line1.count(i) > 0 and line2.count(i) > 0 and line3.count(i) > 0:
            return alphabet.index(i) + 1

    return 0


total = 0
for i in range(0, len(F), 3):
    total += points(F[i], F[i + 1], F[i + 2])

print(total)
