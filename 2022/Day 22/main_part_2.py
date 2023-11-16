F = open("python/Advent of Code/2022/Day 22/input.txt", "r")
F = F.readlines()


def parse_inp(F):
    ret_1, ret_2, ret_3 = [[] for _ in range(6)], "", []

    box_size = int(
        (("".join(F).count(".") + "".join(F).count("#")) / 6) ** 0.5)

    index = 0
    for i in range((len(F) - 1) // box_size):
        box_offsets = []

        for j in range(len(F[box_size * i]) // box_size):
            if F[i * box_size][j * box_size] == " ":
                continue
            box_offsets.append((index, j * box_size))
            ret_3.append([j * box_size, i * box_size])
            index += 1

        for j in range(box_size):
            text = F[i * box_size + j]
            for k in box_offsets:
                ret_1[k[0]].append(text[k[1]:k[1] + box_size])

    ret_2 = [(int(x[:-1]), x[-1]) for x in F[-1].replace("R", "R,")
                                                .replace("L", "L,")
                                                .replace("\n", "")
                                                .split(",")[:-1]]

    if F[-1][-1].isnumeric():
        ret_2.append((int(F[-1].replace("R", "R,")
                      .replace("L", "L,")
                      .replace("\n", "")
                      .split(",")[-1]), "N"))

    return ret_1, ret_2, ret_3, box_size


def determine_grid_teleports(grid_offsets):
    hcf = min([item for sublist in grid_offsets for item in sublist if item != 0])
    grid_offsets = [[value // hcf for value in item] for item in grid_offsets]

    ret = [["" for _ in range(4)] for _ in range(6)]

    # step 1: the simple ones (already connected ones)
    for index, face in enumerate(grid_offsets):
        for index_dir, directions in enumerate([[1, 0], [0, 1], [-1, 0], [0, -1]]):
            new_face = list(map(lambda x, y: x + y, face, directions))

            if new_face not in grid_offsets:
                continue

            ret[index][index_dir] = str(grid_offsets.index(new_face)) \
                + ["l", "u", "r", "d"][index_dir]

    # step 2: the edge cases (on the perimeter)
    loop = []
    for index_dir, directions in enumerate([[1, 0], [0, 1], [-1, 0], [0, -1]]):
        new_face = list(map(lambda x, y: x + y, grid_offsets[0], directions))

        if new_face not in grid_offsets:
            break

    current_face = grid_offsets[0]
    for _ in range(14):
        loop.append(str(grid_offsets.index(current_face)) +
                    ["r", "d", "l", "u"][index_dir])

        # try and walk forward
        tmp_new_face_1 = list(map(lambda x, y: x + y, current_face, [
                              [1, 1], [-1, 1], [-1, -1], [1, -1]][index_dir]))  # mustn't be in the grid
        tmp_new_face_2 = list(map(lambda x, y: x + y, current_face,
                              [[0, 1], [-1, 0], [0, -1], [1, 0]][index_dir]))  # must be in the grid

        if tmp_new_face_1 not in grid_offsets and tmp_new_face_2 in grid_offsets:
            current_face = tmp_new_face_2
            continue

        if tmp_new_face_1 in grid_offsets and tmp_new_face_2 in grid_offsets:
            current_face = tmp_new_face_1
            index_dir -= 1
            index_dir %= 4
            loop.append("*")
            continue

        if tmp_new_face_1 not in grid_offsets and tmp_new_face_2 not in grid_offsets:
            index_dir += 1
            index_dir %= 4
            continue

    while loop != []:
        # handle collisions
        while "*" in loop:
            first_star = loop.index("*")

            first_index = (first_star - 1) % len(loop)
            second_index = (first_star + 1) % len(loop)

            first = loop[first_index]
            second = loop[second_index]

            ret[int(first[0])][["r", "d", "l", "u"].index(first[1])] = second
            ret[int(second[0])][["r", "d", "l", "u"].index(second[1])] = first
            loop[first_star] = "#"

            del loop[max(first_index, second_index)]
            del loop[min(first_index, second_index)]

            index = -1
            while index < len(loop) - 1:
                if loop[index] == "#" and loop[index + 1] == "*":
                    del loop[index]
                else:
                    index += 1

            if (loop.count("*") + loop.count("#")) == len(loop):
                break

        # clean up
        index = -1
        while index < len(loop) - 1:
            if loop[index] == "#" and loop[index + 1] == "#":
                del loop[index + 1]
            else:
                index += 1

        for i in range(len(loop)):
            if loop[i] == "#":
                loop[i] = "*"

        if loop.count("*") == len(loop):
            break

    return ret


def main_teleport(pos, direction, grid_teleports, box_size):
    next_teleport = grid_teleports[pos[0]][direction]
    t = None
    if direction == 0:
        t = pos[1][1]
    elif direction == 1:
        t = box_size - pos[1][0] - 1
    elif direction == 2:
        t = box_size - pos[1][1] - 1
    elif direction == 3:
        t = pos[1][0]

    new_coord = []
    new_edge = next_teleport[1]
    if new_edge == "r":
        new_coord = [box_size - 1, box_size - t - 1]
    elif new_edge == "d":
        new_coord = [t, box_size - 1]
    elif new_edge == "l":
        new_coord = [0, t]
    elif new_edge == "u":
        new_coord = [box_size - t - 1, 0]

    return (int(next_teleport[0]), new_coord), ["l", "u", "r", "d"].index(new_edge)


def main(inp):
    grid, instructions, grid_offsets, box_size = inp
    coord = [grid[0][0].index("."), 0]
    face_index = 0
    directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]
    grid_teleports = determine_grid_teleports(grid_offsets)

    angle = 0
    for pair in instructions:
        amount, turn = pair
        for _ in range(amount):
            next_x = coord[0] + directions[angle][0]
            next_y = coord[1] + directions[angle][1]

            if max(next_x, next_y) >= box_size or min(next_x, next_y) < 0:
                tmp_coords, tmp_angle = main_teleport((face_index, coord),
                                                      angle,
                                                      grid_teleports,
                                                      box_size)

                if grid[tmp_coords[0]][tmp_coords[1][1]][tmp_coords[1][0]] == "#":
                    break

                coord = tmp_coords[1]
                face_index = tmp_coords[0]
                angle = tmp_angle
                continue

            next_obj = grid[face_index][next_y][next_x]

            if next_obj == "#":  # hit the barrier, also on 3.10.6 so no match/case statement
                break

            coord = [next_x, next_y]

        angle += {"R": 1, "L": -1, "N": 0}[turn]
        angle %= 4
        print(face_index, coord, angle)

    return 1000 * (coord[1] + grid_offsets[face_index][1] + 1) + 4 * (coord[0] + grid_offsets[face_index][0] + 1) + angle


print(main(parse_inp(F)))
