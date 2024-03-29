"""
Producer-consumer pattern using Python's asyncio—
where both of the entities are long running.

Producer
--------
Here, the producer generates a sequeunce of numbers 0,1,0,2,0,0,3,0,0,4 indefinitely.
However, it only puts non-zero values into the queue.

Consumer
--------
The consumer only runs when a non-zero value appears on the queue and lets the
producer run again. This juggling between producer and consumer goes on indefinitely.

"""

from __future__ import annotations

import asyncio
import itertools


async def producer(queue: asyncio.Queue, event: asyncio.Event) -> None:
    for i in itertools.cycle([0, 1, 0, 2, 0, 0, 3, 0, 0, 4]):
        print("Running producer...")
        if i:
            await queue.put(i)
        event.set()
        await asyncio.sleep(1)


async def consumer(
    queue: asyncio.Queue, event: asyncio.Event, stop_after: int | None = None
) -> None:
    await event.wait()

    cnt = 0
    while True:
        print("Running consumer...")

        res = await queue.get()
        print(res)
        queue.task_done()
        cnt += 1

        if cnt == stop_after:
            break


async def main() -> None:
    queue = asyncio.Queue()  # type: asyncio.Queue[int]
    event = asyncio.Event()  # type: asyncio.Event

    _ = asyncio.create_task(producer(queue, event))
    consumer_tasks = [asyncio.create_task(consumer(queue, event)) for _ in range(3)]
    await asyncio.gather(*consumer_tasks, return_exceptions=True)

    # This implicitly run the producer.
    await queue.join()

    # Cancel tasks.
    for task in consumer_tasks:
        task.cancel()


if __name__ == "__main__":
    asyncio.run(main())
