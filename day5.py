import time

if False:   
    s = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""
else:
    with open("input_day5.txt") as f:
        s = f.read()

def get_active_rules(pages, rules):
    current_pages = set(pages)
    active_rules = {}
    for page in pages:
        active_rules[page] = set()
        for before in rules.get(page, []):
            if before in current_pages:
                active_rules[page].add(before)
    return active_rules

def is_correct(pages, active_rules):
    for page in pages:
        if active_rules[page]:
            return False
        
        for page2 in pages:
            if page in active_rules[page2]:
                active_rules[page2].remove(page)
    
    return True

def fix_order(pages, active_rules):
    processed_pages = set()
    new_order = []
    while len(processed_pages) < len(pages):
        # Find a page that has no before rule
        next_page = None
        for page in pages:
            if page not in processed_pages and not active_rules[page]:
                next_page = page
                processed_pages.add(page)
                new_order.append(page)
                break

        if not next_page:
            raise ValueError(f"Could not reorder {pages}!")

        # Remove page from all rules since it's gone
        for page in pages:
            if next_page in active_rules[page]:
                active_rules[page].remove(next_page)

    return new_order

def count_pages(s, is_part2):
    result = 0
    rules = {}
    for line in s.split():
        if "|" in line:
            before, after = line.split("|")
            if after not in rules:
                rules[after] = []
            rules[after].append(before)
        else:
            pages = line.split(",")
            active_rules = get_active_rules(pages, rules)
            if is_correct(pages, active_rules):
                if not is_part2:
                    middle = pages[len(pages) // 2]
                    result += int(middle)
            elif is_part2:
                new_order = fix_order(pages, active_rules)
                middle = new_order[len(pages) // 2]
                result += int(middle)

    return result

print("Part 1")
start_time = time.time()
print(count_pages(s, is_part2=False))
elapsed_time = time.time() - start_time
print(f"Execution time: {elapsed_time} seconds")

print("Part 2")
start_time = time.time()
print(count_pages(s, is_part2=True))
elapsed_time = time.time() - start_time
print(f"Execution time: {elapsed_time} seconds")
