F = open("python/Advent of Code/2022/Day 1/input.txt", "r")
top = 0
total = 0

F = F.readlines()
for i in F:
    if i == "\n":
        if top < total:
            top = total
        total = 0
    else:
        total += int(i)

print(top)
