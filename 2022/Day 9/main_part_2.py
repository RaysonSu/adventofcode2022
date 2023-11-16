F = open("python/Advent of Code/2022/Day 9/input.txt", "r")
F = F.readlines()

knots = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0],
         [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
visited = {(0, 0)}
shift = [0, 0]


def parse(lines):
    ret = ""
    for i in lines:
        ret += i[0] * int(i[1:])
    return ret


def move(direction):
    direction = ["R", "L", "U", "D"].index(direction)
    # head logic
    knots[0][0] += (-1) ** direction * (1 - direction // 2)
    knots[0][1] += (-1) ** direction * (direction // 2)
    # tail logic
    for i in range(9):
        x_diff = knots[i][0] - knots[i + 1][0]
        y_diff = knots[i][1] - knots[i + 1][1]
        if abs(x_diff) > 1 and not abs(y_diff) > 0:
            knots[i + 1][0] += x_diff // 2

        if abs(y_diff) > 1 and not abs(x_diff) > 0:
            knots[i + 1][1] += y_diff // 2

        if (abs(x_diff) > 1 or abs(y_diff) > 1) and abs(x_diff) > 0 and abs(y_diff) > 0:
            knots[i + 1][0] += x_diff // abs(x_diff)
            knots[i + 1][1] += y_diff // abs(y_diff)

    visited.add((knots[-1][0], knots[-1][1]))


F = parse(F)
for i in F:
    move(i)

print(len(visited))
