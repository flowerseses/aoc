import time
import math


def task1():
    start = time.time()
    with open("input") as file:
        lines = [line.rstrip() for line in file if len(line) > 1]
    instructions = [int(i) for i in list(lines[0].replace("L", "0").replace("R", "1"))]
    del(lines[0])
    positions = []
    nodemap = {}
    end_node = -1
    start_node = -1
    for line in lines:
        node = line.split(" = ")[0]
        positions.append(node)
        nodemap[node] = len(positions) - 1
        if node == "AAA":
            start_node = len(positions) - 1
        if node == "ZZZ":
            end_node = len(positions) - 1
    nodes = [None]*len(lines)
    for line in lines:
        node = line.split(" = ")[0]
        links = line.split(" = ")[1].replace("(", "").replace(")", "").split(", ")
        node_pos = nodemap[node]
        nodes[node_pos] = (nodemap[links[0]], nodemap[links[1]])
    current_node = start_node
    steps = 0
    while current_node != end_node:
        current_node = nodes[current_node][instructions[steps % len(instructions)]]
        steps += 1
    print(steps)
    print(time.time() - start)


def task2():
    start = time.time()
    with open("input") as file:
        lines = [line.rstrip() for line in file if len(line) > 1]
    instructions = [int(i) for i in list(lines[0].replace("L", "0").replace("R", "1"))]
    del(lines[0])
    positions = []
    nodemap = {}
    end_nodes = []
    start_nodes = []
    min_paths = []
    for line in lines:
        node = line.split(" = ")[0]
        positions.append(node)
        nodemap[node] = len(positions) - 1
        if node.endswith("A"):
            start_nodes.append(len(positions) - 1)
            min_paths.append(-1)
        if node.endswith("Z"):
            end_nodes.append(len(positions) - 1)
    nodes = [None]*len(lines)
    for line in lines:
        node = line.split(" = ")[0]
        links = line.split(" = ")[1].replace("(", "").replace(")", "").split(", ")
        node_pos = nodemap[node]
        nodes[node_pos] = (nodemap[links[0]], nodemap[links[1]])
    for i in range(0, len(start_nodes)):
        current_node = start_nodes[i]
        steps = 0
        while current_node not in end_nodes:
            current_node = nodes[current_node][instructions[steps % len(instructions)]]
            steps += 1
        min_paths[i] = steps
    print(math.lcm(*min_paths))
    print(time.time() - start)


if __name__ == '__main__':
    task1()
    task2()
