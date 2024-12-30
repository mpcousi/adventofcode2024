import time

if False:
    s = "2333133121414131402"
else:
    with open("input_day9.txt") as f:
        s = f.read()

disk = [int(x) for x in s.strip()]

def defrag_part1(disk):
    i = 0
    j = len(disk) - 1

    total = 0
    pos = 0
    if len(disk) % 2 == 0:
        j -= 1

    while i <= j:
        file_id = i // 2
        while disk[i] > 0:
            total = total + (pos * file_id)
            pos += 1
            disk[i] -= 1
        
        next_free_space = disk[i+1]
        while next_free_space > 0:
            while i < j and disk[j] <= 0:
                j -= 2

            if i >= j:
                break

            file_id = j // 2
            total = total + (pos * file_id)
            pos += 1
            disk[j] -= 1
            next_free_space -= 1

        i += 2

    return total

def defrag_part2(disk):
    # 1. Build disk grid
    n = len(disk)
    id = 0
    s = []
    for i in range(n):
        if i % 2 == 0:
            for _ in range(disk[i]):
                s.append(id)
            id += 1
        else:
            for _ in range(disk[i]):
                s.append(".")
    
    disk = s
    n = len(disk)
    to_move = id - 1
    while to_move >= 0:
        # 2. Find file to move in disk
        i = n - 1
        first_pos = None
        last_pos = None

        while i > 0:
            if disk[i] == to_move:
                if last_pos is None:
                    last_pos = i
                first_pos = i
            elif last_pos is not None:
                break
            i -= 1
        
        if not first_pos or not last_pos:
            raise ValueError(f"Could not find {to_move} in disk!")

        # 3. Find a position you can move it to
        file_size = last_pos - first_pos + 1
        i = 0
        free_space = 0
        found_pos = None
        while i < first_pos and free_space < file_size:
            if disk[i] == ".":
                free_space += 1
            else:
                free_space = 0

            if free_space == file_size:
                found_pos = i
                break
            i += 1

        # 4. Move to position if found
        if found_pos:
            first_pos_space = i - file_size + 1
            last_pos_space = i

            while first_pos_space <= last_pos_space:
                disk[first_pos_space] = to_move
                first_pos_space += 1
            
            while first_pos <= last_pos:
                disk[first_pos] = "."
                first_pos += 1

        to_move -= 1

    # 5. Compute checksum
    total = 0
    for i in range(1, n):
        if disk[i] != ".":
            total += i * disk[i]

    return total


print("Part 1")
start_time = time.time()
total = defrag_part1([x for x in disk])
elapsed_time = time.time() - start_time
print(total)
print(f"Execution time: {elapsed_time} seconds")

print("Part 2")
start_time = time.time()
total = defrag_part2([x for x in disk])
elapsed_time = time.time() - start_time
print(total)
print(f"Execution time: {elapsed_time} seconds")
