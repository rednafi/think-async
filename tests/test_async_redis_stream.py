import asyncio
from unittest.mock import Mock, patch

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
