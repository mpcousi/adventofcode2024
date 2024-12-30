import time

if False:
    s = """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
"""
else:
    with open("input_day25.txt") as f:
        s = f.read()

locks = []
keys = []
is_lock = None
prev = []
for line in s.split("\n"):
    if not line:
        if is_lock == True:
            locks.append(prev)
        elif is_lock == False:
            keys.append(prev)
        is_lock = None
        prev = []
        continue
    
    if is_lock is None:
        is_lock = "#" in line

    prev.append([x for x in line])

def count_pins(lock):
    pins = []
    for x in range(len(lock[0])):
        total = 0
        for y in range(1, len(lock) - 1):
            if lock[y][x] == "#":
                total += 1
        pins.append(total)
    return pins

def key_lock_fits(lock_pin, key_pin):
    for i in range(len(lock_pin)):
        if lock_pin[i] + key_pin[i] > len(lock_pin):
            return False
    return True

start_time = time.time()
key_pins = {}
total = 0

for lock in locks:
    lock_pin = count_pins(lock)
    for i, key in enumerate(keys):
        if i not in key_pins:
            key_pins[i] = count_pins(key)
        
        if key_lock_fits(lock_pin, key_pins[i]):
            total += 1

print(total)
elapsed_time = time.time() - start_time
print(f"Execution time: {elapsed_time} seconds")
