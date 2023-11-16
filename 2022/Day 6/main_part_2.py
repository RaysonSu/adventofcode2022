F = open("python/Advent of Code/2022/Day 6/input.txt", "r").readlines()


def check_duplicate(string: str):
    cur_checked = ""
    for i in string:
        if cur_checked.count(i) == 0:
            cur_checked += i
        else:
            return True
    return False


index = 0
while check_duplicate(F[0][index:index + 14]):
    index += 1

print(index + 14)
