import time

if False:
    s = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""
else:
    with open("input_day8.txt") as f:
        s = f.read()

grid = []
for line in s.split():
    grid.append(line)

n = len(grid)
m = len(grid[0])

antennas = {}
for x in range(n):
    for y in range(m):
        if grid[x][y].isalnum():
            if grid[x][y] not in antennas:
                antennas[grid[x][y]] = []
            antennas[grid[x][y]].append((x,y))

def find_antinodes_part1(antennas):
    antinodes = set()
    for x in range(n):
        for y in range(m):
            found_antinode = False
            for antenna in antennas:
                dists = []
                for i,j in antennas[antenna]:
                    dist_x = i-x
                    dist_y = j-y

                    for dist_x2, dist_y2 in dists:
                        if ((2 * dist_x) == dist_x2 and (2 * dist_y) == dist_y2) \
                                or ((dist_x % 2) == 0 and (dist_x / 2) == dist_x2 and (dist_y % 2) == 0 and (dist_y / 2) == dist_y2):
                            found_antinode = True
                            antinodes.add((x,y))
                            break
                    
                    if found_antinode:
                        break

                    dists.append((dist_x, dist_y))

                    if found_antinode:
                        break
            
                if found_antinode:
                    break

    return antinodes

def find_antinodes_part2(antennas):
    antinodes = set()
    for antenna in antennas:
        for antenna1 in range(len(antennas[antenna])):
            for antenna2 in range(1, len(antennas[antenna])):
                if antenna1 == antenna2:
                    continue

                dx = antennas[antenna][antenna1][0] - antennas[antenna][antenna2][0]
                dy = antennas[antenna][antenna1][1] - antennas[antenna][antenna2][1]

                for dir in (-1, 1):
                    x = antennas[antenna][antenna1][0]
                    y = antennas[antenna][antenna1][1]

                    while x >= 0 and x < n and y >= 0 and y < m:
                        antinodes.add((x,y))
                        x = x + dir * dx
                        y = y + dir * dy

    return antinodes

print("Part 1")
start_time = time.time()
antinodes = find_antinodes_part1(antennas)
elapsed_time = time.time() - start_time
print(len(antinodes))
print(f"Execution time: {elapsed_time} seconds")

print("Part 2")
start_time = time.time()
antinodes = find_antinodes_part2(antennas)
elapsed_time = time.time() - start_time
print(len(antinodes))
print(f"Execution time: {elapsed_time} seconds")
