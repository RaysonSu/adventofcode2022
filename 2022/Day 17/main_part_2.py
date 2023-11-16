F = open("python/Advent of Code/2022/Day 17/input.txt", "r")
F = F.readlines()

DIRECTION = {"left": -1, "right": 1, "down": -8}
DIRECTION_F = {"<": -1, ">": 1, "v": -8}

BLOCK_DATA = [
    ([2, 3, 4, 5], 1),
    ([3, 10, 11, 12, 19], 3),
    ([2, 3, 4, 12, 20], 3),
    ([2, 10, 18, 26], 4),
    ([2, 3, 10, 11], 2)
]

def parse_inp(F):
    return F[0]

def add_rows(state, rows=3):
    return state + ".......\n" * rows

def move_block(state, block_state, direction):
    valid = 1
    for block in block_state:
        test = block + direction
        valid = valid * int(state[test] == "." and test > 0) 
    
    for block in range(len(block_state)):
        block_state[block] += direction * valid
    
    return (bool(valid), block_state)

def prune(state: str):
    state = state.replace(".......\n", "")
    return state

def next_block(state):
    return len(state) + 24

def str_assign(string, index, item):
    return string[:index] + item + string[index+1:]

def commit(state, blocks, char="#"):
    for block in blocks:
        state = str_assign(state, block, char)
    return state

def prints(state):
    state = state.split()
    for i in range(len(state) - 1, -1, -1):
        print("|" + state[i] + "|")
    print("+-------+")

def anydup(thelist):
    seen = set()
    for x in thelist:
        if x in seen: return True, x
        seen.add(x)
    return False, None

def main(inp, block_count):
    state = "\n"                                                                                                                         
    blocks = 0
    jet = 0
    seen = []
    heights = {}
    while True:
        state = prune(state)
        base_index = next_block(state)
        block_data, block_height = BLOCK_DATA[blocks % 5]
        block_data = [i + base_index for i in block_data]
        state = add_rows(state, block_height + 3)

        go = True
        while go:
            _, block_data = move_block(state, block_data, DIRECTION_F[inp[jet % len(inp)]])
            go, block_data = move_block(state, block_data, -8)
            jet += 1
        state = commit(state, block_data)
        state = prune(state)
        data = (state[-8 * 6:], jet % len(inp), blocks % 5)
        seen.append(hash(data))
        if anydup(seen)[0]:
            break
        heights[hash(data)] = state.count("\n") - 1
        blocks += 1
    duped = anydup(seen)[1]
    seen = seen[:-1]
    state = prune(state)

    start_index = seen.index(duped)
    base_height = heights[duped]
    period = len(seen) - seen.index(duped)
    gain_value = state.count(chr(10)) - 1 - heights[duped]

    heights_pre = [heights[index] for index in seen[:seen.index(duped)]]
    heights_period = [heights[index] - base_height for index in seen[seen.index(duped):]]

    if block_count < len(heights_pre):
        return base_height[block_count]

    base_gain = heights_pre[-1]
    periods = (block_count - start_index - 1) // period
    extra = (block_count - start_index - 1) % period

    return base_gain + gain_value * periods + heights_period[extra] + 3

print(main(parse_inp(F), 10 ** 12))