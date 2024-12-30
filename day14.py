import re
import time

if False:
    s = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""
    wide = 11
    tall = 7
else:
    with open("input_day14.txt") as f:
        s = f.read()
    wide = 101
    tall = 103

robots = []
for line in s.split("\n"):
    nums = [int(x) for x in re.findall(r"-?\d+", line)]
    if nums:
        robots.append({"p": nums[:2], "v": nums[2:]})

def count_quadrants(robots, wide, tall):
    quadrants = {}
    width = wide // 2
    height = tall // 2

    for robot in robots:
        if robot["p"][0] == width or robot["p"][1] == height:
            quadrant = -1
        elif robot["p"][0] < width:
            if robot["p"][1] < height:
                quadrant = 0
            else:
                quadrant = 2
        else:
            if robot["p"][1] < height:
                quadrant = 1
            else:
                quadrant = 3
                
        quadrants[quadrant] = quadrants.get(quadrant, 0) + 1

    return quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]

def move_robots(robots, seconds, wide, tall):
    for robot in robots:
        robot["p"][0] = (robot["p"][0] + seconds * robot["v"][0]) % wide
        robot["p"][1] = (robot["p"][1] + seconds * robot["v"][1]) % tall
    return robots

def find_straight_line(robots):
    visited = set()
    for robot in robots:
        x = robot["p"][0]
        y = robot["p"][1]
        for i in range(2):
            found = True
            for j in range(1, 10):
                if i == 0:
                    xx = x + j
                else:
                    xx = x - j

                if (xx,y) not in visited:
                    found = False
                    break
        
            if found:
                return True
        
        visited.add((x,y))
    
    return False


def print_robots(robots, wide, tall):
    grid = []
    for _ in range(tall):
        grid.append([" "] * wide)
    
    for robot in robots:
        if grid[robot["p"][1]][robot["p"][0]] == " ":
            grid[robot["p"][1]][robot["p"][0]] = "1"
        else:
            grid[robot["p"][1]][robot["p"][0]] = str(int(grid[robot["p"][1]][robot["p"][0]]) + 1)

    for i in range(tall):
        print("".join(grid[i]))

    print()


print("Part 1")
start_time = time.time()
robots = move_robots(robots, 100, wide, tall)
print(count_quadrants(robots, wide, tall))
elapsed_time = time.time() - start_time
print(f"Execution time: {elapsed_time} seconds")

print()
print("Part 2")
start_time = time.time()
for i in range(10_000):
    robots = move_robots(robots, 1, wide, tall)
    if find_straight_line(robots):
        print_robots(robots, wide, tall)
        print(f"Iteration #{i+1}")
elapsed_time = time.time() - start_time
print(f"Execution time: {elapsed_time} seconds")
