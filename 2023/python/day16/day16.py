import time

field = []
visited = set()
energized = set()


def task1():
    startt = time.time()
    with open("input") as file:
        lines = [line.rstrip() for line in file if len(line) > 1]
        for line in lines:
            field.append([c for c in line])
    max_e = 0
    global visited
    global energized
    for j in range(len(field)): # do left and right first
        visited = set()
        energized = set()
        start = (0, j)
        move(start, "r")
        max_e = max(max_e, len(energized))
        start = (len(field[j]) - 1, j)
        visited = set()
        energized = set()
        move(start, "l")
        max_e = max(max_e, len(energized))
    for j in range(len(field[0]) - 1):
        visited = set()
        energized = set()
        start = (j, 0)
        move(start, "d")
        max_e = max(max_e, len(energized))
        visited = set()
        energized = set()
        start = (j, len(field) - 1)
        move(start, "u")
        max_e = max(max_e, len(energized))
    print(max_e)
    print(time.time() - startt)


# could be cleaner/smarter
def move(start, d):
    movedir = (0, 0)
    if d == "l":
        movedir = (-1, 0)
        opp = "r"
    elif d == "r":
        movedir = (1, 0)
        opp = "l"
    elif d == "u":
        movedir = (0, -1)
        opp = "d"
    elif d == "d":
        movedir = (0, 1)
        opp = "u"
    current = (start[0], start[1])
    while 0 <= current[0] < len(field[0]) and 0 <= current[1] < len(field):
        i = current[0]
        j = current[1]
        place = (i, j, d)
        if place in visited:
            return
        if field[j][i] == "." or (d in ("l", "r") and field[j][i] == "-") or (d in ("d", "u") and field[j][i] == "|"):
            visit((i, j, d))
            visit((i, j, opp))
            current = (i + movedir[0], j + movedir[1])
        elif (d in ("l", "r") and field[j][i] == "|") or (d in ("d", "u") and field[j][i] == "-"):
            visit((i, j, d))
            visit((i, j, opp))
            if d in ("l", "r"):
                move((i, j-1), "u")
                move((i, j+1), "d")
            else:
                move((i-1, j), "l")
                move((i+1, j), "r")
            break
        elif d in ("l", "r"):
            if (field[j][i] == "\\" and d == "l") or (field[j][i] == "/" and d == "r"):
                visit((i, j, d))
                move((i, j-1), "u")
                break
            else:
                visit((i, j, d))
                move((i, j+1), "d")
                break
        else:
            if (field[j][i] == "\\" and d == "u") or (field[j][i] == "/" and d == "d"):
                visit((i, j, d))
                move((i-1, j), "l")
                break
            else:
                visit((i, j, d))
                move((i+1, j), "r")
                break


def visit(place):
    visited.add(place)
    if (place[0], place[1]) not in energized:
        energized.add((place[0], place[1]))


if __name__ == '__main__':
    task1()
