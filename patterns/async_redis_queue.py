"""Simple FIFO queue with Redis to run tasks asynchronously.

===========
Description
===========

This script implements a rudimentary FIFO task queue using Redis's list data
structure.

This script roughly implements the following steps:

-> Task callables are turned into task objects.

-> Each task object has a uuid attached to that.

-> These task objects are then pickle serialized and sent to the broker. Here the
   broker is a Redis database that stores the serialized tasks.

-> Broker stores the tasks in a FIFO queue.

-> A single worker picks up the tasks.

-> When a task is found by the worker, it pops that from the FIFO queue, performs
   deserialization, and executes it in a non-blocking fashion.

-> The worker sends the task result to a result backend which is just another
   Redis database.

============
Instructions
============

To run the script —
-> Install docker.
-> Spin a Redis instance with the following commands:

```
docker stop dev-redis
docker rm dev-redis
docker run --name dev-redis -d -h localhost -p 6379:6379 redis:alpine

```
-> Install the dependencies:
```
pip install -r requirements.txt

```
-> Run the script:

```
python redis_queue.py
```

-> To inspect the results, connect to Redis DB with RedisInsight, and the results
can be found in Database 1.

=======
License
=======

MIT License.
Copyright (c) 2021 Redowan Delowar.

"""
from __future__ import annotations

import asyncio
import logging
import pickle
import random
import sys
import uuid
from collections.abc import Awaitable, Callable
from typing import Any

import aioredis
import uvloop

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
sh = logging.StreamHandler(stream=sys.stdout)
sh.setLevel(logging.INFO)
logger.addHandler(sh)

uvloop.install()


class SimpleTask:
    """Assign a unique `task_id` to the target function."""

    def __init__(
        self,
        func: Callable[..., Awaitable],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self.id = str(uuid.uuid4())
        self.func = func
        self.args = args
        self.kwargs = kwargs

    async def process_task(self) -> Awaitable[Any]:
        """Execute the function."""
        return await self.func(*self.args, **self.kwargs)


class RedisQueue:
    """Simplified FIFO queue with Redis."""

    def __init__(
        self,
        broker: aioredis.Redis,
        result_backend: aioredis.Redis,
        queue_name: str,
    ) -> None:
        self.broker = broker
        self.result_backend = result_backend
        self.queue_name = queue_name

    async def enqueue(self, func: Callable, *args: Any, **kwargs: Any) -> str:
        # Apply `SimpleTask` on the target function to convert it to a `task` object.
        task = SimpleTask(func, *args, **kwargs)

        # Pickle serialize the `task` object.
        serialized_task = pickle.dumps(task, protocol=pickle.HIGHEST_PROTOCOL)

        # Append the `task` to the right side of Redis's native `list` structure.
        await self.broker.rpush(self.queue_name, serialized_task)

        # Return the `task_id` just like Celery.
        return task.id

    async def dequeue(self) -> None:
        # Fetch the pickle serialized `task` object from Redis.
        serialized_task = await self.broker.blpop(self.queue_name)
        serialized_task = serialized_task[1]

        # Deserialize the pickled object to the `task` object.
        task = pickle.loads(serialized_task)
        logger.info(f"Task ID: {task.id}, Args: {task.args}, Kwargs: {task.kwargs}")

        # Execute the task here.
        result = await task.process_task()

        # Save the result using Redis's `key:val` structure.
        await self.result_backend.set(f"result:{task.id}", result)
        logger.info("Task processing complete.")

    async def get_length(self) -> Awaitable[int]:
        return await self.broker.llen(self.queue_name)


async def worker(queue: RedisQueue) -> None:
    """Mimicks the celery worker."""

    async def _execute_task(queue: RedisQueue) -> None:
        if await queue.get_length() > 0:  # type: ignore
            await queue.dequeue()
        else:
            logger.info("No tasks in the queue")
            await asyncio.sleep(0)

    for _ in range(await queue.get_length()):  # type: ignore
        await _execute_task(queue)


# Define a task to be run asynchronously.
async def foo(start: int, end: int) -> int:
    await asyncio.sleep(0)
    return random.randint(start, end)


async def orchestrator() -> None:
    # Instantiate Redis `broker` and `result_backend` connection pools.
    broker = aioredis.from_url("redis://localhost:6379/0")
    result_backend = aioredis.from_url("redis://localhost:6379/1")

    async with broker.client() as b:
        async with result_backend.client() as rb:
            queue = RedisQueue(b, rb, "default")
            funcs = [foo for _ in range(10)]
            args = [(i, j) for (i, j) in zip(range(10), range(100, 110))]

            # Enqueue tasks.
            for func, arg in zip(funcs, args):
                logger.info("enqueing task")
                await queue.enqueue(func, *arg)

            # Dequeue and execute tasks.
            await worker(queue)


if __name__ == "__main__":
    asyncio.run(orchestrator(), debug=True)
