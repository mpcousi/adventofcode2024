import heapq
import multiprocessing
import time

if False:
    s = """5,4
    4,2
    4,5
    3,0
    2,1
    6,3
    2,4
    1,5
    0,6
    3,3
    2,6
    5,1
    1,2
    5,5
    2,5
    6,5
    1,4
    0,4
    6,4
    1,1
    6,1
    1,0
    0,5
    1,6
    2,0"""
    n = 7
    num_bytes = 12
else:
    with open("input_day18.txt") as f:
        s = f.read()
    n = 71
    num_bytes = 1024


corruptions = []
for line in s.split():
    corruptions.append([int(x) for x in line.split(",")])

def create_grid(n):
    grid = []
    for _ in range(n):
        grid.append(["." for _ in range(n)])
    return grid

def print_grid(grid, coord=None):
    for y in range(n):
        for x in range(n):
            if coord and x == coord[0] and y == coord[1]:
                print("O", end="")
            else:
                print(grid[y][x], end="")
        
        print()

def apply_corruptions(grid, corruptions, first_corruption, num_corruptions):
    for i in range(first_corruption, first_corruption + num_corruptions):
        x,y = corruptions[i]
        grid[y][x] = "#"
    return grid

def find_shortest_path(start, end, grid):
    queue = [(0, start[0], start[1])]
    distances = {(start[0], start[1]): 0}

    while queue:
        distance, x, y = heapq.heappop(queue)

        if x == end[0] and y == end[1]:
            return distance

        if distance > distances[(x,y)]:
            continue

        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            x2 = x + dx
            y2 = y + dy
            new_distance = distance + 1

            if x2 < 0 or x2 >= n or y2 < 0 or y2 >= n or grid[y2][x2] == "#":
                continue

            if (x2,y2) not in distances or new_distance < distances[(x2,y2)]:
                distances[(x2,y2)] = new_distance
                heapq.heappush(queue, (new_distance, x2, y2))

def part2(i):
    grid = create_grid(n)
    grid = apply_corruptions(grid, corruptions, 0, i)
    if not find_shortest_path((0,0), (n-1, n-1), grid):
        return i
    else:
        return len(corruptions)

print("Part 1")
start_time = time.time()
grid = create_grid(n)
grid = apply_corruptions(grid, corruptions, 0, num_bytes)
distance = find_shortest_path((0,0), (n-1, n-1), grid)
print(distance)
elapsed_time = time.time() - start_time
print(f"Execution time: {elapsed_time} seconds")

print("Part 2")
start_time = time.time()
with multiprocessing.Pool() as pool:
    results = pool.map(part2, range(1, len(corruptions)))
print(corruptions[min(results) - 1])
elapsed_time = time.time() - start_time
print(f"Execution time: {elapsed_time} seconds")
