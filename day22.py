import time
from collections import deque

if False:
    s = """1
2
3
2024"""
else:
    with open("input_day22.txt") as f:
        s = f.read()

secrets = []
for line in s.split():
    secrets.append(int(line))

def next_secret(previous_secret):
    step1 = (previous_secret ^ (previous_secret * 64)) % 16777216
    step2 = (step1 ^ (step1 // 32)) % 16777216
    step3 = (step2 ^ (step2 * 2048)) % 16777216
    return step3

def next_secret_n(secret, num_times):
    for _ in range(num_times):
        secret = next_secret(secret)
    return secret

def highest_last_four_diffs(secret, num_times):
    highest_changes = {}
    last_four_diffs = deque()
    last_price = secret % 10
    for i in range(num_times):
        secret = next_secret(secret)
        price = secret % 10
        diff_price = price - last_price

        last_four_diffs.append(diff_price)
        if i > 3:
            last_four_diffs.popleft()
        if i > 2:
            node = tuple(last_four_diffs)
            if node not in highest_changes:
                highest_changes[node] = price
        last_price = price
    
    return highest_changes

def get_combined_highest(all_changes):
    combined_highest_changes = {}
    for secret in all_changes:
        for node in all_changes[secret]:
            combined_highest_changes[node] = combined_highest_changes.get(node, 0) + all_changes[secret][node]

    max_val = None
    best_sequence = None
    for node in combined_highest_changes:
        if max_val is None or max_val < combined_highest_changes[node]:
            best_sequence = node
            max_val = combined_highest_changes[node]
    
    return max_val, best_sequence

num_secrets = 2000

print("Part 1")
start_time = time.time()
total = 0
for secret in secrets:
    total += next_secret_n(secret, num_secrets)
elapsed_time = time.time() - start_time
print(total)
print(f"Execution time: {elapsed_time} seconds")

print("Part 2")
start_time = time.time()
all_changes = {}
for secret in secrets:
    all_changes[secret] = highest_last_four_diffs(secret, num_secrets)
max_val, best_sequence = get_combined_highest(all_changes)
elapsed_time = time.time() - start_time
print(best_sequence)
print(max_val)
print(f"Execution time: {elapsed_time} seconds")
