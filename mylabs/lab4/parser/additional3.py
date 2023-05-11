import time
from main import main as main_task
from additional1 import main as additional1_task
from additional2 import main as additional2_task


def benchmark(function):
    start_time = time.time()
    for _ in range(100):
        function()
    print("--- %s seconds ---" % (time.time() - start_time))


print("> pure_python...")
benchmark(main_task)

print("> external_library...")
benchmark(additional1_task)

print("> regular_expressions...")
benchmark(additional2_task)
