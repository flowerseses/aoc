import time

corners = "FLJ7"
valid_chars = {
    "F": (1, 1),
    "-": (-1, 1),
    "|": (-1, 1),
    "L": (1, -1),
    "J": (-1, -1),
    "7": (-1, 1),
    "S": (0, 0),
}
discount = {
    "F": "7",
    "L": "J",
    "J": "",
    "7": "",
}
checks = [(-1, 0), (0, -1), (1, 0), (0, 1)]
values = []


def task1():
    start = time.time()
    startx = 0
    starty = 0
    lines = []
    line_num = 0
    with open("input") as file:
        for line in file.readlines():
            lines.append(list(line.rstrip()))
            values.append([-1 for i in list(line.rstrip())])
            if "S" in line:
                starty = line_num
                startx = line.index("S")
                values[starty][startx] = 0
            line_num += 1

    start_points = []
    for point in checks:
        if connected(lines, (startx, starty), (startx+point[0], starty+point[1])):
            start_points.append((startx+point[0], starty+point[1]))
            values[starty+point[1]][startx+point[0]] = 1
    res = calc_max_dist(lines, (startx, starty), start_points)
    print(res)
    print(time.time() - start)


def calc_max_dist(lines, start, next_points):
    done = False
    prev = [start, start]
    max_v = 0
    while not done:
        for i in range(0, 2):
            x = next_points[i][0]
            y = next_points[i][1]
            current_value = values[y][x]
            elem = lines[y][x]
            if elem in corners:
                if prev[i][0] == x:
                    next_point = (x+valid_chars[elem][0], y)
                else:
                    next_point = (x, y+valid_chars[elem][1])
            elif elem == "-":  # assume we can't hit a wall
                if prev[i][0] < x:
                    next_point = (x+1, y)
                else:
                    next_point = (x-1, y)
            elif elem == "|":
                if prev[i][1] > y:
                    next_point = (x, y-1)
                else:
                    next_point = (x, y+1)
            if values[next_point[1]][next_point[0]] >= 0:
                max_v = max(max_v, values[next_point[1]][next_point[0]])
                done = True
            else:
                values[next_point[1]][next_point[0]] = current_value + 1
                prev[i] = next_points[i]
                next_points[i] = next_point
    return max_v


def connected(lines, pos1, pos2):
    posx = pos2[0]
    posy = pos2[1]
    elem = lines[posy][posx]
    if elem in valid_chars.keys():
        if elem in corners:
            if posx + valid_chars[elem][0] == pos1[0] or posy + valid_chars[elem][1] == pos1[1]:
                return True
        elif elem == "-":
            if posx + valid_chars[elem][0] == pos1[0] or posx + valid_chars[elem][1] == pos1[0]:
                return True
        elif elem == "|":
            if posy + valid_chars[elem][0] == pos1[1] or posy + valid_chars[elem][1] == pos1[1]:
                return True
    return False


def task2():
    start = time.time()
    startx = 0
    starty = 0
    lines = []
    inside = []
    line_num = 0
    with open("input") as file:
        for line in file.readlines():
            lines.append(list(line.rstrip()))
            values.append([-1 for i in list(line.rstrip())])
            inside.append(list(line.rstrip()))
            if "S" in line:
                starty = line_num
                startx = line.index("S")
                values[starty][startx] = 0
            line_num += 1

    start_points = []
    replace_start(lines, startx, starty)
    for point in checks:
        if connected(lines, (startx, starty), (startx+point[0], starty+point[1])):
            start_points.append((startx+point[0], starty+point[1]))
            values[starty+point[1]][startx+point[0]] = 1
    calc_max_dist(lines, (startx, starty), start_points)
    for j in range(len(lines)):
        for i in range(len(lines[j])):
            if values[j][i] < 0:
                lines[j][i] = "."
    cast_some_rays(lines, inside)
    print(time.time() - start)


def replace_start(lines, x, y):
    start_points = []
    for point in checks:
        if connected(lines, (x, y), (x+point[0], y+point[1])):
            start_points.append((point[0], point[1]))
    else:
        if start_points[0][0] == -1:
            if start_points[1][1] == -1:
                lines[y][x] = "J"
            elif start_points[1][1] == 0:
                lines[y][x] = "-"
            else:
                lines[y][x] = "7"
        elif start_points[0][0] == 0:
            if start_points[1][1] == 0:
                lines[y][x] = "L"
            else:
                lines[y][x] = "|"
        else:
            lines[y][x] = "F"


def cast_some_rays(lines, inside):
    total = 0
    for j in range(len(lines)):
        yline = lines[j]
        hits = 0
        prev = "0"
        for i in range(len(yline)):
            line = lines[j]
            val = line[i]
            if val == "." and hits % 2 == 1:
                total += 1
                inside[j][i] = "I"
            elif val == "." and hits % 2 == 0:
                inside[j][i] = "O"
            else:
                elem = line[i]
                # edge casessss
                if elem in corners:
                    if prev == "0":
                        prev = elem
                    else:
                        if elem not in discount[prev]:
                            hits += 1
                        prev = "0"
                elif elem == "|":
                    # simple, trivial
                    hits += 1
                    prev = "0"
                elif elem == "-":
                    # simple, trivial as well, ignore
                    pass
    print(total)

if __name__ == '__main__':
    task1()
    task2()
