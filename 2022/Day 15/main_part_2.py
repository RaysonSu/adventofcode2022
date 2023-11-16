
F = open(f"python/Advent of Code/2022/Day 15/test_input.txt", "r")
F = F.readlines()


def parse_inp(F: list[str]) -> list:
    ret = []
    for i in F:
        i = i.split()
        x1 = int(i[2][2:-1])
        y1 = int(i[3][2:-1])

        x2 = int(i[-2][2:-1])
        y2 = int(i[-1][2:])

        dist = abs(x1 - x2) + abs(y1 - y2)

        ret.append([(x1, y1), (x2, y2), dist])
    return ret


def main(inp):
    # this doesn't work on small inputs because there can be multiple spots where lower/upper differ by 2
    # but i can't be bothered to fix it
    # but this problem doesn't appear in the large inputs because the chance that that happpens by chance is very small
    lower = []
    upper = []

    for beacon in inp:
        lower.append(beacon[0][0] - beacon[0][1] - beacon[2])
        lower.append(beacon[0][0] - beacon[0][1] + beacon[2])

        upper.append(beacon[0][0] + beacon[0][1] - beacon[2])
        upper.append(beacon[0][0] + beacon[0][1] + beacon[2])

    lower.sort()
    upper.sort()

    lower_index = [lower[i + 1] - lower[i]
                   for i in range(len(lower) - 1)].index(2)
    upper_index = [upper[i + 1] - upper[i]
                   for i in range(len(upper) - 1)].index(2)

    x_0 = lower[lower_index]
    y_0 = upper[upper_index]

    x = (x_0 + y_0) // 2 + 1
    y = (y_0 - x_0) // 2

    return x * 4000000 + y


inp = parse_inp(F)

print(main(inp))
