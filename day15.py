import time

if False:
    s = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""
else :
    with open("input_day15.txt") as f:
        s3 = f.read()

def parse_input(s, is_part2=False):
    found_grid = False
    grid = []
    moves = []
    for line in s.split("\n"):
        if not line:
            found_grid = True
            continue

        if found_grid:
            moves.extend([c for c in line.strip()])
        else:
            grid_line = []
            for c in line.strip():
                if is_part2:
                    if c in ("#", "."):
                        grid_line.extend([c, c])
                    elif c == "O":
                        grid_line.extend(["[", "]"])
                    elif c == "@":
                        grid_line.extend(["@", "."])
                else:
                    grid_line.append(c)
            grid.append(grid_line)

    return grid, moves

def print_grid(grid, robot):
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if x == robot[0] and y == robot[1]:
                print("@", end="")
            else:
                print(grid[x][y], end="")
        print()

def find_robot(grid):
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == "@":
                grid[x][y] = "."
                return [x, y]
    
    raise ValueError("Could not find robot!")

movements = {"<": (0,-1), ">": (0,1), "^": (-1,0), "v": (1,0)}

def move_robot1(robot, move, grid):
    x = robot[0] + movements[move][0]
    y = robot[1] + movements[move][1]

    if grid[x][y] == "#":
        pass
    elif grid[x][y] in "O":
        first_box = (x,y)
        second_box = None
        while grid[x][y] != "#":
            x += movements[move][0]
            y += movements[move][1]
            if grid[x][y] == ".":
                second_box = (x,y)
                break
        
        if second_box:
            grid[first_box[0]][first_box[1]] = "."
            grid[second_box[0]][second_box[1]] = "O"
            robot[0] = first_box[0]
            robot[1] = first_box[1]
    else:
        robot[0] = x
        robot[1] = y
    
    return robot

def find_adjacent_boxes(x, y, move, grid, boxes):
    if move in ("<", ">"):
        edge = "]" if move == "<" else "["
        dy = -1 if move == "<" else 0
        
        while grid[x][y] == edge:
            boxes.add((x,y+dy))
            y += movements[move][1] * 2

        if grid[x][y] == "#":
            return None
        else:
            return boxes
    elif move in ("v", "^"):
        if grid[x][y] == "]":
            y -= 1
        boxes.add((x,y))
        dx = 1 if move == "v" else -1

        if grid[x+dx][y] == "." and grid[x+dx][y+1] == ".":
            return boxes
        elif grid[x+dx][y] == "#" or grid[x+dx][y+1] == "#":
            return None
        elif grid[x+dx][y] == "[":
            return find_adjacent_boxes(x+dx, y, move, grid, boxes)
        else:
            if grid[x+dx][y-1] == "[":
                boxes = find_adjacent_boxes(x+dx, y-1, move, grid, boxes)
                if not boxes:
                    return None
            if grid[x+dx][y+1] == "[":
                boxes = find_adjacent_boxes(x+dx, y+1, move, grid, boxes)
            return boxes

def move_boxes(boxes, move, grid):
    moved_to = set()
    for box in boxes:
        x = box[0] + movements[move][0]
        y = box[1] + movements[move][1]

        grid[x][y] = "["
        grid[x][y+1] = "]"
        moved_to.add((x,y))
        moved_to.add((x,y+1))
        if box not in moved_to:
            grid[box[0]][box[1]] = "."
        if (box[0], box[1]+1) not in moved_to:
            grid[box[0]][box[1]+1] = "."

def move_robot2(robot, move, grid):
    x = robot[0] + movements[move][0]
    y = robot[1] + movements[move][1]
    
    if grid[x][y] == "#":
        pass
    elif grid[x][y] in ("[", "]"):
        boxes = find_adjacent_boxes(x, y, move, grid, set())
        if boxes:
            move_boxes(boxes, move, grid)
            robot[0] = x
            robot[1] = y
    else:
        robot[0] = x
        robot[1] = y
    
    return robot

def compute_gps(grid):
    total = 0
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] in ("O", "["):
                total += 100 * x + y
    
    return total

s = s3
print("Part 1")
start_time = time.time()
grid, moves = parse_input(s)
robot = find_robot(grid)
for move in moves:
    robot = move_robot1(robot, move, grid)

print(compute_gps(grid))
elapsed_time = time.time() - start_time
print(f"Execution time: {elapsed_time} seconds")

print("Part 2")
start_time = time.time()
grid, moves = parse_input(s, is_part2=True)
robot = find_robot(grid)
for move in moves:
    robot = move_robot2(robot, move, grid)

print(compute_gps(grid))
elapsed_time = time.time() - start_time
print(f"Execution time: {elapsed_time} seconds")
