import time

if False:
    s = "125 17"
else:
    with open("input_day11.txt") as f:
        s = f.read()

stones = [int(x) for x in s.split()]

class Num:
    def __init__(self, num, next=None):
        self.num = num
        self.next = next

def count_stones(root):
    n = 0
    while root:
        n += 1
        root = root.next

    return n

def blink(root):
    current = root
    old_next = None

    while current:
        if current.num == 0:
            current.num = 1
            current = current.next
        else:
            num_str = str(current.num)
            if len(num_str) % 2 == 0:
                old_next = current.next
                current.num = int(num_str[:len(num_str)//2])
                current.next = Num(int(num_str[len(num_str)//2:]), old_next)
                current = old_next
            else:
                current.num *= 2024
                current = current.next

    return root

def part1(stones, num_blinks):
    root = None
    prev = None
    for stone in stones:
        num = Num(stone)
        if not prev:
            root = num
        else:
            prev.next = num

        prev = num

    for i in range(num_blinks):
        root = blink(root)
    return root


def split_stone(stone, num_blinks_left, processed):
    if num_blinks_left == 0:
        return 1
    
    if (stone, num_blinks_left) in processed:
        return processed[(stone, num_blinks_left)]

    if stone == 0:
        result = split_stone(1, num_blinks_left - 1, processed)
    else:
        num_str = str(stone)
        if len(num_str) % 2 == 0:
            result = split_stone(int(num_str[:len(num_str)//2]), num_blinks_left - 1, processed) \
                + split_stone(int(num_str[len(num_str)//2:]), num_blinks_left - 1, processed)
        else:
            result = split_stone(stone * 2024, num_blinks_left - 1, processed)
    
    processed[(stone, num_blinks_left)] = result
    return result

def part2(stones, num_blinks):
    processed = {}
    result = 0
    for stone in stones:
        result += split_stone(stone, num_blinks, processed)
    return result

print("Part 1")
start_time = time.time()
print(count_stones(part1(stones, 25)))
elapsed_time = time.time() - start_time
print(f"Execution time: {elapsed_time} seconds")

print("Part 2")
start_time = time.time()
print(part2(stones, 75))
elapsed_time = time.time() - start_time
print(f"Execution time: {elapsed_time} seconds")