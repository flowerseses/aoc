import time
from queue import PriorityQueue

grid = []
open_set = PriorityQueue()
solved = set()
set_copy = set()
costs = {}
visited = set()
max_cost = 9*150*150
GX = 0
GY = 0


class Node:
    def __init__(self, x, y, d, distance=9*150*150):
        global grid
        self.x = x
        self.y = y
        self.dx = d[0]
        self.dy = d[1]
        self.value = grid[y][x]
        self.distance = distance

    def get_key(self):
        return self.x, self.y, (self.dx, self.dy)

    def __lt__(self, other):
        return self.distance - self.y - self.x < other.distance - other.y - other.x


# Note: I broke this while fixing stuff for p1, so it needs rewriting/rethinking to work
def task1():
    startt = time.time()
    global max_cost
    with open("input") as file:
        for line in file:
            grid.append([int(i) for i in list(line.rstrip())])
    global GX, GY
    GX = len(grid[0])
    GY = len(grid)
    for j in range(GY):
        for i in range(GX):
            for p in range(1, 4):
                costs[(i, j, (-1, 0), p)] = max_cost
                costs[(i, j, (1, 0), p)] = max_cost
                costs[(i, j, (0, -1), p)] = max_cost
                costs[(i, j, (0, 1), p)] = max_cost
    print(f"{GX}, {GY}")
    start_r = Node(0, 0, (1, 0), 0, 0)
    open_set.put(start_r)
    costs[start_r.get_key()] = 0
    while not open_set.empty():
        node = open_set.get()
        if node.x == GX - 1 and node.y == GY - 1:
            print(node.distance)
            break
        next_nodes = []
        if node.path_length < 3:
            next_nodes.append((node.dx, node.dy, node.path_length + 1))
        if node.dy == 0:
            next_nodes.extend([(0, -1, 1), (0, 1, 1)])
        else:
            next_nodes.extend([(-1, 0, 1), (1, 0, 1)])
        for dx, dy, l in next_nodes:
            if not is_valid_node(node.x+dx, node.y+dy):
                continue
            next_node = Node(node.x+dx, node.y+dy, (dx, dy), l)
            key = next_node.get_key()
            score = min(node.distance + next_node.value, next_node.distance)
            next_node.distance = score
            if key not in costs or costs[key] > next_node.distance:
                costs[key] = next_node.distance
                open_set.put(next_node)
    print(time.time() - startt)


def is_valid_node(a, b):
    if 0 <= a < GX and 0 <= b < GY:
        return True
    return False


def task2():
    startt = time.time()
    global max_cost, costs, open_set, grid
    costs = {}
    open_set = PriorityQueue()
    grid = []
    with open("input") as file:
        for line in file:
            grid.append([int(i) for i in list(line.rstrip())])
    global GX, GY
    GX = len(grid[0])
    GY = len(grid)
    for j in range(GY):
        for i in range(GX):
            for p in range(1, 4):
                costs[(i, j, (-1, 0))] = max_cost
                costs[(i, j, (1, 0))] = max_cost
                costs[(i, j, (0, -1))] = max_cost
                costs[(i, j, (0, 1))] = max_cost
    start_r = Node(0, 0, (1, 0), 0)
    open_set.put(start_r)
    costs[start_r.get_key()] = 0
    while not open_set.empty():
        node = open_set.get()
        if node.x == GX - 1 and node.y == GY - 1:
            print("found the end node")
            print(node.distance)
            break
        next_nodes = []
        if node.dy:
            if node.x > 3:
                for i in range(*(max(0, node.x-10), node.x -3)):
                    next_nodes.append((i, node.y, (-1, 0)))
            if node.x < GX - 4:
                for i in range(*(node.x + 4, min(GX, node.x+11))):
                    next_nodes.append((i, node.y, (1, 0)))
        elif node.dx:
            if node.y > 3:
                for i in range(*(max(0, node.y-10), node.y - 3)):
                    next_nodes.append((node.x, i, (0, -1)))
            if node.y < GY - 4:
                for i in range(*(node.y + 4, min(GY, node.y+11))):
                    next_nodes.append((node.x, i, (0, 1)))

        for x, y, d in next_nodes:
            dx = d[0]
            dy = d[1]
            next_node = Node(x, y, (dx, dy))

            key = next_node.get_key()
            score = node.distance
            if node.y == next_node.y:
                if node.x < next_node.x:
                    score += sum(grid[y][i] for i in range(node.x + 1, x + 1))
                else:
                    score += sum(grid[y][i] for i in range(x, node.x))
            else:
                if node.y < next_node.y:
                    score += sum(grid[i][x] for i in range(node.y + 1, y + 1))
                else:
                    score += sum(grid[i][x] for i in range(y, node.y))
            next_node.distance = min(score, next_node.distance)
            if key not in costs or costs[key] > next_node.distance:
                costs[key] = next_node.distance
                open_set.put(next_node)
    print(time.time() - startt)


if __name__ == '__main__':
    #task1()
    task2()
