F = open("python/Advent of Code/2022/Day 4/input.txt", "r").readlines()


def points(line: str):
    line = line.strip()
    line = line.split(",")

    elf1 = line[0].split("-")
    elf2 = line[1].split("-")

    elf1 = set(range(int(elf1[0]), int(elf1[1]) + 1))
    elf2 = set(range(int(elf2[0]), int(elf2[1]) + 1))

    return int(len(elf1.intersection(elf2)) == min(len(elf1), len(elf2)))


total = 0
for i in range(0, len(F)):
    total += points(F[i])

print(total)
