F = open("python/Advent of Code/2022/Day 12/input.txt", "r")
F = F.readlines()


def get_graph(F):
    add_y = len(F[0].strip())

    fmap = ""
    for i in F:
        fmap += i.strip()

    fmap = fmap.replace("S", "a")
    fmap = fmap.replace("E", "z")

    graph = []
    for i in range(len(fmap)):
        connections = []
        try:
            if ord(fmap[i]) + 1 >= ord(fmap[i + add_y]):
                connections.append(i + add_y)
        except:
            pass

        try:
            if ord(fmap[i]) + 1 >= ord(fmap[i - add_y]) and i > add_y:
                connections.append(i - add_y)
        except:
            pass

        try:
            if (i + 1) % add_y != 0:
                if ord(fmap[i]) + 1 >= ord(fmap[i + 1]):
                    connections.append(i + 1)
        except:
            pass

        try:
            if i % add_y != 0:
                if ord(fmap[i]) + 1 >= ord(fmap[i - 1]):
                    connections.append(i - 1)
        except:
            pass

        graph.append(connections)

    return graph


fmap = ""
for i in F:
    fmap += i.strip()

best = 10000000
new_S = 0
cont = True
rounds = 0


graph = get_graph(F)

start = fmap.index("S")
end = fmap.index("E")

checked = [start]
round_checked = [[start]]

while checked.count(end) == 0 and len(round_checked[-1]) > 0:
    found = []
    for i in round_checked[-1]:
        for j in graph[i]:
            if checked.count(j) == 0:
                found.append(j)

    found = list(set(found))

    for i in found:
        checked.append(i)

    round_checked.append(found)
if len(round_checked[-1]) > 0:
    best = min(best, len(round_checked) - 1)

print(best)
