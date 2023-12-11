import time

def task1():
    start = time.time()
    total = 0
    with open("input") as file:
        lines = [line.rstrip() for line in file]
    for line in lines:
        line_total = 0
        data = line.split(": ")[1]
        numbs = data.split(" | ")
        win = get_sorted(numbs[0].strip())
        our = get_sorted(numbs[1].strip())
        for i in win:
            for j in our:
                if i == j:
                    line_total += 1
                    break
                if i < j:
                    break
        if line_total > 0:
            total += 2**(line_total-1)
    print(total)
    print(time.time() - start)


def task2():
    start = time.time()
    total = 0
    all_lines = []
    with open("input") as file:
        lines = [line.rstrip() for line in file]
        for line in lines:
            line_data = line.split(": ")
            all_lines.append({"count": 1, "val": line_data[1].strip()})
    for i in range(len(all_lines)):
        line = all_lines[i]
        line_total = 0
        my_total = line["count"]
        numbs = line["val"].split(" | ")
        win = get_sorted(numbs[0].strip())
        our = get_sorted(numbs[1].strip())
        done = False
        for j in win:
            for k in our:
                if j == k:
                    line_total += 1
                    break
                if j < k:
                    break
        if line_total > 0:
            for j in range(i+1, i+1+line_total):
                if j < len(all_lines):
                    all_lines[j]["count"] += my_total
        total += my_total
    print(total)
    print(time.time() - start)


def get_sorted(numbers):
    res = [int(i) for i in numbers.split()]
    res.sort()
    return res


if __name__ == '__main__':
    task1()
    task2()
