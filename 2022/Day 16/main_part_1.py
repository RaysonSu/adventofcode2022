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
    def __init__(self, current_node, active_nodes=[], time=30, score=0, actions=["open_valve"]):
        self.current_node = current_node
        self.active_nodes = active_nodes
        self.time = 31 - len(actions)
        self.score = score
        self.actions = actions
    
    def get_actions(self):
        if self.actions[-1].startswith("move_"):
            if self.actions[-1].split("_")[2] == "0":
                return ["open_valve"]

            x = self.actions[-1].split("_")
            return [f"move_{x[1]}_{int(x[2]) - 1}"]

        ret = []
        for key, _ in Nodes.items():
            if key in self.active_nodes or Nodes[key].value == 0:
                continue
            ret.append(f"move_{key}_{Node_distances[self.current_node.id][key] - 1}")
        
        if ret == []:
            return ["do_nothing"]

        return ret
    
    def get_score_rate(self):
        ret = 0
        for node in self.active_nodes:
            ret += Nodes[node].value
        
        return ret

    def do_action(self, action):
        self.score += self.get_score_rate()
        self.actions.append(action)
        self.time = 31 - len(self.actions)

        if action.count("move_") > 0:
            action = action.split("_")[1]
            self.current_node = Nodes[action]
            return self

        if action == "open_valve":
            self.active_nodes.append(self.current_node.id)
            return self
        
        return self
    
    def maximum_possible_score(self):
        maximum = 0
        for key, node in Nodes.items():
            maximum += node.value

        return self.score + maximum * self.time
    
    def minumum_possible_score(self):
        return self.score + self.get_score_rate() * self.time
    
    def copy(self):
        return State(self.current_node, self.active_nodes.copy(), self.time, self.score, self.actions.copy())

def parse_inp(F: list[str]):
    q = ""
    print(Node._allNodes)
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
    states = [State(current_node=Nodes[q])]
    best_state = State(current_node=Nodes[q])#, score=2289, actions=["do_nothing" for _ in range(30)])
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
            if best_state.score <= new.score:
                best_state = new
            
            if best_state.minumum_possible_score() <= new.maximum_possible_score():
                states.insert(0, new)
            del new
        if i % 100000 == 0:
            print(f"Round {i}, {len(states)} more leaf nodes")
            print(best_state.score, best_state.maximum_possible_score(), best_state.minumum_possible_score(), best_state.time, best_state.get_score_rate(), best_state.active_nodes, best_state.actions)
            print()
            print(f"Next 8: {states[0].actions[:8]}")
            print("\n")

    print(f"Best found:")
    print(f"Score: {best_state.maximum_possible_score()}")
    print("Actions")
    for i in best_state.actions:
        print(i)

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
print(Node_distances)
main("AA")