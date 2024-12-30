import time

if False:
    s = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""
else:
    with open("input_day19.txt") as f:
        s = f.read()

designs = set()
patterns = []
longest_design = 0
for line in s.split("\n"):
    if not line:
        continue
    if not longest_design:
        for design in line.split(", "):
            designs.add(design)
            longest_design = max(longest_design, len(design))
    else:
        patterns.append(line)

def find_pattern(pattern, designs, longest_design, visited, i=0):
    if i == len(pattern):
        return 1
    elif pattern[i:] in visited:
        return visited[pattern[i:]]
    
    count = 0
    for j in range(min(len(pattern), i + longest_design + 1), i, -1):
        if pattern[i:j] in designs:
            count += find_pattern(pattern, designs, longest_design, visited, j)
        
    visited[pattern[i:]] = count
    return count

visited = {}
part1 = 0
part2 = 0
start_time = time.time()
for pattern in patterns:
    count = find_pattern(pattern, designs, longest_design, visited)
    if count > 0:
        part1 += 1
    part2 += count

print("Part 1")
print(part1)
print("Part 2")
print(part2)
elapsed_time = time.time() - start_time
print(f"Execution time: {elapsed_time} seconds")
