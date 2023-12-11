import time
import re

galaxies = []
full_rows = set()
full_cols = set()

def task1():
    start = time.time()
    lines = []
    with open("input") as file:
        for line in file.readlines():
            lines.append(line.rstrip())
    for i in range(len(lines)):
        row = lines[i]
        if "#" in row:
            full_rows.add(i)
            gals = re.finditer("(#)", row)
            for gal in gals:
                galaxies.append((gal.start(), i))
                full_cols.add(gal.start())
    small = find_distances(1)
    print(small)
    print(time.time() - start)


def task2():
    start = time.time()
    lines = []
    with open("input") as file:
        for line in file.readlines():
            lines.append(line.rstrip())
    for i in range(len(lines)):
        row = lines[i]
        if "#" in row:
            full_rows.add(i)
            gals = re.finditer("(#)", row)
            for gal in gals:
                galaxies.append((gal.start(), i))
                full_cols.add(gal.start())
    dists = find_distances(999999)
    print(dists)
    print(time.time() - start)


def find_distances(expansion):
    distances = []
    total = 0
    for i in range(len(galaxies)):
        for j in range(i, len(galaxies)):
            start = galaxies[i]
            end = galaxies[j]
            dist = abs(end[0] - start[0]) + abs(end[1] - start[1])
            for k in range(min(start[0], end[0]), max(start[0], end[0])):
                if k not in full_cols:
                    dist += expansion
            for k in range(min(start[1], end[1]), max(start[1], end[1])):
                if k not in full_rows:
                    dist += expansion
            distances.append((i, j, dist))
            total += dist
    return total


if __name__ == '__main__':
    task1()
    task2()
