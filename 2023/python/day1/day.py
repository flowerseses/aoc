import re

digits = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}

with open("input") as file:
    lines = [line.rstrip() for line in file]
task1 = 0
task2 = 0
regex = r"(?=(one|two|three|four|five|six|seven|eight|nine|\d))"
for line in lines:
    matches = re.findall("(\d)", line)
    task1 += int(matches[0])*10 + int(matches[-1])
    matches = [match for match in re.finditer(regex, line)]
    first = matches[0].groups()[0]
    last = matches[-1].groups()[0]
    a = int(first) if first.isdigit() else digits[first]
    b = int(last) if last.isdigit() else digits[last]
    task2 += a * 10 + b
print(task1)
print(task2)
