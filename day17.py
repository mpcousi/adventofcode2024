import re
import time

if False:
    s1 = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""
else:
    with open("input_day17.txt") as f:
        s = f.read()

for line in s.split("\n"):
    if not line:
        continue

    nums = [int(x) for x in re.findall(r"\d+", line)]
    if line.startswith("Register A"):
        a = nums[0]
    elif line.startswith("Register B"):
        b = nums[0]
    elif line.startswith("Register C"):
        c = nums[0]
    elif line.startswith("Program"):
        program = nums

def get_combo_operand(operand, a, b, c):
    if operand <= 3:
        return operand
    elif operand == 4:
        return a
    elif operand == 5:
        return b
    elif operand == 6:
        return c
    else:
        raise ValueError(f"Unsupported combo operand {operand}")

def compute_program(a, b, c, program, looking_for=None):
    pointer = 0
    outputs = []

    while pointer < len(program):
        instruction = program[pointer]
        operand = program[pointer + 1]
        is_jump = False

        if instruction == 0: # adv
            a = int(a / (2 ** get_combo_operand(operand, a, b, c)))
        elif instruction == 1: # bxl
            b = b ^ operand
        elif instruction == 2: # bst
            b = get_combo_operand(operand, a, b, c) % 8
        elif instruction == 3: # jnz
            if a != 0:
                is_jump = True
                pointer = operand
        elif instruction == 4: # bxc
            b = b ^ c
        elif instruction == 5: # out
            outputs.append(get_combo_operand(operand, a, b, c) % 8)
            if looking_for and outputs != looking_for[:len(outputs)]:
                return None
        elif instruction == 6: # bdv
            b = int(a / (2 ** get_combo_operand(operand, a, b, c)))
        elif instruction == 7: # cdv
            c = int(a / (2 ** get_combo_operand(operand, a, b, c)))
        else:
            raise ValueError(f"Unsupported instruction {instruction}")
        
        if not is_jump:
            pointer += 2

    if looking_for and len(outputs) != len(looking_for):
        return None
    
    return outputs

print("Part 1")
start_time = time.time()
outputs = compute_program(a, b, c, program)
print(",".join([str(x) for x in outputs]))
elapsed_time = time.time() - start_time
print(f"Execution time: {elapsed_time} seconds")

def find_a(program):
    a = 0

    for i in range(len(program)):
        a *= 0o10
        looking_for = program[-(i+1):]
        print(looking_for)

        while not compute_program(a, 0, 0, program, looking_for):
            a += 1
        
        print(oct(a))
        
    return a

print("Part 2")
start_time = time.time()
a = find_a(program)
print(a)
elapsed_time = time.time() - start_time
print(f"Execution time: {elapsed_time} seconds")