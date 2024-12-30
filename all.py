import subprocess
import time

global_start_time = time.time()

for i in range(1, 26):
    start_time = time.time()
    subprocess.run(["python", f"day{i}.py"], capture_output=True)
    elapsed_time = time.time() - start_time
    print(f"Day {i}: {str(elapsed_time)[:10]} seconds")

elapsed_time = time.time() - global_start_time
print(f"All runs: {elapsed_time} seconds")
