F = open("python/Advent of Code/2022/Day 21/input.txt", "r")
F = list(map(str.strip, F.readlines()))

class linpoly:
    def __init__(self, x, c):
        self.x = float(x)
        self.c = float(c)
    
    def __str__(self):
        return f"{self.x}x + {self.c}"
    
    def add(self, y):
        x = self.x + y.x
        c = self.c + y.c
        
        return linpoly(x, c)
    
    def sub(self, y):
        x = self.x - y.x
        c = self.c - y.c
        
        return linpoly(x, c)
    
    def mul(self, y):
        if y.x == 0:
            x = self.x * y.c
            c = self.c * y.c
            
            return linpoly(x, c)
        
        if self.x == 0:
            x = self.c * y.x
            c = self.c * y.c
            
            return linpoly(x, c)
        
        raise ValueError("Uh oh non-linear poly!")
    
    def div(self, y):
        if y.x == 0:
            x = self.x / y.c
            c = self.c / y.c
            return linpoly(x, c)
        
        raise ValueError("Uh oh non-linear poly")

def parse_inp(F):
    ret = {}
    for monkey in F:
        monkey = monkey.split(":")
        if monkey[0] == "humn":
            ret[monkey[0]] = linpoly(1, 0)
            continue

        try:
            ret[monkey[0]] = linpoly(0, monkey[1])
        except:
            if monkey[0] == "root":
                monkey[1] = monkey[1].strip().split(" ")
                ret[monkey[0]] = [monkey[1][0], "-", monkey[1][2]]
            else:
                ret[monkey[0]] = [x for x in monkey[1].split(" ") if x != ""]
    return ret

def main(inp):
    monkeys = inp

    def resolve_monkey(monkey):
        data = monkeys[monkey]

        if isinstance(data, linpoly):
            return data

        operator = data[1]
        new = 0

        if monkey == "root":
            pass

        if operator == "+":
            new = resolve_monkey(data[0]).add(resolve_monkey(data[2]))
        if operator == "-":
            new = resolve_monkey(data[0]).sub(resolve_monkey(data[2]))
        if operator == "*":
            new = resolve_monkey(data[0]).mul(resolve_monkey(data[2]))
        if operator == "/":
            new = resolve_monkey(data[0]).div(resolve_monkey(data[2]))
        monkeys[monkey] = new

        return new

    r = resolve_monkey("root")

    return int(-r.c // r.x)

print(main(parse_inp(F)))

