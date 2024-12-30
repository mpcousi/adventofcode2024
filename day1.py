
import time

list1 = []
list2 = []
distance = 0

if False:
    s = """3   4
4   3
2   5
1   3
3   9
3   3"""
else:
    with open("input_day1.txt") as f:
        s = f.read()

for line in s.split("\n"):
    if not line:
        continue
    x,y = line.split()
    list1.append(x)
    list2.append(y)

print("Part 1")
start_time = time.time()

list1.sort()
list2.sort()
for x, y in zip(list1, list2):
    distance += abs(int(y) - int(x))

print(distance)
elapsed_time = time.time() - start_time
print(f"Execution time: {elapsed_time} seconds")

print("Part 2")
start_time = time.time()

elems_in_list2 = {}
for elem in list2:
    elems_in_list2[elem] = 1 + elems_in_list2.get(elem, 0)

similarity = 0
for elem in list1:
    similarity += int(elem) * elems_in_list2.get(elem, 0)

print(similarity)
elapsed_time = time.time() - start_time
print(f"Execution time: {elapsed_time} seconds")
