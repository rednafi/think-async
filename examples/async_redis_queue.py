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
pip install aio-redis==2.0.0a && pip install uvloop

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
import uuid
from collections.abc import Callable, Coroutine
from typing import Any

import aioredis
import uvloop
from aioredis.client import Redis

logging.basicConfig(level=logging.INFO)

uvloop.install()


class SimpleTask:
    """Assign a unique `task_id` to the target function."""

    def __init__(
        self,
        func: Callable[..., Coroutine],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self.id = str(uuid.uuid4())
        self.func = func
        self.args = args
        self.kwargs = kwargs

    async def process_task(self) -> Coroutine[None, None, Any]:
        """Execute the function."""
        return await self.func(*self.args, **self.kwargs)


class Queue:
    """Simplified FIFO queue with Redis."""

    def __init__(self, broker: Redis, result_backend: Redis, queue_name: str) -> None:
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
        logging.info(f"Task ID: {task.id}, Args: {task.args}, Kwargs: {task.kwargs}")

        # Execute the task here.
        result = await task.process_task()

        # Save the result using Redis's `key:val` structure.
        await self.result_backend.set(f"result:{task.id}", result)
        logging.info("Task processing complete.")

    async def get_length(self) -> Coroutine[None, None, int]:
        return await self.broker.llen(self.queue_name)


async def worker(queue: Queue) -> None:
    """Mimicks the celery worker."""

    async def _execute_task(queue: Queue) -> None:
        if await queue.get_length() > 0:  # type: ignore
            await queue.dequeue()
        else:
            logging.info("No tasks in the queue")
            await asyncio.sleep(0)

    for _ in range(await queue.get_length()):  # type: ignore
        await _execute_task(queue)


# Define a task to be run asynchronously.
async def foo(start: int, end: int) -> int:
    await asyncio.sleep(0)
    return random.randint(start, end)


async def main() -> None:
    # Instantiate Redis `broker` and `result_backend` connection pools.
    broker = aioredis.from_url("redis://localhost:6379/0")
    result_backend = aioredis.from_url("redis://localhost:6379/1")

    async with broker.client() as b:
        async with result_backend.client() as rb:
            queue = Queue(b, rb, "default")
            funcs = [foo for _ in range(1000)]
            args = [(i, j) for (i, j) in zip(range(1000), range(1000, 2000))]

            # Enqueue tasks.
            for func, arg in zip(funcs, args):
                print("enqueing task")
                await queue.enqueue(func, *arg)

            # Dequeue and execute tasks.
            await worker(queue)


asyncio.run(main(), debug=True)
