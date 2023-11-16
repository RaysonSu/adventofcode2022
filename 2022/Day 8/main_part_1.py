F = open("python/Advent of Code/2022/Day 8/input.txt", "r").readlines()


def is_visible(grid: list[str], pos: tuple[int, int]):
    value = int(grid[pos[1]][pos[0]])
    for i in range(4):
        ret = True
        j = pos[1 - i // 2]
        while 0 < j and j < (len(grid) - 1):
            j += (-1) ** i
            if i // 2 == 0:
                ret = ret and int(grid[j][pos[0]]) < value
            else:
                ret = ret and int(grid[pos[1]][j]) < value
        if ret:
            return ret
    return False


def scenic_score(grid: list[str], pos: tuple[int, int]):
    ret = 1
    value = int(grid[pos[1]][pos[0]])
    for i in range(4):
        not_blocked = True
        trees_seen = 0
        j = pos[1 - i // 2]
        while 0 < j and j < (len(grid) - 1) and not_blocked:
            trees_seen += 1
            j += (-1) ** i
            if i // 2 == 0:
                not_blocked = not_blocked and int(grid[j][pos[0]]) < value
            else:
                not_blocked = not_blocked and int(grid[pos[1]][j]) < value
        ret *= max(trees_seen, 1)
    return ret


ret = 0
for i in range(len(F)):
    for j in range(len(F)):
        ret += int(is_visible(F, (i, j)))

print(ret)
