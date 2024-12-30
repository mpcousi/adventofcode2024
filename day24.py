import copy
import time
from collections import deque

if False:
    s = """x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02"""
else:
    with open("input_day24.txt") as f:
        s = f.read()

values = {}
gates = deque()
for line in s.split("\n"):
    if not line:
        continue
    if ":" in line:
        parts = line.split(":")
        values[parts[0]] = int(parts[1])
    else:
        gates.append(line)

def operation(op, val1, val2):
    if op == "AND":
        yes = val1 == 1 and val2 == 1
    elif op == "OR":
        yes = val1 == 1 or val2 == 1
    elif op == "XOR":
        yes = val1 != val2
    else:
        raise ValueError(f"WTF {op}")

    return 1 if yes else 0

def perform_gates(gates, values, swaps={}):
    graph = {}
    gates = copy.deepcopy(gates)
    values = copy.deepcopy(values)

    while gates:
        gate = gates.popleft()
        parts = gate.split()
        op = parts[1]
        val1 = parts[0]
        val2 = parts[2]
        res = parts[4]

        if res in swaps:
            res = swaps[res]

        if res not in graph:
            graph[res] = {}
        graph[res]["op"] = op
        graph[res]["vals"] = [val1, val2]

        if val1 not in values or val2 not in values:
            gates.append(gate)
            continue

        values[res] = operation(op, values[val1], values[val2])

    return values, graph

def get_number(letter, values):
    total = 0
    for i in range(100):
        label = letter + str(i).zfill(2)
        if label not in values:
            break
        total += (2 ** i) * values[label]
    return total

def find_errors(graph, len_z):
    for i in range(len_z - 1):
        x = f"x{str(i).zfill(2)}"
        y = f"y{str(i).zfill(2)}"
        z = f"z{str(i).zfill(2)}"
        if z not in graph:
            break
        
        op = graph[z]["op"]
        vals = graph[z]["vals"]
        
        # Zn-1 = aaa XOR bbb
        # Zn = (Xn XOR Yn) XOR ((Xn-1 AND Yn-1) OR (aaa AND bbb))

        if op != "XOR":
            print(f"{z} doesn't have a XOR operation! {op} found instead")
        found_x_y_term = False
        for val in vals:
            if val not in graph:
                continue
            if graph[val]["op"] == "XOR" and all([a in graph[val]["vals"] for a in (x,y)]):
                found_x_y_term = True
            if i > 0 and graph[val]["op"] == "OR":
                found_prev_x_y = False
                found_prev_z = False
                for val in graph[val]["vals"]:
                    if graph[val]["op"] == "AND" and all([graph[prev_z]["vals"][i] in graph[val]["vals"] for i in (0,1)]):
                        found_prev_z = True
                    elif graph[val]["op"] == "AND" and all([a in graph[val]["vals"] for a in (prev_x, prev_y)]):
                        found_prev_x_y = True
                
                if not found_prev_x_y:
                    print(f"{z} doesn't have '{prev_x} AND {prev_y}' in children")
                if not found_prev_z:
                    print(f"{z} doesn't have {prev_z} in children")

        if i > 0 and not found_x_y_term:
            print(f"{z} doesn't have an '{x} XOR {y}' term!")
        
        prev_x = x
        prev_y = y
        prev_z = z

print("Part 1")
start_time = time.time()
values, graph = perform_gates(gates, values)
x = get_number("x", values)
y = get_number("y", values)
z = get_number("z", values)
print(z)
elapsed_time = time.time() - start_time
print(f"Execution time: {elapsed_time} seconds")

print("\nPart 2 exploration")
start_time = time.time()
print(f"X+Y: {bin(x+y)}")
print(f" Z : {bin(z)}")
find_errors(graph, len(bin(z)[2:]))
elapsed_time = time.time() - start_time
print(f"Execution time: {elapsed_time} seconds")

print("\nPart 2 solved")
# Note: swaps found manually using errors found in exploration step
swaps = [("z16", "hmk"), ("z20", "fhp"), ("tpc", "rvf"), ("z33", "fcd")]  # This is specific to my input...
swaps_dict = {k:v for k,v in swaps}
swaps_dict.update({v:k for k,v in swaps})
values, graph = perform_gates(gates, values, swaps_dict)
x = get_number("x", values)
y = get_number("y", values)
z = get_number("z", values)
print(f"X+Y: {bin(x+y)}")
print(f" Z : {bin(z)}")
print(",".join(sorted(list(swaps_dict.keys()))))
