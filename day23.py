import time

if False:
    s = """kh-tc
    qp-kh
    de-cg
    ka-co
    yn-aq
    qp-ub
    cg-tb
    vc-aq
    tb-ka
    wh-tc
    yn-cg
    kh-ub
    ta-co
    de-co
    tc-td
    tb-wq
    wh-td
    ta-ka
    td-qp
    aq-cg
    wq-ub
    ub-vc
    de-ta
    wq-aq
    wq-vc
    wh-yn
    ka-de
    kh-ta
    co-tc
    wh-qp
    tb-vc
    td-yn"""
else:
    with open("input_day23.txt") as f:
        s = f.read()

connections = {}
for line in s.split():
    computers = line.split("-")
    if computers[0] not in connections:
        connections[computers[0]] = set()
    if computers[1] not in connections:
        connections[computers[1]] = set()
    connections[computers[0]].add(computers[1])
    connections[computers[1]].add(computers[0])

def is_neighbor_of_all(computer, group, connections):
    for computer2 in group:
        if computer2 not in connections[computer]:
            return False
    return True

def group_has_t(group):
    for computer in group:
        if computer.startswith("t"):
            return True
    return False

def find_groups(computer, connections, so_far, result, visited, is_part1):
    node = tuple(sorted(so_far))

    if is_part1 and len(so_far) == 3:
        if group_has_t(so_far):
            result.add(node)
        return
    
    if node in visited:
        return
    visited.add(node)

    found_new = False
    for computer2 in connections[computer]:
        if computer2 not in so_far and is_neighbor_of_all(computer2, so_far, connections):
            found_new = True
            find_groups(computer2, connections, so_far | set([computer2]), result, visited, is_part1)

    if not is_part1 and not found_new and len(so_far) > len(result[0]):
        result.pop()
        result.append(so_far)

print("Part 1")
start_time = time.time()
groups = set()
visited = set()
for computer in connections:
    find_groups(computer, connections, set([computer]), groups, visited, is_part1=True)

print(len(groups))
elapsed_time = time.time() - start_time
print(f"Execution time: {elapsed_time} seconds")

print("Part 2")
start_time = time.time()
visited = set()
result = [[]]
for computer in connections:
    find_groups(computer, connections, set([computer]), result, visited, is_part1=False)

print(",".join(sorted(result[0])))
elapsed_time = time.time() - start_time
print(f"Execution time: {elapsed_time} seconds")
