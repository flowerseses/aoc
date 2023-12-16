import time
import re

seen = {}

def task1():
    start = time.time()
    total = 0
    data = []
    patterns = []
    with open("input_n") as file:
        # replace all special regex characters to not have to escaoe all things
        lines = [line.rstrip() for line in file if len(line) > 1]
    for line in lines:
        info, pats = line.split()
        pattern = [int(p) for p in pats.split(",")]
        count = find_seq(info, pattern)
        total += count
        print(f"{count} combinations for {info}: {pattern}")
    print(total)
    print(time.time() - start)


def find_seq(line, sequences):
    key = line, tuple(sequences)
    #print(key)
    if key in seen:
        return seen[key]
    score = find_seq_sub(line, sequences)
    seen[key] = score
    return score


def find_seq_sub(line, sequence):
    count_left = sum(sequence)
    if len(line) < count_left:
        return 0
    if line == "":
        if count_left > 0:
            return 0
        return 1
    if line[0] == ".":
        return find_seq(line[1:], sequence)
    if line[0] == "?":
        remaining_valid = line.count(r"#") + line.count(r"?")
        if remaining_valid > count_left:
            return find_seq("." + line[1:], sequence) + find_seq("#" + line[1:], sequence)
        return find_seq("#" + line[1:], sequence)
    if line[0] == "#":
        if len(sequence) == 0:
            return 0
        pat = re.compile(f"[#\?]{{{sequence[0]}}}")
        pat2 = re.compile(f"[#\?]{{{sequence[0]}}}#")
        if not pat.match(line):
            return 0
        if len(line) == sequence[0] and len(sequence) == 1:
            return 1
        if pat2.match(line):
            return 0

        return find_seq(line[sequence[0]+1:], sequence[1:])


def task2():
    start = time.time()
    total = 0
    data = []
    patterns = []
    with open("input1") as file:
        # replace all special regex characters to not have to escaoe all things
        lines = [line.rstrip() for line in file if len(line) > 1]
    for line in lines:
        info, pats = line.split()
        pattern = [int(p) for p in pats.split(",")]
        unfolded = f"{info}?"*5
        full_pat = pattern*5
        print(f"{unfolded} - {full_pat}")
        count = find_seq(unfolded[:], full_pat)
        total += count
        print(f"{count} combinations for {info}: {pattern}")
    print(total)
    print(time.time() - start)

if __name__ == '__main__':
    #task1()
    task2()
