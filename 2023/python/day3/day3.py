import re
import time

symbols = "(!|@|\#|\$|%|\&|\*|\-|_|=|\+|/|\?)"
numbers = {}
symbs = []


def task1():
    start = time.time()
    total = 0
    line_num = 1
    with open("input") as file:
        lines = [line.rstrip() for line in file]
    for line in lines:
        res = re.finditer(symbols, line)
        nums = re.finditer("(\d+)", line)
        nums_in_line = []
        for j in nums:
            n = {"start": j.start(), "end": j.end() - 1, "num": int(j.group()), "used": False}
            nums_in_line.append(n)
        for i in res:
            symbs.append({"pos": i.start(), "line": line_num, "val": i.group()})
        numbers[line_num] = nums_in_line
        line_num += 1
    for symbol in symbs:
        total += get_sum_from_pos(symbol["line"], symbol["pos"])
    print(total)
    print(time.time() - start)


def task2():
    start = time.time()
    total = 0
    line_num = 1
    with open("input") as file:
        lines = [line.rstrip() for line in file]
    for line in lines:
        res = re.finditer("(\*)", line)
        nums = re.finditer("(\d+)", line)
        nums_in_line = []
        for j in nums:
            n = {"start": j.start(), "end": j.end() - 1, "num": int(j.group()), "used": False}
            nums_in_line.append(n)
        for i in res:
            symbs.append({"pos": i.start(), "line": line_num, "val": i.group()})
        numbers[line_num] = nums_in_line
        line_num += 1
    for symbol in symbs:
        total += get_gears_from_pos(symbol["line"], symbol["pos"])
    print(total)
    print(time.time() - start)


def get_sum_from_pos(line, pos):
    total = 0
    for line in range(line-1, line+2):
        for n in numbers[line]:
            if not n["used"] and (n["start"] == pos + 1 or n["end"] == pos - 1 or (n["start"] <= pos <= n["end"])):
                total += n["num"]
                n["used"] = True
    return total


def get_gears_from_pos(line, pos):
    adjacent = []
    for line in range(line-1, line+2):
        for n in numbers[line]:
            if n["start"] == pos + 1 or n["end"] == pos - 1 or (n["start"] <= pos <= n["end"]):
                adjacent.append(n["num"])
    if len(adjacent) == 2:
        return adjacent[0]*adjacent[1]
    return 0


if __name__ == '__main__':
    task1()
    task2()
