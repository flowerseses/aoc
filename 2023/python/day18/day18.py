import time
import math
from turtle import *
from pprint import pprint
from itertools import pairwise

maxx = 0
maxy = 0
minx = 0
miny = 0

discounts = {
    "UR": ["RD", "UL"],
    "LD": ["RD", "UL"],
    "DR": ["RU", "DL"],
    "LU": ["RU", "DL"],
    "DL": [],
    "RU": [],
    "UL": [],
    "RD": [],
}
connections = {}


def task1():
    startt = time.time()
    with open("input") as file:
        lines = [line.rstrip() for line in file if len(line) > 1]
    nc = lines[0].split()[0]
    borders = []
    corners = {}
    prev = (0, 0)
    global minx, miny, maxx, maxy
    border_size = 0
    for l, line in enumerate(lines):
        dir, dist, color = line.split()
        match dir:
            case "R":
                for i in range(1, int(dist)):
                    borders.append((prev[0] + i, prev[1]))
                n = (prev[0]+int(dist), prev[1])
            case "L":
                for i in range(1, int(dist)):
                    borders.append((prev[0] - i, prev[1]))
                n = (prev[0]-int(dist), prev[1])
            case "U":
                for i in range(1, int(dist)):
                    borders.append((prev[0], prev[1]- i))
                n = (prev[0], prev[1]-int(dist))
            case "D":
                for i in range(1, int(dist)):
                    borders.append((prev[0], prev[1] + i))
                n = (prev[0], prev[1]+int(dist))
        border_size += int(dist)
        if n[0] < minx:
            minx = n[0]
        elif n[0] > maxx:
            maxx = n[0]
        if n[1] < miny:
            miny = n[1]
        elif n[1] > maxy:
            maxy = n[1]
        borders.append(n)
        if l < len(lines) - 1:
            nextl = lines[l+1].split()[0]
        else:
            nextl = nc
        corners[n] = dir + "" + nextl
        prev = n
    borders.sort()
    total = cast_some_rays(borders, corners)
    print(total)
    print(time.time() - startt)


# just stolen from the previous day where we did this, slow af but oh well
def cast_some_rays(borders, corners):
    total = 0
    for j in range(miny, maxy + 1):
        hits = 0
        prev = "."
        for i in range(minx, maxx + 1):
            if (i, j) not in borders and hits % 2 == 1:
                total += 1
            elif (i, j) in borders:
                total += 1
                if (i, j) in corners:
                    if prev == ".":
                        prev = corners[(i, j)]
                    else:
                        corner = corners[(i, j)]
                        if corner not in discounts[prev]:
                            hits += 1
                        prev = "."
                elif prev == ".":
                    # simple, trivial
                    hits += 1
                    prev = "."
                else:
                    # simple, trivial as well, ignore
                    pass
    return total


def task2():
    startt = time.time()
    with open("input") as file:
        lines = [line.rstrip() for line in file if len(line) > 1]
    global maxx, maxy, minx, miny, connections
    edges = []
    prev = (0, 0)
    edges.append(prev)
    for line in lines:
        hex_str = line.split()[2][1:-1]
        d = int(hex_str[-1])
        dist = int(hex_str[1:-1], 16)
        n = None
        if d == 0:
            n = (prev[0]+dist, prev[1])
        elif d == 1:
            n = (prev[0], prev[1]+dist)
        elif d == 2:
            n = (prev[0]-dist, prev[1])
        elif d == 3:
            n = (prev[0], prev[1]-dist)
        if n[0] < minx:
            minx = n[0]
        elif n[0] > maxx:
            maxx = n[0]
        if n[1] < miny:
            miny = n[1]
        elif n[1] > maxy:
            maxy = n[1]
        edges.append(n)
        prev = n
    area = 0
    border = 0
    # Just shoelaces, I guess
    for p1, p2 in zip(edges, edges[1:]):
        area += p1[0]*p2[1] - p1[1]*p2[0]
        if p1[0] == p2[0]:
            border += abs(p1[1]-p2[1])
        else:
            border += abs(p1[0]-p2[0])
    print(int(area/2 + border/2 + 1))
    print(time.time() - startt)


if __name__ == '__main__':
    #task1()
    task2()
