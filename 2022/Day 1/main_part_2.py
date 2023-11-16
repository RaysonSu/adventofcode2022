F = open("python/Advent of Code/2022/Day 1/input.txt", "r")
top_3 = [0, 0, 0]
total = 0

F = F.readlines()
for i in F:
    if i == "\n":
        if min(top_3) < total:
            top_3.remove(min(top_3))
            top_3.append(total)
        total = 0
    else:
        total += int(i)

print(sum(top_3))
