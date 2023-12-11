import time
bag1 = {"red": 12, "green": 13, "blue": 14}


def task1():
    start = time.time()
    total = 0
    with open("input") as file:
        lines = [line.rstrip() for line in file]
    for line in lines:
        parts = line.split(":")
        game_num = int(parts[0].split(" ")[1])
        groups = parts[1].split(";")
        valid = True
        for group in groups:
            balls = group.split(", ")
            for ball in balls:
                ball = ball.strip()
                count = ball.split(" ")
                if bag1[count[1]] < int(count[0]):
                    valid = False
                    break
            if not valid:
                break
        if valid:
            total += game_num
    print(total)
    print(time.time() - start)


def task2():
    start = time.time()
    total = 0
    with open("input") as file:
        lines = [line.rstrip() for line in file]
    for line in lines:
        parts = line.split(":")
        min_values = [0, 0, 0]
        groups = parts[1].split(";")
        for group in groups:
            balls = group.split(", ")
            for ball in balls:
                ball = ball.strip()
                count = ball.split(" ")
                color = count[1].strip()
                num = int(count[0].strip())
                if color == "red":
                    if min_values[0] < num:
                        min_values[0] = num
                elif color == "green":
                    if min_values[1] < num:
                        min_values[1] = num
                else:
                    if min_values[2] < num:
                        min_values[2] = num

        power = min_values[0]*min_values[1]*min_values[2]
        total += power
    print(total)
    print(time.time() - start)


if __name__ == '__main__':
    task1()
    task2()
