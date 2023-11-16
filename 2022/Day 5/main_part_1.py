F = open("python/Advent of Code/2022/Day 5/input.txt", "r")

F = F.readlines()


def get_stack(lines: list[str]):
    lines_new = []

    i = 0
    while lines[i] != "\n":
        lines_new.append(lines[i])
        i += 1

    stacks = int(lines_new[-1][-3])
    ret = []

    stack = []
    for i in range(stacks):
        for j in range(len(lines_new) - 1):
            if lines_new[j][1 + 4 * i] != " ":
                stack.append(lines_new[j][1 + 4 * i])
        ret.append(stack)
        stack = []

    return (ret, lines[stacks + 1:])


def do_move(stack: list[list[str]], action: str):
    action = action.split("move ")
    action = action[1].split(" from ")

    moves = int(action[0])
    action = action[1].split(" to ")

    start = int(action[0]) - 1
    end = int(action[1]) - 1

    temp_moves = []
    for _ in range(moves):
        temp_moves.append(stack[start].pop(0))
    for _ in range(moves):
        stack[end].insert(0, temp_moves.pop(0))
#    print_stack(stack)
    return stack


def print_stack(stack: list[list[str]]):
    max_len = 0
    for i in stack:
        max_len = max(max_len, len(i))

    for i in range(-1 * max_len, 1):
        ret = ""
        for j in stack:
            try:
                ret += f"[{j[i - 1][0]}] "
            except:
                ret += "    "
        print(ret)

    print(" ", end="")
    for i in range(1, len(stack) + 1):
        print(f"{i}   ", end="")
    print()


F = get_stack(F)

stack = F[0]
actions = F[1]

for action in actions:
    #    print(action)
    stack = do_move(stack, action)

for column in stack:
    print(column[0], end="")
