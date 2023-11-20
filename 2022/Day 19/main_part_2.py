import math
import multiprocessing
import time


class State:
    def __init__(self, bots_built=[1, 0, 0, 0], resources=[0, 0, 0, 0], time=32, blueprint=[], cheap=None):
        self.bots_built = bots_built
        self.resources = resources
        self.time = time
        self.blueprint = blueprint
        self.cheap = cheap

    def __hash__(self):
        return hash(tuple(self.bots_built, self.resources))

    def get_actions(self):
        ret = [bot for bot in range(4) if self.bots_built[bot] < self.cheap[bot] and (
            self.get_build_time(bot) + 1) <= self.time]

        try:
            m_ret = max(ret) - 2
            ret = [i for i in ret if i >= m_ret]
            return ret
        except:
            return [-1]

    def get_build_time(self, n):
        try:
            data = [math.ceil((cost - curr) / gain)
                    for cost, curr, gain
                    in zip(self.blueprint[n], self.resources, self.bots_built)
                    if cost != 0]
            data.append(0)
            return max(data)
        except:
            return 100

    def do_action(self, action):
        if action + 1:
            time_steps = self.get_build_time(action) + 1
        else:
            time_steps = 1 + self.time

        self.time -= time_steps

        # gain resources
        if not (action + 1):
            self.resources[3] += self.bots_built[3] * time_steps
            return self

        for resource in range(4):
            self.resources[resource] += self.bots_built[resource] * \
                time_steps - self.blueprint[action][resource]

        self.bots_built[action] += 1

        return self

    def extra_possible_score(self):
        return (self.time - 1) * self.time >> 1

    def minimum_possible_score(self):
        return self.resources[3] + self.bots_built[3] * self.time

    def copy(self):
        return State(self.bots_built.copy(), self.resources.copy(), self.time, self.blueprint, self.cheap)


def parse_inp(F: list[str]):
    ret = []
    for blueprint in F:
        p = [int(l) for l in "".join(
            c for c in blueprint if c.isnumeric() or c == " ").split(" ") if l != ""]
        ret.append([
            [p[1], 0, 0, 0],
            [p[2], 0, 0, 0],
            [p[3], p[4], 0, 0],
            [p[5], 0, p[6], 0]
        ])
    return ret[:3]


def deal_with_blueprint(blueprint):
    global total_score
    cheap = [max(blueprint[1][0], blueprint[2][0], blueprint[3][0]),
             max(blueprint[2][1], blueprint[3][1]),
             blueprint[3][2],
             1000000]
    states = [State(blueprint=blueprint, cheap=cheap)]
    best_min = 0

    while states:
        working = states.pop()

        for action in working.get_actions():
            new = working.copy().do_action(action)

            if new.time < 0:
                break

            mscore = new.minimum_possible_score()
            best_min = max(best_min, mscore)

            bscore = new.extra_possible_score()
            if best_min - mscore <= bscore:
                states.append(new)

#    print(f"BP: {best_min} geodes")
    return best_min


def main(prints):
    ret = 1
    with multiprocessing.Pool(len(prints)) as p:
        for result in p.map(deal_with_blueprint, prints):
            ret *= result
    return ret


if __name__ == "__main__":
    st = time.perf_counter_ns()
    print(main(parse_inp(open(f"python/Advent of Code/2022/Day 19/input.txt", "r"))))
    print(f"{time.perf_counter_ns() - st}ns used")
