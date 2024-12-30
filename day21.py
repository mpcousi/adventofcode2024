import time
from collections import deque

if False:
    s = """029A
980A
179A
456A
379A"""
else:
    with open("input_day21.txt") as f:
        s = f.read()

codes = []
for line in s.split():
    codes.append([x for x in line])

keypad_grids = {
    1: [["7", "8", "9"],
        ["4", "5", "6"],
        ["1", "2", "3"],
        ["#", "0", "A"]],
    2: [["#", "^", "A"],
        ["<", "v", ">"]]
}

character_positions = {}
for keypad_id in keypad_grids:
    character_positions[keypad_id] = {}
    for y in range(len(keypad_grids[keypad_id])):
        for x in range(len(keypad_grids[keypad_id][0])):
            character_positions[keypad_id][keypad_grids[keypad_id][y][x]] = (x, y)

memo_shortest_path = {}
def shortest_path(start, end, num_robots, keypad_id):
    node = (start[0], start[1], end[0], end[1], num_robots, keypad_id)
    if node in memo_shortest_path:
        return memo_shortest_path[node]

    queue = deque([(start[0], start[1], [])])
    result = None

    while queue:
        x, y, moves = queue.pop()

        if x == end[0] and y == end[1]:
            num_moves = count_moves(moves + ["A"], num_robots, 2)
            result = min(result, num_moves) if result else num_moves
            continue
        elif keypad_grids[keypad_id][y][x] == "#":
            # obstacle
            continue

        if x < end[0]:
            queue.append((x + 1, y, moves + [">"]))
        elif x > end[0]:
            queue.append((x - 1, y, moves + ["<"]))
        
        if y < end[1]:
            queue.append((x, y + 1, moves + ["v"]))
        elif y > end[1]:
            queue.append((x, y - 1, moves + ["^"]))

    memo_shortest_path[node] = result
    return result

def count_moves(code, num_robots, keypad_id):
    if num_robots == 0:
        return len(code)
    
    num_moves = 0
    position = character_positions[keypad_id]["A"]
    for character in code:
        next_position = character_positions[keypad_id][character]
        num_moves += shortest_path(position, next_position, num_robots - 1, keypad_id)
        position = next_position
    return num_moves

def compute_complexity(codes, num_robots):
    total = 0
    for code in codes:
        numeric_code = int("".join([x for x in code if x.isdigit()]))
        num_moves = count_moves(code, num_robots, 1)
        total += numeric_code * num_moves
    return total

print("Part 1")
start_time = time.time()
print(compute_complexity(codes, 3))
elapsed_time = time.time() - start_time
print(f"Execution time: {elapsed_time} seconds")

print("Part 2")
start_time = time.time()
print(compute_complexity(codes, 26))
elapsed_time = time.time() - start_time
print(f"Execution time: {elapsed_time} seconds")
