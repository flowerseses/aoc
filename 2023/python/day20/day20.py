import time
from queue import SimpleQueue
from copy import deepcopy
import re
from pprint import pprint
from math import lcm

###
### this whole thing is messier than it needs to be but oh well
###

signals = SimpleQueue()
mods = {}
memo = []
c_vals = {}
repeats = 1000
previouses = {}
counts = []
rx_sent = False
seen = {}
steps = 0


class Comms:
    name = ""
    state = 0
    ctype = "%"
    connected_modules = []

    def __init__(self, name, ctype, connected_modules):
        self.name = name
        self.ctype = ctype
        self.connected_modules = deepcopy(connected_modules)
        self.previous_state = {}
        for n in connected_modules:
            if n not in mods.keys():
                mods[n] = Comms(n, "-", [])

    def set_prev(self):
        for n in self.connected_modules:
            mod = mods[n]
            if mod.ctype in ("&", "-"):
                mod.previous_state[self.name] = 0

    def receive(self, source, p):
        sent = False
        if self.name == "rx" and p == 0:
            return True
        if self.ctype == "-":
            out = 0
        elif self.ctype == "%":
            if p:
                return sent
            self.state = 1 - self.state
            out = self.state
        else:
            self.previous_state[source] = p
            out = 0 if all(self.previous_state.values()) else 1
        counts[out] += len(self.connected_modules)
        if self.name in seen.keys() and out:
            seen[self.name] = steps
        for mod in self.connected_modules:
            signals.put((mod, self.name, out))
        return sent

    def __repr__(self):
        if self.ctype == "%":
            out = f"{self.name}:{'h' if self.state else 'l'}"
        elif self.ctype == "&":
            states = ",".join("{}:{}".format(k, v) for k, v in self.previous_state.items())
            out = f"{self.name}:{states}"
        else:
            out = f"{self.name}"
        return out


def task1():
    start = time.time()
    global counts
    with open("input") as file:
        lines = [line.rstrip() for line in file if len(line) > 1]
    for line in lines:
        name, conn_string = line.split(" -> ")
        conns = conn_string.split(", ")
        if re.match(r"^[%&]", name):
            ctype = name[0]
            name = name[1:]
        else:
            ctype = "-"
        if name in mods:
            mods[name] = Comms(mods[name].name, ctype, conns)
        else:
            mods[name] = Comms(name, ctype, conns)
    for mod in mods.values():
        mod.set_prev()
    totals = [0, 0]
    cycle_found = False
    for i in range(repeats):
        counts = [1, 0]
        signals.put(("broadcaster", None, 0))
        while not signals.empty():
            s = signals.get()
            mod = mods[s[0]]
            mod.receive(s[1], s[2])
        key = get_key()
        if key in memo:
            cycle_found = True
            print(f"found {key} in {memo} with values {c_vals[key]}")
            pend = i
            pstart = memo.index(key)
            if pstart != 0:
                totals = get_sum(0, pstart)
            print(f"cycle starts at {pstart} and ends at {pend-1}")
            cycle_s = get_sum(pstart, pend)
            num_c = (repeats-pstart) // i
            extras = (repeats-pstart) % i
            totals[0] += cycle_s[0]*num_c
            totals[1] += cycle_s[1]*num_c
            extra_s = get_sum(pstart, pstart + extras)
            totals[0] += extra_s[0]
            totals[1] += extra_s[1]
            break
        else:
            memo.append(key)
            c_vals[key] = counts
            #print(counts)
    if not cycle_found:
        totals = get_sum(0, repeats)
    print(totals)
    print(totals[0]*totals[1])
    print(time.time() - start)


def get_key():
    key = "||".join([str(mod) for mod in mods.values()])
    return key


def get_sum(start, end):
    sums = [0, 0]
    for i in range(start, end):
        sums[0] += c_vals[memo[i]][0]
        sums[1] += c_vals[memo[i]][1]
    return sums


def task2():
    start = time.time()
    global counts, seen, steps
    with open("input2") as file:
        lines = [line.rstrip() for line in file if len(line) > 1]
    for line in lines:
        name, conn_string = line.split(" -> ")
        conns = conn_string.split(", ")
        if re.match(r"^[%&]", name):
            ctype = name[0]
            name = name[1:]
        else:
            ctype = "-"
        if name in mods:
            mods[name] = Comms(mods[name].name, ctype, conns)
        else:
            mods[name] = Comms(name, ctype, conns)
    for mod in mods.values():
        mod.set_prev()
    # Note: this only works if there's just one entry into the final point. not a general solution
    last = list(mods["rx"].previous_state.keys())[0]
    seen = {}
    for k in mods[last].previous_state.keys():
        seen[k] = -1
    print(seen)
    while True:
        steps += 1
        counts = [1, 0]
        signals.put(("broadcaster", None, 0))
        while not signals.empty():
            s = signals.get()
            mod = mods[s[0]]
            mod.receive(s[1], s[2])
        done = True
        for k, v in seen.items():
            done = done and v > 0
        if done:
            break
    # This only works because of the problem setup and will *not* work for a generic version
    print(lcm(*seen.values()))
    print(time.time() - start)


if __name__ == '__main__':
    #task1()
    task2()
