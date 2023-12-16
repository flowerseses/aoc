import time
import math
import re

test_string = "HASH"
boxes = {}
labels = {}


def task1():
    start = time.time()
    with open("input1") as file:
        line = file.readlines()
        words = line[0].rstrip().split(",")
    total = 0
    for word in words:
        if len(word) == 0:
            continue
        val = transform(word.strip())
        print(f"{word} - {val}")
        total += val
    print(total)

    print(time.time() - start)


def transform(word):
    total = 0
    for char in word:
        total += ord(char)
        total *= 17
        total = total % 256
    return total


def task2():
    start = time.time()
    total = 0
    with open("input") as file:
        line = file.readlines()
        words = line[0].rstrip().split(",")
    for word in words:
        process_lens(word)
    for box_num, lenses in boxes.items():
        box_score = 0
        if not lenses:
            continue
        a = 1 + box_num
        count = 1
        #print(box_num)
        for label, lens in lenses.items():
            b = count
            count += 1
            c = lens
            score = a*b*c
            total += score
            #print(f"{label}: {score}")
    print(total)
    print(time.time() - start)


def process_lens(lens):
    info = re.split("[=-]", lens)
    label = info[0]
    if label not in labels:
        labels[label] = transform(label)
    box = labels[label]
    if box not in boxes:
        boxes[box] = {}
    focal = -1
    if "=" in lens:
        focal = info[1]
        boxes[box][label] = int(focal)
    else:
        if label in boxes[box]:
            del boxes[box][label]
    #for count, box in boxes.items():
        #print(f"box {count}: {box}")




if __name__ == '__main__':
    #task1()
    task2()
