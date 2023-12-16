import time
from pprint import pprint
import re

seen = []
puzzles = []


def task1():
    start = time.time()
    puzzle = []
    total = 0
    with open("input") as file:
        for line in file:
            puzzle.append(line.rstrip())
    rotated = rotate(puzzle)
    for row in rotated:
        line = shift_rocks(row)
        total += calc_load(line)
    print(total)
    print(time.time() - start)


def calc_load(line):
    load = 0
    for i in range(len(line)):
        if line[i] == "O":
            load += i + 1
    return load


def task2():
    start = time.time()
    puzzle = []
    total = 0
    with open("input1") as file:
        for line in file:
            puzzle.append(line.rstrip())
    i = 0
    cycles = 1000000000
    rotated = rotate(puzzle)
    for i in range(cycles):
        rotated, repeat = one_cycle(rotated)
        temp = rotate(rotate(rotate(rotated)))
        #pprint(temp)
        if repeat < 0:
            print(f"{i}: no repeat")
        if repeat >= 0:
            print(f"found a repeat at {i}")
            cycle_start = repeat
            cycle_len = len(seen) - cycle_start
            rem = (1000000000 - cycle_start) % cycle_len
            print(f"pos = {rem} - {seen[cycle_start + rem]}")
            pprint(seen[cycle_start + rem - 1][1])
            print(calc_full_load(seen[cycle_start + rem - 1][1]))
            break

    print(calc_full_load(rotated))
    # res = one_cycle(rotated)
    cycle = 100
    print(total)
    print(time.time() - start)


def one_cycle(puzzle):
    helper = puzzle
    for i in range(4):
        out = move_all(helper)
        helper = rotate(out)
    key = (i, helper)
    if key in seen:
        return helper, seen.index(key)
    seen.append(key)
    #    pprint(out)
    #    print("---")
    return helper, -1


def move_all(puzzle):
    slid = []
    for row in puzzle:
        slid.append(shift_rocks(row))
    return slid


def shift_rocks(line):
    chunks = re.split("(#+)", line)
    new_line = ""
    for chunk in chunks:
        if chunk.startswith(".") or chunk.startswith("O"):
            rocks = chunk.count("O")
            dots = chunk.count(".")
            new_line = new_line + "".join(["." for i in range(dots)]) + "".join(["O" for i in range(rocks)])
        else:
            new_line = new_line + chunk
    return new_line


def calc_full_load(puzzle):
    total = 0
    for row in puzzle:
        total += calc_load(row)
    return total


def rock_pos(puzzle):
    rocks = set()
    for i in range(len(puzzle)):
        row = puzzle[i]
        for j in range(len(row)):
            if row[j] == "O":
                rocks.add((i, j))
    print(rocks)
    return rocks


# this isn't a real rotation!
def rotate(puzzle):
    rotated = list(zip(*puzzle[::-1]))
    res = []
    for row in rotated:
        line = "".join(row)
        res.append(line)
    return res


if __name__ == '__main__':
    # task1()
    task2()