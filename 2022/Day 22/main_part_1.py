F = open("python/Advent of Code/2022/Day 22/input.txt", "r")
F = F.readlines()

def strformat(a,b): # i wrote this for a completely diffrent project, please forgive me
    lng = 0
    for i in a:
        lng += 1
    ret = ""
    for i in range(0,b):
        if i < lng:
            ret += a[i]
        else:
            ret += "@"
    return ret

def parse_inp(F):
    ret_1, ret_2 = [], ""
    
    index = 0
    while F[index] != "\n":
        ret_1.append(f"@{F[index].replace(' ', '@').replace(chr(0xa), '')}@")
        index += 1

    max_len = max([len(x) for x in ret_1])
    ret_1 = [strformat(x, max_len) for x in ret_1]
    
    ret_1.insert(0, "@" * len(ret_1[0]))
    ret_1.append("@" * len(ret_1[0]))
    
    ret_2 = [(int(x[:-1]), x[-1]) for x in F[-1].replace("R", "R,").replace("L", "L,").replace("\n", "").split(",")[:-1]]

    return ret_1, ret_2

def main(inp):
    grid, instructions = inp
    coord = [grid[1].index("."), 1]
    directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]

    angle = 0
    for pair in instructions:
        amount, turn = pair
        for _ in range(amount):
            next_x = coord[0] + directions[angle][0]
            next_y = coord[1] + directions[angle][1]
            next_obj = grid[next_y][next_x]

            if next_obj == "#":  # hit the barrier, also on 3.10.6 so no match/case statement
                break

            if next_obj == "@": # off the world
                tmp_next_obj = "."

                next_x -= directions[angle][0]
                next_y -= directions[angle][1]

                while tmp_next_obj != "@":
                    next_x -= directions[angle][0]
                    next_y -= directions[angle][1]
                    tmp_next_obj = grid[next_y][next_x]
                
                next_x += directions[angle][0]
                next_y += directions[angle][1]

                if grid[next_y][next_x] == "#":
                    break
            
            coord = [next_x, next_y]
        
        angle += {"R": 1, "L": -1}[turn]
        angle %= 4
    
    return 1000 * coord[1] + 4 * coord[0] + angle

print(main(parse_inp(F)))
