"""
Here, we use the built-in concurrent.futures module to fire tasks concurrently.
This is great if you need to quickly achieve concurrency in some part of your
application.

There are 4 examples. All of these are firing a dummy task 10 times.

1. Spawns 4 threads and uses excecutor.submit
2. Spawns 4 threads and uses executor.map
3. Spawns 4 processes and uses executor.submit
4. Spawns 4 processes and uses executor.map

Notice that none of the approaches returns the results maintaining
scheduling order. This is intentional.
"""


from __future__ import annotations

import concurrent.futures as confu
import time

MAX_CONCURRENCY = 4
N_TASKS = 10


def foo(task_id: int) -> None:
    time.sleep(0.5)
    print(f"task-id: {task_id}, status: done")


def threads_with_executor_submit():

    print("\nDoing it with thread submit\n")

    with confu.ThreadPoolExecutor(MAX_CONCURRENCY) as executor:
        futures = []
        for task_id in range(N_TASKS):
            fut = executor.submit(foo, task_id)
            futures.append(fut)

        for future in confu.as_completed(futures):
            try:
                future.result()
                future.cancel()
            except Exception:
                print("oops")


def threads_with_executor_map():

    print("\nDoing it with thread map\n")
    
    with confu.ThreadPoolExecutor(MAX_CONCURRENCY) as executor:
        results = executor.map(foo, [task_id for task_id in range(N_TASKS)])

        try:
            for result in results:
                result
        except Exception:
            print("oops")


def processes_with_executor_submit():
    print("\nDoing it with process submit\n")
    with confu.ThreadPoolExecutor(MAX_CONCURRENCY) as executor:
        futures = []
        for task_id in range(N_TASKS):
            fut = executor.submit(foo, task_id)
            futures.append(fut)

        for future in confu.as_completed(futures):
            try:
                future.result()
                future.cancel()
            except Exception:
                print("oops")


def processes_with_executor_map():
    print("\nDoing it with process map\n")
    with confu.ProcessPoolExecutor(MAX_CONCURRENCY) as executor:
        results = executor.map(foo, [task_id for task_id in range(N_TASKS)])

        try:
            for result in results:
                result
        except Exception:
            print("oops")


if __name__ == "__main__":
    threads_with_executor_submit()
    threads_with_executor_map()
    processes_with_executor_submit()
    processes_with_executor_map()
