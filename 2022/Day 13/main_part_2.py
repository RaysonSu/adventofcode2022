from functools import cmp_to_key

F = open("python/Advent of Code/2022/Day 13/input.txt", "r")
F = F.readlines()


def compare(left: list | int, right: list | int) -> int:
    left_type = [list, int].index(type(left))
    right_type = [list, int].index(type(right))

    if left_type == 1 and right_type == 1:
        if left < right:
            return 1
        elif left == right:
            return 0
        else:
            return -1
    elif left_type != right_type:
        if left_type == 1:
            left = [left]
        else:
            right = [right]
        return compare(left, right)
    else:
        for i in range(min(len(left), len(right))):
            comp = compare(left[i], right[i])
            if comp != 0:
                return comp
        if len(left) < len(right):
            return 1
        elif len(left) == len(right):
            return 0
        else:
            return -1

    print("THIS SHOULD NEVER BE REACHED")


def parse_input(inp: list[str]) -> list[list]:
    ret = []
    for i in range((len(inp) + 1) // 3):
        left = inp[3 * i]
        right = inp[3 * i + 1]

        left = eval(left)
        right = eval(right)

        ret.append(left)
        ret.append(right)

    return ret


inp = parse_input(F)
inp.append([[2]])
inp.append([[6]])

inp.sort(key=cmp_to_key(compare), reverse=True)

print((inp.index([[2]]) + 1) * (inp.index([[6]]) + 1))
