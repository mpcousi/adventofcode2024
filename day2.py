import time

if False:
    s = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""
else:
    with open("input_day2.txt") as f:
        s = f.read()

all_nums = []
for line in s.split("\n"):
    if line:
        all_nums.append([int(x) for x in line.split()])

def is_safe(nums):
    is_increasing = None
    last_n = nums[0]
    
    for n in nums[1:]:
        if n == last_n:
            return False
        
        if is_increasing is None:
            is_increasing = n > last_n
        
        if (is_increasing and n < last_n) or (not is_increasing and n > last_n):
            return False

        diff = abs(n - last_n)
        if diff < 1 or diff > 3:
            return False

        last_n = n
    
    return True

def is_safe_remove_one(nums):
    for i in range(len(nums)):
        if is_safe(nums[:i] + nums[i+1:]):
            return True
    
    return False

print("Part 1")
start_time = time.time()
num_safe = 0
for nums in all_nums:
    if is_safe(nums):
        num_safe += 1

print(num_safe)
elapsed_time = time.time() - start_time
print(f"Execution time: {elapsed_time} seconds")

print("Part 2")
start_time = time.time()
num_safe_remove_one = 0
for nums in all_nums:
    if is_safe_remove_one(nums):
        num_safe_remove_one += 1

print(num_safe_remove_one)
elapsed_time = time.time() - start_time
print(f"Execution time: {elapsed_time} seconds")