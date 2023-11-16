import math
F = open("python/Advent of Code/2022/Day 11/input.txt", "r")
F = F.readlines()

class IterMonkey(type):
    def __iter__(cls):
        return iter(cls._allMonkeys)


class Monkey(metaclass = IterMonkey):
    _allMonkeys = []
    def __init__(self, id: int, items: list[int], operation, test, test_true, test_false):
        self._allMonkeys.append(self)

        self.id = id
        self.items = items
        self.operation = operation
        self.test = test
        self.test_res = [test_true, test_false]
        self.inspected = 0

    
    def get_modulo(self):
        ret = 1
        for monkey in Monkey:
            ret *= monkey.test
        return ret

    def inspect_item(self):
        item = self.items.pop(0)
        item = self.operation(item)
#        item = math.floor(item / 3)
        item = item % self.get_modulo()
        item_tested = item % self.test
        monkey_id = self.test_res[min(item_tested, 1)]
        for monkey in Monkey:
            if monkey.id == monkey_id:
                monkey.get_item(item)
        self.inspected += 1
    
    def inspect_all(self):
        while len(self.items) != 0:
            self.inspect_item()

    def get_item(self, item):
        self.items.append(item)

    def print_items(self):
        ret = f"Monkey {self.id}: "
        for i in self.items:
            ret += f"{i}, "
        if len(self.items) > 0:
            ret = ret[:-2]
        print(ret)

def define_operation(oper):
    if oper.count("old") == 2:
        return lambda x: x * x
    elif oper.count("*") == 1:
        mult = int(oper[-2:])
        return lambda x: x * mult
    else:
        add = int(oper[-2:])
        return lambda x: x + add

allmonkeys = []
F[-1] += "\n"
for i in range((len(F) + 1) // 7):
    id = i
    items = []
    items_str = F[7 * i + 1][18:-1].split(", ")
    for j in items_str:
        items.append(int(j))
    operation = define_operation(F[7 * i + 2][19:-1])
    test = int(F[7 * i + 3][-3:-1])
    test_true = int(F[7 * i + 4][-3:-1])
    test_false = int(F[7 * i + 5][-3:-1])
    allmonkeys.append(Monkey(id, items, operation, test, test_true, test_false))

for i in range(10000):
    for monkey in Monkey:
        monkey.inspect_all()
    print(f"Round {i + 1}:")
    for monkey in Monkey:
        monkey.print_items()
    print()

best = [0, 0]
for monkey in Monkey:
    print(f"Monkey {monkey.id} inspected items {monkey.inspected} times")
    if min(best) < monkey.inspected:
        best[best.index(min(best))] = monkey.inspected


print(best[0] * best[1])
print(allmonkeys[0].get_modulo())






