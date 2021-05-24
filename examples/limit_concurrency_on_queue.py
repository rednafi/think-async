from __future__ import annotations

import asyncio
from contextvars import ContextVar
from collections.abc import Iterable

CONCURRENT_TASK_COUNT = ContextVar("concurrent_task_count", default=5)


async def foo(func_id: int) -> None:
    print(f"Doing work - {func_id}")
    await asyncio.sleep(1)


async def producer(func_ids: Iterable[int], queue: asyncio.Queue) -> None:
    for func_id in func_ids:
        await queue.put(func_id)
        if queue.full():
            print("\nQueue is full, letting the consumer run...\n")
            await asyncio.sleep(1)


async def consumer(queue: asyncio.Queue) -> None:
    while queue.qsize():
        func_id = await queue.get()
        await foo(func_id)
        queue.task_done()
    await asyncio.sleep(1)


async def main() -> None:
    limit = CONCURRENT_TASK_COUNT.get()
    func_ids = range(0, 20)
    queue = asyncio.Queue(maxsize=limit)  # type: asyncio.Queue[int]

    tasks = []
    producer_task = asyncio.create_task(producer(func_ids, queue))
    consumer_tasks = [asyncio.create_task(consumer(queue)) for _ in range(limit)]
    tasks.append(producer_task)
    tasks.extend(consumer_tasks)

    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION)

    for fut in done | pending:
        try:
            if exc := fut.exception():
                raise exc
        except asyncio.exceptions.InvalidStateError:
            pass
        fut.cancel()

    await queue.join()


if __name__ == "__main__":
    asyncio.run(main())
