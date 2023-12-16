import time
from pprint import pprint
import difflib

puzzles = []


def get_reflection(puzzle):
    rotated = rotate(puzzle)
    # This could be smarter!
    # first, check rows:
    for i in range(len(puzzle) - 1):
        if puzzle[i] == puzzle[i+1]:
            if is_mirror(puzzle, i, i+1):
                return(i+1)*100
    # now columns
    for i in range(len(rotated) - 1):
        if rotated[i] == rotated[i+1]:
            if is_mirror(rotated, i, i+1):
                return i+1
    pass


def is_mirror(puzzle, x, y):
    comps = min(x, len(puzzle) - 1 - y)
    for i in range(1, comps + 1):
        if puzzle[x-i] != puzzle[y+i]:
            return False
    return True


def rotate(puzzle):
    rotated = []
    for j in range(len(puzzle[0])):
        row = ""
        for i in range(len(puzzle)):
            row += puzzle[i][j]
        rotated.append(row)
    return rotated


def task1():
    start = time.time()
    puzzle = []
    total = 0
    with open("input") as file:
        for line in file:
            if line == "\n":
                puzzles.append(puzzle)
                puzzle = []
            else:
                puzzle.append(line.rstrip())
        puzzles.append(puzzle)
    for puzzle in puzzles:
        total += get_reflection(puzzle)
    print(total)
    print(time.time() - start)


def get_smudgey_reflection(puzzle):
    rotated = rotate(puzzle)
    # This could be smarter!
    # first, check rows:
    for i in range(len(puzzle) - 1):
        if puzzle[i] == puzzle[i+1]:
            if is_mirror_smudged(puzzle, i, i+1):
                return(i+1)*100
        elif close_enough(puzzle[i], puzzle[i+1]):
            if is_mirror(puzzle, i, i+1):
                return (i+1)*100
    # now columns
    for i in range(len(rotated) - 1):
        if rotated[i] == rotated[i+1]:
            if is_mirror_smudged(rotated, i, i+1):
                return i+1
        elif close_enough(rotated[i], rotated[i+1]):
            if is_mirror(rotated, i, i+1):
                return i+1
    return 0


def close_enough(x, y):
    y = int(x, 2)^int(y, 2)
    if "{0:b}".format(y).count("1") == 1:
        return True
    return False


def is_mirror_smudged(puzzle, x, y):
    comps = min(x, len(puzzle) - 1 - y)
    smudges = 1
    for i in range(1, comps + 1):
        if puzzle[x-i] != puzzle[y+i] and not close_enough(puzzle[x-i], puzzle[y+i]):
            return False
        if puzzle[x-i] == puzzle[y+i]:
            continue
        elif close_enough(puzzle[x-i], puzzle[y+i]):
            if smudges < 1:
                return False
            smudges -= 1
    return smudges == 0


def task2():
    start = time.time()
    puzzle = []
    total = 0
    with open("input") as file:
        for line in file:
            if line == "\n":
                puzzles.append(puzzle)
                puzzle = []
            else:
                binary = line.replace(".", "0")
                binary = binary.replace("#", "1")
                puzzle.append(binary.rstrip())
        puzzles.append(puzzle)
    for puzzle in puzzles:
        total += get_smudgey_reflection(puzzle)
    print(total)
    print(time.time() - start)


if __name__ == '__main__':
    #task1()
    task2()
