import heapq
import multiprocessing
import time

if False:
    s = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""
    min_save_time = 1
else:
    with open("input_day20.txt") as f:
        s = f.read()
    min_save_time = 100

grid = []
for line in s.split():
    grid.append(line)
n = len(grid)
m = len(grid[0])

start = None
end = None
for y in range(n):
    for x in range(m):
        if grid[y][x] == "S":
            start = (x,y)
        elif grid[y][x] == "E":
            end = (x,y)

def dijkstra(start, end, grid):
    queue = [(0, start[0], start[1])]
    previous = {(start[0], start[1]): None}
    distances = {(start[0], start[1]): 0}

    while queue:
        distance, x, y = heapq.heappop(queue)

        if x == end[0] and y == end[1]:
            return previous

        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            x2 = x + dx
            y2 = y + dy
            if x2 < 0 or x2 >= m or y2 < 0 or y2 >= n or grid[y][x] == "#":
                continue

            distance2 = distance + 1
            if (x2,y2) not in distances or distance2 < distances[(x2,y2)]:
                distances[(x2,y2)] = distance2
                heapq.heappush(queue, (distance2, x2, y2))
                previous[(x2,y2)] = (x,y)

start_time = time.time()
previous = dijkstra(start, end, grid)

path = [end]
current = end
while current != start:
    current = previous[current]
    path.append(current)

path_size = len(path)

def count_cheats(i):
    part1 = 0
    part2 = 0
    for j in range(i + min_save_time + 2, path_size):
        distance = abs(path[j][0] - path[i][0]) + abs(path[j][1] - path[i][1])
        if j - i - distance < min_save_time:
            continue

        if distance == 2:
            part1 += 1
        if distance <= 20:
            part2 += 1
    
    return part1, part2

with multiprocessing.Pool() as pool:
    results = pool.map(count_cheats, range(path_size))
print("Part 1")
print(sum([x[0] for x in results]))
print("Part 2")
print(sum([x[1] for x in results]))
elapsed_time = time.time() - start_time
print(f"Execution time: {elapsed_time} seconds")
