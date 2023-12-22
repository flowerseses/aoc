import time
from collections import deque
from pprint import pprint

directions = [(-1, 0), (0, -1), (0, 1), (1, 0)]
steppy = 26501365


def task1():
    startt = time.time()
    grid = []
    with open("input") as file:
        lines = [line.rstrip() for line in file if len(line) > 1]
        for j, line in enumerate(lines):
            grid.append([])
            for i, c in enumerate(line):
                grid[j].append(c)
                if c == "S":
                    start = (i, j)
    visited = bfs(grid, start, 64)
    print(visited)
    print(time.time() - startt)


def expand(grid, times):
    return [[grid[j % len(grid)][i % len(grid[0])] for i in range(times * len(grid[0]))] for j in range(times * len(grid))]


def is_valid(grid, x, y):
    return 0 <= y < len(grid) and 0 <= x < len(grid[0]) and grid[y][x] != "#"


def bfs(grid, start, step_count):
    visited = set()
    queue = deque([(start, 0)])
    while queue:
        (x, y), steps = queue.popleft()
        if steps > step_count:
            continue
        for dx, dy in directions:
            nx, ny = x + dx, y+dy
            if is_valid(grid, nx, ny) and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append(((nx, ny), steps + 1))
    return len([(x, y) for x, y in visited if (x + y) % 2 == step_count % 2])


def bfs_expanded(grid, start, step_count):
    visited = set()
    queue = deque([(start, 0)])
    while queue:
        (x, y), steps = queue.popleft()
        if steps > step_count:
            continue
        for dx, dy in directions:
            nx, ny = x + dx, y+dy
            if is_valid(grid, nx, ny) and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append(((nx, ny), steps + 1))
    out = []
    for j in range(0, 9):
        out.append([])
        for i in range(0, 9):
            out[j].append(len([(x, y) for x, y in visited if (x + y) % 2 == step_count % 2 and i*131 <= x < (i+1)*131 and j*131 <= y < (j+1)*131]))
    return out


def task2():
    startt = time.time()
    grid = []
    with open("input") as file:
        lines = [line.rstrip() for line in file if len(line) > 1]
        for j, line in enumerate(lines):
            grid.append([])
            for i, c in enumerate(line):
                grid[j].append(c)
                if c == "S":
                    start = (i, j)
    # we have an even number of grid repetitions + 65 steps. at 4 repetitions (so 4*131 + 65 steps), we get values for each node that don't change
    big = expand(grid, 9)
    start = len(big) // 2, len(big) // 2
    expanded_values = bfs_expanded(big, start, 65+4*131)
    # this diamond grows in a predictable way now
    pprint(expanded_values)
    total = get_total(expanded_values, steppy)
    print(total)
    print(time.time() - startt)


# uglyyy but ugh
def get_total(values, steps):
    e = values[4][1]
    o = values[4][2]
    points = [values[4][0], values[0][4], values[4][-1], values[-1][4]]
    oe = [values[3][0], values[5][0], values[3][-1], values[5][-1]]
    ie = [values[3][1], values[5][1], values[3][-2], values[5][-2]]
    n = (steps-65)//131
    total = n*n*e
    total += (n-1)*(n-1)*o
    total += n*sum(oe)
    total += (n-1)*sum(ie)
    total += sum(points)
    return total


if __name__ == '__main__':
    #task1()
    task2()
