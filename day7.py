import multiprocessing
import time
from collections import deque

if False:
    s = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""
else:
    with open("input_day7.txt") as f:
        s = f.read()

def gen_combinations(nums, combinations, operations, i=0, so_far=[]):
    if i == len(nums) - 1:
        gen_combinations(nums, combinations, operations, i + 1, so_far + [nums[-1]])
    elif i >= len(nums):
        combinations.append(so_far)
    else:
        for op in operations:
            gen_combinations(nums, combinations, operations, i + 1, so_far + [nums[i], op])

def found_result(total, combinations):
    for comb in combinations:
        comb = deque(comb)
        while len(comb) > 1:
            last_num = comb.popleft()
            op = comb.popleft()
            next_num = comb.popleft()
            if op == "+":
                next_num = last_num + next_num
            elif op == "*":
                next_num = last_num * next_num
            elif op == "|":
                next_num = int(str(last_num) + str(next_num))
            comb.appendleft(next_num)
        
        res = comb.popleft()
        if res == total:
            return True

    return False

def compute_calibration(line, operations):
    if not line:
        return 0
    parts = line.split(":")
    expected_total = int(parts[0])
    numbers = [int(x) for x in parts[1].split()]
    combinations = []
    gen_combinations(numbers, combinations, operations)
    if found_result(expected_total, combinations):
        return expected_total
    return 0

print("Part 1")
start_time = time.time()
def part1(line):
    return compute_calibration(line, ["+", "*"])
with multiprocessing.Pool() as pool:
    results = pool.map(part1, s.split("\n"))
print(sum(results))
elapsed_time = time.time() - start_time
print(f"Execution time: {elapsed_time} seconds")

print("Part 2")
start_time = time.time()
def part2(line):
    return compute_calibration(line, ["+", "*", "|"])
with multiprocessing.Pool() as pool:
    results = pool.map(part2, s.split("\n"))
print(sum(results))
elapsed_time = time.time() - start_time
print(f"Execution time: {elapsed_time} seconds")
