import random, math, threading, time
F = open(f"python/Advent of Code/2022/Day 19/input.txt", "r")
total_score = 0
init_time = time.time()

class State:
    def __init__(self, bots_built=[1, 0, 0, 0], resources=[0, 0, 0, 0], actions=["do_nothing"], blueprint={}):
        self.bots_built = bots_built
        self.resources = resources
        self.time = 25 - len(actions)
        self.actions = actions
        self.blueprint = blueprint
    
    def get_actions(self):
        ret = []
        for bot in range(4):
            time = self.get_build_time(bot)
            if time + 1 > self.time:
                continue
            ret.append(f"build_{bot}")
        
        if ret == []:
            return ["do_nothing"]
        
        return ret
    
    def get_build_time(self, n):
        data = [math.ceil((cost - curr) / max(0.01, gain)) for cost, curr, gain in zip(self.blueprint[n], self.resources, self.bots_built) if cost != 0]
        return max(0, int(max(data)))
    
    def get_score_rate(self):
        return self.bots_built[3]

    def do_action(self, action):
        time_steps = 1
        if action.startswith("build_"):
            time_steps = self.get_build_time(int(action[6:])) + 1

        self.actions.extend([action for _ in range(time_steps)])
        self.time = 25 - len(self.actions)

        # gain resources
        self.resources = list(map(lambda x, y: x + y * time_steps, self.resources, self.bots_built))
        
        if action == "do_nothing":
            return self
        
        to_build = int(action[6:])
        self.resources = list(map(lambda x, y: x - y, self.resources, self.blueprint[to_build]))
        self.bots_built[to_build] += 1
        
        return self
    
    def maximum_possible_score(self):
        return self.resources[3] + self.get_score_rate() * self.time + (self.time - 1) * self.time // 2
    
    def minimum_possible_score(self):
        return self.resources[3] + self.get_score_rate() * self.time
    
    def copy(self):
        return State(self.bots_built.copy(), self.resources.copy(), self.actions.copy(), self.blueprint.copy())

def parse_inp(F: list[str]):
    ret = []
    for blueprint in F:
        p = [int(l) for l in "".join(c for c in blueprint if c.isnumeric() or c == " ").split(" ") if l != ""]
        ret.append([
            [p[1], 0, 0, 0],
            [p[2], 0, 0, 0],
            [p[3], p[4], 0, 0],
            [p[5], 0, p[6], 0]
        ])
    return ret

def deal_with_blueprint(blueprint, index):
    global total_score
    states = [State(blueprint=blueprint)]
    best_state = State(blueprint=blueprint)
    i = 0
    while True:
        i += 1
        if states == []:
            break
        working = states.pop(0).copy()
        paths = working.get_actions()

        for action in paths:
            new = working.copy().do_action(action)
            if new.time < 0:
                break

            if best_state.minimum_possible_score() <= new.minimum_possible_score():
                best_state = new
            
            if best_state.minimum_possible_score() <= new.maximum_possible_score():
                states.insert(0, new)

#        if i % 1 == 0:
#            print(f"Round {i}, {len(states)} more leaf nodes")
#            print(f"Next: {states[0].actions}")
#            print(f"bots: {states[0].bots_built}")
#            print(f"resources: {states[0].resources}")
#            print(f"bp: {states[0].blueprint}")
#            print(f"Time: {states[0].time}")
#            print(f"min score: {states[0].minimum_possible_score()}")
#            print(f"max score: {states[0].maximum_possible_score()}")
#            print(f"Best: {best_state.resources[3]}")
#            print("\n")

#    print(f"Best found:")
#    print(f"Score: {best_state.maximum_possible_score()}")
#    print("Actions")
#    for i in best_state.actions:
#        print(i)
    print(f"BP {index + 1}: {best_state.minimum_possible_score()} geodes ({i} nodes searched, {time.time() - init_time}s used)")
    total_score += best_state.minimum_possible_score() * (index + 1)


def randomise(blueprint):
    s = State(blueprint=blueprint).copy()
    while s.time > 0:
        action = s.get_actions()[random.randint(0, len(s.get_actions()) - 1)]
        if "build_3" in s.get_actions():
            action = "build_3"
        s.do_action(action)
    return s.resources[3]

def main(prints):
    threads = []
    for index, blueprint in enumerate(prints):
        thread = threading.Thread(target=deal_with_blueprint, args=(blueprint, index))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    return total_score

#main_alt()
print(main(parse_inp(F)))