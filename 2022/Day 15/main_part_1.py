
F = open(f"python/Advent of Code/2022/Day 15/input.txt", "r")
F = F.readlines()


class Ranges:
    def __init__(self, *args):
        self.ranges = []
        for i in args:
            self.ranges.append(i)

        self.fix_everything()

    def __str__(self):
        return str(self.ranges)

    def clean_up(self):
        succeded = True
        while succeded:
            succeded = self.one_step_clean_up()

    def one_step_clean_up(self):
        for i in range(len(self.ranges)):
            for j in range(i):
                new = self.combine(self.ranges[j], self.ranges[i])
                if len(new) == 1:
                    self.ranges.pop(i)
                    self.ranges.pop(j)
                    self.ranges.append(new[0])
                    return True
        return False

    def rem(self):
        new = []
        for i in self.ranges:
            if i[1] >= i[0]:
                new.append(i)
        self.ranges = new

    def combine(self, a, b):
        if a[0] < b[0]:
            if a[1] < b[0]:
                return [a, b]
            elif b[1] <= a[1]:
                return [a]
            else:
                return [(a[0], b[1])]
        elif a[0] == b[0]:
            return [(a[0], max(a[1], b[1]))]
        else:
            return self.combine(b, a)

    def sort(self):
        from functools import cmp_to_key

        def compare(left, right):
            if right[1] <= left[0]:
                return 1
            else:
                return -1

        self.ranges.sort(key=cmp_to_key(compare))

    def fix_everything(self):
        self.rem()
        self.clean_up()
        self.sort()

    def length(self) -> int:
        ret = 0
        for i in self.ranges:
            ret += i[1] - i[0] + 1
        return ret

    def add(self, *args):
        for i in args:
            self.ranges.append(i)

        self.fix_everything()


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


def calc_row(beacons: list, row: int):
    row_beacons = []
    row_F = Ranges()
    for i in beacons:
        row_dist = i[2] - abs(row - i[0][1])
        new = (i[0][0] - row_dist, i[0][0] + row_dist)
        if row_dist >= 0:
            row_F.add(new)
        else:
            new = "N/A"
        if i[1][1] == row:
            row_beacons.append(i[1][0])
        if False:
            if P2:
                x = i[0][0]
                y = i[0][1]
                d = i[2]
                print(
                    f"polygon(({x}, {y} + min({d}, t)), ({x} + min({d}, t), {y}), ({x}, {y} - min({d}, t)), ({x} - min({d}, t), {y}))")
            else:
                print(f"Processing sensor {i[0]}")
                if new != "N/A":
                    print(f"Detected Beacon: {i[1]}")
                    print(f"Possible # of slots: {2 * row_dist + 1}")
                    print(f"impossible slots: {new}")
                    print(f"New empty Beacon row {str(row_F)}")
                    print(f"Slots: {row_F.length()}")
                else:
                    print("Not important, skipped")
                print()

#    print(set(row_beacons))
    return row_F.length() - len(set(row_beacons))


inp = parse_inp(F)

print(calc_row(inp, 2906101))

# to do implement part 2
