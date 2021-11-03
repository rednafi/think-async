from unittest.mock import patch

import fakeredis.aioredis
import pytest

import patterns.async_redis_stream as main


@patch.object(main, "REDIS_POOL", fakeredis.aioredis.FakeRedis())
def test_globals():

    # Assert.
    assert isinstance(main.REDIS_POOL, fakeredis.aioredis.FakeRedis)
    assert main.CONSUMER_GROUP_NAME == "demo_consumer"
    assert main.STREAM_NAME == "dhaka"
    assert main.STREAM_MAP == {main.STREAM_NAME: "$"}


@pytest.mark.asyncio
@patch.object(main, "REDIS_POOL", fakeredis.aioredis.FakeRedis())
async def test_create_consumer_group():
    # Call 'create_consumer_group'.
    stream_name = "test_stream"
    consumer_group_name = "test_consumer"
    await main.create_consumer_group(
        stream_name=stream_name,
        consumer_group_name=consumer_group_name,
    )


class AlmostAlwaysTrue:
    def __init__(self, total_iterations=1):
        self.total_iterations = total_iterations
        self.current_iteration = 0

    def __bool__(self):
        if self.current_iteration < self.total_iterations:
            self.current_iteration += 1
            return True
        return False
