import time


def task1():
    start = time.time()
    lines = []
    with open("input") as file:
        for line in file.readlines():
            lines.append([int(num) for num in line.split()])
    total = 0
    for line in lines:
        prediction = get_prediction(line)
        total += prediction
    print(total)
    print(time.time() - start)


def task2():
    start = time.time()
    lines = []
    with open("input") as file:
        for line in file.readlines():
            lines.append([int(num) for num in line.split()])
    lt = 0
    rt = 0
    total = 0
    for line in lines:
        l = get_past(line)
        r = get_prediction(line)
        print(f"{l}, {r}")
        lt += l
        rt += r
    print(lt+rt)
    print(time.time() - start)

def get_past(numbers):
    if all(n == 0 for n in numbers):
        return 0
    nums = [m - n for n, m in zip(numbers, numbers[1:])]
    prediction = get_past(nums)
    return numbers[0] - prediction


def get_prediction(numbers):
    if all(n == 0 for n in numbers):
        return 0
    nums = [m - n for n, m in zip(numbers, numbers[1:])]
    prediction = get_prediction(nums)
    return prediction + numbers[-1]


if __name__ == '__main__':
    task1()
    task2()
