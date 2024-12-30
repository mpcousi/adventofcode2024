import multiprocessing
import time

if False:
    s = """....#.....
    .........#
    ..........
    ..#.......
    .......#..
    ..........
    .#..^.....
    ........#.
    #.........
    ......#..."""
else:
    with open("input_day6.txt") as f:
        s = f.read()

grid = [[elem for elem in row] for row in s.split()]
n = len(grid)
m = len(grid[0])
guard_pos = {"^", ">", "v", "<"}
moves = {"^": (-1,0), ">": (0,1), "v": (1,0), "<": (0,-1)}
turns = {"^": ">", ">": "v", "v": "<", "<": "^"}

def find_guard(grid):
    for x in range(n):
        for y in range(m):
            if grid[x][y] in guard_pos:
                return x, y, grid[x][y]
    
    raise ValueError("Could not find guard!")

def solve_maze(grid, is_part2, extra_obstacle=(-1,-1)):
    x, y, pos = find_guard(grid)
    if is_part2:
        visited = {(x, y, pos)}
    else:
        visited = {(x, y)}

    while True:
        dx, dy = moves[pos]
        next_x = x + dx
        next_y = y + dy

        if next_x < 0 or next_x >= n or next_y < 0 or next_y >= m:
            # Out of bounds, end of path
            return True if is_part2 else len(visited)
        
        if grid[next_x][next_y] == "#" or (next_x == extra_obstacle[0] and next_y == extra_obstacle[1]):
            pos = turns[pos]
        elif (next_x, next_y, pos) in visited:
            # Already visited, cycle!
            return False
        else:
            if is_part2:
                visited.add((next_x, next_y, pos))
            else:
                visited.add((next_x, next_y))

            x = next_x
            y = next_y

print("Part 1")
start_time = time.time()
print(solve_maze(grid, is_part2=False))
elapsed_time = time.time() - start_time
print(f"Execution time: {elapsed_time} seconds")

print("Part 2")
start_time = time.time()
extra_obstacles = []
for i in range(n):
    for j in range(m):
        if grid[i][j] == ".":
            extra_obstacles.append((i,j))

def parallel_solve_maze(obstacle):
    return 0 if solve_maze(grid, True, obstacle) else 1

num_obstacles = 0
with multiprocessing.Pool() as pool:
    results = pool.map(parallel_solve_maze, extra_obstacles)
num_obstacles = sum(results)

print(num_obstacles)
elapsed_time = time.time() - start_time
print(f"Execution time: {elapsed_time} seconds")
