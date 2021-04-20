from __future__ import annotations
import asyncio
import itertools
from typing import AsyncGenerator


MAX_CONSUMERS = 20


async def generate_number() -> AsyncGenerator[int, None]:
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
    result_queue, event: asyncio.Event, limit: asyncio.Semaphore
) -> None:
    async with limit:
        while True:
            await event.wait()
            result = await result_queue.get()
            print(result)
            result_queue.task_done()
            await asyncio.sleep(0.1)
            if limit.locked():
                print("sleeping for 2 sec")
                await asyncio.sleep(2)


async def main():
    result_queue = asyncio.Queue()
    event = asyncio.Event()
    limit = asyncio.Semaphore(5)
    producer_task = asyncio.create_task(producer(result_queue, event))
    consumer_tasks = [
        consumer(result_queue, event, limit) for _ in range(MAX_CONSUMERS)
    ]

    await asyncio.gather(*consumer_tasks)
    await result_queue.join()


asyncio.run(main())
