import random
F = open(f"python/Advent of Code/2022/Day 16/input.txt", "r")

Nodes = {}
Node_distances = {}


class Node():
    _allNodes = {}
    def __init__(self, id, directions, value):
        global Nodes
        self._allNodes[id] = self
        Nodes[id] = self

        self.id = id
        self.directions = directions
        self.value = value

class State:
    def __init__(self, current_node, active_nodes=[], time=30, score=0, actions=(["open_valve_AA"],["open_valve_AA"]), pressures=[]):
        self.current_node = current_node
        self.active_nodes = active_nodes
        self.time = 27 - len(actions[0])
        self.score = score
        self.actions = actions
        self.rates = pressures
    
    def get_actions_n(self, n):
        if self.actions[n][-1].startswith("move_"):
            if self.actions[n][-1].split("_")[2] == "0":
                return [f"open_valve_{self.current_node[n].id}"]

            x = self.actions[n][-1].split("_")
            return [f"move_{x[1]}_{int(x[2]) - 1}"]

        ret = []
        for key, _ in Nodes.items():
            if key in self.active_nodes or Nodes[key].value == 0 or key in self.actions[1 - n][-1]:
                continue
            ret.append(f"move_{key}_{Node_distances[self.current_node[n].id][key] - 1}")
        
        if ret == []:
            return ["do_nothing"]

        return ret
    
    def get_actions(self):
        actions_0 = self.get_actions_n(0)
        actions_1 = self.get_actions_n(1)
        ret = []
        for action_0 in actions_0:
            for action_1 in actions_1:
                if action_1.split("_")[1] in action_0 and action_1 != "do_nothing" and not (action_0.startswith("open_valve") and action_1.startswith("open_valve")):
                    continue
                ret.append((action_0, action_1))
        
        return ret
    
    def get_score_rate(self):
        ret = 0
        for node in self.active_nodes:
            ret += Nodes[node].value
        
        return ret

    def do_action(self, action):
        self.score += self.get_score_rate()
        self.rates.append(self.get_score_rate())
        self.actions[0].append(action[0])
        self.actions[1].append(action[1])
        self.time = 27 - len(self.actions[0])

        if action[0].count("move_") > 0:
            action0 = action[0].split("_")[1]
            self.current_node[0] = Nodes[action0]

        if action[0].startswith("open_valve") and not self.current_node[0].id in self.active_nodes:
            self.active_nodes.append(self.current_node[0].id)
        
        if action[1].count("move_") > 0:
            action1 = action[1].split("_")[1]
            self.current_node[1] = Nodes[action1]

        if action[1].startswith("open_valve") and not self.current_node[1].id in self.active_nodes:
            self.active_nodes.append(self.current_node[1].id)
        
        return self
    
    def maximum_possible_score(self):
        maximum = 0
        for key, node in Nodes.items():
            maximum += node.value

        return self.score + maximum * self.time
    
    def minumum_possible_score(self):
        return self.score + self.get_score_rate() * self.time
    
    def copy(self):
        return State(self.current_node.copy(), self.active_nodes.copy(), self.time, self.score, (self.actions[0].copy(), self.actions[1].copy()), self.rates.copy())

def parse_inp(F: list[str]):
    q = ""
    for i in F:
        i = i.split(";")
        name = i[0][6:8]
        if q == "":
            q = name
        rate = int(i[0][23:])
        new = eval("['" + i[1][23:].replace(",", "','").replace("\n", "").replace(" ", "") + "']")

        Node(name, new, rate)
    return q

def precompute_dist():
    for k, _ in Nodes.items():
        distances = get_distances(k)
        add = {}
        for key, val in distances.items():
            if Nodes[key].value != 0 and key != k:
                add[key] = val
        Node_distances[k] = add

def main(q):
    states = [State(current_node=[Nodes[q], Nodes[q]])]
    best_state = State(current_node=[Nodes[q], Nodes[q]])#, score=2289, actions=["do_nothing" for _ in range(30)])
    i = 0
    while True:
        i += 1
        if states == []:
            break
        if i == 538:
            pass
        working = states.pop().copy()
        paths = working.get_actions()

        for action in paths:
            new = working.copy().do_action(action)
#            print("New state", new.score, new.maximum_possible_score(), new.minumum_possible_score(), 27 - new.time, new.get_score_rate(), new.active_nodes, format_x(new.actions), new.rates)
            if new.time < 0:
                break
            if best_state.score <= new.score:
                best_state = new
            
            if best_state.minumum_possible_score() <= new.maximum_possible_score():
                states.append(new)
            del new

        if i % 100000 == 0:
            try:
                print(f"Round {i}, {len(states)} more leaf nodes")
                print(best_state.score, best_state.maximum_possible_score(), best_state.minumum_possible_score(), best_state.time, best_state.get_score_rate(), best_state.active_nodes, format_x(best_state.actions))
                print()
                print(f"Next: {format_x(states[-1].actions)}")
                print("\n")
            except:
                pass

    print(f"Best found:")
    print(f"Score: {best_state.maximum_possible_score()}")
    print("Actions")
    for i in range(len(best_state.actions[0])):
        print(best_state.actions[0][i], best_state.actions[1][i])
    print(len(best_state.actions[0]), len(best_state.actions[1]))
    print(best_state.active_nodes)
    print(best_state.time)
    print(i)

def format_x(s):
    s0 = s[0]
    s1 = s[1]

    r0 = []
    r1 = []
    
    for i in s0:
        if i.startswith("open_valve_"):
            r0.append(i[11:])
    
    for i in s1:
        if i.startswith("open_valve_"):
            r1.append(i[11:])

    r0.append(s0[-1][5:])
    r1.append(s1[-1][5:])
    
    return [r0, r1]

def main_alt():
    s = State(Nodes["AA"])
    while s.time > 0:
        action = s.get_actions()[random.randint(0, len(s.get_actions()) - 1)]
        s.do_action(action)
        print(action)
        print(s.score)
        print(s.maximum_possible_score())
        print(s.minumum_possible_score())
        print(s.time)
        print(s.get_score_rate())
        print(s.actions)
        print()

def get_distances(node):
    ret = {}
    ret[node] = 0
    new = [node]
    while new != []:
        current = new.pop(0)
        for path in Nodes[current].directions:
            try:
                ret[path]
            except:
                ret[path] = ret[current] + 1
                new.append(path)
    
    return ret


parse_inp(F)
#main_alt()
precompute_dist()
main("AA")
