from __future__ import annotations

import asyncio
import random
import uuid

import aioredis

REDIS_POOL = aioredis.Redis(host="127.0.0.1", port=6379, db=0)
STREAM_NAME = "dhaka"
STREAM_MAP = {"dhaka": "$"}
CONSUMER_GROUP_NAME = "demo_consumer"


# Create consumer group.
async def create_consumer_group(
    stream_name: str = STREAM_NAME,
    consumer_group_name: str = CONSUMER_GROUP_NAME,
) -> None:
    async with REDIS_POOL.client() as conn:
        try:
            await conn.xgroup_create(stream_name, consumer_group_name)
        except Exception:
            pass


async def producer(
    redis_pool: aioredis.Redis = REDIS_POOL,
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
            await asyncio.sleep(1)


async def consumer(
    redis_pool: aioredis.Redis = REDIS_POOL,
    stream_name: str = STREAM_NAME,
    stream_map: dict[str, str] = STREAM_MAP,
    consumer_group_name: str = CONSUMER_GROUP_NAME,
) -> None:

    async with redis_pool.client() as conn:

        while True:
            result = await conn.xread(stream_map, block=1)
            if result:
                stream_id = result[0][1][0][0]
                await conn.xack(stream_name, consumer_group_name, stream_id)
                print(f"consumer ingested data :{result}")
                await asyncio.sleep(1)
            else:
                await asyncio.sleep(1)


async def orchestrator() -> None:
    await create_consumer_group()
    await create_consumer_group(
        stream_name="chittagong",
        consumer_group_name="another",
    )
    task_coros = (
        producer(),
        producer(stream_name="chittagong"),
        consumer(),
        consumer(
            stream_name="chittagong",
            stream_map={"chittagong": "$"},
        ),
    )
    await asyncio.gather(*task_coros)


if __name__ == "__main__":
    asyncio.run(orchestrator())
