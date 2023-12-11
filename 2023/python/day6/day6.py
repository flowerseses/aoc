import math
import time

maps = {}


def task1():
    start = time.time()
    total = 0
    with open("input") as file:
        lines = [line.rstrip() for line in file if len(line) > 1]
    t = int("".join(lines[0].split(": ")[1].strip().split()))
    d = int("".join(lines[1].split(": ")[1].strip().split()))
    diff = math.sqrt(t**2 - 4*d)
    low = (t - diff)/2
    high = (t + diff)/2
    print(math.floor(high) - math.ceil(low) + 1)
    print(time.time() - start)


def task2():
    start = time.time()
    with open("input") as file:
        lines = [line.rstrip() for line in file if len(line) > 1]
    times = int("".join(lines[0].split(": ")[1].strip().split()))
    distances = int("".join(lines[1].split(": ")[1].strip().split()))
    winning = 1
    first_split = 0
    last_split = 0
    dist = distances+1
    split = times//2
    while dist > distances and split > 0:
        split = split//2
        dist = split*(times-split)
    while dist <= distances and split < times:
        dist = split*(times-split)
        split += 1
    if dist > distances:
        first_split = split - 1
    dist = distances + 1
    split = times//2
    while dist > distances and split < times:
        split = split*2
        dist = split*(times-split)
    while dist <= distances and split >= 0:
        dist = split * (times - split)
        split -= 1
    if dist > distances:
        last_split = split + 1
    winning = (last_split - first_split + 1)
    print(winning)
    print(time.time() - start)


if __name__ == '__main__':
    task1()
    task2()
