import time

bricks = []
brick_info = {}
grid = []
xy = (0, 0)
zeds = (0, 0)


class Brick:
    def __init__(self, start, end, name):
        self.x1, self.y1, self.z1 = start
        self.x2, self.y2, self.z2 = end
        self.name = name
        self.supported_by = set()
        self.supports = set()

    def can_delete(self):
        for b in self.supports:
            other = brick_info[b]
            if len(other.supported_by) == 1:
                return False
        return True

    def chain_reaction(self, below):
        falls = 0

        for b in self.supports:
            brick = brick_info[b]
            remaining = brick.supported_by.difference(below)
            if len(remaining) == 1:

                falls += 1 + brick.chain_reaction(below)
                below.add(b)
        return falls

    def xrange(self):
        return range(self.x1, self.x2 + 1)

    def yrange(self):
        return range(self.y1, self.y2 + 1)

    def zrange(self):
        return range(self.z1, self.z2 + 1)

    def drop(self, g):
        z_bot = self.drop_dist(g)
        self.z2 = z_bot + (self.z2 - self.z1)
        self.z1 = z_bot
        for z in self.zrange():
            for y in self.yrange():
                for x in self.xrange():
                    g[z][y][x] = self.name
        self.make_supports(g)

    def add_support(self, other):
        self.supports.add(other)

    def make_supports(self, g):
        for y in self.yrange():
            for x in self.xrange():
                if g[self.z1-1][y][x] not in (".", "#"):
                    self.supported_by.add(g[self.z1-1][y][x])
                    brick_info[g[self.z1-1][y][x]].add_support(self.name)

    def drop_dist(self, g):
        clear = True
        drop = self.z1
        while clear:
            drop -= 1
            for y in self.yrange():
                for x in self.xrange():
                    if g[drop][y][x] != ".":
                        clear = False
        return drop + 1

    def __lt__(self, other):
        if self.z1 == other.z1:
            return self.z2 < other.z2
        return self.z1 < other.z1

    def __repr__(self):
        xc = f"x = ({self.x1}, {self.x2})"
        yc = f"y = ({self.y1}, {self.y2})"
        zc = f"z = ({self.z1}, {self.z2})"
        coords = ", ".join((xc, yc, zc))
        return f"{self.name}: {coords}"


def task1():
    startt = time.time()
    global xy, zeds, grid, bricks
    bricks = []
    with open("input") as file:
        lines = [line.rstrip() for line in file if len(line) > 1]
    for i, line in enumerate(lines):
        s, e = line.split("~")
        start_pos = [int(n) for n in s.split(",")]
        end_pos = [int(n) for n in e.split(",")]
        mx = max(xy[0], start_pos[0], end_pos[0])
        my = max(xy[1], start_pos[1], end_pos[1])
        xy = (mx, my)
        zeds = (max(zeds[0], start_pos[2]), max(zeds[1], end_pos[2]))
        b = Brick(start_pos, end_pos, str(i))
        bricks.append(b)
        brick_info[str(i)] = b
    grid = [[["." for k in range(0, xy[0]+1)] for j in range(0, xy[1]+1)] for i in range(0, zeds[1]+1)]
    for j in range(0, xy[1]+1):
        for i in range(xy[0]+1):
            grid[0][j][i] = "#"
    bricks.sort()
    for brick in bricks:
        brick.drop(grid)
    deletions = 0
    for brick in bricks:
        if brick.can_delete():
            deletions += 1
    print(deletions)
    print(time.time() - startt)


def task2():
    startt = time.time()
    global xy, zeds, grid, bricks
    bricks = []
    with open("input") as file:
        lines = [line.rstrip() for line in file if len(line) > 1]
    for i, line in enumerate(lines):
        s, e = line.split("~")
        start_pos = [int(n) for n in s.split(",")]
        end_pos = [int(n) for n in e.split(",")]
        mx = max(xy[0], start_pos[0], end_pos[0])
        my = max(xy[1], start_pos[1], end_pos[1])
        xy = (mx, my)
        zeds = (max(zeds[0], start_pos[2]), max(zeds[1], end_pos[2]))
        b = Brick(start_pos, end_pos, str(i))
        bricks.append(b)
        brick_info[str(i)] = b
    grid = [[["." for k in range(0, xy[0]+1)] for j in range(0, xy[1]+1)] for i in range(0, zeds[1]+1)]
    for j in range(0, xy[1]+1):
        for i in range(xy[0]+1):
            grid[0][j][i] = "#"
    bricks.sort()
    for brick in bricks:
        brick.drop(grid)
    deletions = 0
    bricks = sorted(bricks, reverse=True)
    for brick in bricks:
        falls = brick.chain_reaction(set())
        deletions += falls
        print(f"{brick.name}: {falls} falls")
    print(deletions)
    print(time.time() - startt)


if __name__ == '__main__':
    #task1()
    task2()
