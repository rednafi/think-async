from __future__ import annotations

import asyncio
from contextvars import ContextVar
from typing import Iterable

CONCURRENT_TASK_COUNT = ContextVar("concurrent_task_count", default=5)


async def foo(func_id: int) -> None:
    print(f"Doing work - {func_id}")
    await asyncio.sleep(1)


async def producer(func_ids: Iterable[int], queue: asyncio.Queue[int]) -> None:
    for func_id in func_ids:
        await queue.put(func_id)
        if queue.full():
            await asyncio.sleep(0)


async def consumer(queue: asyncio.Queue[int]) -> None:
    while queue.qsize():
        func_id = await queue.get()
        await foo(func_id)
        queue.task_done()
        await asyncio.sleep(0)


async def main() -> None:

    func_ids = range(0, 20)
    queue = asyncio.Queue(maxsize=CONCURRENT_TASK_COUNT.get())  # type: asyncio.Queue

    tasks = [producer(func_ids, queue)]
    for _ in range(CONCURRENT_TASK_COUNT.get()):
        tasks.append(consumer(queue))

    await asyncio.gather(*tasks)
    await queue.join()


if __name__ == "__main__":
    asyncio.run(main())
