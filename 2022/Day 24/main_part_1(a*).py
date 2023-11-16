from collections import defaultdict
import heapq

F = open("python/Advent of Code/2022/Day 24/input.txt", "r")
F = list(map(str.strip, F.readlines()))


class State:
    def __init__(self, location, time, blizzards, bounding_box, h):
        self.location = location
        self.time = time
        self.blizzards = blizzards
        self.bounding_box = bounding_box
        self.h = h

    def __str__(self):
        return f"{self.location}"

    def __hash__(self):
        return hash((self.location, self.time))

    def __eq__(self, other):
        return self.location == other.location

    def __lt__(self, other):
        return (self.time + self.h(self)) < (other.time + other.h(other))

    def is_valid(self):
        return self.location[0] >= 0 and self.location[0] < self.bounding_box[0] and self.location[1] >= 0 and self.location[1] < self.bounding_box[1]

    def move(self, direction):
        return State((self.location[0] + direction[0], self.location[1] + direction[1]), self.time + 1, self.blizzards, self.bounding_box, self.h)

    def neighbors(self):
        ret = []
        for direction in ([0, 1], [1, 0], [0, -1], [-1, 0], [0, 0]):
            new_state = self.move(direction)
            append = True
            if (new_state.location[0] == self.bounding_box[0] - 1 and new_state.location[1] == self.bounding_box[1]) or self.location == (0, -1):
                ret.append((1, new_state))
                continue

            for blizzard in [("v", [0, -1]), (">", [-1, 0]), ("<", [1, 0]), ("^", [0, 1])]:
                blizzard_location = (blizzard[0],
                                     (new_state.location[0] + new_state.time *
                                      blizzard[1][0]) % self.bounding_box[0],
                                     (new_state.location[1] + new_state.time * blizzard[1][1]) % self.bounding_box[1])
                append = append and blizzard_location not in self.blizzards
            if append and new_state.is_valid():
                ret.append((1, new_state))

        return ret


# very much based on the pesudocode on the wikipedia article of a* pathfinding algorithm

def a_star(start, goal, h):
    def reconstruct_path(came_from, current):
        total_path = [current]
        while current in came_from.keys():
            current = came_from[current]
            total_path.insert(0, current)

        return total_path

    open_set = [start]
    heapq.heapify(open_set)

    came_from = {}

    g_score = defaultdict(lambda: 10 ** 200)
    g_score[start] = 0

    f_score = defaultdict(lambda: 10 ** 200)
    f_score[start] = h(start)

    i = 0

    while open_set != []:
        i += 1
        current = heapq.heappop(open_set)
        if i % 1000 == 0:
            print(
                f"Checking node #{i} {str(current)}, t={current.time}, {len(open_set)} nodes left")
        if current == goal:
            return reconstruct_path(came_from, current)

        for distance, neighbor in current.neighbors():
            # print(
            #     f"New neighbor: {str(neighbor)}, t={neighbor.time}")
            tentative_g_score = g_score[current] + distance
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + h(neighbor)
                if neighbor not in open_set:
                    open_set.append(neighbor)

    raise ValueError("No path found to goal state")


def parse_inp(F):
    blizzards = []
    for i in range(1, len(F) - 1):
        for j in range(1, len(F[0]) - 1):
            if F[i][j] == ".":
                continue

            blizzards.append((F[i][j], j - 1, i - 1))

    return blizzards, (len(F[0]) - 2, len(F) - 2)


def main(inp):
    def hueristic(x): return 0
    initial_state = State((0, -1), 0, inp[0], inp[1], hueristic)

    goal_state = State((inp[1][0] - 1, inp[1][1]),
                       0, inp[0], inp[1], hueristic)

    return a_star(initial_state, goal_state, hueristic)


m = main(parse_inp(F))
for i, v in enumerate(m):
    print(f"{i} {str(v)}")
print(len(m) - 1)
