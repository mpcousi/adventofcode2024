import heapq
import sys
import time

if False:
    s = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""
else:
    with open("input_day16.txt") as f:
        s3 = f.read()

grid = []
for line in s3.split():
    grid.append([x for x in line])

def find_extremeties(grid):
    start = None
    end = None
    n = len(grid)
    m = len(grid[0])

    for x in range(n):
        for y in range(m):
            if grid[x][y] == "S":
                start = (x,y)
                if end:
                    return start, end
            elif grid[x][y] == "E":
                end = (x,y)
                if start:
                    return start, end

    return start, end

def print_grid(grid, current=None, visited=None):
    n = len(grid)
    m = len(grid[0])

    for x in range(n):
        for y in range(m):
            if current and x == current[0] and y == current[1]:
                print("@", end="")
            elif visited and (x,y) in visited:
                print("O", end="")
            elif grid[x][y] == "#":
                print("#", end="")
            else:
                print(" ", end="")
        print()

def move(x, y, direction):
    if direction == "east":
        return x, y+1
    elif direction == "west":
        return x, y-1
    elif direction == "north":
        return x-1, y
    elif direction == "south":
        return x+1, y
    else:
        raise ValueError(f"Unexpected direction {direction}")

def rotate(direction):
    if direction in ("east", "west"):
        return ["north", "south"]
    elif direction in ("north", "south"):
        return ["east", "west"]
    else:
        raise ValueError(f"Unexpected direction {direction}")

def find_path(x, y, end, direction, grid):
    if x == end[0] and y == end[1]:
        return

    new_directions = [direction] + rotate(direction)
    for new_direction in new_directions:
        x2, y2 = move(x, y, new_direction)
        if x2 < 0 or y2 < 0 or x2 >= len(grid) or y2 >= len(grid[0]) or grid[x2][y2] == "#":
            continue

        if new_direction == direction:
            new_cost = grid[x][y] + 1
        else:
            new_cost = grid[x][y] + 1001

        if isinstance(grid[x2][y2], str) or grid[x2][y2] >= new_cost:
            grid[x2][y2] = new_cost
            find_path(x2, y2, end, new_direction, grid)


def find_all_paths(x, y, direction, previous, visited=set()):
    visited.add((x,y))
    for x2, y2, new_direction in previous.get((x, y, direction), []):
        find_all_paths(x2, y2, new_direction, previous, visited)
    return visited

def dijkstra(x, y, end, grid):
    queue = [(0, x, y, "east")]
    costs = {(x, y, "east"): 0}
    previous = {}

    while queue:
        cost, x, y, direction = heapq.heappop(queue)
        if x == end[0] and y == end[1]:
            return cost, find_all_paths(x, y, direction, previous)

        new_directions = [direction] + rotate(direction)
        for new_direction in new_directions:
            x2, y2 = move(x, y, new_direction)
            if x2 < 0 or y2 < 0 or x2 >= len(grid) or y2 >= len(grid[0]) or grid[x2][y2] == "#":
                continue
            
            if new_direction == direction:
                new_cost = cost + 1
            else:
                new_cost = cost + 1001

            next = (x2, y2, new_direction)
            go_next = True
            if next not in costs or new_cost < costs[next]:
                costs[next] = new_cost
                previous[next] = set([(x, y, direction)])
            elif new_cost == costs[next]:
                previous[next].add((x, y, direction))
            else:
                go_next = False
            
            if go_next:
                heapq.heappush(queue, (new_cost, x2, y2, new_direction))

start, end = find_extremeties(grid)

print("Part 1")
sys.setrecursionlimit(10_000)  # SHAME!
start_time = time.time()
grid[start[0]][start[1]] = 0
find_path(start[0], start[1], end, "east", grid)
min_cost = grid[end[0]][end[1]]
print(min_cost)
elapsed_time = time.time() - start_time
print(f"Execution time: {elapsed_time} seconds")

print("Part 2")
start_time = time.time()
cost, paths = dijkstra(start[0], start[1], end, grid)
print(len(paths))
elapsed_time = time.time() - start_time
print(f"Execution time: {elapsed_time} seconds")
