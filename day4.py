import time

if False:
    s = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""
else:
    with open("input_day4.txt") as f:
        s = f.read()

grid = s.split()
m = len(grid)
n = len(grid[0])

def find_xmas(i, j):
    num_words = 0
    for dx, dy in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
        x = i
        y = j
        found_word = True
        
        for c in "XMAS":
            if x < 0 or x >= m or y < 0 or y >= n or grid[x][y] != c:
                found_word = False
                break
            x += dx
            y += dy

        if found_word:
            num_words += 1

    return num_words

def find_cross(i, j):
    if grid[i][j] != "A":
        return False
    
    for diag in [[(-1,-1),(1,1)],[(-1,1),(1,-1)]]:
        last_char = None
        for dx, dy in diag:
            x = i + dx
            y = j + dy
            if x < 0 or x >= m or y < 0 or y >= m or grid[x][y] not in ("M", "S") or grid[x][y] == last_char:
                return False
            last_char = grid[x][y]
        
    return True

print("Part 1")
start_time = time.time()
num_xmas = 0
for x in range(m):
    for y in range(n):
        if grid[x][y] == "X":
            num_xmas += find_xmas(x,y)
print(num_xmas)
elapsed_time = time.time() - start_time
print(f"Execution time: {elapsed_time} seconds")

print("Part 2")
start_time = time.time()
num_cross = 0
for x in range(m):
    for y in range(n):
        if grid[x][y] == "A" and find_cross(x,y):
            num_cross += 1

print(num_cross)
elapsed_time = time.time() - start_time
print(f"Execution time: {elapsed_time} seconds")
