"""Simple FIFO queue with Redis to run tasks asynchronously.

===========
Description
===========

This script implements a rudimentary FIFO task queue using Redis's list data
structure. I took a peek under Celery and RQ's source code to understand how
they've implemented the async task queue — harnessing the features of Redis and
Python's multiprocessing paradigm.

Here, I've attempted to emulate a similar task queue — albeit in a much simpler
fashion — to strengthen my grasp on the concept of async task queue. This script
roughly implements the following steps:

-> Task callables are turned into task objects.

-> Each task object has a uuid attached to that.

-> These task objects are then pickle serialized and sent to the broker. Here the
   broker is a Redis database that stores the serialized tasks.

-> Broker stores the tasks in a FIFO queue.

-> A worker runs 4 OS processes that listen to the broker database to find tasks.

-> When a task is found by the worker, it pops that from the FIFO queue, performs
   deserialization, and executes it.

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
from dataclasses import dataclass
from typing import Any, Callable, Coroutine, Iterator

import aioredis
import uvloop
from aioredis.client import Redis

logging.basicConfig(level=logging.INFO)

MAX_WORKERS = 4
uvloop.install()


@dataclass
class Config:
    broker_url: str
    result_backend_url: str
    task_map: dict[str, Iterator[Callable[[Any], Any]]]

    @property
    def _broker(self) -> Redis:

        return aioredis.from_url(self.broker_url)

    @property
    def _result_backend(self) -> Redis:
        return aioredis.from_url(self.result_backend_url)

    def distill(self) -> None:
        """Sanitizes the inputs."""
        if not isinstance(self.broker_url, str):
            raise TypeError("`broker_url` needs to be a string")

        if not isinstance(self.result_backend_url, str):
            raise TypeError("`result_backend_url` needs to be a string")

        if not isinstance(self.task_map, dict):
            raise TypeError(
                "`task_map` needs to be a dict where the key is the queue name and the value is a tuple of coroutine functions."
            )

    def __post_init__(self) -> None:
        self.distill()


class SimpleTask:
    """Assign a unique `task_id` to the target function."""

    def __init__(
        self,
        func: Callable[..., Any],
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

    async def enqueue(
        self, func: Callable[[Any], Any], *args: Any, **kwargs: Any
    ) -> str:
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
        await self.result_backend.set(f"{task.id}", result)
        logging.info("Task processing complete.")

    async def get_length(self) -> int:
        return await self.broker.llen(self.queue_name)


class Orchestrator:
    def __init__(self, config: Config) -> None:
        self.config = config

    async def enqueue_all(self, args: tuple[tuple, ...]) -> None:
        for queue_name, funcs in self.config.task_map.items():
            self.queue = Queue(
                self.config._broker,
                self.config._result_backend,
                queue_name,
            )
            for func, arg in zip(funcs, args):
                await self.queue.enqueue(func, *arg)


async def worker(queue: Queue, max_worker: int = MAX_WORKERS) -> None:
    """Mimicks the celery worker."""

    async def _execute_task(queue: Queue) -> None:
        if await queue.get_length() > 0:
            await queue.dequeue()
        else:
            logging.info("No tasks in the queue")

    logging.info(f"Running tasks with {max_worker} processes!")

    background_tasks = [
        asyncio.create_task(_execute_task(queue))
        for _ in range(await queue.get_length())
    ]

    await asyncio.gather(*background_tasks)


# Define a task to be run asynchronously.
async def task(start: int, end: int) -> int:
    # await asyncio.sleep(0)
    return random.randint(start, end)


async def main():
    # Instantiate Redis `broker` and `result_backend` connections.
    task_map = {"default": (task for _ in range(1000))}
    args = tuple((1000, 2000) for _ in range(1000))

    config = Config(
        broker_url="redis://localhost:6379/0",
        result_backend_url="redis://localhost:6379/0",
        task_map=task_map,
    )

    orch = Orchestrator(config)
    await orch.enqueue_all(args)

    # Spawn 4 parallel processes, fetch tasks from the queue and execute them
    # asynchronously.
    await worker(orch.queue)


asyncio.run(main())
