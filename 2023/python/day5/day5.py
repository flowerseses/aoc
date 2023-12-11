import time
from typing import List
maps = {}
all_maps = []

def task1():
    start = time.time()
    total = 0
    with open("input") as file:
        lines = [line.rstrip() for line in file if len(line) > 1]
    target_seeds = [int(i) for i in lines[0].split(": ")[1].split()]
    i = 1
    while i < len(lines):
        name = lines[i].split()[0]
        j = i + 1
        done = False
        mappings = {}
        while not done:
            if j >= len(lines):
                done = True
                i = j
                break
            if lines[j][0].isdigit():
                nums = lines[j].split()
                name_map = {"dest": int(nums[0]), "source": int(nums[1]), "count": int(nums[2])}
                mappings[name_map["source"]] = name_map
                j += 1
            else:
                i = j
                done = True
        maps[name] = mappings
    min_location = max(target_seeds)
    for seed in target_seeds:
        soil = find_val(maps["seed-to-soil"], seed)
        fert = find_val(maps["soil-to-fertilizer"], soil)
        water = find_val(maps["fertilizer-to-water"], fert)
        light = find_val(maps["water-to-light"], water)
        temp = find_val(maps["light-to-temperature"], light)
        humid = find_val(maps["temperature-to-humidity"], temp)
        location = find_val(maps["humidity-to-location"], humid)
        if location < min_location:
            min_location = location
    print(min_location)
    print(time.time() - start)


def task2():
    start = time.time()
    with open("input") as file:
        lines = [line.rstrip() for line in file if len(line) > 1]
    all_seeds = [int(i) for i in lines[0].split(": ")[1].split()]
    seeds = [(all_seeds[i], all_seeds[i+1] + all_seeds[i]) for i in range(0, len(all_seeds), 2)]
    i = 1
    while i < len(lines):
        name = lines[i].split()[0]
        j = i + 1
        done = False
        mappings = []
        while not done:
            if j >= len(lines):
                done = True
                i = j
                break
            if lines[j][0].isdigit():
                nums = lines[j].split()
                name_map = (int(nums[1]), int(nums[2]), int(nums[0]))
                mappings.append(name_map)
                j += 1
            else:
                i = j
                done = True
        all_maps.append(sorted(mappings, key=lambda x: x[0]))
    res = []
    sorted_seeds = sorted(seeds, key=lambda x: x[0])
    locations = slice_tuples(0, sorted_seeds)
    res.extend(locations)
    print(sorted(res, key=lambda x: x[0]))
    print(time.time() - start)


def slice_tuples(current: int, seeds: List[tuple]):
    ranges = []
    mapping = all_maps[current]
    for i in range(0, len(mapping)):
        m = mapping[i]
        ranges.append((m[0], m[0] + m[1], m[2] - m[0]))
        if i < len(mapping) - 1:
            n = mapping[i+1]
            if m[0] + m[1] < n[0]:
                ranges.append((m[0] + m[1], n[0], 0))
    ranges = sorted(ranges, key=lambda x: x[0])
    seed = 0
    rst = seeds[seed][0]
    rend = seeds[seed][1]
    output = []
    i = 0
    while i < len(ranges):
        curr = ranges[i]
        if rst < curr[0]:
            output.append((rst, min(rend, curr[0])))
            rst = min(rend, curr[0])
        if curr[0] <= rst < curr[1]:
            output.append((rst + curr[2], min(rend, curr[1]) + curr[2]))
            rst = min(rend, curr[1])
        if rst < rend:
            i += 1
        else:
            if seed < len(seeds) - 1:
                seed += 1
                rst = seeds[seed][0]
                rend = seeds[seed][1]
            else:
                break
    seed += 1
    if rst < rend:
        output.append((rst, rend))
    while seed < len(seeds):
        rst = seeds[seed][0]
        rend = seeds[seed][1]
        output.append((rst, rend))
        seed += 1
    output = sorted(output, key=lambda x: x[0])
    if current < len(all_maps) - 1:
        next_map = current + 1
        res = slice_tuples(next_map, output)
    else:
        res = output
    return res


def find_lowest(mapping: dict, seeds: tuple, next: str):
    sources = list(mapping.keys())
    range_start = seeds[0]
    range_end = seeds[1]
    sources.sort()
    if next == "location":
        next_mapping = None
        followup = None
    else:
        for k, v in maps.items():
            if k.startswith(next):
                next_mapping = v
                followup = k.split("-")[2]
                break
    ranges = []
    for i in range(0, len(sources)):
        if range_start >= range_end:
            break
        count = mapping[sources[i]]["count"]
        diff = mapping[sources[i]]["dest"] - sources[i]
        if range_start < sources[i]:
            endpoint = min(range_end, sources[i])
            ranges.append((range_start, endpoint))
            range_start = endpoint
            if range_end < sources[i]:
                break
        if sources[i] <= range_start < sources[i] + count:
            dest = range_start + diff
            dest_end = min(sources[i] + count, range_end) + diff
            ranges.append((dest, dest_end))
            range_start = min(sources[i] + count, range_end)
    if range_start < range_end:
        ranges.append((range_start, range_end))
    if next_mapping is not None:
        output = []
        for i in range(len(ranges)):
            res = find_lowest(next_mapping, ranges[i], followup)
            output.extend(res)
        res = output
    else:
        res = sorted(ranges, key=lambda x: x[0])
    return res


def find_val(mapping: dict, value: int):
    sources = list(mapping.keys())
    sources.sort()
    pos = len(sources) - 1
    while sources[pos] > value and pos >= 0:
        pos -= 1
    if pos < 0:
        return value
    vals = mapping[sources[pos]]
    if vals["source"] + vals["count"] < value:
        return value
    else:
        diff = value - vals["source"]
        return vals["dest"] + diff


if __name__ == '__main__':
    task1()
    task2()
