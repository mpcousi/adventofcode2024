import re
import time

if False:
    s = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
else:
    with open("input_day3.txt") as f:
        s = f.read()

def parse_mul(s, is_part2):
    result = 0
    muls = re.finditer("mul\((\d{1,3}),(\d{1,3})\)", s)

    if is_part2:
        dos = re.finditer("do\(\)", s)
        donts = re.finditer("don't\(\)", s)
        
        def get_next_val(my_iter):
            try:
                return next(my_iter).start()
            except StopIteration:
                return len(s)
        
        is_disabled = False
        next_do = get_next_val(dos)
        next_dont = get_next_val(donts)
    
    for mul in muls:
        if is_part2:
            last_do = -1
            while next_do < mul.start():
                last_do = next_do
                next_do = get_next_val(dos)
            
            last_dont = -1
            while next_dont < mul.start():
                last_dont = next_dont
                next_dont = get_next_val(donts)
            
            if last_do != -1 or last_dont != -1:
                is_disabled = last_dont > last_do
        
        if not is_part2 or not is_disabled:
            result += int(mul.group(1)) * int(mul.group(2))

    return result


print("Part 1")
start_time = time.time()
print(parse_mul(s, is_part2=False))
elapsed_time = time.time() - start_time
print(f"Execution time: {elapsed_time} seconds")

print("Part 2")
start_time = time.time()
print(parse_mul(s, is_part2=True))
elapsed_time = time.time() - start_time
print(f"Execution time: {elapsed_time} seconds")
