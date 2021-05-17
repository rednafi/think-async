from __future__ import annotations

import asyncio
import random
import uuid

import aioredis
from aioredis.client import Redis


def redis_pool() -> Redis:
    connection_pool = aioredis.ConnectionPool(max_connections=100)
    REDIS_POOL = aioredis.Redis(
        host="127.0.0.1", port=6379, db=0, connection_pool=connection_pool
    )
    return REDIS_POOL


REDIS_POOL = redis_pool()
STREAM_NAME = "dhaka"
STREAM_MAP = {"dhaka": "$"}
CONSUMER_GROUP_NAME = "demo_consumer"


async def producer(
    redis_pool: Redis = REDIS_POOL,
    stream_name: str = STREAM_NAME,
) -> None:

    async with redis_pool.client() as conn:
        while True:
            data = {
                "uuid": str(uuid.uuid4()),
                "temperature": random.randint(0, 100),
                "humidity": random.randint(0, 100),
            }
            result = await conn.xadd(stream_name, data)
            print(f"producer added data :{result}")
            await asyncio.sleep(0.5)


async def consumer(
    redis_pool: Redis = REDIS_POOL,
    stream_name: str = STREAM_NAME,
    stream_map: dict[str, str] = STREAM_MAP,
    consumer_group: str = CONSUMER_GROUP_NAME,
) -> None:

    async with redis_pool.client() as conn:
        # Create consumer group.
        try:
            await conn.xgroup_create(stream_name, consumer_group)
        except:
            pass

        while True:
            result = await conn.xread(stream_map, block=1)
            if result:
                stream_id = result[0][1][0][0]
                await conn.xack(stream_name, consumer_group, stream_id)
                print(f"consumer ingested data :{result}")
                await asyncio.sleep(1)
            else:
                await asyncio.sleep(1)


async def orchestrator() -> None:
    task_coros = (producer(), consumer(), consumer())
    await asyncio.gather(*task_coros)


asyncio.run(orchestrator())
