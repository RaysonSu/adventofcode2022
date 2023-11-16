F = open("python/Advent of Code/2022/Day 7/input.txt", "r").readlines()


def get_disk(lines: list[str]):
    disk = {"/": {}}
    cur_dir = []

    for line in lines:
        if line.startswith("$ cd"):
            if line.count("..") == 1:
                cur_dir.pop()
            else:
                cur_dir.append(line[5:-1])
        elif line.startswith("$ ls"):
            pass
        elif line.startswith("dir"):
            key = cur_dir.copy()
            key.append(line[4:-1])
            disk = dict_append(disk, key, {})
        else:
            line = line.split()
            key = cur_dir.copy()
            key.append(line[1])
            disk = dict_append(disk, key, int(line[0]))
    return disk


def dict_append(main: dict, keys: list[str], val: any):
    ret = {}
    if len(keys) == 1:
        main[keys[0]] = val
        return main
    for key, value in main.items():
        if key == keys[0]:
            ret[key] = dict_append(main[keys[0]], keys[1:], val)
        else:
            ret[key] = value
    return main


def get_size(disk: dict, directory: list[str]):
    for i in directory:
        disk = disk[i]

    ret = 0
    for key, value in disk.items():
        if type(value) == int:
            ret += value
        else:
            ret += get_size(disk, [key])
    return ret


def get_directories(disk: dict):
    ret = []
    for key, value in disk.items():
        if type(value) == dict:
            sub_directories = get_directories(value)
            for sub_directory in sub_directories:
                to_add = [key]
                for i in sub_directory:
                    to_add.append(i)
                ret.append(to_add)
            ret.append([key])
    return ret


disk = get_disk(F)
total = 0

space_req = get_size(disk, ["/"]) - 40000000
min_space = 30000000
for i in get_directories(disk):
    size = get_size(disk, i)
    if size > space_req:
        min_space = min(min_space, size)

print(min_space)
