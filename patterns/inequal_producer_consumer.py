from __future__ import annotations

import asyncio
import itertools
import sys
from collections.abc import AsyncIterator

MAX_CONSUMERS = 20


async def generate_number() -> AsyncIterator[int]:
    for i in itertools.cycle([0, 0, 1, 0, 0, 2, 0, 0, 3, 0, 0, 4, 0, 0, 5]):
        yield i
        await asyncio.sleep(0)


async def producer(result_queue: asyncio.Queue, event: asyncio.Event) -> None:
    async for i in generate_number():
        if i:
            await result_queue.put(i)
            event.set()
            await asyncio.sleep(0)


async def consumer(
    result_queue,
    event: asyncio.Event,
    limit: asyncio.Semaphore,
    stop_after: int | None = None,
) -> None:
    cnt = 0
    async with limit:
        while True:
            await event.wait()
            result = await result_queue.get()
            print(result)
            result_queue.task_done()
            cnt += 1

            await asyncio.sleep(0.1)
            if limit.locked():
                print("sleeping for 2 sec")
                await asyncio.sleep(2)

            if cnt == stop_after:
                sys.exit(0)


async def main() -> None:
    result_queue = asyncio.Queue()  # type: asyncio.Queue[int]
    event = asyncio.Event()  # type: asyncio.Event
    limit = asyncio.Semaphore(5)  # type: asyncio.Semaphore

    # Running the producer task in the background.
    _ = asyncio.create_task(producer(result_queue, event))

    consumer_tasks = [
        consumer(result_queue, event, limit) for _ in range(MAX_CONSUMERS)
    ]

    await asyncio.gather(*consumer_tasks, return_exceptions=True)
    await result_queue.join()


if __name__ == "__main__":
    asyncio.run(main())
