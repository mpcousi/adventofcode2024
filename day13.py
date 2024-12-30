import re
import time

if False:
    s = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""
else:
    with open("input_day13.txt") as f:
        s = f.read()

machine = {}
machines = []
for line in s.split("\n"):
    if not line:
        if machine:
            machines.append(machine)
            machine = {}
    else:
        nums = [int(x) for x in re.findall(r"\d+", line)]
        if line.startswith("Button A"):
            machine["A"] = nums
        elif line.startswith("Button B"):
            machine["B"] = nums
        elif line.startswith("Prize"):
            machine["Prize"] = nums

if machine:
    machines.append(machine)

def part1(a, b, prize):
    min_cost = None

    for i in range(101):
        for j in range(101):
            x = i * a[0] + j * b[0]
            y = i * a[1] + j * b[1]
            if x == prize[0] and y == prize[1]:
                cost = 3 * i + j
                if min_cost:
                    min_cost = min(min_cost, cost)
                else:
                    min_cost = cost

    if min_cost:
        return min_cost
    else:
        return 0

def is_integer(n):
    return abs(round(n) - n) < 0.0001

def part2(a, b, prize):
    num_b = (((a[1] * prize[0]) / a[0]) - prize[1]) / (((a[1] * b[0]) / a[0]) - b[1])
    num_a = (prize[0] - b[0] * num_b) / a[0]

    if is_integer(num_a) and is_integer(num_b):
        return round(num_a) * 3 + round(num_b)
    else:
        return 0

start_time = time.time()
total = 0
for machine in machines:
    total += part1(machine["A"], machine["B"], machine["Prize"])
print(total)
elapsed_time = time.time() - start_time
print(f"Execution time: {elapsed_time} seconds")

start_time = time.time()
total = 0
for machine in machines:
    for i in range(2):
        machine["Prize"][i] += 10000000000000
    total += part2(machine["A"], machine["B"], machine["Prize"])
print(total)
elapsed_time = time.time() - start_time
print(f"Execution time: {elapsed_time} seconds")
