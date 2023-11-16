F: list[str] = list(map(str.strip, open(
    "python/Advent of Code/2022/Day 25/input.txt", "r").readlines()))


def convert_to_decimal(num: str) -> int:
    num = num[::-1]
    ret: int = 0
    for place, digit in enumerate(num):
        ret += {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}[digit] * 5 ** place
    return ret


def convert_to_bquniary(num: int) -> str:
    if num == 0:
        return "0"

    digits: list[str] = ["0", "1", "2", "=", "-"]
    ret: str = ""
    digit_index: int = 0
    remove: int = 0
    while num >= 5 ** (digit_index) - remove:
        ret = digits[(num + remove) // 5 ** digit_index % 5] + ret
        digit_index += 1
        remove = (5 ** digit_index - 1) // 2

    return ret


def main(inp: list[str]) -> str:
    ret: int = 0
    for number in inp:
        ret += convert_to_decimal(number)
    return convert_to_bquniary(ret)


print(main(F))
