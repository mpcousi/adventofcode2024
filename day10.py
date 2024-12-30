import time

if False:
    s = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""
else:
    with open("input_day10.txt") as f:
        s = f.read()

grid = []
for line in s.split():
    grid.append([int(x) for x in line])

n = len(grid)
m = len(grid[0])

def find_trails(x, y, part1=False, pos=0, visited=None):
    if pos == 9:
        return 1

    if not visited:
        visited = set([(x,y)])
    
    total = 0
    next_pos = pos + 1
    for dx, dy in ((-1,0), (0,-1), (0,1), (1,0)):
        next_x = x + dx
        next_y = y + dy

        if next_x < 0 or next_x >= n or next_y < 0 or next_y >= m \
                or grid[next_x][next_y] != next_pos or (next_x, next_y) in visited:
            continue

        if part1:
            # We don't care about unicity of trail, never come back to this point
            visited.add((next_x, next_y))
            next_visited = visited
        else:
            # We do care about unicity of trail, allow yourself to come back
            next_visited = visited | set([(next_x, next_y)])

        total += find_trails(next_x, next_y, part1, next_pos, next_visited)

    return total

for i, part in enumerate([True, False]):
    print(f"Part {i+1}")
    start_time = time.time()
    total = 0

    for x in range(n):
        for y in range(m):
            if grid[x][y] == 0:
                total += find_trails(x, y, part1=part)

    print(total)
    elapsed_time = time.time() - start_time
    print(f"Execution time: {elapsed_time} seconds")
