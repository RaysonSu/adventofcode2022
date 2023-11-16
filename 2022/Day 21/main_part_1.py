F = open("python/Advent of Code/2022/Day 21/input.txt", "r")
F = list(map(str.strip, F.readlines()))


def parse_inp(F):
    ret = {}
    for monkey in F:
        monkey = monkey.split(":")
        try:
            ret[monkey[0]] = int(monkey[1])
        except:
            ret[monkey[0]] = [x for x in monkey[1].split(" ") if x != ""]
    return ret

def main(inp):
    monkeys = inp

    def resolve_monkey(monkey):
        data = monkeys[monkey]
        if isinstance(data, int):
            return data
        
        operator = data[1]
        new = 0
        if operator == "+":
            new = resolve_monkey(data[0]) + resolve_monkey(data[2])
        if operator == "-":
            new = resolve_monkey(data[0]) - resolve_monkey(data[2])
        if operator == "*":
            new = resolve_monkey(data[0]) * resolve_monkey(data[2])
        if operator == "/":
            new = resolve_monkey(data[0]) // resolve_monkey(data[2])
            if resolve_monkey(data[0]) % resolve_monkey(data[2]) != 0:
                raise ValueError("Well crap")
        monkeys[monkey] = new
        return new

    print(monkeys)

    return resolve_monkey("root")

print(main(parse_inp(F)))
