from time import sleep
F = open("python/Advent of Code/2022/Day 14/input.txt", "r")
F = F.readlines()


def parse_input(inp: list[str]) -> list[list[list[str]]]:
    ret = []
    for i in inp:
        i = i.replace(",", " ")
        i = i.replace(" -> ", " ")
        i = i.split()

        ret2 = []
        for j in range(len(i) // 2):
            ret2.append([int(i[2 * j]), int(i[2 * j + 1])])

        ret.append(ret2)
    return ret


def floor_height(grid: list[list[str]]):
    for index in range(len(grid)):
        if grid[-1 * index - 1].count("#") > 0:
            return len(grid) - index + 1


def add_line(grid: list[list[str]], line: list[list[int]]) -> list[list[int]]:
    for i in range(min(line[0][0], line[1][0]), max(line[0][0], line[1][0]) + 1):
        for j in range(min(line[0][1], line[1][1]), max(line[0][1], line[1][1]) + 1):
            grid[j][i] = "#"
    return grid


def add_lines(grid: list[list[str]], lines: list[list[int]]) -> list[list[str]]:
    for i in range(len(lines) - 1):
        grid = add_line(grid, [lines[i], lines[i + 1]])
    return grid


def add_sand(grid: list[list[str]]) -> list[list[str]]:
    x = 500
    y = 0
    while y < 190:
        if grid[y + 1][x] == ".":
            y += 1
        elif grid[y + 1][x - 1] == ".":
            y += 1
            x -= 1
        elif grid[y + 1][x + 1] == ".":
            y += 1
            x += 1
        else:
            grid[y][x] = "o"
#            print_grid(grid)
#            print(x, y)
            return grid
    return grid


def make_grid(x: int, y: int) -> list[list[int]]:
    ret = []
    for _ in range(y):
        ret.append(["."] * x)
    return ret


def print_grid(grid: list[list[str]]) -> None:
    for i in grid:
        p = ""
        for j in i:
            p += j
        print(p)


grid = make_grid(1000, 200)
all_lines = parse_input(F)
for lines in all_lines:
    grid = add_lines(grid, lines)

floor = floor_height(grid)
grid = add_line(grid, [[0, floor], [999, floor]])


i = 0
while "o" not in grid[floor - 1]:
    grid = add_sand(grid)
    i += 1

print(i - 1)
