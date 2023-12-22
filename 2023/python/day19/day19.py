import time
import re
from pprint import pprint
from copy import deepcopy

maxv = 4001
minv = 1

transforms = {
    "x": 0,
    "m": 1,
    "a": 2,
    "s": 3,
}


def task1():
    start = time.time()
    with open("input") as file:
        lines = [line for line in file]
    rules = {}
    objs = []
    for i, line in enumerate(lines):
        if len(line) <= 1:
            break
        name, c = line.rstrip()[:-1].split("{")
        rules[name] = get_rule(c)
    for j in range(i+1, len(lines)):
        objs.append(get_obj(lines[j]))
    total = 0
    for elem in objs:
        next_rule = "in"
        while next_rule not in ("R", "A"):
            rule = rules[next_rule]
            for check in rule:
                if check[0] is None:
                    next_rule = check[1]
                    break
                params = check[0]
                if params[1] == ">":
                    if elem[params[0]] > params[2]:
                        next_rule = check[1]
                        break
                else:
                    if elem[params[0]] < params[2]:
                        next_rule = check[1]
                        break
        if next_rule == "A":
            e_sum = get_sum(elem)
            total += e_sum
    print(total)
    print(time.time() - start)


def get_sum(o):
    res = 0
    for k, v in o.items():
        res += v
    return res


def get_obj(o):
    obj = {}
    params = o.rstrip()[1:-1].split(",")
    for param in params:
        n, v = param.split("=")
        obj[n] = int(v)
    return obj


def get_rule(s):
    rules = s.split(",")
    res = []
    for rule in rules:
        if ":" in rule:
            cond, dest = rule.split(":")
            param, rel, count = re.split("([<>])", cond)
            count = int(count)
            res.append(((transforms[param], rel, count), dest))
        else:
            res.append((None, rule))
    return res


def task2():
    start = time.time()
    with open("input") as file:
        lines = [line for line in file]
    rules = {}
    for i, line in enumerate(lines):
        if len(line) <= 1:
            break
        name, c = line.rstrip()[:-1].split("{")
        rules[name] = get_rule(c)
    rules_to_check = []
    rules_to_check.append(("in", [(minv, maxv), (minv, maxv), (minv, maxv), (minv, maxv)]))
    total = 0
    while True:
        if not rules_to_check:
            break
        rule = rules_to_check.pop(0)
        if rule[0] == "A":
            constraints = rule[1]
            x = constraints[0]
            m = constraints[1]
            a = constraints[2]
            s = constraints[3]
            sum = (x[1] - x[0]) * (m[1] - m[0]) * (a[1] - a[0]) * (s[1] - s[0])
            total += sum
            continue
        elif rule[0] == "R":
            continue
        outputs = check_rule(rules[rule[0]], rule[1])
        rules_to_check.extend(outputs)
    print(total)
    print(time.time() - start)


def check_rule(rule, ranges):
    out = []
    remaining = ranges
    for param in rule:
        if param[0] is None:
            out.append((param[1], remaining))
            continue
        info = param[0]
        ppos = info[0]
        incl = deepcopy(remaining)
        excl = deepcopy(remaining)
        left, right = remaining[ppos]
        if info[1] == ">":
            incl[ppos] = (info[2] + 1, right)
            excl[ppos] = (left, info[2] + 1)
        else:
            incl[ppos] = (left, info[2])
            excl[ppos] = (info[2], right)
        out.append((param[1], incl))
        remaining = excl
    return out


if __name__ == '__main__':
    #task1()
    task2()
