import time
faces = {"A": 14, "K": 13, "Q": 12, "J": 1, "T": 10}


def task2():
    start = time.time()
    with open("input") as file:
        lines = [(line.split()[0].rstrip(), line.split()[1]) for line in file if len(line) > 1]
    output = []
    for line in lines:
        res = (get_score(line[0]), line[0], line[1])
        output.append(res)
    output = sorted(output, key=lambda i: i[0])
    total = 0
    for i in range(0, len(output)):
        total += (i+1)*int(output[i][2])
    print(total)
    print(time.time() - start)


def get_score(hand):
    chars = [(c, hand.count(c)) for c in set(hand)]
    jokers = hand.count("J")
    maxc = 0
    numtwos = 0
    for c in chars:
        if c[0] == "J":
            continue
        maxc = max(maxc, c[1] + jokers)
        if c[1] == 2:
            numtwos += 1
    score = 7
    match maxc:
        case 4:
            score = 6
        case 3:
            if ("J" in hand and numtwos == 2) or "J" not in hand and numtwos == 1:
                score = 5
            else:
                score = 4
        case 2:
            if numtwos == 2:
                score = 3
            else:
                score = 2
        case 1:
            score = 1
    for i in range(0, len(hand)):
        if hand[i] not in faces.keys():
            score = 100*score + int(hand[i])
        else:
            score = 100*score + faces[hand[i]]
    return score


if __name__ == '__main__':
    task2()
