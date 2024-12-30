import time

if False:
    s = """RRRRIICCFF
    RRRRIICCCF
    VVRRRCCFFF
    VVRCCCJFFF
    VVVVCJJCFE
    VVIVCCJJEE
    VVIIICJJEE
    MIIIIIJJEE
    MIIISIJEEE
    MMMISSJEEE"""
else:
    with open("input_day12.txt") as f:
        s = f.read()

grid = []
for line in s.split():
    grid.append(line)

n = len(grid)
m = len(grid[0])

def is_plant(x, y, plant):
    return x >= 0 and x < n and y >= 0 and y < m and grid[x][y] == plant

def visit_plant(plant, x, y, block_id, visited, block_coords, results):
    if not is_plant(x ,y, plant):
        return False
    if (x,y) in visited:
        return True

    visited.add((x,y))
    block_coords.add((x,y))
    num_same_neighbors = 0

    for dx, dy in ((-1,0), (0,-1), (0,1), (1,0)):
        xx = x + dx
        yy = y + dy

        if visit_plant(plant, xx, yy, block_id, visited, block_coords, results):
            num_same_neighbors += 1

    results["areas"][block_id] = results["areas"].get(block_id, 0) + 1
    results["perimeters"][block_id] = results["perimeters"].get(block_id, 0) + 4 - num_same_neighbors
    return True

def count_sides(plant, block_id, block_coords, results):
    sides = 0

    # Horizontal, check up & down sides
    for x in range(n):
        up = False
        down = False
        for y in range(m):
            if (x,y) not in block_coords:
                # Reset in case the block comes back on this line later in a separate side
                up = False
                down = False
                continue

            if not is_plant(x-1, y, plant):
                # Different plant above, this is an "up" side of our block
                if not up:
                    sides += 1
                    up = True
            else:
                up = False

            if not is_plant(x+1, y, plant):
                # Different plant below, this is a "down" side of our block
                if not down:
                    sides += 1
                    down = True
            else:
                down = False

    # Vertical, check left and right sides
    for y in range(m):
        left = False
        right = False
        for x in range(n):
            if (x,y) not in block_coords:
                # Reset in case the block comes back on this line later in a separate side
                left = False
                right = False
                continue

            if not is_plant(x, y-1, plant):
                # Different plant on the left, this is a "left" side of our block
                if not left:
                    sides += 1
                    left = True
            else:
                left = False

            if not is_plant(x, y+1, plant):
                # Different plant on the right, this is a "right" side of our block
                if not right:
                    sides += 1
                    right = True
            else:
                right = False

    results["num_sides"][block_id] = sides

def get_new_block_id(plant, plants):
    plants[plant] = plants.get(plant, 0) + 1
    return f"{plant}_{plants[plant]}"

def compute_price(is_part2):
    visited = set()
    results = {"areas": {}, "perimeters": {}, "num_sides": {}}
    plants = {}

    for x in range(n):
        for y in range(m):
            if (x,y) not in visited:
                block_id = get_new_block_id(grid[x][y], plants)
                block_coords = set()
                visit_plant(grid[x][y], x, y, block_id, visited, block_coords, results)
                if is_part2:
                    count_sides(grid[x][y], block_id, block_coords, results)

    total = 0
    for plant in results["areas"]:
        perim_or_sides = "num_sides" if is_part2 else "perimeters"
        total += results["areas"][plant] * results[perim_or_sides][plant]
    return total

print("Part 1")
start_time = time.time()
print(compute_price(False))
elapsed_time = time.time() - start_time
print(f"Execution time: {elapsed_time} seconds")

print("Part 2")
start_time = time.time()
print(compute_price(True))
elapsed_time = time.time() - start_time
print(f"Execution time: {elapsed_time} seconds")
